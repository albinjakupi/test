# Texte ändern – wo steht was?

## Die eine Regel, die man kennen muss

Es gibt **zwei Arbeitsweisen**, und man muss sich für eine entscheiden:

**Weg 1 – direkt im HTML (einfach).** Datei öffnen, Text ändern, speichern,
hochladen. Ideal für gelegentliche Korrekturen: ein Preis, ein Satz, eine
Öffnungszeit.

**Weg 2 – über den Generator (für grössere Umbauten).** Alle Seiten ausser
`index.html` werden von `tools/seiten-generieren.py` erzeugt. Wer dort eine
Änderung macht und `python3 tools/seiten-generieren.py` laufen lässt, ändert
z. B. die Navigation in einem Rutsch auf allen zwanzig Seiten.

> **Achtung:** Beides gleichzeitig geht nicht. Wer von Hand in
> `bueroreinigung.html` schreibt und danach den Generator laufen lässt,
> verliert diese Änderung. Wer nie mehr generieren will, kann `tools/` auch
> einfach löschen – die Website läuft ohne das Verzeichnis genauso.

Für den Alltag gilt: **Weg 1 ist völlig in Ordnung.** Weg 2 lohnt sich erst,
wenn Navigation, Footer oder eine Leistungsseite grundlegend umgebaut werden.

---

## Wo welcher Text steht

| Was | Datei |
|---|---|
| Startseite: Hero, Vorteile, Leistungsübersicht, Vergleichstabelle, Ablauf, FAQ | `index.html` |
| **Navigation und Footer** (gelten für alle Seiten) | `index.html` – von dort holt der Generator sie |
| Leistungsübersicht | `leistungen.html` |
| Die sechs Leistungsseiten | `unterhaltsreinigung.html`, `bueroreinigung.html`, `fensterreinigung.html`, `umzugsreinigung.html`, `bauendreinigung.html`, `liegenschaftsreinigung.html` |
| Über uns, Familienbetrieb, Werte | `ueber-uns.html` |
| Kontakt und Offertformular | `kontakt.html` |
| Preisrechner: Texte | `preisrechner.html` |
| Preisrechner: **Tarife** | `js/preisrechner.js`, Block `TARIFE` zuoberst |
| Ratgeber-Übersicht und drei Beiträge | `ratgeber.html`, `ratgeber-*.html` |
| Checkliste Wohnungsabgabe | `checkliste.html` |
| Danke-Seite nach dem Absenden | `danke.html` |
| Impressum, Datenschutz | `impressum.html`, `datenschutz.html` |
| Fehlerseite | `404.html` |
| Farben, Schriften, Abstände, Animationen | `css/style.css` |

Suchen und Ersetzen über alle Dateien funktioniert in jedem Editor
(VS Code: `Strg`/`Cmd` + `Shift` + `F`).

---

## Häufige Änderungen – Schritt für Schritt

### Telefon, E-Mail, Inhaber, UID

Nicht von Hand: Diese Angaben stehen an fast 400 Stellen (Kopfzeile, Footer,
mobile Leiste, strukturierte Daten, Impressum …). Dafür gibt es das Skript:

```bash
python3 tools/stammdaten.py --telefon "041 555 12 34"          # Probelauf
python3 tools/stammdaten.py --telefon "041 555 12 34" --anwenden
```

Weitere Schalter: `--domain`, `--inhaber`, `--uid`. Die `tel:`-Form wird aus
der Telefonnummer abgeleitet. `python3 tools/stammdaten.py` allein zeigt, was
aktuell hinterlegt ist.

### Öffnungszeiten

Über alle Dateien nach `Mo–Fr` suchen – die Zeiten stehen im Footer jeder
Seite und im Kontaktbereich von `kontakt.html`. Zusätzlich stehen sie in den
strukturierten Daten in `index.html` (`openingHoursSpecification`, Suchbegriff
`"opens"`). Diese Stelle nicht vergessen, sonst zeigt Google andere Zeiten an
als die Website.

### Preise im Rechner

`js/preisrechner.js`, ganz oben:

```js
var TARIFE = {
  stundensatz: [45, 55],              // von / bis, in CHF
  umzugBasis: {'1.5':390, '2.5':490, '3.5':690, '4.5':890, '5.5':1090},
  fensterProFluegel: [6, 9],  fensterMinimum: 180,
  bueroProM2: [0.45, 0.65],   bueroMinimum: 90,
  bauProM2: { grob:[4,6], fein:[6,9], end:[7,11] },  bauMinimum: 400,
  liegenschaftProWohnung: [10, 16], liegenschaftMinimum: 120
};
```

Die Zahlen auf den Leistungsseiten (Abschnitt «Richtpreis») stehen separat im
jeweiligen HTML und müssen mitgeändert werden – sonst widersprechen sich
Rechner und Text.

### Eine Leistung umbenennen oder eine neue aufnehmen

Das betrifft viele Stellen: Navigation, Footer, Startseite, Übersicht,
Rechner, Formular-Auswahl, `sitemap.xml`. Hier lohnt sich Weg 2:

1. In `tools/seiten-generieren.py` den Block `SERVICES` anpassen (jede Leistung
   ist ein `dict` mit `file`, `name`, `title`, `desc`, `lead`, `pills`,
   `bullets`, `table_rows`, `price` und `faqs`)
2. `python3 tools/seiten-generieren.py`
3. `python3 tools/pruefen.py`
4. `index.html`, `sitemap.xml` und `js/preisrechner.js` von Hand nachziehen

### Einen Ratgeber-Beitrag ergänzen

Block `RATGEBER` in `tools/seiten-generieren.py`, dann generieren. Der Beitrag
erscheint automatisch in der Übersicht und erhält strukturierte Daten.
Alternativ: eine bestehende `ratgeber-*.html` kopieren und von Hand anpassen –
dann aber `ratgeber.html` und `sitemap.xml` nicht vergessen.

### Farben

`css/style.css`, Abschnitt 2 «Design-Tokens». Die Markenfarben stammen aus dem
Logo:

```css
--mint: #26CEB1;  --sky: #26AFD0;  --blue: #2581FF;
```

Eine Änderung hier wirkt auf die ganze Website, inklusive Verläufe, Buttons
und Favicon-Hintergrund.

### Fotos einsetzen

Sobald echte Bilder vorliegen (siehe `docs/fotoguide.md`): in `assets/img/`
ablegen und die Illustration in der jeweiligen Seite ersetzen:

```html
<!-- vorher -->
<img src="assets/illu-buero.svg" alt="…" width="640" height="480">
<!-- nachher -->
<img src="assets/img/buero-sitzungszimmer.jpg" alt="Gereinigtes Sitzungszimmer …"
     width="1600" height="1067" loading="lazy">
```

`width` und `height` müssen den echten Pixelmassen entsprechen, sonst springt
das Layout beim Laden. `alt` beschreibt, was zu sehen ist – das liest der
Screenreader vor und Google wertet es aus.

---

## Nach jeder Änderung

```bash
python3 tools/pruefen.py
```

Prüft alle Seiten auf kaputte Links, fehlende Dateien, doppelte IDs, Bilder
ohne Grössenangabe, zu lange Seitentitel und fehlerhafte strukturierte Daten.
Die Ausgabe soll «Keine Befunde.» lauten.

Zum Anschauen vor dem Hochladen genügt ein Doppelklick auf `index.html`.
Wer den Stand jemandem schicken will, ohne aufzuschalten:

```bash
python3 tools/vorschau-buendeln.py
```

erzeugt `tools/vorschau.html` – eine einzige Datei mit allen Seiten,
Schriften und Bildern darin.
