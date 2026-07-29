"""Integritaet der Wissensbasis und des Retrievals.

Diese Tests pruefen die Daten selbst, nicht nur den Code. Ein Datensatz ohne
Quelle oder ein Gebetsschritt ohne Bewegung ist ein Inhaltsfehler, und
Inhaltsfehler sind bei diesem Projekt die teureren.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

PROJECT_ROOT = Path(__file__).resolve().parents[2]
KNOWLEDGE = PROJECT_ROOT / "knowledge"

from ai.rag.chunker import build_all_chunks  # noqa: E402
from ai.rag.retriever import Retriever, build_context, detect_modules  # noqa: E402
from ai.rag.vector_store import LexicalStore, tokenize  # noqa: E402


def _load(path: Path) -> dict:
    with path.open(encoding="utf-8") as fh:
        return json.load(fh)


def _registry_ids() -> set[str]:
    data = _load(KNOWLEDGE / "sources" / "registry.json")
    return {s["id"] for s in data["sources"]}


def _walk(node, path="$"):
    if isinstance(node, dict):
        yield path, node
        for key, value in node.items():
            yield from _walk(value, f"{path}.{key}")
    elif isinstance(node, list):
        for index, value in enumerate(node):
            yield from _walk(value, f"{path}[{index}]")


def _content_files() -> list[Path]:
    return [
        path
        for path in sorted(KNOWLEDGE.rglob("*.json"))
        if "schema" not in path.parts and path.name != "registry.json"
    ]


# ==========================================================================
# Datenintegrität
# ==========================================================================

def test_all_json_files_are_valid():
    for path in _content_files():
        _load(path)  # wirft bei ungueltigem JSON


def test_every_source_id_is_registered():
    """Content Policy 4.2: nur registrierte Quellen sind zulaessig."""
    known = _registry_ids()
    for path in _content_files():
        for location, node in _walk(_load(path)):
            for entry in node.get("sources") or []:
                if isinstance(entry, dict) and entry.get("source_id"):
                    assert entry["source_id"] in known, (
                        f"{path.name}{location}: unbekannte source_id "
                        f"{entry['source_id']!r}"
                    )


def test_every_record_with_provenance_has_sources():
    for path in _content_files():
        for location, node in _walk(_load(path)):
            if "provenance" not in node:
                continue
            if node["provenance"] == "placeholder":
                continue
            assert node.get("sources"), f"{path.name}{location}: keine Quellen"


def test_no_placeholder_content_in_knowledge_base():
    """Content Policy 4.1: placeholder erreicht keinen Nutzer.

    Streng genommen wuerde der Filter das auch abfangen. Der Test verhindert,
    dass unfertige Inhalte ueberhaupt eingecheckt werden.
    """
    for path in _content_files():
        for location, node in _walk(_load(path)):
            assert node.get("provenance") != "placeholder", (
                f"{path.name}{location}: placeholder eingecheckt"
            )


def test_editorial_fiqh_content_cannot_claim_verified():
    """Redaktionelle Fiqh-Inhalte bleiben auf scholar_review_pending.

    Die Quelle editorial-fiqh-summary traegt provenance_ceiling. Nur eine
    menschliche Gelehrtenpruefung mit Primaerquelle kann verified rechtfertigen.
    """
    for path in _content_files():
        for location, node in _walk(_load(path)):
            if node.get("provenance") != "verified":
                continue
            ids = {
                e.get("source_id")
                for e in node.get("sources") or []
                if isinstance(e, dict)
            }
            assert "editorial-fiqh-summary" not in ids, (
                f"{path.name}{location}: verified mit editorial-fiqh-summary"
            )


def test_every_translation_names_its_translator():
    """Content Policy 4.3: Uebersetzung ohne Uebersetzername wird nicht ausgeliefert."""
    for path in _content_files():
        for location, node in _walk(_load(path)):
            for index, translation in enumerate(node.get("translations") or []):
                if not isinstance(translation, dict):
                    continue
                assert translation.get("translator"), (
                    f"{path.name}{location}.translations[{index}]: kein translator"
                )
                assert translation.get("source_id"), (
                    f"{path.name}{location}.translations[{index}]: keine source_id"
                )


def test_disputed_records_list_at_least_two_positions():
    """Content Policy 3.2: bei Uneinigkeit werden alle Positionen genannt."""
    for path in _content_files():
        for location, node in _walk(_load(path)):
            if node.get("provenance") != "disputed":
                continue
            positions = (
                node.get("variations")
                or node.get("madhhab_variations")
                or node.get("disputed_positions")
                or []
            )
            assert len(positions) >= 2, (
                f"{path.name}{location}: disputed mit {len(positions)} Positionen"
            )


def test_madhhab_values_are_valid():
    valid = {"common", "hanafi", "shafii", "maliki", "hanbali", "jafari"}
    for path in _content_files():
        for location, node in _walk(_load(path)):
            value = node.get("madhhab")
            if value is None:
                continue
            assert value in valid, f"{path.name}{location}: madhhab {value!r}"


# ==========================================================================
# Gebet
# ==========================================================================

def test_all_five_prayers_exist():
    for name in ("fajr", "dhuhr", "asr", "maghrib", "isha"):
        assert (KNOWLEDGE / "prayer" / f"{name}.json").exists(), f"{name}.json fehlt"


def test_prayer_rakat_counts_are_correct():
    """Die Fard-Rak'a-Zahlen sind konsensual und muessen stimmen."""
    expected = {"fajr": 2, "dhuhr": 4, "asr": 4, "maghrib": 3, "isha": 4}
    for name, count in expected.items():
        data = _load(KNOWLEDGE / "prayer" / f"{name}.json")
        assert data["units"]["fard"] == count, (
            f"{name}: {data['units']['fard']} statt {count} Fard-Rak'a"
        )


