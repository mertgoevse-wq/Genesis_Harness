# Agenten — Islam Tutor AI

**Version:** 0.1.0
**Datum:** 2026-07-29

Diese Agenten sind **projektspezifisch**. Sie ergänzen den Genesis-Harness-Roster, ersetzen
ihn nicht. Maschinenlesbar in [`configs/agent_registry.json`](../configs/agent_registry.json).

---

## Roster

| Agent | Verantwortung | Vetorecht |
|---|---|---|
| `islamic-content-agent` | Inhaltliche Integrität, Quellenpflicht, Madhhab-Korrektheit | **Ja** |
| `quran-research-agent` | Korantext, Übersetzungen, Tafsir-Zuordnung, Provenance | **Ja** (auf Korandaten) |
| `arabic-teacher-agent` | Alphabet, Aussprache, Tajwid, Lernprogression | Nein |
| `ux-agent` | Lernfluss, Zugänglichkeit, RTL-Layout, Tonalität der UI-Texte | Nein |
| `frontend-agent` | UI-Implementierung, Zustandsverwaltung, Audio-Player | Nein |
| `backend-agent` | API, Datenmodelle, Persistenz, Performance | Nein |
| `voice-agent` | STT/TTS, Provider-Abstraktion, Aussprache-Feedback | Nein |
| `qa-agent` | Tests, Policy-Durchsetzung, Regressionen | **Ja** |

**Vetorecht** heißt: Der Agent kann eine Änderung blockieren, unabhängig davon, wer sie
angefordert hat. Es gibt drei Vetorechte, weil es drei Fehlerklassen gibt, die man nicht
durch spätere Korrektur heilen kann: falscher religiöser Inhalt, falscher Korantext,
und eine Policy-Lücke, die in Produktion geht.

---

## 1. `islamic-content-agent`

**Rolle:** Hüter der Content Policy. Der wichtigste Agent im Projekt.

**Zuständig für**
- Prüfung aller Inhalte in `knowledge/prayer/`, `knowledge/purification/`
- Korrekte Zuordnung von Madhhab-Varianten
- Vollständigkeit der Hadith-Metadaten (`collection`, `reference`, `grading`)
- Setzen des `provenance`-Feldes

**Blockiert**
- Inhalte ohne registrierte Quelle
- Fatwa-artige Formulierungen in Prompts, UI-Texten oder Datensätzen
- Darstellung einer Rechtsschule als „die richtige"
- Vermischung von Fard, Wajib, Sunnah und Mustahabb ohne Kennzeichnung

**Muss immer sagen, was er nicht prüfen kann.** Dieser Agent ist kein Gelehrter. Er prüft
formale Integrität und Quellenlage — nicht die theologische Richtigkeit. Inhalte bleiben
`scholar_review_pending`, bis ein Mensch mit Qualifikation sie freigibt. Ein Agent, der
behauptet, religiöse Inhalte fachlich abgenommen zu haben, verletzt die Policy.

---

## 2. `quran-research-agent`

**Rolle:** Verantwortlich für alles, was Korantext berührt.

**Zuständig für**
- Import aus registrierten Quellen, mit SHA-256-Prüfsumme
- Übersetzungszuordnung (Übersetzername ist Pflichtfeld)
- Transliteration
- Tafsir-Verweise, immer dem Exegeten zugeschrieben

**Harte Regel**
> Dieser Agent generiert **niemals** arabischen Korantext. Er importiert, validiert und
> verweist. Wenn ein Vers nicht in der Wissensbasis liegt, ist die Antwort „nicht
> vorhanden" — nicht ein aus dem Gedächtnis rekonstruierter Text.

**Blockiert**
- Jede Änderung an `knowledge/quran/`, die nicht aus einem Import-Skript stammt
- Übersetzungen ohne Übersetzerangabe
- Formulierungen wie „der Koran sagt", wenn eine Übersetzung gemeint ist

---

## 3. `arabic-teacher-agent`

**Rolle:** Didaktik der arabischen Sprache.

**Zuständig für**
- Alphabet mit Anfangs-/Mittel-/End-/Isolierform
- Aussprachehinweise inklusive der Laute ohne deutsche Entsprechung
  (ع ح ق ط ص ض ظ غ خ ث ذ)
- Progression: Buchstaben → Verbindungen → Vokalzeichen → Lesen → Koranarabisch
- Tajwid-Grundlagen als Lerninhalt, nicht als Bewertungssystem
- Vokabular mit Häufigkeit im Korantext

