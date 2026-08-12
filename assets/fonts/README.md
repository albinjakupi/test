# Schriften

Beide Schriften sind lokal eingebunden – die Website lädt dadurch nichts von
externen Servern (schneller, und kein Datenabfluss an Dritte).

| Datei | Schrift | Einsatz |
|---|---|---|
| `outfit-600.woff2`, `outfit-700.woff2` | Outfit | Titel, Buttons, Navigation |
| `source-sans-400.woff2`, `source-sans-600.woff2` | Source Sans 3 | Lauftext, Formulare |

Beide stehen unter der SIL Open Font License 1.1 und dürfen kommerziell
eingesetzt und mitgeliefert werden. Die Dateien sind auf die benötigten Zeichen
reduziert (Latein inklusive Umlaute, Zahlen, Satzzeichen, CHF-relevante
Sonderzeichen) und zusammen rund 80 KB gross.

Eingebunden werden sie über die `@font-face`-Regeln am Anfang von
`css/style.css`. Wer eine Schrift austauscht, ersetzt dort Dateinamen und
Familiennamen – und passt die Variablen `--font-display` und `--font-body` an.
