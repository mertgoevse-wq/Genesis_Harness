"""Zerlegung der Wissensbasis in abrufbare Passagen.

Entwurfsentscheidung — inhaltliche statt token-basierte Chunk-Grenzen:
Ein Standard-Chunker schneidet nach n Tokens mit Overlap. Fuer diese Wissensbasis
ist das falsch. Ein halber Vers ist kein Vers; ein Gebetsschritt, der mitten in
der Bewegung endet, ist als Lerninhalt unbrauchbar. Die Chunk-Grenze folgt hier
der inhaltlichen Einheit:

    Koran        ein Chunk pro Ayah
    Gebet        ein Chunk pro Bewegung, plus ein Uebersichts-Chunk pro Gebet
    Reinigung    ein Chunk pro Schritt, plus ein Uebersichts-Chunk
    Arabisch     ein Chunk pro Buchstabe, pro Vokalzeichen, pro Verwechslungsgruppe

Jeder Chunk traegt seine Herkunft mit: source_ids, provenance, madhhab. Ohne diese
Felder kann der Retriever nicht filtern und der CitationChecker nicht pruefen.
"""
from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
KNOWLEDGE_DIR = PROJECT_ROOT / "knowledge"


@dataclass(frozen=True)
class Chunk:
    """Eine abrufbare Passage der Wissensbasis."""

    chunk_id: str
    text: str
    """Suchbarer Volltext. Enthaelt Label, Anleitung, Transliteration und Uebersetzung."""

    module: str
    """quran | prayer | purification | arabic"""

    record_id: str
    """ID des uebergeordneten Datensatzes, z.B. 'fajr' oder 'surah_001'."""

    provenance: str
    source_ids: tuple[str, ...]
    madhhab: str = "common"
    title: str = ""
    deep_link: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

    @property
    def is_deliverable(self) -> bool:
        return self.provenance != "placeholder"


def _collect_source_ids(node: dict[str, Any], fallback: tuple[str, ...] = ()) -> tuple[str, ...]:
    entries = node.get("sources") or []
    ids = tuple(e["source_id"] for e in entries if isinstance(e, dict) and e.get("source_id"))
    return ids or fallback


def _first_text(value: Any, preferred: str = "de") -> str:
    """Holt Text aus einem mehrsprachigen dict oder gibt einen String direkt zurueck."""
    if isinstance(value, str):
        return value
    if isinstance(value, dict):
        for key in (preferred, "en", "arabic", "transliteration"):
            if isinstance(value.get(key), str):
                return value[key]
        for candidate in value.values():
            if isinstance(candidate, str):
                return candidate
    return ""


def _join(*parts: str) -> str:
    return " ".join(p.strip() for p in parts if p and p.strip())


