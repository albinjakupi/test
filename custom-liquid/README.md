# Featured Collection Tabs — als Custom Liquid

Nachbau des Abschnitts „Featured Products" mit Tabs und Produkt-Karussell,
gebaut für einen **Benutzerdefiniertes-Liquid**-Abschnitt.

## Einbau

1. **Themes → Anpassen**
2. **Abschnitt hinzufügen → Benutzerdefiniertes Liquid** *(Custom Liquid)*
3. Kompletten Inhalt von `featured-collection-tabs.liquid` in das große Feld einfügen
4. **Speichern**

Keine weiteren Dateien, keine Snippets, keine Änderung an Theme-Dateien.

## Einstellen

Custom Liquid kennt **kein `{% schema %}`** — alle Einstellungen stehen deshalb
oben im Code im Block `EINSTELLUNGEN` und werden dort bearbeitet, nicht in der
rechten Spalte des Theme-Editors:

| Zeile | Bedeutung |
|---|---|
| `heading` | Überschrift |
| `tab_labels` | Beschriftung der Tabs, durch Komma getrennt |
| `tab_handles` | Collection-Handles in derselben Reihenfolge |
| `products_limit` | Produkte je Tab |
| `swatches_visible` | Farbfelder vor dem „+N" |
| `show_arrows` | Pfeile am Karussell |
| `show_badge` | Rabatt-Badge |
| `cards_desktop` / `cards_tablet` / `cards_mobile` | Karten nebeneinander |

Den Handle einer Collection liefert ihre URL: `/collections/blankets` → `blankets`.
`all` ist die automatische Collection mit allen Produkten.

## Was der Code macht

- Tabs mit gleitendem Unterstrich, per Pfeiltasten bedienbar
- Karussell über **CSS-Scroll-Snapping** statt Swiper — kein jQuery, keine
  externen Dateien, kein zweites Karussell-Skript neben dem des Themes
- Produktkarte: Hauptbild, Hover-Bild, Rabatt-Badge (aus `compare_at_price`
  berechnet), Titel, Preis mit durchgestrichenem Vergleichspreis
- Farbfelder aus der Option „Color" / „Colour" / „Farbe". Ein Klick tauscht
  Bild, Preis und Produktlink der Karte. Ab dem vierten Feld eingeklappt
  hinter „+N"
- Alles CSS ist auf die Abschnitts-ID begrenzt, kollidiert also nicht mit
  dem Theme
- Farben kommen aus `--color-foreground` / `--color-background` des Themes,
  passen sich also an

## Grenzen

- **Nicht im Theme-Editor einstellbar.** Custom Liquid erlaubt kein Schema.
  Wer Überschrift und Collections klickbar braucht, nimmt statt dessen eine
  richtige Section (gleiche Datei plus `{% schema %}`, im Ordner `sections/`).
- **Farbfelder** nutzen Shopifys native Swatches (Admin → Einstellungen →
  Produkte → Swatches). Ohne die fällt der Code auf das Variantenbild zurück —
  dann sind die Punkte kleine Produktfotos statt Farbflächen.
- Die Karte ist ein **Nachbau**, keine Kopie der `card-v2`-Komponente des
  Themes. Bewertungssterne, Schnellkauf und Varianten-JSON sind nicht dabei.
- Zwei Instanzen auf derselben Seite funktionieren nur, wenn `section.id`
  verfügbar ist (Standardfall). Sonst oben `assign uid = ...` je Instanz
  unterschiedlich setzen.
