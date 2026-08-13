# Website aufschalten

Diese Website ist reines HTML, CSS und JavaScript. Kein Server, keine
Datenbank, kein Build. Das heisst: **die Dateien so wie sie hier liegen auf
einen Webspace kopieren – fertig.** Genau das macht sie schnell, günstig und
praktisch unkaputtbar.

---

## 1. Vor dem Aufschalten

Diese vier Punkte zuerst, sonst steht auf der fertigen Seite eine erfundene
Telefonnummer.

| Punkt | Wie |
|---|---|
| Telefon, E-Mail-Domain, Inhaber, UID | `python3 tools/stammdaten.py --telefon "…" --domain "…" --inhaber "…" --uid "…" --anwenden` |
| Preise im Rechner kontrollieren | Block `TARIFE` zuoberst in `js/preisrechner.js` |
| Formular-Empfang einrichten | siehe Abschnitt 4 |
| Kontrolle | `python3 tools/pruefen.py` – muss «Keine Befunde.» sagen |

E-Mail-Postfächer, die im Text vorkommen und beim Hoster angelegt werden
müssen: `offerte@`, `info@`, `datenschutz@`, `jobs@`. Wer nur eines will,
ersetzt die anderen mit Suchen-und-Ersetzen (oder sagt Bescheid, dann macht
das Skript es).

---

## 2. Domain

Für eine Schweizer Firma gehört eine `.ch`-Domain dazu. Registrieren
lässt sie sich bei jedem Schweizer Anbieter, etwa Hostpoint, Infomaniak,
cyon oder Nine – rund 10–20 CHF pro Jahr. Die Domain gehört **auf den Namen
der Firma**, nicht auf den einer Agentur.

Die Website ist auf `www.cleeno-reinigungen.ch` eingestellt (in `canonical`,
`sitemap.xml`, `robots.txt` und den Social-Media-Angaben). Wird eine andere
Domain gewählt, `tools/stammdaten.py --domain …` laufen lassen.

---

## 3. Hosting – drei Wege

### A) Netlify Drop – am schnellsten, in zwei Minuten online

1. Auf <https://app.netlify.com/drop> gehen
2. Den **Inhalt** dieses Ordners (nicht den Ordner selbst) ins Fenster ziehen
3. Die Seite ist sofort unter einer Adresse wie `zufallsname.netlify.app`
   erreichbar
4. Eigene Domain: *Site settings → Domain management → Add custom domain*,
   danach beim Domain-Anbieter die von Netlify angezeigten Nameserver
   eintragen

HTTPS kommt automatisch und kostenlos. Kostenpunkt: 0 CHF für eine Seite
dieser Grösse. Nachteil: jede Änderung muss neu hochgezogen werden.

### B) Cloudflare Pages – aktualisiert sich bei jedem Push selbst

Empfohlen, wenn die Website weiterentwickelt wird.

1. Bei Cloudflare *Workers & Pages → Create → Pages → Connect to Git*
2. Dieses Repository auswählen
3. **Build command:** leer lassen · **Build output directory:** `/`
4. Speichern

Ab jetzt gilt: was auf den Hauptbranch gepusht wird, ist eine Minute später
online. Eigene Domain unter *Custom domains*, HTTPS automatisch.

GitHub Pages funktioniert ebenfalls (*Settings → Pages → Branch: main,
Ordner: / (root)*), kann aber keine `_headers`-Datei lesen.

### C) Klassisches Schweizer Hosting per FTP

Wenn die Daten ausdrücklich in der Schweiz liegen sollen oder die
E-Mail-Postfächer sowieso beim selben Anbieter sind (Hostpoint, Infomaniak,
cyon – ab ca. 6–15 CHF im Monat inklusive Mail).

