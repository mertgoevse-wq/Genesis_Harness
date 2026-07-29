# Status — Islam Tutor AI

**Datum:** 2026-07-30
**Version:** 0.1.0
**Phase:** 1–4 abgeschlossen (Foundation, Knowledge, Backend/RAG, Frontend)

Dieses Dokument unterscheidet strikt zwischen **verifiziert** (in dieser Umgebung
ausgeführt und Ausgabe beobachtet), **implementiert** (Code existiert, nicht ausgeführt)
und **geplant** (existiert nicht). Verfassung §8.4.

---

## 1. Verifiziert

Ausgeführt und Ausgabe beobachtet:

| Prüfung | Ergebnis |
|---|---|
| `python3 tests/run_all.py` | **90 bestanden, 0 fehlgeschlagen**, 3 Testdateien |
| `python3 scripts/verify_knowledge.py` | **11 Dateien, 268 Datensätze, keine Verstöße**, Exit 0 |
| `python3 scripts/generate_prayers.py` | 5 Gebetsdateien, 163 Schritte, alle 14 Bewegungsreferenzen aufgelöst |
| `python3 scripts/generate_alphabet.py` | 28 Buchstaben, 8 Vokalzeichen, 9 Verwechslungsgruppen, 6 Lerneinheiten |
| Chunking der Wissensbasis | 104 Chunks: quran 8, prayer 19, purification 26, arabic 51 |
| Guardrail-Klassifikation | 6 Kategorien, alle Testfälle korrekt zugeordnet |
| Tutor-Antwortpfad | 5 Stationen durchlaufen, Trace beobachtet, Fallback-Kette greift |
| Lernplan-Generierung | 4 Ziele, 13 Tage / 14 Bausteine bei 20 min/Tag geprüft |

### Während der Entwicklung gefundene und behobene Fehler

Diese Liste steht hier, weil sie zeigt, welche Fehlerklassen dieses System betreffen:

1. **Zitatprüfung verwarf korrekte Antworten.** Die Anspruchsdeckung behandelte den
   Rahmentext des extraktiven Generators als inhaltliche Aussage. Behoben durch einen
   eigenen `verbatim`-Prüfpfad, der wortgleiches Enthaltensein verlangt — strenger als
   Anspruchsdeckung, nicht schwächer.
2. **Belastungs-Erkennung verfehlte Umlaut-Umschreibungen.** „kann nicht aufhoeren"
   lief durch, „kann nicht aufhören" nicht. Behoben mit Alternationen `(ö|oe)`.
3. **Alef Wasla brach die Rezitations-Erkennung.** Der Korantext in Uthmani-Orthographie
   nutzt ٱ, nicht ا. Kein Wortmarker griff auf Al-Fatiha — die TTS-Sperre nach ADR-0002
   wäre für echten Korantext wirkungslos gewesen. Behoben durch Alef-Normalisierung.
4. **Arabischer Buchstabenbereich zu eng.** Die Zeichenklasse endete bei ي und verfehlte
   die erweiterten Buchstaben. Behoben über Unicode-Blockprüfung.
5. **Retrieval-Ranking verzerrt.** Deutsche Funktionswörter dominierten; Übersichts-Chunks
   verdrängten präzisere Treffer. Behoben durch Stoppwortfilter und Feldgewichtung
   (BM25F-Prinzip, Titel × 3).
6. **Guardrail-Muster zu starr.** „Ist das haram?" und „Welcher Madhhab ist der beste?"
   liefen durch, weil die Muster feste Artikel erwarteten. Von den Policy-Tests gefunden.

---

## 2. Implementiert, nicht ausgeführt

Code existiert und ist vollständig, wurde aber in dieser Umgebung **nicht gestartet**.
Grund: die Sandbox hat keinen Netzwerkzugang zu PyPI, FastAPI und Pydantic sind nicht
installiert, und die verfügbare Python-Version ist 3.10 statt der deklarierten 3.11.

| Komponente | Zustand |
|---|---|
| `backend/app/main.py` | 19 Endpoints definiert, nie gestartet |
| `backend/app/services/knowledge_service.py` | vollständig, nur indirekt über die Filterlogik getestet |
| `backend/app/schemas/api.py` | Pydantic-Modelle, nie validiert |
| `backend/app/core/config.py` | Settings-Klasse, nie geladen |
| `frontend/index.html` | vollständig, nie in einem Browser geöffnet |

**Vor der Freigabe auszuführen:**

```bash
cd projects/islam-tutor
pip install -e ".[dev]"
pytest tests/ -v                        # dieselben Testdateien wie run_all.py
ruff check ai backend voice scripts
uvicorn backend.app.main:app --port 8100
# dann http://localhost:8100 öffnen und jedes Modul durchklicken
```

Die Backend- und Frontend-Ebene ist damit als **implementiert**, nicht als **verifiziert**
einzustufen. Das ist keine Formalie: die Endpoints können Tippfehler in Feldnamen
enthalten, die erst beim ersten Request auffallen.

---

## 3. Inhaltsstatus der Wissensbasis

| Provenance | Anzahl | Bedeutung |
|---|---|---|
| `verified` | 51 | Arabische Sprachinhalte — linguistisch, nicht religionsrechtlich |
| `scholar_review_pending` | 216 | **Alle Fiqh- und Koran-Inhalte.** Fachlich noch nicht abgenommen |
| `disputed` | 1 | Kopf-Abstreichen beim Wudu, vier Positionen dokumentiert |
| `placeholder` | 0 | Keine unfertigen Inhalte eingecheckt |

Der Nutzer sieht diesen Status: `scholar_review_pending`-Inhalte tragen im Frontend einen
sichtbaren Hinweis, und `/api/v1/content-status` liefert die Zahlen öffentlich.

