#!/usr/bin/env python3
"""Generiert knowledge/arabic/alphabet.json.

Warum generiert: die vier Positionsformen jedes Buchstaben folgen einer Regel.
Sie hier zu berechnen statt 112 Unicode-Praesentationsformen von Hand einzutragen
vermeidet genau die Fehlerklasse, die bei arabischer Schrift am haeufigsten
auftritt - eine falsch kopierte Form, die visuell fast identisch aussieht.

Methode: Tatweel (U+0640) als Verbindungsstrich, wie im Sprachunterricht ueblich.
    isoliert  ب
    initial   بـ
    medial    ـبـ
    final     ـب

Sechs Buchstaben verbinden sich nicht nach vorne (ا د ذ ر ز و). Fuer sie sind
initiale und mediale Form gleich der isolierten bzw. finalen Form. Das Skript
setzt das automatisch um, statt es pro Buchstabe zu wiederholen.

Aufruf:
    python scripts/generate_alphabet.py
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

PROJECT_ROOT = Path(__file__).resolve().parent.parent
OUT_FILE = PROJECT_ROOT / "knowledge" / "arabic" / "alphabet.json"

TATWEEL = "ـ"
SOURCE = [{"source_id": "editorial-arabic-didactics"}]

# Buchstaben, die sich nicht mit dem folgenden Buchstaben verbinden
NON_CONNECTING = {"alif", "dal", "dhal", "ra", "zay", "waw"}

# (id, glyph, name_ar, name_translit, ipa, pronunciation_de, difficulty 1-3, group)
LETTERS: list[tuple[str, str, str, str, str, str, int, str]] = [
    ("alif",  "ا", "أَلِف",  "alif",  "aː",  "Langes a. Traeger fuer Hamza und Vokalzeichen; kein eigener Konsonant.", 1, "alif"),
    ("ba",    "ب", "بَاء",   "bāʾ",   "b",   "Wie deutsches b in Ball.", 1, "b_t_th"),
    ("ta",    "ت", "تَاء",   "tāʾ",   "t",   "Wie deutsches t in Tag.", 1, "b_t_th"),
    ("tha",   "ث", "ثَاء",   "thāʾ",  "θ",   "Stimmloses th wie im englischen think. Zungenspitze zwischen den Zaehnen.", 2, "b_t_th"),
    ("jim",   "ج", "جِيم",   "jīm",   "d͡ʒ", "Wie dsch in Dschungel.", 1, "j_h_kh"),
    ("hha",   "ح", "حَاء",   "ḥāʾ",   "ħ", "Kein deutsches Gegenstueck. Stimmloser Rachenlaut, tief im Hals, ohne Reibung am Gaumen.", 3, "j_h_kh"),
    ("kha",   "خ", "خَاء",   "khāʾ",  "x",   "Wie ch in Bach, aber weiter hinten.", 2, "j_h_kh"),
    ("dal",   "د", "دَال",   "dāl",   "d",   "Wie deutsches d in dann.", 1, "d_dh"),
    ("dhal",  "ذ", "ذَال",   "dhāl",  "ð",   "Stimmhaftes th wie im englischen this.", 2, "d_dh"),
    ("ra",    "ر", "رَاء",   "rāʾ",   "r",   "Gerolltes Zungenspitzen-r, wie im Italienischen. Nicht das deutsche Rachen-r.", 2, "r_z"),
    ("zay",   "ز", "زَاي",   "zāy",   "z",   "Stimmhaftes s wie in Rose.", 1, "r_z"),
    ("sin",   "س", "سِين",   "sīn",   "s",   "Stimmloses s wie in Gras.", 1, "s_sh"),
    ("shin",  "ش", "شِين",   "shīn",  "ʃ", "Wie sch in Schule.", 1, "s_sh"),
    ("sad",   "ص", "صَاد",   "ṣād",   "sɣ", "Emphatisches s. Gleicher Laut wie Sin, aber mit gehobenem Zungenruecken und dunklerem Klang.", 3, "emphatic"),
    ("dad",   "ض", "ضَاد",   "ḍād",   "dɣ", "Emphatisches d. Der charakteristischste Laut des Arabischen.", 3, "emphatic"),
    ("tta",   "ط", "طَاء",   "ṭāʾ",   "tɣ", "Emphatisches t. Dunkler und voller als Ta.", 3, "emphatic"),
    ("zza",   "ظ", "ظَاء",   "ẓāʾ",   "ðɣ", "Emphatisches stimmhaftes th.", 3, "emphatic"),
    ("ain",   "ع", "عَيْن",  "ʿayn",  "ʕ", "Kein deutsches Gegenstueck. Stimmhafter Rachenlaut durch Verengung im tiefen Hals.", 3, "ain_ghain"),
    ("ghain", "غ", "غَيْن",  "ghayn", "ʁ", "Wie ein gerolltes Rachen-r, aehnlich dem franzoesischen r.", 3, "ain_ghain"),
    ("fa",    "ف", "فَاء",   "fāʾ",   "f",   "Wie deutsches f in fein.", 1, "f_q"),
    ("qaf",   "ق", "قَاف",   "qāf",   "q",   "Wie k, aber weit hinten am Gaumensegel gebildet.", 3, "f_q"),
    ("kaf",   "ك", "كَاف",   "kāf",   "k",   "Wie deutsches k in kalt.", 1, "k_l"),
    ("lam",   "ل", "لَام",   "lām",   "l",   "Wie deutsches l in Land.", 1, "k_l"),
    ("mim",   "م", "مِيم",   "mīm",   "m",   "Wie deutsches m in Mut.", 1, "m_n"),
    ("nun",   "ن", "نُون",   "nūn",   "n",   "Wie deutsches n in nein.", 1, "m_n"),
    ("ha",    "ه", "هَاء",   "hāʾ",   "h",   "Wie deutsches h in Haus. Nicht zu verwechseln mit dem tieferen Ha.", 2, "h_w_y"),
    ("waw",   "و", "وَاو",   "wāw",   "w",   "Wie englisches w in water. Auch langes u als Vokal.", 1, "h_w_y"),
    ("ya",    "ي", "يَاء",   "yāʾ",   "j",   "Wie deutsches j in ja. Auch langes i als Vokal.", 1, "h_w_y"),
]

CONFUSION_GROUPS: dict[str, dict[str, Any]] = {
    "b_t_th": {
        "label": "Ba, Ta, Tha und Nun",
        "letters": ["ba", "ta", "tha", "nun"],
        "why": "Gleicher Grundkoerper, Unterscheidung nur ueber Zahl und Lage der Punkte.",
        "tip": "Punkt unten = Ba. Zwei oben = Ta. Drei oben = Tha. Ein Punkt oben bei tieferer Schale = Nun.",
    },
    "j_h_kh": {
        "label": "Jim, Ha und Kha",
        "letters": ["jim", "hha", "kha"],
        "why": "Identische Form, Unterscheidung nur ueber den Punkt.",
        "tip": "Punkt innen = Jim. Kein Punkt = Ha. Punkt oben = Kha.",
    },
    "d_dh": {
        "label": "Dal und Dhal",
        "letters": ["dal", "dhal"],
        "why": "Unterschied nur ein Punkt.",
        "tip": "Ohne Punkt = Dal. Mit Punkt = Dhal.",
    },
    "r_z": {
        "label": "Ra und Zay",
        "letters": ["ra", "zay"],
        "why": "Unterschied nur ein Punkt.",
        "tip": "Ohne Punkt = Ra. Mit Punkt = Zay.",
    },
    "s_sh": {
        "label": "Sin und Shin",
        "letters": ["sin", "shin"],
        "why": "Unterschied nur drei Punkte.",
        "tip": "Ohne Punkte = Sin. Drei Punkte = Shin.",
    },
    "emphatic": {
        "label": "Emphatische Laute",
        "letters": ["sad", "dad", "tta", "zza"],
        "why": "Vier Laute ohne deutsches Gegenstueck. Sie klingen dunkler als ihre nicht-emphatischen Gegenstuecke.",
        "tip": "Sad zu Sin, Dad zu Dal, Ta zu Ta, Za zu Dhal jeweils im Paar ueben. Der Unterschied liegt im gehobenen Zungenruecken.",
    },
    "ain_ghain": {
        "label": "Ain und Ghain",
        "letters": ["ain", "ghain"],
        "why": "Rachenlaute ohne deutsche Entsprechung, gleiche Form.",
        "tip": "Ohne Punkt = Ain. Mit Punkt = Ghain. Beide brauchen Hoerbeispiele - Beschreibung allein genuegt nicht.",
    },
    "h_w_y": {
        "label": "Ha, Waw und Ya",
        "letters": ["ha", "waw", "ya"],
        "why": "Waw und Ya sind zugleich Konsonant und langer Vokal. Ha wird oft mit dem tieferen Ha verwechselt.",
        "tip": "Waw und Ya zuerst als Konsonant lernen, dann als Vokal.",
    },
    "alif": {
        "label": "Alif",
        "letters": ["alif"],
        "why": "Kein eigener Konsonant, sondern Traeger und Laengezeichen.",
        "tip": "Alif als Sonderfall behandeln, nicht als 'A' wie im deutschen Alphabet.",
    },
}

VOWEL_MARKS = [
    {"id": "fatha", "glyph": "َ", "example": "بَ", "name_ar": "فَتْحَة", "translit": "fatha", "sound": "kurzes a", "position": "ueber dem Buchstaben"},
    {"id": "kasra", "glyph": "ِ", "example": "بِ", "name_ar": "كَسْرَة", "translit": "kasra", "sound": "kurzes i", "position": "unter dem Buchstaben"},
    {"id": "damma", "glyph": "ُ", "example": "بُ", "name_ar": "ضَمَّة", "translit": "damma", "sound": "kurzes u", "position": "ueber dem Buchstaben"},
    {"id": "sukun", "glyph": "ْ", "example": "بْ", "name_ar": "سُكُون", "translit": "sukun", "sound": "kein Vokal", "position": "ueber dem Buchstaben"},
    {"id": "shadda", "glyph": "ّ", "example": "بّ", "name_ar": "شَدَّة", "translit": "shadda", "sound": "Verdoppelung des Konsonanten", "position": "ueber dem Buchstaben"},
    {"id": "fathatan", "glyph": "ً", "example": "بً", "name_ar": "فَتْحَتَان", "translit": "fathatan", "sound": "an", "position": "ueber dem Buchstaben"},
    {"id": "kasratan", "glyph": "ٍ", "example": "بٍ", "name_ar": "كَسْرَتَان", "translit": "kasratan", "sound": "in", "position": "unter dem Buchstaben"},
    {"id": "dammatan", "glyph": "ٌ", "example": "بٌ", "name_ar": "ضَمَّتَان", "translit": "dammatan", "sound": "un", "position": "ueber dem Buchstaben"},
]


def build_forms(glyph: str, connects_forward: bool) -> dict[str, str]:
    """Berechnet die vier Positionsformen mit Tatweel als Verbindungsstrich."""
    final = TATWEEL + glyph
    if connects_forward:
        return {
            "isolated": glyph,
            "initial": glyph + TATWEEL,
            "medial": TATWEEL + glyph + TATWEEL,
            "final": final,
        }
    # Nicht nach vorne verbindende Buchstaben: initiale Form = isolierte Form,
    # mediale Form = finale Form.
    return {
        "isolated": glyph,
        "initial": glyph,
        "medial": final,
        "final": final,
        "note": "Dieser Buchstabe verbindet sich nicht mit dem folgenden Buchstaben.",
    }


def build_letters() -> list[dict[str, Any]]:
    letters: list[dict[str, Any]] = []
    for index, (lid, glyph, name_ar, translit, ipa, pron, difficulty, group) in enumerate(LETTERS, start=1):
        connects = lid not in NON_CONNECTING
        letters.append(
            {
                "id": lid,
                "order": index,
                "glyph": glyph,
                "name": {"arabic": name_ar, "transliteration": translit},
                "transliteration": translit,
                "ipa": ipa,
                "connects_forward": connects,
                "forms": build_forms(glyph, connects),
                "pronunciation": {
                    "de": pron,
                    "difficulty_for_german_speakers": difficulty,
                    "has_german_equivalent": difficulty == 1,
                },
                "confusion_group": group,
                "audio": {
                    "available": False,
                    "expected_path": f"letters/{lid}.mp3",
                    "kind": "pronunciation",
                    "note": "Aussprache-Audio ist als Lernhilfe zulaessig. Fehlt die Datei, zeigt die UI nur Text.",
                },
                "provenance": "verified",
                "sources": SOURCE,
            }
        )
    return letters


def build_curriculum() -> list[dict[str, Any]]:
    """Lernreihenfolge nach Schwierigkeit, nicht nach Alphabet.

    Begruendung: die alphabetische Reihenfolge stellt schwere Laute wie Tha und Ha
    direkt neben leichte. Nach Schwierigkeit gruppiert erreicht ein Lernender
    schneller erste Leseerfolge.
    """
    return [
        {
            "unit": 1,
            "title": "Buchstaben mit deutscher Entsprechung",
            "goal": "Die Buchstaben erkennen und schreiben, deren Laut aus dem Deutschen bekannt ist.",
            "letters": ["ba", "ta", "dal", "ra", "zay", "sin", "fa", "kaf", "lam", "mim", "nun"],
            "estimated_sessions": 4,
        },
        {
            "unit": 2,
            "title": "Neue, aber gut beschreibbare Laute",
            "goal": "Laute lernen, die im Deutschen fehlen, sich aber ueber bekannte Sprachen erklaeren lassen.",
            "letters": ["tha", "jim", "dhal", "shin", "kha", "ha", "waw", "ya"],
            "estimated_sessions": 4,
        },
        {
            "unit": 3,
            "title": "Emphatische Laute",
            "goal": "Die vier emphatischen Konsonanten im Kontrast zu ihren Gegenstuecken unterscheiden.",
            "letters": ["sad", "dad", "tta", "zza"],
            "estimated_sessions": 5,
            "note": "Diese Einheit braucht Hoerbeispiele. Reines Textlernen genuegt hier nicht.",
        },
        {
            "unit": 4,
            "title": "Rachenlaute",
            "goal": "Ain, Ghain, Ha und Qaf bilden - die schwierigste Gruppe fuer deutsche Sprecher.",
            "letters": ["ain", "ghain", "hha", "qaf"],
            "estimated_sessions": 6,
            "note": "Realistische Erwartung setzen: diese Laute brauchen Wochen, nicht Tage. Kein Grund zur Entmutigung.",
        },
        {
            "unit": 5,
            "title": "Alif, Vokalzeichen und Verbindungen",
            "goal": "Kurzvokale, Sukun und Shadda lesen; Buchstaben zu Woertern verbinden.",
            "letters": ["alif"],
            "includes_vowel_marks": True,
            "estimated_sessions": 5,
        },
        {
            "unit": 6,
            "title": "Erste Woerter lesen",
            "goal": "Kurze Woerter und die Sure Al-Fatiha Wort fuer Wort lesen.",
            "letters": [],
            "module_link": "quran/surah_001",
            "estimated_sessions": 6,
        },
    ]


def main() -> int:
    letters = build_letters()
    data = {
        "$comment": (
            "Generiert von scripts/generate_alphabet.py. Nicht von Hand bearbeiten - "
            "Aenderungen im Generator vornehmen und neu erzeugen. Die Positionsformen "
            "nutzen Tatweel (U+0640) als Verbindungsstrich."
        ),
        "id": "arabic_alphabet",
        "version": "0.1.0",
        "last_updated": "2026-07-29",
        "provenance": "verified",
        "sources": SOURCE,
        "provenance_note": (
            "Sprachliche Inhalte sind linguistisch, nicht religionsrechtlich. Sie duerfen "
            "verified sein, wenn sie sprachwissenschaftlich korrekt sind - siehe "
            "knowledge/sources/registry.json, editorial-arabic-didactics."
        ),
        "script_direction": "rtl",
        "letter_count": len(letters),
        "letters": letters,
        "vowel_marks": [
            {**mark, "provenance": "verified", "sources": SOURCE} for mark in VOWEL_MARKS
        ],
        "confusion_groups": [
            {"id": gid, **group, "provenance": "verified", "sources": SOURCE}
            for gid, group in CONFUSION_GROUPS.items()
        ],
        "curriculum": build_curriculum(),
        "didactic_notes": [
            "Arabisch wird von rechts nach links geschrieben. Das ist fuer Lernende die erste Umstellung und braucht Uebung mit der Hand, nicht nur mit den Augen.",
            "Buchstaben aendern ihre Form je nach Position im Wort. Alle vier Formen gehoeren von Anfang an zum Lernstoff, sonst wird spaeter neu gelernt.",
            "Sechs Buchstaben verbinden sich nicht nach vorne. Wer diese sechs kennt, kann Wortgrenzen im Schriftbild schneller erkennen.",
            "Im Korantext sind die Vokalzeichen gesetzt. In modernem Alltagsarabisch fehlen sie meist. Fuer das Lesen des Korantexts ist das eine Erleichterung.",
        ],
    }

    OUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    with OUT_FILE.open("w", encoding="utf-8", newline="\n") as fh:
        json.dump(data, fh, ensure_ascii=False, indent=2)
        fh.write("\n")

    non_connecting = [letter["id"] for letter in letters if not letter["connects_forward"]]
    print(f"Geschrieben: {OUT_FILE.relative_to(PROJECT_ROOT)}")
    print(f"  Buchstaben:            {len(letters)}")
    print(f"  Vokalzeichen:          {len(VOWEL_MARKS)}")
    print(f"  Verwechslungsgruppen:  {len(CONFUSION_GROUPS)}")
    print(f"  Lerneinheiten:         {len(build_curriculum())}")
    print(f"  Nicht verbindend:      {', '.join(non_connecting)}")

    if len(letters) != 28:
        print(f"\nFEHLER: erwartet 28 Buchstaben, erzeugt {len(letters)}")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
