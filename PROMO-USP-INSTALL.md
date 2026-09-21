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

Die **Linienstärke** ist global einstellbar (0,8–2,5) und bleibt beim Ändern der
Icon-Größe gleich dünn — die Icons werden also größer, nicht fetter.

## Wichtigste Einstellungen

| Einstellung | Standard | Wirkung |
|---|---|---|
| Spalten Desktop / Mobil | 2 / 2 | Bei langen Texten auf Mobil besser 1 Spalte |
| Icon-Größe | 34 px | |
| Linienstärke der Icons | 1,3 | |
| Rahmenstärke / Ecken-Radius | 1 px / 8 px | Rahmenstärke 0 = Leiste ohne Rahmen |
| Abstand Promo-Leiste ↔ USPs | 26 px | |
| Promo-Leiste anzeigen | an | Aus = nur das USP-Raster |

Die Promo-Leiste kann einen **Link** bekommen (z. B. zur Sale-Collection) — dann
wird die ganze Leiste klickbar.

---

## Variante B — direkt unter dem Warenkorb-Button

Eine Section landet immer über oder unter dem Produktbereich. Für die Position
direkt unter dem Button (wie im Screenshot) braucht es einen Block in
`sections/main-product.liquid`:

1. `sections/main-product.liquid` öffnen
2. Im großen `{% case block.type %}` vor dem `{% else %}` bzw. `{% endcase %}` einfügen:

   ```liquid
   {%- when 'promo_usp' -%}
     <div {{ block.shopify_attributes }}>
       {% render 'promo-usp', s: block.settings, uid: block.id %}
     </div>
   ```