def test_every_prayer_step_resolves_to_a_movement():
    movements = {m["id"] for m in _load(KNOWLEDGE / "prayer" / "movements.json")["movements"]}
    for path in sorted((KNOWLEDGE / "prayer").glob("*.json")):
        if path.name == "movements.json":
            continue
        data = _load(path)
        for step in data.get("sequence", []):
            assert step["movement_id"] in movements, (
                f"{path.name} Schritt {step['step']}: unbekannte Bewegung "
                f"{step['movement_id']!r}"
            )


def test_prayer_sequences_start_and_end_correctly():
    """Jedes Gebet beginnt mit der Absicht und endet mit dem Friedensgruss."""
    for path in sorted((KNOWLEDGE / "prayer").glob("*.json")):
        if path.name == "movements.json":
            continue
        sequence = _load(path)["sequence"]
        assert sequence[0]["movement_id"] == "niyyah", f"{path.name}: Start"
        assert sequence[-1]["movement_id"] == "taslim", f"{path.name}: Ende"
        assert sequence[-2]["movement_id"] == "qada_final", f"{path.name}: vor Taslim"


def test_intermediate_sitting_only_in_longer_prayers():
    """Zwischensitzen gibt es nur bei drei oder vier Rak'a."""
    for path in sorted((KNOWLEDGE / "prayer").glob("*.json")):
        if path.name == "movements.json":
            continue
        data = _load(path)
        has_intermediate = any(
            s["movement_id"] == "qada_intermediate" for s in data["sequence"]
        )
        expected = data["units"]["fard"] > 2
        assert has_intermediate == expected, (
            f"{path.name}: Zwischensitzen={has_intermediate}, "
            f"Fard-Rak'a={data['units']['fard']}"
        )


def test_extra_surah_only_in_first_two_rakat():
    """Nach Al-Fatiha folgt nur in den ersten beiden Rak'a eine weitere Sure."""
    for path in sorted((KNOWLEDGE / "prayer").glob("*.json")):
        if path.name == "movements.json":
            continue
        for step in _load(path)["sequence"]:
            if step["movement_id"] == "surah_recitation":
                assert step["rakah"] <= 2, (
                    f"{path.name}: weitere Sure in Rak'a {step['rakah']}"
                )


def test_fatiha_recited_in_every_rakah():
    for path in sorted((KNOWLEDGE / "prayer").glob("*.json")):
        if path.name == "movements.json":
            continue
        data = _load(path)
        rakat_with_fatiha = {
            s["rakah"] for s in data["sequence"] if s["movement_id"] == "fatiha_recitation"
        }
        expected = set(range(1, data["units"]["fard"] + 1))
        assert rakat_with_fatiha == expected, (
            f"{path.name}: Al-Fatiha in {sorted(rakat_with_fatiha)}, "
            f"erwartet {sorted(expected)}"
        )


def test_two_prostrations_per_rakah():
    for path in sorted((KNOWLEDGE / "prayer").glob("*.json")):
        if path.name == "movements.json":
            continue
        data = _load(path)
        for rakah in range(1, data["units"]["fard"] + 1):
            count = sum(
                1
                for s in data["sequence"]
                if s["movement_id"] == "sujud" and s.get("rakah") == rakah
            )
            assert count == 2, f"{path.name} Rak'a {rakah}: {count} Niederwerfungen"


# ==========================================================================
# Arabisch
# ==========================================================================

def test_alphabet_has_28_letters():
    data = _load(KNOWLEDGE / "arabic" / "alphabet.json")
    assert len(data["letters"]) == 28