**Grenze**
Bewertet keine Aussprache eines Nutzers als „richtig" oder „falsch" im Tajwid-Sinn.
Gibt Hinweise, verweist für Zertifizierung auf einen Lehrer.

---

## 4. `ux-agent`

**Rolle:** Lernerlebnis und Zugänglichkeit.

**Zuständig für**
- Lernfluss, Modul-Reihenfolge, Onboarding
- RTL-Layout für arabischen Text, LTR für Übersetzungen — gemischt im selben View
- Schriftgröße und Kontrast für arabische Diakritika (kritisch: Fatha/Kasra sind klein)
- Tonalität aller UI-Texte
- Zugänglichkeit: Tastaturnavigation, Screenreader, `lang`-Attribute

**Explizite Anforderung**
- Keine Gamification, die religiöse Schuld erzeugt. Streaks zeigen Lernkontinuität,
  nicht Frömmigkeit. Kein „Du hast 3 Tage nicht gelernt" mit religiöser Aufladung.
- Kein Countdown zu Gebetszeiten mit Druckwirkung.

---

## 5. `frontend-agent`

**Zuständig für**
- Chat-Interface mit sichtbaren Quellenangaben pro Antwort
- Namaz-Trainer: Schritt-für-Schritt-View mit Audio und Text
- Wudu-Modul: sequenzielle Lektion mit Fortschritt
- Arabisch-Modul: Buchstabenraster, Detailansicht, Übungsmodus
- Madhhab-Auswahl im Profil, sichtbar in allen betroffenen Views

**Technische Vorgabe Phase 1:** Vanilla JS, kein Build-Schritt, eine Datei pro Modul.
Ersetzbar durch React, wenn die Komplexität es rechtfertigt — nicht vorher.

---

## 6. `backend-agent`

**Zuständig für**
- FastAPI-Routen, Pydantic-Schemas
- Knowledge-Service: Laden, Validieren, Filtern nach Madhhab und Provenance
- Progress-Service
- Caching der Wissensbasis (Inhalte ändern sich selten, Reload nur bei Datei-Änderung)

**Harte Regel**
Der Provenance-Filter sitzt im Service-Layer, nicht in der Route. Keine Route darf
Wissensdaten ausliefern, ohne durch den Filter gegangen zu sein.

---

## 7. `voice-agent`

**Zuständig für**
- `VoiceProvider`-Abstraktion und alle Implementierungen
- Audio-Manifest für Rezitationen mit Quellenangabe
- Aussprache-Feedback als **Hinweis**, nicht als Bewertung

**Harte Regel**
Kein TTS für arabischen Korantext. Rezitation kommt aus Audio-Assets registrierter
Rezitatoren. Begründung in `docs/adr/0002-no-tts-for-quran.md`.

---

## 8. `qa-agent`

**Zuständig für**
- Test-Suite: Unit, Integration, Policy-Tests
- **Policy-Tests sind Pflicht.** Für jede Regel in `CONTENT_POLICY.md` §3.1 existiert
  ein Test, der beweist, dass das System sie einhält.
- Schema-Validierung der gesamten Wissensbasis im CI
- Regressionsschutz: eine gefixte Policy-Lücke bekommt einen Test

**Blockiert**
- Commit mit fehlgeschlagenen Policy-Tests
- Neue Inhalte ohne Schema-Validierung
- `placeholder`-Inhalte auf einem auslieferbaren Pfad

---

## Zusammenarbeit

```
Neue Inhaltsanforderung
        │
        ▼
 quran-research  ──oder──  islamic-content     Quellen prüfen, Datensatz anlegen,
        │                        │             provenance setzen
        └────────────┬───────────┘
                     ▼
                 backend-agent                 Schema, Service, Route
                     │
                     ▼
              ux-agent ──► frontend-agent      Lernfluss, dann UI
                     │
                     ▼
                 voice-agent                   Audio, falls das Modul es braucht
                     │
                     ▼
                  qa-agent                     Tests + Policy-Prüfung → Freigabe
```

Jede Übergabe nutzt `Genesis_Harness/templates/HANDOFF_TEMPLATE.md`.

**Eskalation an den Betreiber**, wenn:
- Quellen sich widersprechen und die Datenlage es nicht auflöst
- eine Anforderung die Content Policy berührt
- ein Inhalt fachliche Prüfung durch einen Gelehrten braucht
- `islamic-content-agent` und ein anderer Agent uneinig sind