def _load(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as fh:
        return json.load(fh)


# --------------------------------------------------------------------------
# Koran
# --------------------------------------------------------------------------

def chunk_quran(data: dict[str, Any]) -> list[Chunk]:
    """Ein Chunk pro Ayah. Der Vers ist die kleinste sinnvolle Einheit."""
    chunks: list[Chunk] = []
    surah_id = data["id"]
    surah_number = data.get("number")
    name = data.get("name", {})
    surah_label = _join(name.get("transliteration", ""), _first_text(name.get("translations", {})))
    base_sources = _collect_source_ids(data)

    for ayah in data.get("ayat", []):
        number = ayah.get("number")
        translations = " ".join(t.get("text", "") for t in ayah.get("translations", []))
        words = " ".join(
            _join(w.get("transliteration", ""), w.get("gloss_de", ""))
            for w in ayah.get("word_analysis", [])
        )
        text = _join(
            f"Sure {surah_number} {surah_label}, Vers {number}.",
            ayah.get("arabic", ""),
            ayah.get("transliteration", ""),
            translations,
            words,
            " ".join(ayah.get("tajwid_notes", [])),
            ayah.get("note", ""),
        )
        chunks.append(
            Chunk(
                chunk_id=f"quran:{surah_id}:ayah_{number}",
                text=text,
                module="quran",
                record_id=surah_id,
                provenance=data.get("provenance", "placeholder"),
                source_ids=base_sources,
                title=f"{surah_label} {surah_number}:{number}",
                deep_link=f"/quran/{surah_number}#{number}",
                metadata={"surah": surah_number, "ayah": number},
            )
        )

    # Uebersichts-Chunk: beantwortet Fragen nach der Sure als Ganzes
    chunks.append(
        Chunk(
            chunk_id=f"quran:{surah_id}:overview",
            text=_join(
                f"Sure {surah_number} {surah_label}.",
                f"{data.get('ayah_count')} Verse.",
                f"Offenbarungsort {data.get('revelation_place', '')}.",
                data.get("learning_note", ""),
            ),
            module="quran",
            record_id=surah_id,
            provenance=data.get("provenance", "placeholder"),
            source_ids=base_sources,
            title=f"{surah_label} — Übersicht",
            deep_link=f"/quran/{surah_number}",
            metadata={"surah": surah_number, "kind": "overview"},
        )
    )
    return chunks


# --------------------------------------------------------------------------
# Gebet
# --------------------------------------------------------------------------

def chunk_movements(data: dict[str, Any]) -> list[Chunk]:
    """Ein Chunk pro Bewegung. Bewegungen sind gebetsuebergreifend wiederverwendet."""
    chunks: list[Chunk] = []
    for movement in data.get("movements", []):
        label = _first_text(movement.get("label", {}))
        recitations = " ".join(
            _join(
                r.get("label", ""),
                r.get("arabic", ""),
                r.get("transliteration", ""),
                " ".join(t.get("text", "") for t in r.get("translations", [])),
            )
            for r in movement.get("recitation", [])
        )
        variations = " ".join(
            f"{v.get('madhhab', '')}: {v.get('position', '')}"
            for v in movement.get("variations", [])
        )
        text = _join(
            f"Gebetsbewegung {label}.",
            movement.get("arabic_term", ""),
            movement.get("transliteration", ""),
            _first_text(movement.get("instruction", {})),
            recitations,
            variations,
            "Häufige Fehler: " + "; ".join(movement.get("common_mistakes", []))
            if movement.get("common_mistakes")
            else "",
            f"Einordnung: {movement.get('ruling', '')}.",
        )
        chunks.append(
            Chunk(
                chunk_id=f"prayer:movement:{movement['id']}",
                text=text,
                module="prayer",
                record_id=movement["id"],
                provenance=movement.get("provenance", "placeholder"),
                source_ids=_collect_source_ids(movement),
                madhhab=movement.get("madhhab", "common"),
                title=label or movement["id"],
                deep_link=f"/prayer/movement/{movement['id']}",
                metadata={
                    "ruling": movement.get("ruling"),
                    "body_position": movement.get("body_position"),
                    "animation_key": movement.get("animation_key"),
                },
            )
        )
    return chunks


def chunk_prayer(data: dict[str, Any]) -> list[Chunk]:
    """Ein Uebersichts-Chunk pro Gebet. Die Schritte selbst liegen in movements."""
    prayer_id = data["id"]
    name = data.get("name", {})
    label = _join(name.get("transliteration", ""), _first_text(name.get("translations", {})))
    units = data.get("units", {})
    unit_text = f"Fard: {units.get('fard')} Rak'a."
    for key, human in (("sunnah_before", "Sunnah davor"), ("sunnah_after", "Sunnah danach"), ("witr", "Witr")):
        entry = units.get(key)
        if isinstance(entry, dict):
            unit_text += f" {human}: {entry.get('count')} Rak'a ({entry.get('ruling')})."

    window = data.get("time_window", {})
    audible = data.get("audible_recitation", {})
    prerequisites = "; ".join(
        f"{p.get('id')}: {p.get('description')}" for p in data.get("prerequisites", [])
    )

    text = _join(
        f"{label}. Gebet Nummer {data.get('order')} von fünf.",
        name.get("arabic", ""),
        unit_text,
        f"Zeitfenster: {window.get('description', '')} Beginn: {window.get('starts', '')} Ende: {window.get('ends', '')}",
        audible.get("description", ""),
        f"Voraussetzungen: {prerequisites}",
        f"Ablauf mit {len(data.get('sequence', []))} Schritten.",
        data.get("learning_note", ""),
    )

    return [
        Chunk(
            chunk_id=f"prayer:{prayer_id}:overview",
            text=text,
            module="prayer",
            record_id=prayer_id,
            provenance=data.get("provenance", "placeholder"),
            source_ids=_collect_source_ids(data),
            title=label or prayer_id,
            deep_link=f"/prayer/{prayer_id}",
            metadata={
                "fard_rakat": units.get("fard"),
                "order": data.get("order"),
                "step_count": len(data.get("sequence", [])),
            },
        )
    ]


# --------------------------------------------------------------------------
# Reinigung
# --------------------------------------------------------------------------

def chunk_purification(data: dict[str, Any]) -> list[Chunk]:
    """Ein Chunk pro Schritt, plus Uebersicht, plus Invalidatoren."""
    chunks: list[Chunk] = []
    record_id = data["id"]
    name = data.get("name", {})
    label = _join(name.get("transliteration", ""), _first_text(name.get("translations", {})))
    base_sources = _collect_source_ids(data)

    fard_text = " ".join(
        f"{entry.get('madhhab')}: {entry.get('count')} Fard-Elemente — "
        + ", ".join(entry.get("elements", []))
        + "."
        for entry in data.get("fard_count_by_madhhab", [])
    )
    chunks.append(
        Chunk(
            chunk_id=f"purification:{record_id}:overview",
            text=_join(
                f"{label}.",
                name.get("arabic", ""),
                _first_text(data.get("purpose", {})),
                fard_text,
                f"{len(data.get('steps', []))} Schritte.",
                data.get("learning_note", ""),
            ),
            module="purification",
            record_id=record_id,
            provenance=data.get("provenance", "placeholder"),
            source_ids=base_sources,
            title=label or record_id,
            deep_link=f"/purification/{record_id}",
            metadata={"step_count": len(data.get("steps", []))},
        )
    )

    for step in data.get("steps", []):
        step_label = _first_text(step.get("label", {}))
        recitation = step.get("recitation") or {}
        variations = " ".join(
            f"{v.get('madhhab', '')}: {v.get('position', '')}" for v in step.get("variations", [])
        )
        text = _join(
            f"{label} Schritt {step.get('step')}: {step_label}.",
            step.get("arabic_term", ""),
            _first_text(step.get("instruction", {})),
            recitation.get("arabic", ""),
            recitation.get("transliteration", ""),
            f"Einordnung: {step.get('ruling', '')}.",
            f"{step.get('repetitions')}-mal." if step.get("repetitions") else "",
            variations,
            "Häufige Fehler: " + "; ".join(step.get("common_mistakes", []))
            if step.get("common_mistakes")
            else "",
        )
        chunks.append(
            Chunk(
                chunk_id=f"purification:{record_id}:step_{step.get('step')}",
                text=text,
                module="purification",
                record_id=record_id,
                provenance=step.get("provenance", "placeholder"),
                source_ids=_collect_source_ids(step, base_sources),
                madhhab=step.get("madhhab", "common"),
                title=f"{label} — {step_label}",
                deep_link=f"/purification/{record_id}#step-{step.get('step')}",
                metadata={"step": step.get("step"), "ruling": step.get("ruling")},
            )
        )

    invalidators = data.get("invalidators")
    if invalidators:
        items = "; ".join(
            f"{i.get('id')}: {i.get('description')}" for i in invalidators.get("items", [])
        )
        chunks.append(
            Chunk(
                chunk_id=f"purification:{record_id}:invalidators",
                text=_join(f"Was {label} aufhebt.", invalidators.get("note", ""), items),
                module="purification",
                record_id=record_id,
                provenance=data.get("provenance", "placeholder"),
                source_ids=base_sources,
                title=f"{label} — Aufhebende Umstände",
                deep_link=f"/purification/{record_id}#invalidators",
                metadata={"kind": "invalidators"},
            )
        )
    return chunks


# --------------------------------------------------------------------------
# Arabisch
# --------------------------------------------------------------------------

def chunk_arabic(data: dict[str, Any]) -> list[Chunk]:
    """Ein Chunk pro Buchstabe, Vokalzeichen, Verwechslungsgruppe und Lerneinheit."""
    chunks: list[Chunk] = []
    base_sources = _collect_source_ids(data)

    for letter in data.get("letters", []):
        forms = letter.get("forms", {})
        pron = letter.get("pronunciation", {})
        text = _join(
            f"Arabischer Buchstabe {letter.get('transliteration')} ({letter.get('glyph')}), "
            f"Nummer {letter.get('order')} von 28.",
            f"Name: {letter.get('name', {}).get('arabic', '')}.",
            f"Formen: isoliert {forms.get('isolated', '')}, initial {forms.get('initial', '')}, "
            f"medial {forms.get('medial', '')}, final {forms.get('final', '')}.",
            f"Aussprache: {pron.get('de', '')}",
            f"IPA {letter.get('ipa', '')}.",
            "Verbindet sich nicht mit dem folgenden Buchstaben."
            if not letter.get("connects_forward")
            else "",
        )
        chunks.append(
            Chunk(
                chunk_id=f"arabic:letter:{letter['id']}",
                text=text,
                module="arabic",
                record_id="arabic_alphabet",
                provenance=letter.get("provenance", "verified"),
                source_ids=_collect_source_ids(letter, base_sources),
                title=f"Buchstabe {letter.get('transliteration')}",
                deep_link=f"/arabic/letter/{letter['id']}",
                metadata={
                    "order": letter.get("order"),
                    "difficulty": pron.get("difficulty_for_german_speakers"),
                    "glyph": letter.get("glyph"),
                },
            )
        )

    for mark in data.get("vowel_marks", []):
        chunks.append(
            Chunk(
                chunk_id=f"arabic:vowel:{mark['id']}",
                text=_join(
                    f"Arabisches Vokalzeichen {mark.get('translit')} ({mark.get('name_ar')}).",
                    f"Laut: {mark.get('sound')}.",
                    f"Position: {mark.get('position')}.",
                    f"Beispiel: {mark.get('example')}.",
                ),
                module="arabic",
                record_id="arabic_alphabet",
                provenance=mark.get("provenance", "verified"),
                source_ids=_collect_source_ids(mark, base_sources),
                title=f"Vokalzeichen {mark.get('translit')}",
                deep_link=f"/arabic/vowel/{mark['id']}",
                metadata={"kind": "vowel_mark"},
            )
        )

    for group in data.get("confusion_groups", []):
        chunks.append(
            Chunk(
                chunk_id=f"arabic:confusion:{group['id']}",
                text=_join(
                    f"Verwechslungsgefahr: {group.get('label')}.",
                    f"Betroffene Buchstaben: {', '.join(group.get('letters', []))}.",
                    f"Warum: {group.get('why', '')}",
                    f"Merkhilfe: {group.get('tip', '')}",
                ),
                module="arabic",
                record_id="arabic_alphabet",
                provenance=group.get("provenance", "verified"),
                source_ids=_collect_source_ids(group, base_sources),
                title=group.get("label", group["id"]),
                deep_link=f"/arabic/confusion/{group['id']}",
                metadata={"kind": "confusion_group"},
            )
        )

    for unit in data.get("curriculum", []):
        chunks.append(
            Chunk(
                chunk_id=f"arabic:curriculum:unit_{unit['unit']}",
                text=_join(
                    f"Lerneinheit {unit['unit']}: {unit.get('title')}.",
                    f"Ziel: {unit.get('goal', '')}",
                    f"Buchstaben: {', '.join(unit.get('letters', []))}."
                    if unit.get("letters")
                    else "",
                    f"Geschätzt {unit.get('estimated_sessions')} Lerneinheiten.",
                    unit.get("note", ""),
                ),
                module="arabic",
                record_id="arabic_alphabet",
                provenance="verified",
                source_ids=base_sources,
                title=f"Lerneinheit {unit['unit']}: {unit.get('title')}",
                deep_link=f"/arabic/curriculum/{unit['unit']}",
                metadata={"kind": "curriculum", "unit": unit["unit"]},
            )
        )
    return chunks


# --------------------------------------------------------------------------
# Gesamtlauf
# --------------------------------------------------------------------------

def build_all_chunks(knowledge_dir: Path | None = None) -> list[Chunk]:
    """Baut alle Chunks aus der Wissensbasis.

    Nicht auslieferbare Chunks (provenance=placeholder) werden hier bereits
    verworfen — sie sollen nicht einmal im Index landen.
    """
    root = knowledge_dir or KNOWLEDGE_DIR
    chunks: list[Chunk] = []

    for path in sorted((root / "quran").glob("surah_*.json")):
        chunks.extend(chunk_quran(_load(path)))

    movements_path = root / "prayer" / "movements.json"
    if movements_path.exists():
        chunks.extend(chunk_movements(_load(movements_path)))

    for path in sorted((root / "prayer").glob("*.json")):
        if path.name == "movements.json":
            continue
        chunks.extend(chunk_prayer(_load(path)))

    for path in sorted((root / "purification").glob("*.json")):
        chunks.extend(chunk_purification(_load(path)))

    alphabet_path = root / "arabic" / "alphabet.json"
    if alphabet_path.exists():
        chunks.extend(chunk_arabic(_load(alphabet_path)))

    return [c for c in chunks if c.is_deliverable]
