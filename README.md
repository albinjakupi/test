# Website Cleeno Reinigungen

Statische Website für den Reinigungsbetrieb Cleeno Reinigungen (Perlen LU) –
reines HTML, CSS und JavaScript, ohne Build-Schritt, ohne Framework und ohne
externe Abhängigkeiten. Schriften, Logo und Icons liegen im Projekt: Die Seite
lädt nichts von fremden Servern, ist dadurch schnell und
datenschutzfreundlich.

## Schnellstart

Doppelklick auf `index.html` genügt zum Anschauen. Für ein realistischeres Bild
lokal einen kleinen Server starten:

```bash
python3 -m http.server 8000
# danach http://localhost:8000 öffnen
```

## Aufbau

```
index.html                    Startseite (Hero mit Schnellofferte, Leistungen,
                              Garantien, Vergleich, Ablauf, Einsatzgebiet, FAQ)
leistungen.html               Übersicht aller Leistungen inkl. Richtpreisen
preisrechner.html             Interaktiver Preisrechner mit Übergabe an die Offerte
unterhaltsreinigung.html      Detailseite Leistung
bueroreinigung.html           Detailseite Leistung
fensterreinigung.html         Detailseite Leistung
umzugsreinigung.html          Detailseite Leistung (inkl. Preistabelle)
bauendreinigung.html          Detailseite Leistung
liegenschaftsreinigung.html   Detailseite Leistung
ueber-uns.html                Familienbetrieb, sechs USP, Fakten, offene Stellen
kontakt.html                  Offertformular, Kontaktangaben, FAQ
impressum.html                Impressum (Einzelfirma)
datenschutz.html              Datenschutzerklärung nach Schweizer DSG
ratgeber.html                 Übersicht der Ratgeber-Beiträge
ratgeber-wohnungsabgabe.html  Checkliste für die Wohnungsübergabe
ratgeber-umzugsreinigung-kosten.html   Preise und Kostenfaktoren
ratgeber-reinigungsplan-buero.html     Reinigungsplan mit Vorlage
checkliste.html               Druckbare Checkliste zur Wohnungsabgabe (47 Punkte)
danke.html                    Bestätigung nach dem Absenden des Formulars
404.html                      Fehlerseite
_headers                      Sicherheits- und Cache-Regeln (Netlify, Cloudflare)
site.webmanifest              App-Symbol und Name beim Speichern auf dem Startbildschirm
css/style.css                 Gesamtes Design (Design-Tokens zuoberst)
js/main.js                    Navigation, Scroll-Effekte, Reiter, Vergleichsregler,
                              Formularvalidierung
js/preisrechner.js            Rechenlogik und Tarife des Preisrechners
assets/logo.svg               Wortmarke Cleeno, aus der Vorlage vektorisiert
assets/logo-original.png      gelieferte Originaldatei
assets/favicon.svg            Browser-Symbol
assets/og-cleeno.png          Vorschaubild beim Teilen (WhatsApp, LinkedIn, Facebook)
assets/icon-192.png, icon-512.png, apple-touch-icon.png   App-Symbole
assets/illu-vorher.svg        Illustration für den Vorher/Nachher-Regler
assets/illu-nachher.svg       dieselbe Szene nach der Reinigung
assets/illu-buero.svg …       sechs Szenen-Illustrationen für die Leistungsseiten
docs/veroeffentlichen.md      Anleitung: Hosting, Domain, Formular, Google
docs/texte-aendern.md         Anleitung: welcher Text in welcher Datei steht
docs/fotoguide.md             Aufnahmeliste und Regeln für eigene Fotos
tools/                        Hilfsskripte (Generator, Prüfung, Vorschau) – siehe tools/README.md
assets/fonts/                 Outfit und Source Sans 3, lokal eingebunden
assets/img/                   Ablage für eigene Fotos
robots.txt, sitemap.xml       Für Suchmaschinen
```

Header und Footer stehen in jeder Datei gleich drin (so funktioniert eine
statische Seite ohne Build-Schritt). Wer etwas an der Navigation ändert, muss
die Änderung in allen Dateien nachziehen – am schnellsten mit
Suchen-und-Ersetzen über alle `.html`-Dateien.

## Noch offen: diese Angaben ersetzen

