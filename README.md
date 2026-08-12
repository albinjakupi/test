# Website Reinigungsfirma (Glanzwerk Reinigung)

Statische Website für eine Reinigungsfirma – reines HTML, CSS und JavaScript, ohne
Build-Schritt, ohne Framework und ohne externe Abhängigkeiten (keine CDNs, keine
Google Fonts, keine Tracker). Damit läuft die Seite auf jedem Webhosting und ist
von Haus aus datenschutzfreundlich.

## Schnellstart

Doppelklick auf `index.html` genügt zum Anschauen. Für ein realistischeres Bild
(saubere Pfade, Formularverhalten) lokal einen kleinen Server starten:

```bash
python3 -m http.server 8000
# danach http://localhost:8000 öffnen
```

## Aufbau

```
index.html                    Startseite (Hero, Leistungen, Ablauf, Referenzen, FAQ)
leistungen.html               Übersicht aller Leistungen inkl. Richtpreisen
unterhaltsreinigung.html      Detailseite Leistung
bueroreinigung.html           Detailseite Leistung
fensterreinigung.html         Detailseite Leistung
umzugsreinigung.html          Detailseite Leistung (inkl. Preistabelle)
bauendreinigung.html          Detailseite Leistung
liegenschaftsreinigung.html   Detailseite Leistung
ueber-uns.html                Firma, Werte, Team, Zahlen, offene Stellen
kontakt.html                  Offertformular, Kontaktangaben, FAQ
impressum.html                Impressum (Platzhalter)
datenschutz.html              Datenschutzerklärung nach Schweizer DSG (Platzhalter)
404.html                      Fehlerseite
css/style.css                 Gesamtes Design (Design-Tokens zuoberst)
js/main.js                    Navigation, Scroll-Effekte, Formularvalidierung
assets/favicon.svg            Favicon
assets/img/                    Ablage für eigene Fotos
robots.txt, sitemap.xml       Für Suchmaschinen
```

Header und Footer stehen in jeder Datei gleich drin (so funktioniert eine
statische Seite ohne Build-Schritt). Wer etwas an der Navigation ändert, muss die
Änderung in allen Dateien nachziehen – am schnellsten mit Suchen-und-Ersetzen
über alle `.html`-Dateien.

## Vor dem Livegang anpassen

Alle Firmenangaben sind Platzhalter. Am einfachsten per Suchen-und-Ersetzen über
alle Dateien:

| Platzhalter | Bedeutung |
|---|---|
| `Glanzwerk Reinigung GmbH` / `Glanzwerk` | Firmenname |
| `044 123 45 67` | Telefonnummer (Anzeige) |
| `+41441234567` | Telefonnummer in `tel:`-Links |
| `offerte@glanzwerk-reinigung.ch` | E-Mail für Offertanfragen |
| `info@` / `datenschutz@` / `jobs@glanzwerk-reinigung.ch` | weitere Adressen |
| `Musterstrasse 12`, `8005 Zürich` | Adresse |
| `https://www.glanzwerk-reinigung.ch` | Domain (Canonical, Sitemap, robots.txt) |
| `CHE-123.456.789` | UID / MWST-Nummer im Impressum |
| `Zürich`, `Winterthur`, … | Einsatzgebiet |

Ebenfalls prüfen:

- **Preise** in `leistungen.html`, `umzugsreinigung.html` und den FAQ-Blöcken.
- **Zahlen** auf der Startseite und in `ueber-uns.html` (Jahre, Mitarbeitende, Objekte).
- **Kundenstimmen** auf der Startseite – nur echte Zitate verwenden.
- **Team** in `ueber-uns.html` (Namen, Funktionen, später Fotos).
- **Impressum und Datenschutz**: Vorlagen, die vor der Veröffentlichung rechtlich
  geprüft werden sollten.
- **Strukturierte Daten** (`application/ld+json`) am Ende von `index.html`.

## Farben und Schriften

Alle Farben stehen als CSS-Variablen ganz oben in `css/style.css` unter `:root`.
Für ein anderes Erscheinungsbild genügt es meistens, `--brand`, `--brand-dark`
und `--accent` zu ändern. Als Schrift wird die System-Schriftart des jeweiligen
Geräts verwendet – das ist schnell und benötigt keine externen Ressourcen.

## Bilder einsetzen

Wo jetzt farbige Flächen mit Symbol stehen (`<div class="media">`), gehören
später echte Fotos hin. Eigene Bilder in `assets/img/` ablegen und den Block
ersetzen:

```html
<div class="media">
  <img src="assets/img/team-bei-der-arbeit.jpg"
       alt="Zwei Mitarbeitende reinigen ein Treppenhaus" width="1200" height="900" loading="lazy">
</div>
```

Empfehlung: Breite ca. 1600 px, als WebP oder JPEG mit rund 150–250 KB. Jedes
Bild braucht ein aussagekräftiges `alt`-Attribut.

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
gesendet, ohne dass die Seite neu lädt; Erfolg und Fehler erscheinen direkt über
dem Formular. Ein verstecktes Honeypot-Feld hält einfache Spam-Bots ab.

Wer PHP-Hosting nutzt, kann stattdessen ein eigenes `sendmail.php` schreiben und
dessen Pfad als `FORM_ENDPOINT` eintragen – das JavaScript sendet ein normales
`FormData`-Objekt per POST.

## Veröffentlichen

Es müssen nur die Dateien auf den Server – kein Build, kein Node.

- **Eigenes Hosting**: Inhalt des Ordners per FTP/SFTP ins Web-Root laden.
- **Netlify / Cloudflare Pages**: Repository verbinden, Build-Befehl leer lassen,
  Publish-Verzeichnis `/`.
- **GitHub Pages**: In den Repository-Einstellungen unter *Pages* den Branch
  wählen und als Ordner `/ (root)` angeben.

Nach dem Aufschalten die Domain in `sitemap.xml`, `robots.txt` und in den
`canonical`-Links der HTML-Dateien anpassen.

## Barrierefreiheit und Technik

- Semantische Struktur mit `header`/`main`/`footer`, Sprunglink zum Inhalt
- Sichtbare Fokusrahmen, `aria-current` für die aktive Seite, beschriftete Icons
- Mobile Navigation mit `aria-expanded`, bedienbar per Tastatur (inkl. Escape)
- Formularfehler werden mit `aria-invalid` und Textmeldung ausgegeben
- Animationen respektieren `prefers-reduced-motion`
- Ohne JavaScript bleiben alle Inhalte sichtbar und lesbar