### Was das konkret bedeutet

Kein einziger Fiqh-Inhalt in diesem Projekt ist fachlich geprüft. Die Gebetsabläufe und
Reinigungsschritte stammen aus einer redaktionellen Zusammenfassung breit dokumentierter
Inhalte — sie sind mit hoher Wahrscheinlichkeit korrekt, aber „hohe Wahrscheinlichkeit"
ist bei religiösen Inhalten kein ausreichender Standard.

Das System ist genau dafür gebaut, das nicht zu verschweigen. Die technische Grenze steht
in `knowledge/sources/registry.json`: die Quelle `editorial-fiqh-summary` trägt
`provenance_ceiling: scholar_review_pending`, und `verify_knowledge.py` setzt das durch.
Ein Inhalt mit dieser Quelle **kann** nicht auf `verified` gesetzt werden, auch nicht
versehentlich.

---

## 4. Bekannte Lücken

### Blockierend für einen produktiven Einsatz

| Lücke | Warum blockierend |
|---|---|
| **Keine fachliche Prüfung** | 216 Inhalte auf `scholar_review_pending`. Für ein Lernangebot, dem Menschen folgen, braucht es die Abnahme durch qualifizierte Personen. |
| **Korantext nicht importiert** | Nur Al-Fatiha, und die noch ohne Prüfsummen-Abgleich gegen `tanzil-uthmani`. `scripts/ingest_quran.py` ist geplant, nicht geschrieben. |
| **Lizenzstatus mehrerer Quellen ungeklärt** | Fünf Registry-Einträge tragen `license_status: needs_verification`. Vor kommerzieller oder öffentlicher Nutzung juristisch zu klären. |
| **Kein Audio** | Blockiert durch Lizenzklärung, nicht durch Technik. Für die Rachenlaute und emphatischen Laute ist ein Hörbeispiel funktional unersetzlich. |

### Nicht blockierend, aber offen

- **Semantische Suche.** `HybridStore` ist gebaut und fusioniert per Reciprocal Rank
  Fusion, aber kein Embedding-Anbieter ist angebunden. Der lexikalische Weg trägt die
  aktuelle Wissensbasis; bei Umschreibungen ohne Fachterminus wird er schwächer.
- **LLM nicht angebunden.** `AnthropicGenerator` ist implementiert, ohne API-Key läuft
  der extraktive Generator. Dessen Antworten sind quellentreu, aber trocken — sie zitieren
  statt zu erklären.
- **Kein Fortschritts-Tracking.** Kein Auth, keine Datenbank, kein Nutzerkonto.
  Der Lernplan wird generiert, aber nicht gespeichert.
- **Animationen fehlen.** Jeder Gebetsschritt trägt einen `animation_key`, aber
  `assets/animations/` ist leer. Die UI zeigt Text ohne Animation.
- **Nur Al-Fatiha im Koran-Modul.** Das Datenmodell ist vollständig und für 114 Suren
  ausgelegt; es fehlen die Daten.
- **Sprachen.** Deutsch vollständig, Englisch in den Übersetzungen teilweise, Türkisch
  nur in den Modulnamen.

---

## 5. Nächste Schritte

Executable durch einen Agenten ohne Kenntnis dieser Sitzung:

1. **Umgebung einrichten und verifizieren.**
   `cd projects/islam-tutor && pip install -e ".[dev]" && pytest tests/ -v && ruff check ai backend voice scripts`
   Dann `uvicorn backend.app.main:app --port 8100`, `http://localhost:8100` öffnen und
   alle sieben Tabs durchklicken. Jeden Fehler in `CHANGELOG.md` und im Session-Log
   festhalten.

2. **`scripts/ingest_quran.py` schreiben.**
   Lädt den Uthmani-Text von tanzil-uthmani, bildet SHA-256 über den Rohtext, schreibt
   `knowledge/quran/surah_NNN.json` und setzt `provenance: verified` **nur** bei
   übereinstimmender Prüfsumme. Die Prüfsumme wird in `registry.json` hinterlegt.
   Danach `python3 scripts/verify_knowledge.py`.

3. **Lizenzstatus klären.**
   Die fünf Einträge mit `license_status: needs_verification` in
   `knowledge/sources/registry.json` prüfen. Ergebnis dort eintragen. Ohne geklärte
   Lizenz bleibt der betroffene Inhalt aus der produktiven Auslieferung.

4. **Fachliche Prüfung organisieren.**
   `knowledge/prayer/` und `knowledge/purification/` als Pull Request zur Abnahme
   vorlegen. Nach Abnahme eine Primärquelle in `registry.json` eintragen, in den
   Datensätzen referenzieren und `provenance` auf `verified` heben — in dieser
   Reihenfolge, sonst blockiert `verify_knowledge.py`.

5. **Buchstaben-Audio beschaffen.**
   Priorität vor Rezitations-Audio. 28 Dateien nach `voice/audio_assets/letters/`,
   Einträge in `manifest.json`, `audio.available` in `alphabet.json` setzen —
   über `scripts/generate_alphabet.py`, nicht von Hand.

---

## 6. Metriken

| Metrik | Wert |
|---|---|
| Python-Dateien (ohne `__init__.py`) | 15 |
| Python-LOC | ca. 4.100 |
| JSON-Wissensdateien | 11 |
| Datensätze in der Wissensbasis | 268 |
| Abrufbare Chunks | 104 |
| Tests | 90, alle bestanden |
| Policy-Tests | 30 |
| API-Endpoints | 19 |
| Externe Laufzeit-Abhängigkeiten | 4 (FastAPI, Uvicorn, Pydantic, Pydantic-Settings) |
| ADRs | 2 |
