# ADR-0001: Wissensbasis als versionierte JSON-Dateien

**Datum:** 2026-07-29
**Status:** Akzeptiert
**Entscheider:** Betreiber, vorbereitet durch `islamic-content-agent`

---

## Kontext

Islam Tutor AI braucht eine Wissensbasis für Korantexte, Gebetsabläufe, Reinigungsrituale
und arabische Sprachinhalte. Diese Inhalte sind religiös sensibel: ein Fehler ist nicht
nur ein Bug, sondern potenziell eine falsche Aussage über die Religion einer Person.

Optionen:

1. **Relationale Datenbank** mit Admin-UI
2. **Headless CMS** (Strapi, Directus)
3. **Versionierte JSON-Dateien** in Git
4. **Vector Store als Primärspeicher**

---

## Entscheidung

**Versionierte JSON-Dateien in Git**, validiert gegen JSON-Schema, als *Source of Truth*.
Der Vector Store ist ein abgeleiteter Index, nie die Primärquelle.

---

## Begründung

### Reviewbarkeit ist wichtiger als Editier-Komfort

Eine Änderung an einem Gebetsablauf muss von einem Menschen geprüft werden können, bevor
sie live geht. Ein Git-Diff zeigt genau: diese Zeile war vorher X, jetzt ist sie Y, geändert
von Z, mit dieser Begründung im Commit.

Ein CMS-Edit hinterlässt ein Audit-Log, aber keinen reviewbaren Diff im normalen
Entwicklungsprozess. Und ein Datenbank-UPDATE hinterlässt gar nichts.

### Content-Review als Pull Request

Wenn ein Gelehrter oder fachkundiger Prüfer Inhalte abnehmen soll, ist der Pull Request
der natürliche Ort: Diff lesen, kommentieren, freigeben. Das ist kein Umweg, sondern
genau der Prozess, den religiöse Inhalte brauchen.

### Kein stiller Drift

Bei einer Datenbank kann Inhalt sich ändern, ohne dass es im Repository sichtbar wird.
Das ist bei generischer Software akzeptabel und hier nicht: Was das System über das
Gebet sagt, muss zu jedem Zeitpunkt aus dem Repository rekonstruierbar sein.

### Prüfsummen sind trivial

Der Korantext trägt eine SHA-256-Prüfsumme. Bei Dateien ist das eine Zeile im
Verify-Skript. In einer Datenbank bräuchte es Trigger oder eine separate Integritätstabelle.

### Datenmenge ist unkritisch

Vollständiger Korantext mit mehreren Übersetzungen liegt im einstelligen bis niedrigen
zweistelligen MB-Bereich. Fiqh- und Sprachinhalte sind deutlich kleiner. Das lädt
vollständig in den Speicher — es gibt kein Skalierungsproblem, das eine Datenbank löst.

---

## Konsequenzen

### Positiv

- Jede Inhaltsänderung ist diffbar, reviewbar, rückrollbar
- Schema-Validierung läuft im CI und blockiert fehlerhafte Inhalte vor dem Merge
- Prüfsummenvalidierung des Korantexts ist einfach umsetzbar
- Keine Infrastruktur-Abhängigkeit für die Kerninhalte
- Offline-fähig

### Negativ

- Kein Web-Editor für Nicht-Techniker. Content-Beiträge brauchen Git-Kenntnis oder
  einen Vermittler. **Bewusst akzeptiert** — die Hürde ist bei diesem Inhaltstyp ein
  Feature, nicht ein Mangel.
- Volltextsuche muss selbst gebaut werden (macht die RAG-Pipeline ohnehin)
- Bei sehr großen Übersetzungssammlungen wird ein Lazy-Loading-Mechanismus nötig

### Abgrenzung

Nutzerdaten — Fortschritt, Profil, Chatverlauf — liegen **nicht** in Dateien, sondern in
einer Datenbank (SQLite → PostgreSQL). Diese Entscheidung betrifft ausschließlich die
Wissensbasis.

---

## Umsetzung

- `knowledge/schema/*.json` — JSON-Schema pro Inhaltstyp
- `scripts/verify_knowledge.py` — Validierung, blockiert bei Fehler
- Vector Store wird aus den Dateien gebaut, nie umgekehrt
- Pflichtfelder in jedem Datensatz: `id`, `provenance`, `sources[]`, `madhhab`
