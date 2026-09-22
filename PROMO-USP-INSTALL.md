# Promo-Leiste + USPs — Einbau-Anleitung

Nachbau des Screenshots: eine umrandete Promo-Leiste („HERBST-SALE: Spare **50% Rabatt**")
und darunter ein Raster aus USPs mit Linien-Icons. Alles im Theme-Editor editierbar.

**Drei Dateien**, alle über **Online Store → Themes → `...` → Edit code**.
Vorher das Theme duplizieren (Backup).

## Schritt 1 — Zwei Snippets anlegen

Ordner **Snippets → Add a new snippet**:

| Name eingeben | Inhalt aus |
|---|---|
| `usp-icon` | `snippets/usp-icon.liquid` |
| `promo-usp` | `snippets/promo-usp.liquid` |

`usp-icon` ist die Icon-Bibliothek, `promo-usp` das Markup samt CSS.

## Schritt 2 — Section anlegen

Ordner **Sections → Add a new section** → Name `promo-usp` → vorbefüllte Vorlage
komplett löschen → Inhalt aus `sections/promo-usp.liquid` einfügen → **Save**.

## Schritt 3 — Im Theme-Editor benutzen

**Themes → Customize** → oben **Products → Default product** → **Add section** →
**„Promo + USPs"**.

Die vier USPs aus dem Screenshot sind als Voreinstellung schon drin. Über
**Add block → USP** kommen weitere dazu (max. 12), per Drag & Drop sortierbar.

---

## Texte bearbeiten

**Promo-Leiste** — zwei Felder:

- **Fetter Anfang**: `HERBST-SALE` → fett, optional in Großbuchstaben, Doppelpunkt kommt automatisch
- **Text**: `Spare **50% Rabatt**` → alles zwischen zwei Sternchen wird fett

Also genau wie im Screenshot: `HERBST-SALE` + `Spare **50% Rabatt**`.
Für „Nur noch heute **-30%**" einfach die Sternchen umsetzen.

**USPs** — pro Block ein Text, ein Icon aus der Liste und optional eine
Zusatzzeile in kleinerer, blasserer Schrift.

## Icons

27 Linien-Icons im Stil des Screenshots, im Editor per Dropdown wählbar:

`yarn`, `cloud`, `droplet`, `wind`, `leaf`, `feather`, `sprout`, `shirt`, `washing`, `thermometer`, `sun`, `moon`, `heart`, `star`, `sparkles`, `check`, `shield`, `lock`, `award`, `truck`, `box`, `return`, `clock`, `globe`, `tag`, `percent`, `gift`

Alternativ pro USP ein **eigenes Icon-Bild** hochladen (PNG/SVG, quadratisch,
transparenter Hintergrund) — das überschreibt die Dropdown-Auswahl.

Die **Linienstärke** ist global wählbar (Sehr dünn bis Sehr kräftig) und bleibt beim
Ändern der Icon-Größe gleich dünn — die Icons werden also größer, nicht fetter.

## Wichtigste Einstellungen

| Einstellung | Standard | Wirkung |
|---|---|---|
| Spalten Desktop / Mobil | 2 / 2 | Bei langen Texten auf Mobil besser 1 Spalte |
| Icon-Größe | 34 px | |
| Linienstärke der Icons | Dünn | |
| Rahmenstärke / Ecken-Radius | 1 px / 8 px | Rahmenstärke 0 = Leiste ohne Rahmen |
| Abstand Promo-Leiste ↔ USPs | 26 px | |
| Promo-Leiste anzeigen | an | Aus = nur das USP-Raster |

Die Promo-Leiste kann einen **Link** bekommen (z. B. zur Sale-Collection) — dann
wird die ganze Leiste klickbar.

---

## Variante B — als Block innerhalb des Produktbereichs

Eine Section landet immer über oder unter dem Produktbereich. Damit der Inhalt
zwischen Preis und Warenkorb-Button sitzt, muss er ein **Block** in
`sections/main-product.liquid` werden.

Zwei Einfügungen in diese eine Datei. Beide kommen an den **Anfang** der
jeweiligen Liste — das ist unabhängig davon, wie das Theme darunter aufgebaut
ist, und damit die sicherste Stelle.

### B1 — Markup einfügen

1. **Sections → `main-product.liquid`** öffnen
2. Mit `Strg/Cmd + F` nach `case block.type` suchen
3. Den Inhalt von `product-block/1-liquid-einfuegen.liquid` **direkt in die Zeile
   darunter** setzen:

   ```liquid
   {%- when 'promo_usp' -%}
     <div {{ block.shopify_attributes }}>
       {% render 'promo-usp', s: block.settings, uid: block.id %}
     </div>
   ```

   Es sieht danach so aus:

   ```liquid
   {%- case block.type -%}
     {%- when 'promo_usp' -%}          <- neu
       <div {{ block.shopify_attributes }}>
         {% render 'promo-usp', s: block.settings, uid: block.id %}
       </div>
     {%- when '@app' -%}               <- war schon da
       ...
   ```

### B2 — Einstellungen einfügen

1. In derselben Datei nach `"blocks": [` suchen (steht im `{% schema %}` ganz unten)
2. Den kompletten Inhalt von `product-block/2-schema-einfuegen.json` **direkt in
   die Zeile darunter** setzen

   Das Komma am Ende der Datei ist Absicht — es trennt den neuen Block von den
   bereits vorhandenen. Ergebnis:

   ```json
   "blocks": [
     { "type": "promo_usp", ... },     <- neu, mit Komma am Ende
     { "type": "@app" },               <- war schon da
     ...
   ]
   ```

3. **Speichern**

### B3 — Block einsetzen

**Themes → Anpassen → Produkte → Standard-Produkt** → in der linken Spalte den
Produktbereich aufklappen → **Block hinzufügen** *(Add block)* → **„Promo + USPs"**
→ an die gewünschte Position ziehen → **Speichern**.

### Wenn die Datei anders aussieht

Nicht jedes Theme heißt `main-product.liquid`. Ältere (Vintage-)Themes nutzen
`sections/product-template.liquid` und haben oft gar keine Blöcke — dort
funktioniert nur die Section aus Schritt 2. Manche Premium-Themes lagern die
Blöcke in ein Snippet aus; dann steht `case block.type` dort statt in der
Section.

Findest du `case block.type` nicht, hilft die Suche nach `when 'title'` oder
`when 'price'` — das sind Block-Typen, die fast jedes Theme hat, und die Stelle
ist dieselbe.

### Unterschiede zur Section

- **Vier feste USP-Felder** statt beliebig vieler Blöcke: Shopify erlaubt keine
  Blöcke innerhalb von Blöcken. Wer mehr als vier braucht, nimmt die Section.
- **Keine Abschnitts-Abstände und keine Breitenbegrenzung** — der Block
  übernimmt die Breite des Produktbereichs.
- Beide Varianten können parallel installiert sein; sie teilen sich dieselben
  Snippets.

### Achtung bei Theme-Updates

`main-product.liquid` ist eine Theme-Datei. Ein Update des Themes überschreibt
sie und damit beide Einfügungen. Vor einem Update also die Datei sichern oder
die Schritte danach wiederholen. Die beiden Snippets und die Section sind davon
nicht betroffen — die gehören nicht zum Theme.

## Hinweise

- Die Section funktioniert auf jedem Template, nicht nur auf Produktseiten —
  auch Startseite, Collection- oder Info-Seiten.
- Das CSS ist auf die jeweilige Section-ID begrenzt. Zwei Instanzen mit
  unterschiedlichen Farben auf derselben Seite sind also kein Problem.
- Keine Abhängigkeit von jQuery oder Theme-Klassen wie `page-width` — läuft in
  Dawn genauso wie in Premium-Themes.
- Angaben wie „100% natürliche Fasern" müssen zum Produkt passen; USP-Zeilen
  sind Werbeaussagen, für die du als Händler haftest.