Firmenname, Rechtsform, Adresse und Einsatzgebiet sind eingetragen. Diese
Platzhalter fehlen noch. Sie stehen an rund 400 Stellen – deshalb nicht von
Hand ersetzen, sondern mit `tools/stammdaten.py`:

```bash
python3 tools/stammdaten.py --telefon "041 555 12 34" --inhaber "Vorname Name" \
                            --uid "CHE-123.456.789 MWST"           # Probelauf
python3 tools/stammdaten.py --telefon "041 555 12 34" --anwenden   # schreibt
```

| Platzhalter | Bedeutung |
|---|---|
| `041 123 45 67` | Telefonnummer (Anzeige) – **erfunden, unbedingt ersetzen** |
| `+41411234567` | dieselbe Nummer in `tel:`-Links |
| `cleeno-reinigungen.ch` | Domain – aus dem Namen abgeleitet, noch nicht bestätigt |
| `offerte@` / `info@` / `datenschutz@` / `jobs@cleeno-reinigungen.ch` | E-Mail-Adressen |
| `[Vor- und Nachname eintragen]` | Inhaber im Impressum |
| `[CHE-000.000.000 eintragen]` | UID- / MWST-Nummer im Impressum |

Ebenfalls prüfen:

- **Preise** in `leistungen.html`, `umzugsreinigung.html`, den FAQ-Blöcken und im
  Preisrechner – aktuell branchenübliche Richtwerte, keine kalkulierten Zahlen.
  **Bitte vor dem Livegang mit den eigenen Kalkulationen abgleichen** (siehe
  Abschnitt «Preisrechner»).
- **Garantien** (Festpreis, Abnahme, Reaktion innert 24 Stunden): Sie stehen
  prominent auf jeder Seite. Bitte nur so stehen lassen, wie sie auch
  eingehalten werden.
- **Vergleichstabelle** auf der Startseite: Die Spalte «Häufig bei anderen»
  ist bewusst zurückhaltend formuliert. Konkrete Mitbewerber sollten dort
  weiterhin nicht genannt werden.
- **Impressum und Datenschutz**: Vorlagen, die vor der Veröffentlichung
  rechtlich geprüft werden sollten. Eine Einzelfirma muss im Firmennamen den
  Familiennamen des Inhabers führen – die vollständige Firmenbezeichnung gehört
  deshalb ins Impressum.
- **Strukturierte Daten** (`application/ld+json`) am Ende von `index.html`.

Bewusst **nicht** enthalten sind erfundene Kundenstimmen, Mitarbeiterzahlen
oder Bewertungen. Sobald echte Referenzen vorliegen, lassen sie sich als
eigener Abschnitt ergänzen.

## Logo

`assets/logo.svg` ist direkt aus der gelieferten Bilddatei vektorisiert: Die
Konturen wurden aus dem Original nachgezeichnet, die Verlaufsfarben spaltenweise
daraus gemessen. Das Ergebnis ist konturgleich mit der Vorlage, aber bei jeder
Grösse scharf und nur rund 4 KB gross. Die Originaldatei liegt unverändert als
`assets/logo-original.png` daneben.

Falls das Logo als echte Vektordatei (SVG, AI, EPS) vorliegt, kann sie
`assets/logo.svg` einfach ersetzen – im HTML muss nichts geändert werden.
`assets/favicon.svg` enthält das «C» aus derselben Vorlage auf einer
Verlaufsfläche.

Aus dem Logo stammt auch die Farbwelt der Website. Alle Farben stehen als
CSS-Variablen zuoberst in `css/style.css`:

| Variable | Wert | Einsatz |
|---|---|---|
| `--mint` | `#26CEB1` | Verlauf links (Logo), Häkchen, Akzente |
| `--blue` | `#2581FF` | Verlauf rechts (Logo) |
| `--blue-deep` | `#1467E0` | Links, Buttons, Icons |
| `--ink` | `#0C1B33` | Titel und Fliesstext |
| `--bg-deep` | `#0A1830` | Footer und Aktionsflächen |

## Schriften

Outfit (Titel, Buttons) und Source Sans 3 (Lauftext) liegen unter
`assets/fonts/`, sind auf die benötigten Zeichen reduziert und zusammen rund
80 KB gross. Beide stehen unter der SIL Open Font License und dürfen
kommerziell verwendet werden. Details in `assets/fonts/README.md`.

