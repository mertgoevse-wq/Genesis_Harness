#!/usr/bin/env python3
"""Test-Runner ohne pytest.

Warum: die Guardrails muessen ueberpruefbar sein, bevor irgendeine Abhaengigkeit
installiert ist. Ein Policy-Test, der erst nach `pip install` laeuft, schuetzt
nicht in der Situation, in der er am wichtigsten ist — beim ersten Aufsetzen.

Auf einem eingerichteten System ist `pytest tests/ -v` der normale Weg; dieselben
Testdateien laufen dort unveraendert. Dieser Runner ist der Notausgang, nicht
der Ersatz.

Aufruf:
    python tests/run_all.py
    python tests/run_all.py --only policy
"""
from __future__ import annotations

import argparse
import importlib.util
import sys
import traceback
from pathlib import Path

TESTS_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = TESTS_DIR.parent
sys.path.insert(0, str(PROJECT_ROOT))


def load_module(path: Path):
    spec = importlib.util.spec_from_file_location(f"_t_{path.stem}", path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Kann {path} nicht laden")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def run_file(path: Path) -> tuple[int, int, list[str]]:
    rel = path.relative_to(PROJECT_ROOT)
    print(f"\n{rel}")
    print("-" * 70)

    try:
        module = load_module(path)
    except Exception as exc:
        print(f"  IMPORT FEHLGESCHLAGEN: {type(exc).__name__}: {exc}")
        traceback.print_exc()
        return 0, 1, [f"{rel}: Import fehlgeschlagen"]

    tests = sorted(
        (name, fn)
        for name, fn in vars(module).items()
        if name.startswith("test_") and callable(fn)
    )

    passed = 0
    failed: list[str] = []

    for name, fn in tests:
        try:
            fn()
        except AssertionError as exc:
            failed.append(f"{rel}::{name}")
            print(f"  FEHLER  {name}")
            message = str(exc).strip()
            if message:
                for line in message.splitlines()[:4]:
                    print(f"            {line}")
        except Exception as exc:  # noqa: BLE001 - Runner faengt alles
            failed.append(f"{rel}::{name}")
            print(f"  FEHLER  {name}  ({type(exc).__name__}: {exc})")
            tb = traceback.format_exc().splitlines()
            for line in tb[-4:]:
                print(f"            {line}")
        else:
            passed += 1
            print(f"  ok      {name}")

    return passed, len(failed), failed


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--only", help="Nur Dateien, deren Name diesen Text enthält")
    args = parser.parse_args()

    files = sorted(
        path
        for path in TESTS_DIR.rglob("test_*.py")
        if args.only is None or args.only in path.name
    )
    if not files:
        print("Keine Testdateien gefunden.")
        return 1

    total_passed = 0
    all_failed: list[str] = []

    for path in files:
        passed, _, failed = run_file(path)
        total_passed += passed
        all_failed.extend(failed)

    print("\n" + "=" * 70)
    print(f"{total_passed} bestanden, {len(all_failed)} fehlgeschlagen, "
          f"{len(files)} Dateien")

    if all_failed:
        print("\nFehlgeschlagen:")
        for name in all_failed:
            print(f"  {name}")
        return 1

    print("Alle Tests bestanden.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
