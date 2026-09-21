# Sale-Countdown — Einbau-Anleitung

Zwei Dateien, ca. 5 Minuten. Funktioniert mit allen Online-Store-2.0-Themes
(Dawn, Refresh, Craft, Sense, Studio, Impulse, Prestige …).

## Schritt 0 — Backup

Shopify Admin → **Online Store → Themes** → beim aktiven Theme auf `...` →
**Duplicate**. Erst dann Code bearbeiten.

## Schritt 1 — Snippet anlegen

1. **Online Store → Themes → `...` → Edit code**
2. Links im Ordner **Snippets** auf **Add a new snippet**
3. Name: `sale-countdown` (ohne `.liquid`, das hängt Shopify an)
4. Den kompletten Inhalt von `snippets/sale-countdown.liquid` einfügen → **Save**

## Schritt 2 — Section anlegen

1. Im selben Code-Editor im Ordner **Sections** auf **Add a new section**
2. Name: `sale-countdown`
3. Falls Shopify eine Vorlage vorbefüllt: **alles markieren und löschen**
4. Den kompletten Inhalt von `sections/sale-countdown.liquid` einfügen → **Save**

## Schritt 3 — Im Theme-Editor benutzen

**Online Store → Themes → Customize** → oben in der Dropdown-Leiste
**Products → Default product** wählen → **Add section** → **„Sale endet bald“**.

Per Drag & Drop an die gewünschte Stelle schieben → **Save**.

Die Section lässt sich genauso auf Startseite, Collection-Seiten oder als
Template-übergreifender Abschnitt einsetzen.

---

## Variante B — direkt unter dem Preis / Warenkorb-Button

Eine normale Section landet immer *über oder unter* dem Produktbereich, nie
mitten drin. Für die Platzierung direkt unter Preis oder Button braucht es
einen Block in `sections/main-product.liquid`:

1. `sections/main-product.liquid` öffnen
2. Im großen `{% case block.type %}` (bei Dawn im Bereich der Produkt-Blöcke)
   vor dem `{% else %}` bzw. `{% endcase %}` einfügen:

   ```liquid
   {%- when 'sale_countdown' -%}
     <div {{ block.shopify_attributes }}>
       {% render 'sale-countdown', s: block.settings, uid: block.id, product: product %}
     </div>
   ```