## Interaktive Bausteine

| Baustein | Wo | Was es tut |
|---|---|---|
| Preisrechner | `preisrechner.html` | Drei Schritte, Live-Preisspanne, Übergabe an das Offertformular |
| Schnelleinstieg | Startseite, Hero | Leistung wählen und direkt im Rechner landen |
| Leistungsumfang | Startseite | Reiter nach Bereich (Küche, Bad, Wohnräume, Fenster, Extras) |
| Vorher/Nachher | Startseite | Regler zum Vergleichen, per Maus, Finger und Tastatur bedienbar |
| Sprungnavigation | Leistungsseiten | Klebt unter dem Kopf und markiert den sichtbaren Abschnitt |
| Fortschrittsbalken | alle Seiten | Zeigt die Leseposition am oberen Rand |
| Zähler | Startseite, Über uns | Zahlen laufen beim Sichtbarwerden hoch |
| Checkliste | `checkliste.html` | 47 Punkte zum Abhaken, Fortschritt bleibt gespeichert, druckbar |

Alle Effekte respektieren `prefers-reduced-motion`, und ohne JavaScript bleiben
sämtliche Inhalte lesbar: Die Reiter zeigen dann den ersten Bereich, der
Vergleichsregler steht in der Mitte, und statt des Rechners erscheint ein
Hinweis mit Link auf die Richtpreise und das Offertformular.

## Checkliste und Danke-Seite

`checkliste.html` ist mehr als ein Beitrag: 47 Kontrollpunkte zum Abhaken, mit
Fortschrittsbalken. Der Stand wird im Browser des Besuchers gespeichert
(`localStorage`) – wer die Seite Tage später wieder öffnet, findet die Häkchen
vor. Es werden keine Daten an uns übertragen; ein Cookie-Hinweis ist dafür
nicht nötig, weil die Speicherung ausschliesslich lokal und funktional ist.

Der Druckknopf erzeugt eine zweiseitige Fassung im Zweispaltensatz mit Logo und
Kontaktzeile – gedacht für den Rundgang durch die leere Wohnung. Solche
Werkzeuge werden verlinkt und weitergegeben; das ist die günstigste Werbung,
die es gibt.

Nach dem Absenden des Offertformulars landen Besucher auf `danke.html`. Das ist
nicht nur freundlicher als eine Statusmeldung, sondern die Voraussetzung für
Erfolgsmessung: Wer später Google Ads schaltet, zählt genau diesen Seitenaufruf
als Anfrage.

## Preisrechner

Die Rechenlogik steht in `js/preisrechner.js`. Ganz oben in der Datei liegt der
Block `TARIFE` – dort und nur dort werden die Ansätze gepflegt:

```js
var TARIFE = {
  stundensatz: [45, 55],        // CHF pro Stunde, Unterhaltsreinigung
  umzugBasis: { '1.5': 390, '2.5': 490, '3.5': 690, ... },
  fensterProFluegel: [6, 9],
  bueroProM2: [0.45, 0.65],     // pro Einsatz
  ...
};
```

Jede Leistung hat darunter einen eigenen Block mit Feldern, Auswahlmöglichkeiten
und Extras. Wer eine Position ergänzen will, kopiert einen bestehenden Eintrag –
die Oberfläche baut sich daraus automatisch auf.

**Wichtig:** Die hinterlegten Werte sind branchenübliche Erfahrungswerte, keine
Kalkulation dieses Betriebs. Bitte vor dem Aufschalten prüfen und mit den
Richtpreisen auf den Leistungsseiten abgleichen. Der Rechner weist an mehreren
Stellen darauf hin, dass es sich um eine unverbindliche Schätzung handelt –
dieser Hinweis sollte stehen bleiben.

## Sichtbarkeit bei Google und in sozialen Netzwerken

Jede Seite liefert strukturierte Daten (JSON-LD) aus, damit Suchmaschinen die
Inhalte einordnen können:

