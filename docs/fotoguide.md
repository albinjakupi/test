# Fotoguide für die Cleeno-Website

Diese Anleitung listet auf, welche Aufnahmen die Website braucht, in welchem
Format, und worauf beim Fotografieren zu achten ist. Ein aktuelles Smartphone
genügt vollkommen – wichtiger als die Kamera sind Licht und Bildausschnitt.

## Warum eigene Fotos

Die ganze Website argumentiert mit «Familienbetrieb», «dieselben Leute»,
«Inhaberfamilie als Ansprechperson». Ein gekauftes Stockfoto mit lachendem
Model und Putzeimer widerlegt genau diese Aussage – Besucherinnen und Besucher
erkennen solche Bilder sofort. Ein etwas schiefes, aber echtes Foto vom eigenen
Team wirkt stärker als jedes perfekte Katalogbild.

Bis eigene Fotos vorliegen, zeigt die Website eigens gezeichnete Illustrationen
im Markenstil. Die sind ehrlich – sie geben sich nicht als Fotografie aus.

## Die Aufnahmeliste

| # | Wofür | Motiv | Format | Hinweise |
|---|---|---|---|---|
| 1 | Über uns | Das Team oder die Inhaberfamilie, draussen vor dem Fahrzeug | quer 4:3 | Der Kern der ganzen Seite. Freundlich, nicht gestellt-steif. |
| 2 | Über uns | Firmenfahrzeug mit Beschriftung, ganze Seite | quer 4:3 | Zeigt Professionalität und ist gleichzeitig Werbung. |
| 3+4 | Startseite, Vorher/Nachher | **Zwei** Bilder derselben Stelle – vor und nach der Reinigung | quer 16:10 | Kamera exakt gleich halten, am besten Stativ oder Markierung am Boden. Ohne identische Position wirkt der Regler unglaubwürdig. |
| 5 | Unterhaltsreinigung | Wohnzimmer oder Küche nach dem Einsatz | quer 4:3 | Aufgeräumt, Tageslicht, keine persönlichen Gegenstände der Kundschaft. |
| 6 | Büroreinigung | Leeres Büro, saubere Pulte, Boden mit Glanz | quer 4:3 | Am Abend nach dem Einsatz, ohne Mitarbeitende im Bild. |
| 7 | Fensterreinigung | Person mit Abzieher an einer grossen Scheibe | quer 4:3 | Gegenlicht vermeiden, Wassertropfen sind erwünscht. |
| 8 | Umzugsreinigung | Leere Wohnung, offene Küche mit sauberem Backofen | quer 4:3 | Räume wirken leer besser als möbliert. |
| 9 | Bauendreinigung | Neubauwohnung nach der Endreinigung | quer 4:3 | Baustellenkontext darf sichtbar bleiben, das erklärt die Leistung. |
| 10 | Liegenschaftsreinigung | Treppenhaus von oben oder unten fotografiert | hoch oder quer | Perspektive entlang der Treppe wirkt am stärksten. |

Zusätzlich immer nützlich: Detailaufnahmen von entkalkten Armaturen, einem
sauberen Backofen oder frisch gereinigten Storen. Solche Bilder lassen sich
später für Beiträge und Social Media verwenden.

## Technische Vorgaben

- **Quer fotografieren**, ausser bei Treppenhäusern. Die Bildplätze auf der
  Website sind querformatig.
- **Tageslicht** nutzen, Blitz vermeiden. Vorhänge auf, Licht einschalten.
- **Kamera auf Brusthöhe**, gerade halten – nicht von oben herab.
- **Mindestens 2000 Pixel** Breite aufnehmen. Verkleinern geht immer,
  vergrössern nie.
- **HEIC in JPEG umwandeln** (iPhone: Einstellungen → Kamera → Formate →
  «Maximale Kompatibilität»).
- **Aufräumen vor dem Auslösen**: Kabel, Putzwagen, Znüni und Jacken aus dem
  Bild. Ein einzelner störender Gegenstand macht das ganze Foto unbrauchbar.

## Rechtliches – bitte ernst nehmen

- **Personen** dürfen nur mit ihrer Einwilligung abgebildet werden. Für
  Mitarbeitende genügt eine kurze schriftliche Bestätigung; sie sollte auch
  regeln, was nach einem Austritt passiert.
- **Kundenobjekte** nur mit Erlaubnis der Eigentümerschaft oder Verwaltung
  fotografieren – und nichts abbilden, was Rückschlüsse auf die Bewohnenden
  zulässt: Namensschilder, Post, Fotos, Dokumente, Kinderzeichnungen.
- **Autokennzeichen** von Dritten unkenntlich machen.
- **Keine Bilder aus dem Internet** verwenden, auch nicht «nur kurz». Bei
  Bildrechtsverletzungen sind Forderungen im vierstelligen Bereich üblich, und
  sie treffen den Website-Betreiber, nicht den Fotografen.

## Wenn es doch Stockbilder sein müssen

Für Beiträge oder Übergangslösungen sind Bilddatenbanken in Ordnung. Dann gilt:

- Nur Anbieter mit klarer kommerzieller Lizenz (etwa Unsplash, Pexels oder
  kostenpflichtige Anbieter). Lizenztext herunterladen und ablegen.
- Schweizer Kontext bevorzugen – amerikanische Innenräume fallen auf.
- Keine Klischees: lachendes Model mit Putzeimer, Daumen hoch, blitzende
  Sterneffekte.
- Niemals ein Stockfoto als «unser Team» ausgeben.

## Bilder einsetzen

1. Datei nach `assets/img/` legen, sprechender Name, zum Beispiel
   `team-vor-fahrzeug.jpg`.
2. Auf etwa 1600 Pixel Breite verkleinern und als JPEG mit rund 80 Prozent
   Qualität speichern (Ziel: 150 bis 250 KB).
3. Im HTML den Platzhalter ersetzen:

```html
<div class="media">
  <img src="assets/img/team-vor-fahrzeug.jpg"
       alt="Das Team von Cleeno Reinigungen vor dem Firmenfahrzeug"
       width="1600" height="1200" loading="lazy">
</div>
```

Der `alt`-Text beschreibt, was zu sehen ist – er hilft blinden Nutzerinnen und
Nutzern und wird von Suchmaschinen gelesen.

Für den Vorher/Nachher-Regler auf der Startseite die beiden Quellen im Block
`<div class="ba">` ersetzen und anschliessend den Hinweissatz «Schematische
Darstellung …» darunter entfernen.