3. Im `{% schema %}` dieser Datei im Array `"blocks"` als weiteren Eintrag
   ergänzen (Komma zum vorherigen Block nicht vergessen):

   ```json
   {
     "type": "sale_countdown",
     "name": "Sale-Countdown",
     "settings": [
       { "type": "text", "id": "icon", "label": "Icon / Emoji", "default": "🔥" },
       { "type": "text", "id": "heading", "label": "Überschrift", "default": "Sale endet bald!" },
       { "type": "text", "id": "subheading", "label": "Untertext", "default": "" },
       {
         "type": "select", "id": "mode", "label": "Modus", "default": "fixed",
         "options": [
           { "value": "fixed", "label": "Festes Enddatum" },
           { "value": "evergreen", "label": "Pro Besucher (Evergreen)" }
         ]
       },
       { "type": "text", "id": "end_date", "label": "Enddatum (JJJJ-MM-TT)", "default": "2026-12-24" },
       { "type": "text", "id": "end_time", "label": "Endzeit (HH:MM)", "default": "23:59" },
       {
         "type": "select", "id": "utc_offset", "label": "Zeitzone", "default": "+02:00",
         "options": [
           { "value": "Z", "label": "UTC" },
           { "value": "+01:00", "label": "UTC+1" },
           { "value": "+02:00", "label": "UTC+2" }
         ]
       },
       { "type": "range", "id": "evergreen_hours", "label": "Evergreen-Dauer", "min": 1, "max": 72, "step": 1, "unit": "h", "default": 24 },
       { "type": "checkbox", "id": "show_days", "label": "Tage anzeigen", "default": true },
       { "type": "checkbox", "id": "show_seconds", "label": "Sekunden anzeigen", "default": true },
       { "type": "text", "id": "label_days", "label": "Label: Tage", "default": "Tage" },
       { "type": "text", "id": "label_hours", "label": "Label: Stunden", "default": "Std." },
       { "type": "text", "id": "label_minutes", "label": "Label: Minuten", "default": "Min." },
       { "type": "text", "id": "label_seconds", "label": "Label: Sekunden", "default": "Sek." },
       {
         "type": "select", "id": "on_expire", "label": "Nach Ablauf", "default": "hide",
         "options": [
           { "value": "message", "label": "Hinweistext anzeigen" },
           { "value": "hide", "label": "Ausblenden" }
         ]
       },
       { "type": "text", "id": "expired_text", "label": "Text nach Ablauf", "default": "Diese Aktion ist beendet." },
       { "type": "checkbox", "id": "only_if_on_sale", "label": "Nur bei reduzierten Produkten", "default": true },
       {
         "type": "select", "id": "layout", "label": "Timer-Stil", "default": "boxed",
         "options": [
           { "value": "boxed", "label": "Kacheln" },
           { "value": "plain", "label": "Schlicht" }
         ]
       },
       {
         "type": "select", "id": "alignment", "label": "Ausrichtung", "default": "left",
         "options": [
           { "value": "left", "label": "Links" },
           { "value": "center", "label": "Zentriert" }
         ]
       },
       { "type": "range", "id": "heading_size", "label": "Größe Überschrift", "min": 16, "max": 48, "step": 1, "unit": "px", "default": 20 },
       { "type": "range", "id": "number_size", "label": "Größe Ziffern", "min": 18, "max": 64, "step": 1, "unit": "px", "default": 24 },
       { "type": "color", "id": "bg_color", "label": "Hintergrund", "default": "#fff4f0" },
       { "type": "color", "id": "text_color", "label": "Textfarbe", "default": "#111111" },
       { "type": "color", "id": "box_bg", "label": "Hintergrund Ziffern", "default": "#111111" },
       { "type": "color", "id": "box_text", "label": "Farbe Ziffern", "default": "#ffffff" },
       { "type": "color", "id": "button_bg", "label": "Button Hintergrund", "default": "#ff3b30" },
       { "type": "color", "id": "button_text", "label": "Button Text", "default": "#ffffff" },
       { "type": "checkbox", "id": "show_border", "label": "Rahmen anzeigen", "default": true },
       { "type": "color", "id": "border_color", "label": "Rahmenfarbe", "default": "#ffd9cc" },
       { "type": "range", "id": "border_radius", "label": "Ecken-Radius", "min": 0, "max": 30, "step": 2, "unit": "px", "default": 10 }
     ]
   }
   ```

4. Speichern → im Theme-Editor auf der Produktseite **Add block → Sale-Countdown**
   und an die gewünschte Position ziehen.

Der Block hat **keinen** Button und keine Abschnitts-Abstände — dafür die
Standalone-Section aus Schritt 2 nutzen.

---

## Einstellungen im Überblick

| Einstellung | Wirkung |
|---|---|
| **Modus: Festes Enddatum** | Echter Stichtag, für alle Besucher gleich. Datum als `JJJJ-MM-TT`, Uhrzeit als `HH:MM`. |
| **Modus: Evergreen** | Jeder Besucher bekommt beim ersten Aufruf seinen eigenen Timer (z. B. 24 h), gespeichert im Browser. Läuft nie global ab. |
| **Zeitzone** | Bezugspunkt für das Enddatum. Deutschland: Sommer = UTC+2, Winter = UTC+1. |
| **Nach Ablauf** | Hinweistext anzeigen oder Banner komplett ausblenden. Im Theme-Editor bleibt es sichtbar, damit du weiter bearbeiten kannst. |
| **Nur bei reduzierten Produkten** | Banner erscheint nur, wenn `compare_at_price` > Preis. |
| **Tage / Sekunden anzeigen** | Ohne Tage werden diese in Stunden umgerechnet (z. B. `72 Std.`). |

## Hinweise

- Der Countdown läuft im Browser des Besuchers — er ist eine Design-/Marketing-
  Anzeige, keine technische Rabatt-Steuerung. Den Rabatt selbst weiterhin über
  Shopify-Rabatte oder `compare_at_price` setzen, sonst stimmen Timer und
  tatsächlicher Preis nicht überein.
- Bei einem Evergreen-Timer sieht jeder Besucher eine andere Restzeit. In
  manchen Märkten (u. a. DE/EU) gilt ein dauerhaft „ablaufender“ Countdown bei
  einem Angebot, das gar nicht endet, als irreführende Werbung. Also
  entweder ein echtes Enddatum verwenden, oder die Aktion für den jeweiligen
  Besucher wirklich nach Ablauf beenden.
- Alle Einstellungen sind pro Section/Block — der Countdown kann auf der
  Startseite anders aussehen als auf der Produktseite.