def test_every_letter_has_four_forms():
    for letter in _load(KNOWLEDGE / "arabic" / "alphabet.json")["letters"]:
        forms = letter["forms"]
        for key in ("isolated", "initial", "medial", "final"):
            assert forms.get(key), f"{letter['id']}: Form {key} fehlt"


def test_non_connecting_letters_are_marked():
    """Sechs Buchstaben verbinden sich nicht nach vorne."""
    expected = {"alif", "dal", "dhal", "ra", "zay", "waw"}
    data = _load(KNOWLEDGE / "arabic" / "alphabet.json")
    actual = {letter["id"] for letter in data["letters"] if not letter["connects_forward"]}
    assert actual == expected, f"{actual} statt {expected}"


def test_non_connecting_letters_have_identical_initial_and_isolated_form():
    data = _load(KNOWLEDGE / "arabic" / "alphabet.json")
    for letter in data["letters"]:
        if letter["connects_forward"]:
            continue
        forms = letter["forms"]
        assert forms["initial"] == forms["isolated"], letter["id"]
        assert forms["medial"] == forms["final"], letter["id"]


def test_curriculum_covers_all_letters():
    """Kein Buchstabe fehlt in der Lernreihenfolge."""
    data = _load(KNOWLEDGE / "arabic" / "alphabet.json")
    all_ids = {letter["id"] for letter in data["letters"]}
    covered = {lid for unit in data["curriculum"] for lid in unit.get("letters", [])}
    assert covered == all_ids, f"Nicht abgedeckt: {sorted(all_ids - covered)}"


def test_hard_letters_are_marked_as_difficult():
    """Rachen- und Emphatiklaute sind als schwierig eingeordnet."""
    hard = {"ain", "ghain", "hha", "qaf", "sad", "dad", "tta", "zza"}
    data = _load(KNOWLEDGE / "arabic" / "alphabet.json")
    for letter in data["letters"]:
        if letter["id"] in hard:
            level = letter["pronunciation"]["difficulty_for_german_speakers"]
            assert level == 3, f"{letter['id']}: Schwierigkeit {level}"


# ==========================================================================
# Reinigung
# ==========================================================================

def test_purification_modules_exist():
    for kind in ("wudu", "ghusl", "tayammum"):
        assert (KNOWLEDGE / "purification" / f"{kind}.json").exists()


def test_purification_covers_all_four_sunni_schools():
    for kind in ("wudu", "ghusl"):
        data = _load(KNOWLEDGE / "purification" / f"{kind}.json")
        schools = {entry["madhhab"] for entry in data["fard_count_by_madhhab"]}
        assert {"hanafi", "shafii", "maliki", "hanbali"} <= schools, (
            f"{kind}: nur {schools}"
        )


def test_purification_steps_are_sequentially_numbered():
    for kind in ("wudu", "ghusl", "tayammum"):
        data = _load(KNOWLEDGE / "purification" / f"{kind}.json")
        numbers = [s["step"] for s in data["steps"]]
        assert numbers == list(range(1, len(numbers) + 1)), f"{kind}: {numbers}"


def test_wudu_and_ghusl_carry_a_wellbeing_note():
    """Content Policy 7: Skrupulositaet wird angesprochen, nicht verstaerkt."""
    for kind in ("wudu", "ghusl"):
        data = _load(KNOWLEDGE / "purification" / f"{kind}.json")
        note = data.get("wellbeing_note", "")
        assert note, f"{kind}: kein wellbeing_note"
        assert "Regel" in note or "Detailwissen" in note or "Detailregeln" in note


# ==========================================================================
# Koran
# ==========================================================================

def test_fatiha_has_seven_ayat():
    data = _load(KNOWLEDGE / "quran" / "surah_001.json")
    assert data["ayah_count"] == 7
    assert len(data["ayat"]) == 7
    assert [a["number"] for a in data["ayat"]] == list(range(1, 8))


def test_quran_text_is_not_marked_verified_before_import():
    """Korantext erreicht verified nur ueber den Import mit Pruefsumme."""
    for path in sorted((KNOWLEDGE / "quran").glob("surah_*.json")):
        data = _load(path)
        if data.get("provenance") == "verified":
            registry = {s["id"]: s for s in _load(KNOWLEDGE / "sources" / "registry.json")["sources"]}
            ids = {e["source_id"] for e in data["sources"]}
            assert any(
                registry.get(i, {}).get("imported") and registry.get(i, {}).get("checksum_required")
                for i in ids
            ), f"{path.name}: verified ohne importierte Primaerquelle"


def test_quran_audio_absence_does_not_fall_back_to_tts():
    """ADR-0002: fehlt Audio, wird nicht synthetisiert."""
    for path in sorted((KNOWLEDGE / "quran").glob("surah_*.json")):
        audio = _load(path).get("audio") or {}
        if not audio.get("available"):
            reason = (audio.get("reason") or "").lower()
            assert "0002-no-tts-for-quran" in reason, (
                f"{path.name}: Begruendung verweist nicht auf ADR-0002"
            )
            assert "tts" in reason, f"{path.name}: TTS-Ausschluss nicht benannt"