| Seite | Strukturierte Daten |
|---|---|
| Startseite | `CleaningService` mit Adresse, Öffnungszeiten, Einsatzgebiet, plus `FAQPage` |
| Leistungsseiten | `Service`, `FAQPage`, `BreadcrumbList` |
| Ratgeber-Beiträge | `Article`, `BreadcrumbList` |
| Kontakt, Preisrechner | `FAQPage`, `BreadcrumbList` |

Die FAQ-Auszeichnung ist der Grund, warum Google einzelne Fragen direkt im
Suchergebnis anzeigen kann. Wenn Sie Fragen und Antworten im HTML ändern,
laufen die strukturierten Daten automatisch mit – sie werden aus demselben
Text erzeugt.

Beim Teilen eines Links erscheint `assets/og-cleeno.png` als Vorschaubild.
Wer es neu erzeugen will, passt die Vorlage an und exportiert wieder mit
1200 × 630 Pixeln.

## Ratgeber erweitern

Die drei Beiträge sind bewusst als Nachschlagewerk geschrieben, nicht als
Werbetexte – das ist der Grund, warum solche Seiten überhaupt gefunden und
verlinkt werden. Weitere Themen mit Potenzial: Kalk in Badezimmern,
Bodenpflege nach Material, Hygiene in Gemeinschaftsküchen, Winterdienst und
Räumungspflicht.

Beim Ergänzen eines Beitrags gehören dazu: eine eigene Seite nach dem Muster
der bestehenden, ein Eintrag in `ratgeber.html`, eine Zeile in `sitemap.xml`
und die Verlinkung am Ende der verwandten Beiträge.

## Bilder einsetzen

Wo jetzt farbige Flächen mit Symbol stehen (`<div class="media">`), gehören
später echte Fotos hin – Team, Referenzobjekte, Vorher/Nachher. Eigene Bilder
in `assets/img/` ablegen und den Block ersetzen:

```html
<div class="media">
  <img src="assets/img/team-bei-der-arbeit.jpg"
       alt="Zwei Mitarbeitende reinigen ein Treppenhaus" width="1200" height="900" loading="lazy">
</div>
```

Empfehlung: Breite ca. 1600 px, als WebP oder JPEG mit rund 150–250 KB. Jedes
Bild braucht ein aussagekräftiges `alt`-Attribut. Echte Fotos vom eigenen Team
wirken deutlich stärker als Stockbilder – gerade bei einem Familienbetrieb.

Alle Bildplätze zeigen zurzeit selbst gezeichnete Illustrationen im Markenstil
– sie geben sich bewusst nicht als Fotografie aus. Welche Aufnahmen die Website
braucht und worauf rechtlich zu achten ist, steht in **`docs/fotoguide.md`**.

**Vorher/Nachher:** Der Regler auf der Startseite zeigt zurzeit zwei
Illustrationen. Sobald echte Aufnahmen vorliegen, ersetzen Sie einfach die beiden
`<img>`-Quellen im Block `<div class="ba">` – wichtig ist nur, dass beide Bilder
dieselbe Kameraposition und dasselbe Seitenverhältnis haben. Danach den
Hinweissatz «Schematische Darstellung …» darunter entfernen.

## Offertformular anschliessen

Standardmässig gibt es kein Backend: Beim Absenden prüft `js/main.js` die
Eingaben und öffnet anschliessend das E-Mail-Programm mit einer fertig
ausgefüllten Nachricht. Das funktioniert überall, ist aber nicht besonders
komfortabel.

Für einen echten Versand einen Formulardienst eintragen – oben in `js/main.js`:

```js
var FORM_ENDPOINT = 'https://formspree.io/f/xxxxxxx';  // z. B. Formspree, Getform, Basin
var FALLBACK_MAIL = 'offerte@ihre-domain.ch';
```

Ist `FORM_ENDPOINT` gesetzt, wird das Formular per `fetch` an den Dienst
gesendet, ohne dass die Seite neu lädt; Erfolg und Fehler erscheinen direkt
über dem Formular. Ein verstecktes Honeypot-Feld hält einfache Spam-Bots ab.

Die Schnellofferte im Hero und die Buttons auf den Leistungsseiten übergeben
die gewünschte Leistung als `?leistung=…` an die Kontaktseite, wo das
Auswahlfeld automatisch vorbelegt wird.

## Veröffentlichen

Es müssen nur die Dateien auf den Server – kein Build, kein Node.

