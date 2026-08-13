# Werkzeuge

Die Website ist reines HTML und braucht diese Skripte **nicht**, um zu
funktionieren. Sie helfen nur dabei, wiederkehrende Arbeiten zuverlässig zu
erledigen – vor allem dort, wo dieselbe Änderung in zwanzig Dateien landen
müsste.

Alle Skripte laufen mit Python 3 ohne Zusatzpakete, ausser wo unten anders
vermerkt. Aufruf immer aus dem Projektverzeichnis:

```bash
python3 tools/pruefen.py
```

## `pruefen.py` – Qualitätskontrolle

Prüft alle HTML-Dateien auf:

- genau eine `h1` pro Seite und lückenlose Überschriftenreihenfolge
- doppelte IDs, ins Leere zeigende `href="#…"`, `aria-controls`,
  `aria-labelledby` und `label for=…`
- fehlende Dateien in `href` und `src`
- Bilder ohne `alt`, `width` oder `height`
- Links ohne Text und ohne `aria-label`
- Titel- und Beschreibungslängen, `canonical`, `og:image`, `theme-color`
- syntaktisch fehlerhafte strukturierte Daten (JSON-LD)
- nicht geschlossene HTML-Elemente

**Nach jeder inhaltlichen Änderung laufen lassen.** Die Ausgabe soll
«Keine Befunde.» sein.

## `seiten-generieren.py` – Unterseiten erzeugen

Erzeugt alle Seiten ausser `index.html` neu: Leistungsseiten, Preisrechner,
Ratgeber, Checkliste, Kontakt, Impressum, Datenschutz, Danke und 404.
Kopf- und Fusszeile werden dabei aus `index.html` übernommen – deshalb ist die
Startseite die einzige Datei, in der Navigation und Footer gepflegt werden.

**Ablauf bei einer Änderung an der Navigation:**

1. `index.html` anpassen
2. `python3 tools/seiten-generieren.py`
3. `python3 tools/pruefen.py`

Inhalte der Leistungsseiten stehen im Block `SERVICES` weit oben im Skript,
die Ratgeber-Beiträge in `RATGEBER`, die Checkliste in `CL_GRUPPEN`.

> Wer lieber direkt im HTML arbeitet, kann das tun – dann aber das Skript nicht
> mehr laufen lassen, sonst werden die Änderungen überschrieben. Beides
> gleichzeitig geht nicht.

## `illustrationen.py` – Szenen neu zeichnen

Erzeugt die sechs Szenen-Illustrationen in `assets/`. Farben und Formen stehen
direkt im Skript. Nur nötig, wenn die Illustrationen geändert werden sollen –
sobald echte Fotos vorliegen, wird es überflüssig.

## `logo-vektorisieren.py` – Logo aus einer Bilddatei nachzeichnen

Wandelt `assets/logo-original.png` in ein SVG um und misst die Verlaufsfarben
aus der Vorlage. Braucht `pillow`, `numpy` und `potracer`:

```bash
pip install pillow numpy potracer
python3 tools/logo-vektorisieren.py
```

Nur nötig, falls das Logo ersetzt wird und keine Vektordatei vorliegt.

## `vorschau-buendeln.py` – alle Seiten in einer Datei

Packt sämtliche Seiten mitsamt Schriften, Logo und Illustrationen in eine
einzige HTML-Datei (`tools/vorschau.html`, wird nicht versioniert). Praktisch,
um jemandem den aktuellen Stand zu zeigen, ohne die Website aufzuschalten:
Datei verschicken, Empfänger öffnet sie im Browser, Navigation funktioniert.

Die echte Website bleibt davon unberührt.