# ==========================================================================
# Retrieval
# ==========================================================================

def test_chunks_are_built():
    chunks = build_all_chunks()
    assert len(chunks) > 80, f"nur {len(chunks)} Chunks"


def test_all_modules_are_represented():
    modules = {c.module for c in build_all_chunks()}
    assert modules == {"quran", "prayer", "purification", "arabic"}, modules


def test_no_chunk_is_placeholder():
    assert all(c.provenance != "placeholder" for c in build_all_chunks())


def test_every_chunk_has_sources_and_id():
    for chunk in build_all_chunks():
        assert chunk.chunk_id, "Chunk ohne ID"
        assert chunk.source_ids, f"{chunk.chunk_id}: keine Quellen"
        assert chunk.text.strip(), f"{chunk.chunk_id}: leerer Text"


def test_chunk_ids_are_unique():
    ids = [c.chunk_id for c in build_all_chunks()]
    duplicates = {i for i in ids if ids.count(i) > 1}
    assert not duplicates, f"Doppelte Chunk-IDs: {duplicates}"


def test_stopwords_are_removed_from_tokens():
    """Funktionswoerter verzerren sonst das Ranking."""
    tokens = tokenize("Was ist das Ruku im Gebet?")
    assert "ruku" in tokens
    assert "gebet" in tokens
    for stopword in ("was", "ist", "das", "im"):
        assert stopword not in tokens, f"Stoppwort {stopword!r} nicht entfernt"


def test_arabic_diacritics_are_normalised():
    """Vokalisierter und unvokalisierter Text ergeben dasselbe Token."""
    assert tokenize("رَبِّ") == tokenize("ربّ")


def test_module_detection():
    assert "prayer" in detect_modules("Wie viele Rakat hat Fajr?")
    assert "purification" in detect_modules("Wudu Schritte")
    assert "arabic" in detect_modules("Wie spreche ich den Buchstaben aus?")
    assert "quran" in detect_modules("Sure Al-Fatiha")
    assert detect_modules("Hauptstadt von Frankreich") == ()


def test_title_boost_ranks_exact_topic_first():
    """Ein Treffer im Titel schlaegt einen im Fliesstext.

    Regressionstest: ohne Feldgewichtung fand 'Wudu Schritte' die
    Tayammum-Uebersicht vor der Wudu-Uebersicht.
    """
    store = LexicalStore()
    store.index(build_all_chunks())
    hits = store.search("Wudu Schritte", limit=3)
    assert hits, "keine Treffer"
    assert "wudu" in hits[0].chunk.record_id, (
        f"Erster Treffer: {hits[0].chunk.chunk_id}"
    )


def test_retrieval_finds_relevant_content():
    retriever = Retriever()
    cases = [
        ("Wie viele Rakat hat Fajr?", "fajr"),
        ("Was passiert im Ruku?", "ruku"),
        ("Wudu Schritte", "wudu"),
        ("Buchstabe Ain", "ain"),
    ]
    for query, expected in cases:
        result = retriever.retrieve(query, limit=5)
        assert not result.is_empty, f"{query!r}: keine Treffer"
        ids = " ".join(h.chunk.chunk_id for h in result.hits)
        assert expected in ids, f"{query!r}: {expected!r} nicht in {ids}"


def test_retrieval_is_empty_for_unrelated_query():
    """Eine Frage ausserhalb des Themas ergibt keine Treffer statt schlechter."""
    result = Retriever().retrieve("Wie hoch ist der Eiffelturm?", limit=5)
    assert result.is_empty


def test_madhhab_filter_applies_to_retrieval():
    retriever = Retriever()
    result = retriever.retrieve("Handhaltung beim Stehen", limit=10, madhhab="hanafi")
    for hit in result.hits:
        assert hit.chunk.madhhab in ("common", "hanafi"), hit.chunk.chunk_id


def test_context_carries_citations_for_every_passage():
    result = Retriever().retrieve("Wie viele Rakat hat Fajr?", limit=4)
    context = build_context(result)
    assert len(context.passages) == len(context.citations)
    for citation in context.citations:
        assert citation.source_ids, f"{citation.chunk_id}: keine Quellen"
        assert citation.provenance != "placeholder"


def test_prompt_block_labels_every_passage():
    """Der Generator muss Passagen mit [n] referenzieren koennen."""
    context = build_context(Retriever().retrieve("Wudu Schritte", limit=3))
    block = context.as_prompt_block()
    for index in range(1, len(context.passages) + 1):
        assert f"[{index}]" in block