- **Eigenes Hosting**: Inhalt des Ordners per FTP/SFTP ins Web-Root laden.
- **Netlify / Cloudflare Pages**: Repository verbinden, Build-Befehl leer
  lassen, Publish-Verzeichnis `/`.
- **GitHub Pages**: In den Repository-Einstellungen unter *Pages* den Branch
  wählen und als Ordner `/ (root)` angeben.

Die Domain in `sitemap.xml`, `robots.txt` und in den `canonical`-Links ändert
`python3 tools/stammdaten.py --domain … --anwenden` in einem Durchgang.

**Ausführliche Anleitungen:**

- [`docs/veroeffentlichen.md`](docs/veroeffentlichen.md) – Hosting im Vergleich,
  Domain, HTTPS, Formularempfang, Google-Eintrag
- [`docs/texte-aendern.md`](docs/texte-aendern.md) – welcher Text in welcher
  Datei steht und wie man ihn gefahrlos ändert

## Besucherzahlen messen (optional)

Die Website enthält bewusst keine Analyse-Werkzeuge. Wer trotzdem wissen will,
was funktioniert, nimmt am besten einen Dienst ohne Cookies – dann bleibt der
Cookie-Banner aus und die Datenschutzerklärung braucht nur einen kurzen Absatz.
Der Aufruf von `danke.html` ist dabei das wichtigste Ereignis: Er entspricht
einer eingegangenen Anfrage.

Was danach zu tun ist: Abschnitt 4 der Datenschutzerklärung ergänzen (dort steht
heute ausdrücklich, dass keine Analysedienste eingebunden sind) und den Hinweis
«Keine Cookies, kein Tracking» in der Fusszeile prüfen.

## Gestaltung

Abschnitt 17 in `css/style.css` («Feinschliff») enthält alles, was rein
visuell wirkt: die treibenden Lichter im Hero, die Verlaufskante auf Karten
beim Überfahren, den Schimmer auf der Hauptaktion, die feine Textur auf
dunklen Flächen und das gestaffelte Einblenden von Rasterinhalten. Der Block
lässt sich vollständig löschen, ohne dass Struktur oder Funktion leiden – das
ist Absicht.

Sämtliche Bewegung hält sich an `prefers-reduced-motion`: Wer im
Betriebssystem reduzierte Bewegung eingestellt hat, sieht eine ruhige Seite.

## Bewegung und Seitenübergänge

Abschnitt 18 in `css/style.css` bündelt alle Bewegung:

| Was | Wo |
|---|---|
| Weicher Übergang beim Seitenwechsel | alle Seiten, über `@view-transition` |
| Gestaffelter Auftritt von Titel, Text und Karte | Startseite und Seitenköpfe |
| Aufklappen des mobilen Menüs | überall |
| Einblenden der FAQ-Antworten | überall |
| Bilder ziehen beim Hereinscrollen leicht auf | Leistungsseiten |
| Preis pulsiert bei Auswahländerung | Preisrechner |

Die Seitenübergänge nutzen die View-Transitions-Schnittstelle des Browsers.
Kopfzeile und mobile Aktionsleiste sind davon ausgenommen und bleiben beim
Wechsel stehen – das lässt den Wechsel ruhiger wirken. Browser ohne
Unterstützung zeigen den Seitenwechsel wie bisher; es geht nichts verloren
und es wird kein zusätzliches JavaScript geladen.

Wer im Betriebssystem «Bewegung reduzieren» eingestellt hat, bekommt alles
davon ausgeschaltet – inklusive der Seitenübergänge.

## Barrierefreiheit und Technik

- Semantische Struktur mit `header`/`main`/`footer`, Sprunglink zum Inhalt
- Sichtbare Fokusrahmen, `aria-current` für die aktive Seite, beschriftete Icons
- Mobile Navigation mit `aria-expanded`, bedienbar per Tastatur (inkl. Escape)
- Feste Aktionsleiste auf dem Handy mit «Anrufen» und «Offerte anfordern»
- Formularfehler werden mit `aria-invalid` und Textmeldung ausgegeben
- Animationen respektieren `prefers-reduced-motion`
- Ohne JavaScript bleiben alle Inhalte sichtbar und bedienbar