1. Mit einem FTP-Programm verbinden (z. B. FileZilla, Zugangsdaten vom Hoster)
2. Den Inhalt dieses Ordners nach `/public_html` bzw. `/htdocs` kopieren
3. Beim Hoster HTTPS aktivieren (Let's Encrypt, meist ein Klick)

Wichtig: `_headers` versteht nur Netlify und Cloudflare. Auf einem
Apache-Server gehört stattdessen eine `.htaccess` in den Hauptordner:

```apache
<IfModule mod_headers.c>
  Header set X-Content-Type-Options "nosniff"
  Header set Referrer-Policy "strict-origin-when-cross-origin"
  Header set X-Frame-Options "SAMEORIGIN"
  Header set Permissions-Policy "geolocation=(), microphone=(), camera=(), payment=()"
</IfModule>

<IfModule mod_expires.c>
  ExpiresActive On
  ExpiresByType font/woff2 "access plus 1 year"
  ExpiresByType image/svg+xml "access plus 1 month"
  ExpiresByType text/css "access plus 1 week"
  ExpiresByType application/javascript "access plus 1 week"
</IfModule>

ErrorDocument 404 /404.html
```

Bei Netlify und Cloudflare wird `404.html` von selbst als Fehlerseite genutzt.

### Was wählen?

| | Netlify Drop | Cloudflare Pages | Schweizer Hoster |
|---|---|---|---|
| Aufwand | zwei Minuten | einmalig 10 Minuten | eine halbe Stunde |
| Kosten | gratis | gratis | ca. 6–15 CHF/Monat |
| Änderungen | manuell hochziehen | automatisch bei Push | manuell per FTP |
| E-Mail-Postfächer | nein | nein | ja, inklusive |
| Daten in der Schweiz | nein | nein | ja |

Pragmatisch: **Cloudflare Pages für die Website, Schweizer Anbieter für Domain
und E-Mail.** Das ist die günstigste Kombination und trennt sauber.

---

## 4. Das Offertformular zum Laufen bringen

Solange nichts eingerichtet ist, öffnet das Formular beim Absenden das
E-Mail-Programm des Besuchers mit fertig ausgefülltem Text. Das funktioniert,
verliert aber jeden zweiten Interessenten, der kein E-Mail-Programm
eingerichtet hat.

Besser: einen Formulardienst eintragen. Beide haben ein kostenloses Kontingent,
das für den Anfang reicht:

- **Formspree** – <https://formspree.io>, Adresse angeben, man erhält eine
  Endpunkt-Adresse wie `https://formspree.io/f/abcdwxyz`
- **Getform**, **Basin** oder **Web3Forms** funktionieren gleich

Diese Adresse in `js/main.js` ganz oben eintragen:

```js
var FORM_ENDPOINT = 'https://formspree.io/f/abcdwxyz';
```

Fertig – ab dann landen Anfragen direkt im Postfach, der Besucher sieht die
Danke-Seite. Ohne Eintrag bleibt der E-Mail-Weg als Rückfallebene aktiv.

> Datenschutz: Diese Dienste stehen teilweise in den USA. Für Namen, Adresse
> und Objektangaben ist das zulässig, gehört aber in die Datenschutzerklärung.
> Wer das vermeiden will, nimmt ein PHP-Skript beim Schweizer Hoster – dafür
> braucht es dann Hosting-Variante C.

---

## 5. Nach dem Aufschalten

1. **Google Unternehmensprofil** anlegen (<https://business.google.com>) –
   für ein lokales Reinigungsunternehmen die mit Abstand wichtigste Massnahme.
   Adresse, Öffnungszeiten und Leistungen identisch zur Website eintragen.
2. **Google Search Console** (<https://search.google.com/search-console>):
   Domain bestätigen, `sitemap.xml` einreichen.
3. **Bing Webmaster Tools** – dasselbe, dauert fünf Minuten.
4. Testen: <https://pagespeed.web.dev> und
   <https://search.google.com/test/rich-results> für die strukturierten Daten.
5. Erst dann echte Fotos nachliefern (siehe `docs/fotoguide.md`) – sie sind
   der grösste verbleibende Qualitätssprung.

Statistik ohne Cookies und ohne Banner, falls gewünscht: Plausible oder
Umami. Beide sind kostenpflichtig bzw. selbst zu hosten, aber
datenschutzfreundlich. Google Analytics würde ein Cookie-Banner nötig machen –
darum steht aktuell «Keine Cookies, kein Tracking» im Footer.
