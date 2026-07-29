# ADR-0002: Kein Text-to-Speech für arabischen Korantext

**Datum:** 2026-07-29
**Status:** Akzeptiert
**Entscheider:** Betreiber, vorbereitet durch `voice-agent` und `quran-research-agent`

---

## Kontext

Das Voice-Modul soll Lerninhalte vorlesen können. Für Erklärungen, Übersetzungen und
Lernhinweise ist TTS naheliegend und nützlich.

Für **arabischen Korantext** stellt sich die Frage anders. Die naheliegende technische
Lösung — dieselbe TTS-Engine für alles — ist hier die falsche.

---

## Entscheidung

TTS wird verwendet für:

- Erklärungen und Lerntexte in der Nutzersprache
- Übersetzungen
- Instruktionen im Namaz- und Wudu-Trainer
- Einzelne arabische Buchstaben und Vokabeln im Sprachmodul, klar als Lernhilfe markiert

TTS wird **nicht** verwendet für:

- Arabischen Korantext, in keiner Länge — auch nicht für einen einzelnen Vers
- Rezitation von Gebetstexten in ihrer rituellen Form

Stattdessen: Audio-Dateien menschlicher Rezitatoren aus `voice/audio_assets/`, mit
vollständiger Quellenangabe im Manifest.

---

## Begründung

### Rezitation ist regelgebunden, TTS kennt die Regeln nicht

Koranrezitation folgt Tajwid — einem detaillierten Regelwerk für Aussprache, Verschmelzung,
Nasalierung und Dehnungslängen. Ein generisches arabisches TTS-Modell ist auf modernes
Standardarabisch trainiert und wendet diese Regeln nicht an. Das Ergebnis ist nicht
„etwas schlechter" — es ist im Sinne der Rezitationsregeln falsch.

### Falsches Lernvorbild

Ein Lernender, der eine synthetische Stimme nachahmt, lernt eine fehlerhafte Aussprache.
Bei einem Text, den viele Menschen wortgetreu memorieren, ist eine falsche
Aussprachevorlage ein Schaden, der schwer zu korrigieren ist. Das läuft dem Zweck des
Systems direkt entgegen.

### Konsistenz mit der Content Policy

`CONTENT_POLICY.md` §4.3 verbietet, dass das System Korantext generiert. Eine
Sprachsynthese des Korantexts ist eine Generierung — im Audiokanal statt im Textkanal.
Die Regel im Textkanal zu befolgen und im Audiokanal zu umgehen, wäre inkonsistent.

### Respekt ist hier auch ein Qualitätsargument

Für viele Nutzer ist die menschliche Rezitation Teil dessen, was den Text ausmacht. Eine
synthetische Version würde als Fehler des Produkts wahrgenommen, unabhängig von der
technischen Qualität. Ein Lernprodukt, dessen Kernaudio die Zielgruppe befremdet, hat
ein Produktproblem.

---

## Konsequenzen

### Positiv

- Aussprachevorbild ist korrekt, weil menschlich und regelkonform
- Quellenangabe für Audio ist möglich (Rezitator, Ausgabe, Lizenz)
- Konsistent mit der Content Policy in allen Kanälen
- Keine Abhängigkeit von der arabischen Qualität eines TTS-Anbieters

### Negativ

- Rezitations-Audio muss beschafft werden. Nur Aufnahmen mit klarer Lizenz sind nutzbar.
- Nicht jeder Vers ist sofort verfügbar. Fehlt Audio, zeigt die UI den Text ohne
  Audio-Option — sie synthetisiert nicht als Notlösung.
- Speicherbedarf für Audio-Assets
- Zwei Audio-Pfade im Code: TTS-Provider und Asset-Player

### Umsetzung

- `voice/audio_assets/manifest.json` — Zuordnung Vers → Audio, mit Rezitator und Lizenz
- `voice/tts/base.py` — `synthesize()` prüft die Sprache und lehnt arabischen
  Korantext-Input ab. Technisch durchgesetzt, nicht nur dokumentiert.
- Test in `tests/unit/test_voice_policy.py`, der beweist, dass der Aufruf abgelehnt wird
- Fehlt Audio: UI zeigt Text, keine Audio-Schaltfläche, kein Fallback auf TTS

---

## Offen

Aussprache-**Feedback** für Lernende (STT-basiert) ist von dieser Entscheidung nicht
betroffen, unterliegt aber einer eigenen Grenze: Es gibt Hinweise, kein Tajwid-Zertifikat.
Siehe `docs/CONTENT_POLICY.md` §10.5.
