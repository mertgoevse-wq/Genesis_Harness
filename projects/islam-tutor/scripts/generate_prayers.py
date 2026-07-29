#!/usr/bin/env python3
"""Generiert die fuenf Gebetsdateien aus einer Spezifikation.

Warum generiert statt handgeschrieben: die Schrittfolge eines Gebets folgt einem
festen Muster, das sich nur in der Rak'a-Zahl und wenigen Details unterscheidet.
Fuenf Dateien von Hand zu pflegen wuerde bedeuten, dieselbe Sequenz fuenfmal
konsistent halten zu muessen. Ein Generator macht die Regel explizit und
Aenderungen an einer Stelle wirksam.

Die inhaltlichen Texte liegen NICHT hier, sondern in knowledge/prayer/movements.json.
Dieses Skript setzt nur die Reihenfolge zusammen.

Aufruf:
    python scripts/generate_prayers.py
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

PROJECT_ROOT = Path(__file__).resolve().parent.parent
PRAYER_DIR = PROJECT_ROOT / "knowledge" / "prayer"
MOVEMENTS_FILE = PRAYER_DIR / "movements.json"

EDITORIAL = [{"source_id": "editorial-fiqh-summary"}]
PROVENANCE = "scholar_review_pending"
UPDATED = "2026-07-29"


# --------------------------------------------------------------------------
# Spezifikation der fuenf Pflichtgebete
# --------------------------------------------------------------------------

PRAYER_SPECS: list[dict[str, Any]] = [
    {
        "id": "fajr",
        "order": 1,
        "name": {
            "arabic": "صَلَاةُ الْفَجْر",
            "transliteration": "Salat al-Fajr",
            "translations": {"de": "Morgengebet", "en": "Dawn prayer", "tr": "Sabah namazı"},
        },
        "fard": 2,
        "loud_rakat": [1, 2],
        "time_window": {
            "description": "Von Beginn der Morgendaemmerung bis kurz vor Sonnenaufgang.",
            "starts": "Beginn der echten Morgendaemmerung (Fajr as-Sadiq)",
            "ends": "Sonnenaufgang",
        },
        "sunnah_before": {"count": 2, "ruling": "sunnah_muakkadah", "madhhab": "common"},
        "sunnah_after": None,
        "learning_note": (
            "Fajr ist mit zwei Rak'a das kuerzeste Pflichtgebet und deshalb ein guter "
            "Einstieg zum Lernen der Abfolge."
        ),
    },
    {
        "id": "dhuhr",
        "order": 2,
        "name": {
            "arabic": "صَلَاةُ الظُّهْر",
            "transliteration": "Salat adh-Dhuhr",
            "translations": {"de": "Mittagsgebet", "en": "Noon prayer", "tr": "Öğle namazı"},
        },
        "fard": 4,
        "loud_rakat": [],
        "time_window": {
            "description": "Nach dem Sonnenhoechststand bis zum Beginn der Asr-Zeit.",
            "starts": "Wenn die Sonne den Zenit ueberschritten hat",
            "ends": "Beginn der Asr-Zeit",
        },
        "sunnah_before": {
            "count": 4,
            "ruling": "sunnah_muakkadah",
            "madhhab": "hanafi",
            "variations": [
                {
                    "madhhab": "hanafi",
                    "position": "Vier Rak'a Sunnah vor dem Fard.",
                    "sources": EDITORIAL,
                },
                {
                    "madhhab": "shafii",
                    "position": "Zwei Rak'a Sunnah mu'akkadah vor dem Fard, vier werden ebenfalls ueberliefert.",
                    "sources": EDITORIAL,
                },
            ],
        },
        "sunnah_after": {"count": 2, "ruling": "sunnah_muakkadah", "madhhab": "common"},
        "learning_note": (
            "Ab vier Rak'a kommt das Zwischensitzen nach der zweiten Rak'a hinzu, und in "
            "der dritten und vierten Rak'a wird nach Al-Fatiha keine weitere Sure rezitiert."
        ),
    },
    {
        "id": "asr",
        "order": 3,
        "name": {
            "arabic": "صَلَاةُ الْعَصْر",
            "transliteration": "Salat al-Asr",
            "translations": {"de": "Nachmittagsgebet", "en": "Afternoon prayer", "tr": "İkindi namazı"},
        },
        "fard": 4,
        "loud_rakat": [],
        "time_window": {
            "description": "Vom Ende der Dhuhr-Zeit bis zum Sonnenuntergang.",
            "starts": "Ende der Dhuhr-Zeit",
            "ends": "Sonnenuntergang",
            "madhhab_variations": [
                {
                    "madhhab": "hanafi",
                    "position": "Die Asr-Zeit beginnt, wenn der Schatten das Doppelte der Objektlaenge erreicht.",
                    "sources": EDITORIAL,
                },
                {
                    "madhhab": "shafii",
                    "position": "Die Asr-Zeit beginnt, wenn der Schatten die Objektlaenge erreicht.",
                    "sources": EDITORIAL,
                },
            ],
        },
        "sunnah_before": {"count": 4, "ruling": "sunnah", "madhhab": "hanafi"},
        "sunnah_after": None,
        "learning_note": "Gleiche Struktur wie Dhuhr, ebenfalls still rezitiert.",
    },
    {
        "id": "maghrib",
        "order": 4,
        "name": {
            "arabic": "صَلَاةُ الْمَغْرِب",
            "transliteration": "Salat al-Maghrib",
            "translations": {"de": "Abendgebet", "en": "Sunset prayer", "tr": "Akşam namazı"},
        },
        "fard": 3,
        "loud_rakat": [1, 2],
        "time_window": {
            "description": "Nach Sonnenuntergang bis zum Verschwinden der Abendroete.",
            "starts": "Sonnenuntergang",
            "ends": "Beginn der Isha-Zeit",
        },
        "sunnah_before": None,
        "sunnah_after": {"count": 2, "ruling": "sunnah_muakkadah", "madhhab": "common"},
        "learning_note": (
            "Das einzige Pflichtgebet mit drei Rak'a. In der dritten Rak'a wird still "
            "rezitiert und nur Al-Fatiha gesprochen."
        ),
    },
    {
        "id": "isha",
        "order": 5,
        "name": {
            "arabic": "صَلَاةُ الْعِشَاء",
            "transliteration": "Salat al-Isha",
            "translations": {"de": "Nachtgebet", "en": "Night prayer", "tr": "Yatsı namazı"},
        },
        "fard": 4,
        "loud_rakat": [1, 2],
        "time_window": {
            "description": "Nach dem Ende der Maghrib-Zeit bis zum Beginn der Morgendaemmerung.",
            "starts": "Wenn die Abendroete verschwunden ist",
            "ends": "Beginn der Fajr-Zeit",
        },
        "sunnah_before": None,
        "sunnah_after": {"count": 2, "ruling": "sunnah_muakkadah", "madhhab": "common"},
        "witr": {
            "count": 3,
            "ruling": "wajib",
            "madhhab": "hanafi",
            "variations": [
                {
                    "madhhab": "hanafi",
                    "position": "Drei Rak'a Witr, wajib.",
                    "sources": EDITORIAL,
                },
                {
                    "madhhab": "shafii",
                    "position": "Witr ist Sunnah mu'akkadah, eine bis elf Rak'a in ungerader Zahl.",
                    "sources": EDITORIAL,
                },
            ],
        },
        "learning_note": (
            "Nach dem Fard folgt das Witr-Gebet. Seine Einordnung und Rak'a-Zahl "
            "unterscheiden sich zwischen den Rechtsschulen deutlich."
        ),
    },
]


# --------------------------------------------------------------------------
# Sequenzaufbau
# --------------------------------------------------------------------------

def build_sequence(fard_rakat: int, loud_rakat: list[int]) -> list[dict[str, Any]]:
    """Setzt die Schrittfolge eines Fard-Gebets zusammen.

    Regel:
      Rak'a 1      Eroeffnung, Thana, Ta'awwudh, Fatiha, weitere Sure, Ruku, Sujud x2
      Rak'a 2      Fatiha, weitere Sure, Ruku, Sujud x2
      danach       bei 3 oder 4 Rak'a: Zwischensitzen
      Rak'a 3/4    nur Fatiha, Ruku, Sujud x2
      Abschluss    abschliessendes Sitzen, Taslim
    """
    sequence: list[dict[str, Any]] = []
    step = 1

    def add(movement_id: str, rakah: int | None, ruling: str, **extra: Any) -> None:
        nonlocal step
        entry: dict[str, Any] = {
            "step": step,
            "movement_id": movement_id,
            "ruling": ruling,
            "provenance": PROVENANCE,
            "sources": EDITORIAL,
        }
        if rakah is not None:
            entry["rakah"] = rakah
        entry.update(extra)
        sequence.append(entry)
        step += 1

    add("niyyah", None, "fard")

    for rakah in range(1, fard_rakat + 1):
        is_first = rakah == 1
        recites_extra_surah = rakah <= 2

        if is_first:
            add("takbir_ihram", rakah, "fard")
            add("qiyam", rakah, "fard")
            add("thana", rakah, "sunnah")
            add("taawwudh_basmala", rakah, "sunnah")
        else:
            add("qiyam", rakah, "fard")

        add(
            "fatiha_recitation",
            rakah,
            "fard",
            audible=rakah in loud_rakat,
        )
        if recites_extra_surah:
            add(
                "surah_recitation",
                rakah,
                "wajib",
                audible=rakah in loud_rakat,
                madhhab="hanafi",
            )

        add("ruku", rakah, "fard")
        add("qiyam_after_ruku", rakah, "fard")
        add("sujud", rakah, "fard")
        add("jalsa", rakah, "fard")
        add("sujud", rakah, "fard")

        if rakah == 2 and fard_rakat > 2:
            add("qada_intermediate", rakah, "wajib", madhhab="hanafi")

    add("qada_final", fard_rakat, "fard")
    add("taslim", fard_rakat, "fard")

    return sequence


def build_prerequisites() -> list[dict[str, Any]]:
    return [
        {
            "id": "taharah",
            "description": "Rituelle Reinheit durch Wudu oder, wo erforderlich, Ghusl.",
            "module_link": "purification/wudu",
            "sources": EDITORIAL,
        },
        {
            "id": "qibla",
            "description": "Ausrichtung zur Kaaba in Mekka.",
            "sources": EDITORIAL,
        },
        {
            "id": "satr",
            "description": "Bedeckung des Koerpers nach den Regeln der jeweiligen Rechtsschule.",
            "sources": EDITORIAL,
        },
        {
            "id": "waqt",
            "description": (
                "Das Gebet faellt in sein Zeitfenster. Dieses System berechnet keine "
                "Gebetszeiten - dafuer ist eine astronomische Berechnung mit lokaler "
                "Konvention erforderlich."
            ),
            "sources": EDITORIAL,
        },
        {
            "id": "place",
            "description": "Ein reiner Ort fuer das Gebet.",
            "sources": EDITORIAL,
        },
    ]


def build_prayer(spec: dict[str, Any]) -> dict[str, Any]:
    units: dict[str, Any] = {"fard": spec["fard"]}
    for key in ("sunnah_before", "sunnah_after", "witr"):
        value = spec.get(key)
        if value:
            unit = dict(value)
            unit.setdefault("sources", EDITORIAL)
            units[key] = unit

    prayer: dict[str, Any] = {
        "id": spec["id"],
        "name": spec["name"],
        "order": spec["order"],
        "provenance": PROVENANCE,
        "sources": EDITORIAL,
        "review_note": (
            "Ablauf und Texte stammen aus einer redaktionellen Zusammenfassung breit "
            "dokumentierter Inhalte. Fachliche Abnahme durch eine qualifizierte Person "
            "steht aus. Der Status wird dem Nutzer angezeigt."
        ),
        "last_updated": UPDATED,
        "units": units,
        "time_window": {**spec["time_window"], "sources": EDITORIAL},
        "audible_recitation": {
            "loud_rakat": spec["loud_rakat"],
            "description": (
                "Laute Rezitation in den genannten Rak'a, sofern im Gemeinschaftsgebet "
                "oder als Imam gebetet wird."
                if spec["loud_rakat"]
                else "Die Rezitation erfolgt in diesem Gebet still."
            ),
            "sources": EDITORIAL,
        },
        "prerequisites": build_prerequisites(),
        "sequence": build_sequence(spec["fard"], spec["loud_rakat"]),
        "learning_note": spec["learning_note"],
    }
    return prayer


# --------------------------------------------------------------------------
# Validierung und Ausgabe
# --------------------------------------------------------------------------

def load_movement_ids() -> set[str]:
    with MOVEMENTS_FILE.open(encoding="utf-8") as fh:
        data = json.load(fh)
    return {m["id"] for m in data["movements"]}


def main() -> int:
    known_movements = load_movement_ids()
    errors: list[str] = []
    written: list[str] = []

    for spec in PRAYER_SPECS:
        prayer = build_prayer(spec)

        for entry in prayer["sequence"]:
            if entry["movement_id"] not in known_movements:
                errors.append(
                    f"{spec['id']}: Schritt {entry['step']} verweist auf unbekannte "
                    f"Bewegung '{entry['movement_id']}'"
                )

        out_path = PRAYER_DIR / f"{spec['id']}.json"
        with out_path.open("w", encoding="utf-8", newline="\n") as fh:
            json.dump(prayer, fh, ensure_ascii=False, indent=2)
            fh.write("\n")
        written.append(f"{out_path.name}  ({len(prayer['sequence'])} Schritte)")

    print("Generierte Gebetsdateien:")
    for line in written:
        print(f"  {line}")

    if errors:
        print("\nFEHLER - unbekannte Bewegungsreferenzen:")
        for err in errors:
            print(f"  {err}")
        return 1

    print(f"\nAlle Bewegungsreferenzen aufgeloest ({len(known_movements)} Bewegungen bekannt).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