3. Im `{% schema %}` derselben Datei im Array `"blocks"` als weiteren Eintrag
   ergänzen (Komma zum vorherigen Block nicht vergessen):

   ```json
   {
     "type": "promo_usp",
     "name": "Promo + USPs",
     "settings": [
       {
         "type": "header",
         "content": "Promo-Leiste"
       },
       {
         "type": "checkbox",
         "id": "show_promo",
         "label": "Promo-Leiste anzeigen",
         "default": true
       },
       {
         "type": "text",
         "id": "promo_label",
         "label": "Fetter Anfang",
         "default": "HERBST-SALE",
         "info": "Wird fett dargestellt, gefolgt von einem Doppelpunkt."
       },
       {
         "type": "text",
         "id": "promo_text",
         "label": "Text",
         "default": "Spare **50% Rabatt**",
         "info": "Text zwischen **zwei Sternchen** wird fett dargestellt."
       },
       {
         "type": "checkbox",
         "id": "promo_uppercase",
         "label": "Fetten Anfang in GROSSBUCHSTABEN",
         "default": true
       },
       {
         "type": "select",
         "id": "promo_icon",
         "label": "Icon",
         "options": [
           {
             "value": "yarn",
             "label": "Wollknäuel"
           },
           {
             "value": "cloud",
             "label": "Wolke (weich)"
           },
           {
             "value": "droplet",
             "label": "Wassertropfen"
           },
           {
             "value": "wind",
             "label": "Wind (atmungsaktiv)"
           },
           {
             "value": "leaf",
             "label": "Blatt"
           },
           {
             "value": "feather",
             "label": "Feder"
           },
           {
             "value": "sprout",
             "label": "Pflanze"
           },
           {
             "value": "shirt",
             "label": "Shirt / Textil"
           },
           {
             "value": "washing",
             "label": "Waschmaschine"
           },
           {
             "value": "thermometer",
             "label": "Temperatur"
           },
           {
             "value": "sun",
             "label": "Sonne"
           },
           {
             "value": "moon",
             "label": "Mond"
           },
           {
             "value": "heart",
             "label": "Herz"
           },
           {
             "value": "star",
             "label": "Stern"
           },
           {
             "value": "sparkles",
             "label": "Funkeln"
           },
           {
             "value": "check",
             "label": "Häkchen"
           },
           {
             "value": "shield",
             "label": "Schild / Garantie"
           },
           {
             "value": "lock",
             "label": "Schloss / sicher"
           },
           {
             "value": "award",
             "label": "Auszeichnung"
           },
           {
             "value": "truck",
             "label": "Versand"
           },
           {
             "value": "box",
             "label": "Paket"
           },
           {
             "value": "return",
             "label": "Rückgabe"
           },
           {
             "value": "clock",
             "label": "Uhr"
           },
           {
             "value": "globe",
             "label": "Weltweit"
           },
           {
             "value": "tag",
             "label": "Preisschild"
           },
           {
             "value": "percent",
             "label": "Prozent"
           },
           {
             "value": "gift",
             "label": "Geschenk"
           },
           {
             "value": "none",
             "label": "Kein Icon"
           }
         ],
         "default": "tag"
       },
       {
         "type": "image_picker",
         "id": "promo_image",
         "label": "Eigenes Icon-Bild",
         "info": "Überschreibt die Icon-Auswahl. Am besten quadratisches PNG/SVG mit transparentem Hintergrund."
       },
       {
         "type": "range",
         "id": "promo_icon_size",
         "label": "Icon-Größe",
         "min": 14,
         "max": 40,
         "step": 2,
         "unit": "px",
         "default": 20
       },
       {
         "type": "url",
         "id": "promo_link",
         "label": "Link (optional)"
       },
       {
         "type": "select",
         "id": "promo_alignment",
         "label": "Ausrichtung",
         "default": "left",
         "options": [
           {
             "value": "left",
             "label": "Links"
           },
           {
             "value": "center",
             "label": "Zentriert"
           }
         ]
       },
       {
         "type": "color",
         "id": "promo_bg",
         "label": "Hintergrund",
         "default": "#ffffff"
       },
       {
         "type": "color",
         "id": "promo_label_color",
         "label": "Farbe fetter Text",
         "default": "#1a1a1a"
       },
       {
         "type": "color",
         "id": "promo_text_color",
         "label": "Farbe normaler Text",
         "default": "#4a4a4a"
       },
       {
         "type": "color",
         "id": "promo_border_color",
         "label": "Rahmenfarbe",
         "default": "#1a1a1a"
       },
       {
         "type": "range",
         "id": "promo_border_width",
         "label": "Rahmenstärke",
         "min": 0,
         "max": 4,
         "step": 1,
         "unit": "px",
         "default": 1
       },
       {
         "type": "range",
         "id": "promo_radius",
         "label": "Ecken-Radius",
         "min": 0,
         "max": 30,
         "step": 1,
         "unit": "px",
         "default": 8
       },
       {
         "type": "range",
         "id": "promo_padding_y",
         "label": "Innenabstand oben/unten",
         "min": 6,
         "max": 30,
         "step": 1,
         "unit": "px",
         "default": 14
       },
       {
         "type": "range",
         "id": "promo_padding_x",
         "label": "Innenabstand links/rechts",
         "min": 8,
         "max": 40,
         "step": 1,
         "unit": "px",
         "default": 18
       },
       {
         "type": "range",
         "id": "promo_font_size",
         "label": "Schriftgröße",
         "min": 12,
         "max": 22,
         "step": 1,
         "unit": "px",
         "default": 15
       },
       {
         "type": "header",
         "content": "USP-Raster",
         "info": "Die einzelnen USPs werden unten als Blöcke hinzugefügt."
       },
       {
         "type": "range",
         "id": "columns_desktop",
         "label": "Spalten Desktop",
         "min": 1,
         "max": 4,
         "step": 1,
         "unit": "",
         "default": 2
       },
       {
         "type": "range",
         "id": "columns_mobile",
         "label": "Spalten Mobil",
         "min": 1,
         "max": 2,
         "step": 1,
         "unit": "",
         "default": 2
       },
       {
         "type": "range",
         "id": "icon_size",
         "label": "Icon-Größe",
         "min": 20,
         "max": 64,
         "step": 2,
         "unit": "px",
         "default": 34
       },
       {
         "type": "range",
         "id": "icon_stroke",
         "label": "Linienstärke der Icons",
         "min": 0.8,
         "max": 2.5,
         "step": 0.1,
         "unit": "px",
         "default": 1.3
       },
       {
         "type": "range",
         "id": "icon_gap",
         "label": "Abstand Icon ↔ Text",
         "min": 6,
         "max": 28,
         "step": 1,
         "unit": "px",
         "default": 12
       },
       {
         "type": "range",
         "id": "column_gap",
         "label": "Spaltenabstand",
         "min": 8,
         "max": 60,
         "step": 2,
         "unit": "px",
         "default": 24
       },
       {
         "type": "range",
         "id": "row_gap",
         "label": "Zeilenabstand",
         "min": 8,
         "max": 48,
         "step": 2,
         "unit": "px",
         "default": 18
       },
       {
         "type": "range",
         "id": "usp_font_size",
         "label": "Schriftgröße",
         "min": 12,
         "max": 22,
         "step": 1,
         "unit": "px",
         "default": 15
       },
       {
         "type": "color",
         "id": "usp_icon_color",
         "label": "Icon-Farbe",
         "default": "#1a1a1a"
       },
       {
         "type": "color",
         "id": "usp_text_color",
         "label": "Textfarbe",
         "default": "#3d3d3d"
       },
       {
         "type": "range",
         "id": "space_between",
         "label": "Abstand Promo-Leiste ↔ USPs",
         "min": 0,
         "max": 60,
         "step": 2,
         "unit": "px",
         "default": 26
       },
       {
         "type": "header",
         "content": "USP 1–4"
       },
       {
         "type": "text",
         "id": "usp_1_text",
         "label": "USP 1: Text",
         "default": "100% natürliche Fasern"
       },
       {
         "type": "select",
         "id": "usp_1_icon",
         "label": "USP 1: Icon",
         "options": [
           {
             "value": "yarn",
             "label": "Wollknäuel"
           },
           {
             "value": "cloud",
             "label": "Wolke (weich)"
           },
           {
             "value": "droplet",
             "label": "Wassertropfen"
           },
           {
             "value": "wind",
             "label": "Wind (atmungsaktiv)"
           },
           {
             "value": "leaf",
             "label": "Blatt"
           },
           {
             "value": "feather",
             "label": "Feder"
           },
           {
             "value": "sprout",
             "label": "Pflanze"
           },
           {
             "value": "shirt",
             "label": "Shirt / Textil"
           },
           {
             "value": "washing",
             "label": "Waschmaschine"
           },
           {
             "value": "thermometer",
             "label": "Temperatur"
           },
           {
             "value": "sun",
             "label": "Sonne"
           },
           {
             "value": "moon",
             "label": "Mond"
           },
           {
             "value": "heart",
             "label": "Herz"
           },
           {
             "value": "star",
             "label": "Stern"
           },
           {
             "value": "sparkles",
             "label": "Funkeln"
           },
           {
             "value": "check",
             "label": "Häkchen"
           },
           {
             "value": "shield",
             "label": "Schild / Garantie"
           },
           {
             "value": "lock",
             "label": "Schloss / sicher"
           },
           {
             "value": "award",
             "label": "Auszeichnung"
           },
           {
             "value": "truck",
             "label": "Versand"
           },
           {
             "value": "box",
             "label": "Paket"
           },
           {
             "value": "return",
             "label": "Rückgabe"
           },
           {
             "value": "clock",
             "label": "Uhr"
           },
           {
             "value": "globe",
             "label": "Weltweit"
           },
           {
             "value": "tag",
             "label": "Preisschild"
           },
           {
             "value": "percent",
             "label": "Prozent"
           },
           {
             "value": "gift",
             "label": "Geschenk"
           },
           {
             "value": "none",
             "label": "Kein Icon"
           }
         ],
         "default": "yarn"
       },
       {
         "type": "image_picker",
         "id": "usp_1_image",
         "label": "USP 1: Eigenes Icon-Bild"
       },
       {
         "type": "text",
         "id": "usp_2_text",
         "label": "USP 2: Text",
         "default": "Unglaublich weich",
         "info": "Leer lassen, um diesen USP auszublenden."
       },
       {
         "type": "select",
         "id": "usp_2_icon",
         "label": "USP 2: Icon",
         "options": [
           {
             "value": "yarn",
             "label": "Wollknäuel"
           },
           {
             "value": "cloud",
             "label": "Wolke (weich)"
           },
           {
             "value": "droplet",
             "label": "Wassertropfen"
           },
           {
             "value": "wind",
             "label": "Wind (atmungsaktiv)"
           },
           {
             "value": "leaf",
             "label": "Blatt"
           },
           {
             "value": "feather",
             "label": "Feder"
           },
           {
             "value": "sprout",
             "label": "Pflanze"
           },
           {
             "value": "shirt",
             "label": "Shirt / Textil"
           },
           {
             "value": "washing",
             "label": "Waschmaschine"
           },
           {
             "value": "thermometer",
             "label": "Temperatur"
           },
           {
             "value": "sun",
             "label": "Sonne"
           },
           {
             "value": "moon",
             "label": "Mond"
           },
           {
             "value": "heart",
             "label": "Herz"
           },
           {
             "value": "star",
             "label": "Stern"
           },
           {
             "value": "sparkles",
             "label": "Funkeln"
           },
           {
             "value": "check",
             "label": "Häkchen"
           },
           {
             "value": "shield",
             "label": "Schild / Garantie"
           },
           {
             "value": "lock",
             "label": "Schloss / sicher"
           },
           {
             "value": "award",
             "label": "Auszeichnung"
           },
           {
             "value": "truck",
             "label": "Versand"
           },
           {
             "value": "box",
             "label": "Paket"
           },
           {
             "value": "return",
             "label": "Rückgabe"
           },
           {
             "value": "clock",
             "label": "Uhr"
           },
           {
             "value": "globe",
             "label": "Weltweit"
           },
           {
             "value": "tag",
             "label": "Preisschild"
           },
           {
             "value": "percent",
             "label": "Prozent"
           },
           {
             "value": "gift",
             "label": "Geschenk"
           },
           {
             "value": "none",
             "label": "Kein Icon"
           }
         ],
         "default": "cloud"
       },
       {
         "type": "image_picker",
         "id": "usp_2_image",
         "label": "USP 2: Eigenes Icon-Bild"
       },
       {
         "type": "text",
         "id": "usp_3_text",
         "label": "USP 3: Text",
         "default": "Mit jeder Wäsche weicher",
         "info": "Leer lassen, um diesen USP auszublenden."
       },
       {
         "type": "select",
         "id": "usp_3_icon",
         "label": "USP 3: Icon",
         "options": [
           {
             "value": "yarn",
             "label": "Wollknäuel"
           },
           {
             "value": "cloud",
             "label": "Wolke (weich)"
           },
           {
             "value": "droplet",
             "label": "Wassertropfen"
           },
           {
             "value": "wind",
             "label": "Wind (atmungsaktiv)"
           },
           {
             "value": "leaf",
             "label": "Blatt"
           },
           {
             "value": "feather",
             "label": "Feder"
           },
           {
             "value": "sprout",
             "label": "Pflanze"
           },
           {
             "value": "shirt",
             "label": "Shirt / Textil"
           },
           {
             "value": "washing",
             "label": "Waschmaschine"
           },
           {
             "value": "thermometer",
             "label": "Temperatur"
           },
           {
             "value": "sun",
             "label": "Sonne"
           },
           {
             "value": "moon",
             "label": "Mond"
           },
           {
             "value": "heart",
             "label": "Herz"
           },
           {
             "value": "star",
             "label": "Stern"
           },
           {
             "value": "sparkles",
             "label": "Funkeln"
           },
           {
             "value": "check",
             "label": "Häkchen"
           },
           {
             "value": "shield",
             "label": "Schild / Garantie"
           },
           {
             "value": "lock",
             "label": "Schloss / sicher"
           },
           {
             "value": "award",
             "label": "Auszeichnung"
           },
           {
             "value": "truck",
             "label": "Versand"
           },
           {
             "value": "box",
             "label": "Paket"
           },
           {
             "value": "return",
             "label": "Rückgabe"
           },
           {
             "value": "clock",
             "label": "Uhr"
           },
           {
             "value": "globe",
             "label": "Weltweit"
           },
           {
             "value": "tag",
             "label": "Preisschild"
           },
           {
             "value": "percent",
             "label": "Prozent"
           },
           {
             "value": "gift",
             "label": "Geschenk"
           },
           {
             "value": "none",
             "label": "Kein Icon"
           }
         ],
         "default": "droplet"
       },
       {
         "type": "image_picker",
         "id": "usp_3_image",
         "label": "USP 3: Eigenes Icon-Bild"
       },
       {
         "type": "text",
         "id": "usp_4_text",
         "label": "USP 4: Text",
         "default": "Immer atmungsaktiv",
         "info": "Leer lassen, um diesen USP auszublenden."
       },
       {
         "type": "select",
         "id": "usp_4_icon",
         "label": "USP 4: Icon",
         "options": [
           {
             "value": "yarn",
             "label": "Wollknäuel"
           },
           {
             "value": "cloud",
             "label": "Wolke (weich)"
           },
           {
             "value": "droplet",
             "label": "Wassertropfen"
           },
           {
             "value": "wind",
             "label": "Wind (atmungsaktiv)"
           },
           {
             "value": "leaf",
             "label": "Blatt"
           },
           {
             "value": "feather",
             "label": "Feder"
           },
           {
             "value": "sprout",
             "label": "Pflanze"
           },
           {
             "value": "shirt",
             "label": "Shirt / Textil"
           },
           {
             "value": "washing",
             "label": "Waschmaschine"
           },
           {
             "value": "thermometer",
             "label": "Temperatur"
           },
           {
             "value": "sun",
             "label": "Sonne"
           },
           {
             "value": "moon",
             "label": "Mond"
           },
           {
             "value": "heart",
             "label": "Herz"
           },
           {
             "value": "star",
             "label": "Stern"
           },
           {
             "value": "sparkles",
             "label": "Funkeln"
           },
           {
             "value": "check",
             "label": "Häkchen"
           },
           {
             "value": "shield",
             "label": "Schild / Garantie"
           },
           {
             "value": "lock",
             "label": "Schloss / sicher"
           },
           {
             "value": "award",
             "label": "Auszeichnung"
           },
           {
             "value": "truck",
             "label": "Versand"
           },
           {
             "value": "box",
             "label": "Paket"
           },
           {
             "value": "return",
             "label": "Rückgabe"
           },
           {
             "value": "clock",
             "label": "Uhr"
           },
           {
             "value": "globe",
             "label": "Weltweit"
           },
           {
             "value": "tag",
             "label": "Preisschild"
           },
           {
             "value": "percent",
             "label": "Prozent"
           },
           {
             "value": "gift",
             "label": "Geschenk"
           },
           {
             "value": "none",
             "label": "Kein Icon"
           }
         ],
         "default": "wind"
       },
       {
         "type": "image_picker",
         "id": "usp_4_image",
         "label": "USP 4: Eigenes Icon-Bild"
       }
     ]
   }
   ```

4. **Save** → im Theme-Editor auf der Produktseite **Add block → Promo + USPs**
   und an die gewünschte Position ziehen.

Der Block hat vier feste USP-Felder statt beliebig vieler Unterblöcke — Shopify
erlaubt keine Blöcke innerhalb von Blöcken. Wer mehr als vier USPs oder
Abschnitts-Abstände braucht, nimmt die Section aus Schritt 2.

## Hinweise

- Die Section funktioniert auf jedem Template, nicht nur auf Produktseiten —
  auch Startseite, Collection- oder Info-Seiten.
- Das CSS ist auf die jeweilige Section-ID begrenzt. Zwei Instanzen mit
  unterschiedlichen Farben auf derselben Seite sind also kein Problem.
- Keine Abhängigkeit von jQuery oder Theme-Klassen wie `page-width` — läuft in
  Dawn genauso wie in Premium-Themes.
- Angaben wie „100% natürliche Fasern" müssen zum Produkt passen; USP-Zeilen
  sind Werbeaussagen, für die du als Händler haftest.
