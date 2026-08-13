#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generiert die statischen Unterseiten mit identischem Header/Footer.
Läuft einmalig im Scratchpad; das Repo enthält am Ende reines HTML/CSS/JS."""

import os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + "/"

import os, re, io

PHONE = "041 123 45 67"
TEL = "+41411234567"

index = io.open(os.path.join(ROOT, "index.html"), encoding="utf-8").read()

HEADER = re.search(r'(<a class="skip-link".*?</header>)', index, re.S).group(1)
FOOTER = re.search(r'(<footer class="site-footer">.*?</footer>)', index, re.S).group(1)
MOBILE_CTA = re.search(r'(<div class="mobile-cta">.*?</div>\s*</div>)', index, re.S)
MOBILE_CTA = MOBILE_CTA.group(1) if MOBILE_CTA else re.search(
    r'(<div class="mobile-cta">.*?\n</div>)', index, re.S).group(1)

HEADER = HEADER.replace(' aria-current="page"', '')

ICON_CHECK = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" '
              'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
              '<path d="M12 21a9 9 0 1 0 0-18 9 9 0 0 0 0 18Z"/><path d="m8.5 12.2 2.4 2.4 4.6-4.9"/></svg>')
ICON_ARROW = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" '
              'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
              '<path d="M5 12h14"/><path d="m13 6 6 6-6 6"/></svg>')

ICONS = {
    "home": '<path d="m4 10.5 8-6.2 8 6.2V19a1.6 1.6 0 0 1-1.6 1.6H5.6A1.6 1.6 0 0 1 4 19v-8.5Z"/><path d="M9.6 20.6v-6h4.8v6"/>',
    "office": '<rect x="3" y="7.5" width="18" height="12" rx="2.5"/><path d="M8.8 7.5V6a2 2 0 0 1 2-2h2.4a2 2 0 0 1 2 2v1.5"/><path d="M3 12.5h18"/>',
    "window": '<rect x="4" y="3.5" width="16" height="17" rx="2"/><path d="M12 3.5v17M4 12h16"/>',
    "truck": '<path d="M3 6.5h10.5v10H3z"/><path d="M13.5 10h3.8l2.7 3v3.5h-6.5z"/><circle cx="7.2" cy="18" r="1.8"/><circle cx="16.8" cy="18" r="1.8"/>',
    "hat": '<path d="M4 16.5a8 8 0 0 1 16 0"/><path d="M9.5 8.4V5.6A1.6 1.6 0 0 1 11.1 4h1.8a1.6 1.6 0 0 1 1.6 1.6v2.8"/><path d="M2.8 16.5h18.4a1 1 0 0 1 1 1v1.2a1 1 0 0 1-1 1H2.8a1 1 0 0 1-1-1v-1.2a1 1 0 0 1 1-1Z"/>',
    "building": '<rect x="4" y="3" width="16" height="18" rx="2"/><path d="M9 7h2M13 7h2M9 11h2M13 11h2M9 15h2M13 15h2"/>',
    "sparkle": '<path d="M12 3.5 13.8 9l5.5 1.8-5.5 1.8L12 18l-1.8-5.4L4.7 10.8 10.2 9 12 3.5Z"/><path d="M18.6 3v3.4M20.3 4.7h-3.4M5.4 16.2v2.8M6.8 17.6H4"/>',
    "leaf": '<path d="M20 4c0 8-4.6 12.5-11 12.5H5.5C5.5 9.5 10.5 4 20 4Z"/><path d="M4 20c2-4.5 5-7 9-8.6"/>',
    "shield": '<path d="M12 3l7 3v5.5c0 4.4-3 8.1-7 9.5-4-1.4-7-5.1-7-9.5V6l7-3Z"/><path d="m9 12 2.2 2.2L15.4 10"/>',
    "users": '<circle cx="9" cy="8" r="3.4"/><path d="M2.8 20a6.4 6.4 0 0 1 12.4 0"/><path d="M16 5.2a3.4 3.4 0 0 1 0 6.6"/><path d="M17.6 14.4A6.4 6.4 0 0 1 21.6 20"/>',
    "clock": '<circle cx="12" cy="12" r="9"/><path d="M12 7v5.2l3.4 2"/>',
    "pin": '<path d="M12 21s7-5.6 7-11a7 7 0 1 0-14 0c0 5.4 7 11 7 11Z"/><circle cx="12" cy="10" r="2.6"/>',
    "phone": '<path d="M6.6 3.5h3l1.6 4-2 1.4a12 12 0 0 0 5.9 5.9l1.4-2 4 1.6v3a2 2 0 0 1-2.2 2A17 17 0 0 1 4.6 5.7a2 2 0 0 1 2-2.2Z"/>',
    "mail": '<rect x="3" y="5" width="18" height="14" rx="2.5"/><path d="m3.8 6.6 8.2 5.7 8.2-5.7"/>',
    "doc": '<path d="M6 3.5h8.5L19 8v12.5H6z"/><path d="M14 3.5V8h5"/><path d="M9 12.5h6M9 16h4"/>',
    "calendar": '<rect x="3.5" y="5" width="17" height="15" rx="2.5"/><path d="M3.5 10h17M8 3.5V7M16 3.5V7"/>',
    "carpet": '<rect x="3" y="6" width="18" height="12" rx="2"/><path d="M3 10h18M3 14h18M8 6v12M16 6v12"/>',
    "snow": '<path d="M12 3v18M4.2 7.5l15.6 9M19.8 7.5l-15.6 9"/>',
    "tools": '<path d="M14.5 6.5a3.8 3.8 0 0 0 5 5l-9 9a2.5 2.5 0 0 1-3.5-3.5l9-9Z"/><path d="m6.5 6.5 3 3"/>',
    "heart": '<path d="M12 20s-7.5-4.7-7.5-9.6A4.4 4.4 0 0 1 12 7.6a4.4 4.4 0 0 1 7.5 2.8C19.5 15.3 12 20 12 20Z"/>',
    "wallet": '<rect x="3" y="6" width="18" height="13" rx="2.5"/><path d="M3 10h18M16.5 14.5h1.5"/>',
}


def icon(name, sw="1.7"):
    return ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="' + sw +
            '" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">' + ICONS[name] + '</svg>')


def checklist(items, cls="checklist"):
    out = ['<ul class="' + cls + '">']
    for it in items:
        if isinstance(it, tuple):
            out.append('<li>' + ICON_CHECK + '<div><strong>' + it[0] + '</strong><span>' + it[1] + '</span></div></li>')
        else:
            out.append('<li>' + ICON_CHECK + '<div><strong>' + it + '</strong></div></li>')
    out.append('</ul>')
    return "\n        ".join(out)


def pills(items):
    return ('<div class="hero__pills">'
            + "".join('<span class="pill">' + ICON_CHECK + i + '</span>' for i in items)
            + '</div>')


def faq(items):
    out = ['<div class="faq reveal">']
    for q, a in items:
        out.append('<details><summary>' + q + '</summary><p>' + a + '</p></details>')
    out.append('</div>')
    return "\n        ".join(out)


def table(head, rows):
    out = ['<div class="table-wrap"><table>',
           '<thead><tr>' + "".join('<th>' + h + '</th>' for h in head) + '</tr></thead>', '<tbody>']
    for r in rows:
        out.append('<tr>' + "".join('<td>' + c + '</td>' for c in r) + '</tr>')
    out.append('</tbody></table></div>')
    return "\n        ".join(out)


import json as _json

BASE = "https://www.cleeno-reinigungen.ch/"
ORTE = ["Perlen", "Root", "Ebikon", "Buchrain", "Emmen", "Luzern",
        "Kriens", "Rotkreuz", "Cham", "Baar", "Zug", "Hochdorf", "Sursee"]


def ld(*blocks):
    """Ein oder mehrere JSON-LD-Blöcke ausgeben."""
    out = ""
    for b in blocks:
        if b:
            out += ('<script type="application/ld+json">\n'
                    + _json.dumps(b, ensure_ascii=False, indent=2) + '\n</script>\n')
    return out


def ld_breadcrumb(items):
    """items: [(Name, Datei), …] – die Startseite wird automatisch vorangestellt."""
    liste = [("Startseite", "")] + list(items)
    return {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": i + 1, "name": n, "item": BASE + f}
            for i, (n, f) in enumerate(liste)
        ],
    }


def ld_faq(paare):
    return {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": q,
             "acceptedAnswer": {"@type": "Answer", "text": a}}
            for q, a in paare
        ],
    }


def ld_service(name, beschreibung, datei):
    return {
        "@context": "https://schema.org",
        "@type": "Service",
        "name": name,
        "serviceType": name,
        "description": beschreibung,
        "url": BASE + datei,
        "provider": {
            "@type": "LocalBusiness",
            "name": "Cleeno Reinigungen",
            "telephone": TEL,
            "url": BASE,
            "address": {
                "@type": "PostalAddress",
                "streetAddress": "Am Kanal 30",
                "postalCode": "6035",
                "addressLocality": "Perlen",
                "addressRegion": "LU",
                "addressCountry": "CH",
            },
        },
        "areaServed": [{"@type": "City", "name": n} for n in ORTE],
    }


def ld_article(titel, beschreibung, datei, datum="2026-08-13"):
    return {
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": titel,
        "description": beschreibung,
        "inLanguage": "de-CH",
        "datePublished": datum,
        "dateModified": datum,
        "mainEntityOfPage": {"@type": "WebPage", "@id": BASE + datei},
        "image": BASE + "assets/og-cleeno.png",
        "author": {"@type": "Organization", "name": "Cleeno Reinigungen", "url": BASE},
        "publisher": {
            "@type": "Organization",
            "name": "Cleeno Reinigungen",
            "logo": {"@type": "ImageObject", "url": BASE + "assets/icon-512.png"},
        },
    }


def cta(title="Holen Sie sich den Festpreis – kostenlos und in 24 Stunden",
        text="Sagen Sie uns kurz, worum es geht. Sie erhalten eine schriftliche Offerte mit fixem Preis und allen drei Garantien.",
        href="kontakt.html"):
    return """  <section class="section section--tight">
    <div class="container">
      <div class="cta-band reveal">
        <div>
          <h2>""" + title + """</h2>
          <p>""" + text + """</p>
          <p class="cta-band__note">Unverbindlich, ohne Anzahlung – und wir sagen auch, wenn weniger genügt.</p>
        </div>
        <div class="btn-row">
          <a class="btn btn--light" href=\"""" + href + """\">Offerte anfordern</a>
          <a class="btn btn--outline-light" href="tel:""" + TEL + """\">""" + PHONE + """</a>
        </div>
      </div>
    </div>
  </section>"""


GUARANTEES = """  <section class="section section--soft" id="garantien">
    <div class="container">
      <div class="section-head section-head--center reveal">
        <span class="eyebrow">Unsere Garantien</span>
        <h2>Drei Zusagen, die in jeder Offerte stehen</h2>
      </div>
      <div class="guarantees reveal">
        <div class="guarantee">
          <div class="guarantee__icon">""" + icon("doc") + """</div>
          <h3>Festpreis-Garantie</h3>
          <p>Der Preis in der Offerte ist der Preis auf der Rechnung – Mehraufwand geht zu unseren Lasten.</p>
        </div>
        <div class="guarantee">
          <div class="guarantee__icon">""" + icon("shield") + """</div>
          <h3>Abnahmegarantie</h3>
          <p>Bei Umzugsreinigungen reinigen wir kostenlos nach, falls bei der Abgabe etwas beanstandet wird.</p>
        </div>
        <div class="guarantee">
          <div class="guarantee__icon">""" + icon("clock") + """</div>
          <h3>Reaktionsgarantie</h3>
          <p>Antwort auf jede Anfrage innert 24 Stunden, Reklamationen noch am selben Werktag.</p>
        </div>
      </div>
    </div>
  </section>"""


def page(filename, title, desc, active, body, canonical=None, noindex=False, scripts="", jsonld=""):
    header = HEADER
    if active:
        header = header.replace('<a class="nav__link" href="' + active + '">',
                                '<a class="nav__link" href="' + active + '" aria-current="page">')
        header = header.replace('<li><a href="' + active + '">',
                                '<li><a href="' + active + '" aria-current="page">')
    canon = canonical or ("https://www.cleeno-reinigungen.ch/" + filename)
    html = """<!DOCTYPE html>
<html lang="de-CH">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>""" + title + """</title>
<meta name="description" content=\"""" + desc + """\">
""" + ('<meta name="robots" content="noindex">' if noindex else '<link rel="canonical" href="' + canon + '">') + """
<meta property="og:type" content="website">
<meta property="og:title" content=\"""" + title + """\">
<meta property="og:description" content=\"""" + desc + """\">
<meta property="og:locale" content="de_CH">
<meta property="og:site_name" content="Cleeno Reinigungen">
<meta property="og:url" content=\"""" + canon + """\">
<meta property="og:image" content="https://www.cleeno-reinigungen.ch/assets/og-cleeno.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="Cleeno Reinigungen – Reinigung mit Abnahmegarantie in Perlen, Luzern und Zug">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#ffffff" media="(prefers-color-scheme: light)">
<meta name="theme-color" content="#0A1830" media="(prefers-color-scheme: dark)">
<link rel="icon" href="assets/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="assets/apple-touch-icon.png">
<link rel="manifest" href="site.webmanifest">
<link rel="preload" href="assets/fonts/outfit-700.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="assets/fonts/source-sans-400.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="css/style.css">
</head>
<body>
""" + header + """

<main id="main">

""" + body + """

</main>

""" + FOOTER + """

""" + MOBILE_CTA + """

""" + jsonld + """<script src="js/main.js" defer></script>
""" + scripts + """</body>
</html>
"""
    io.open(os.path.join(ROOT, filename), "w", encoding="utf-8").write(html)
    print("geschrieben:", filename, len(html), "Zeichen")


def pagehead(crumbs, h1, lead, eyebrow=None, cta_href="kontakt.html",
             cta_label="Kostenlose Offerte anfordern", extra="", second=None):
    items = ['<li><a href="index.html">Startseite</a></li>']
    for c in crumbs[:-1]:
        items.append('<li><a href="' + c[1] + '">' + c[0] + '</a></li>')
    items.append('<li aria-current="page">' + crumbs[-1][0] + '</li>')
    buttons = ""
    if cta_href:
        buttons = ("""
      <div class="btn-row mt-24">
        <a class="btn btn--grad" href=\"""" + cta_href + """\">""" + cta_label + " " + ICON_ARROW + """</a>
        """ + ('<a class="btn btn--ghost" href="' + second[0] + '">' + second[1] + '</a>' if second else '') + """
        <a class="btn btn--ghost" href="tel:""" + TEL + """\">""" + PHONE + """</a>
      </div>""")
    return """  <section class="pagehead">
    <div class="container">
      <nav class="breadcrumb" aria-label="Brotkrumen-Navigation"><ol>
        """ + "\n        ".join(items) + """
      </ol></nav>
      """ + ('<span class="eyebrow">' + eyebrow + '</span>' if eyebrow else '') + """
      <h1>""" + h1 + """</h1>
      <p>""" + lead + """</p>""" + buttons + extra + """
    </div>
  </section>"""


# ============================================================
# Leistungsdaten
# ============================================================
SERVICES = [
    dict(
        file="unterhaltsreinigung.html", key="unterhaltsreinigung", icon="home", name="Unterhaltsreinigung",
        short="Regelmässige Reinigung von Wohnung oder Haus – wöchentlich, vierzehntäglich oder monatlich, immer durch dieselbe Person.",
        title="Unterhaltsreinigung Luzern &amp; Zug | Cleeno Reinigungen",
        desc="Regelmässige Unterhaltsreinigung für Wohnungen und Häuser in Luzern und Zug: dieselbe Reinigungskraft, Material inklusive, fester Stundenansatz.",
        lead="Sie kommen nach Hause und alles ist gemacht: Wir übernehmen die wiederkehrende Reinigung Ihrer Wohnung oder Ihres Hauses – in Ihrem Rhythmus und immer mit derselben Person.",
        pills=["Immer dieselbe Person", "Material inklusive", "Monatlich kündbar"],
        intro_h2="Ihre Wohnung, zuverlässig sauber – ohne dass Sie daran denken müssen",
        intro_p=("Die Unterhaltsreinigung ist unser häufigster Auftrag im Privatbereich. Wir vereinbaren einmal, "
                 "was regelmässig gemacht wird und was nur turnusmässig – zum Beispiel Sockelleisten, Fenster oder "
                 "der Kühlschrank innen. Diesen Reinigungsplan halten wir schriftlich fest, damit für beide Seiten "
                 "klar ist, was zum Einsatz gehört."),
        bullets=[
            ("Feste Reinigungskraft", "Dieselbe Person kennt Ihre Wohnung, Ihre Produkte und Ihre Wünsche."),
            ("Ihr Rhythmus", "Wöchentlich, alle zwei Wochen, monatlich oder nur bei Bedarf."),
            ("Schlüsselservice", "Auf Wunsch übernehmen wir die Schlüssel treuhänderisch und protokolliert."),
            ("Ferienvertretung", "Bei Krankheit oder Ferien stellen wir eine eingearbeitete Vertretung."),
        ],
        table_head=["Bereich", "Was regelmässig gemacht wird"],
        table_rows=[
            ["Küche", "Arbeitsflächen, Kochfeld, Spüle und Armaturen, Schrankfronten, Geräte von aussen, Boden feucht"],
            ["Bad und WC", "WC, Dusche und Badewanne, Lavabo, Spiegel, Armaturen entkalken, Boden feucht"],
            ["Wohn- und Schlafräume", "Staubsaugen, Böden feucht reinigen, Staub auf freien Flächen, Spiegel und Glastüren"],
            ["Allgemein", "Abfall entsorgen, Türgriffe und Lichtschalter, Sockelleisten und Türrahmen turnusmässig"],
            ["Auf Wunsch", "Fenster innen, Kühlschrank und Backofen innen, Wäsche waschen und bügeln, Pflanzen giessen"],
        ],
        price="Richtwert CHF 45.– bis 55.– pro Stunde inklusive Material und Anfahrt. Eine 3,5-Zimmer-Wohnung benötigt erfahrungsgemäss rund drei Stunden.",
        faqs=[
            ("Muss ich während der Reinigung zu Hause sein?",
             "Nein. Die meisten Kundinnen und Kunden übergeben uns einen Schlüssel. Die Übergabe wird protokolliert, die Schlüssel bewahren wir nummeriert und ohne Adressangabe auf."),
            ("Kann ich den Rhythmus später ändern?",
             "Jederzeit. Sagen Sie uns zwei Wochen im Voraus Bescheid, dann passen wir die Planung an – auch eine Pause während der Ferien ist problemlos möglich."),
            ("Werden meine eigenen Reinigungsmittel verwendet?",
             "Wenn Sie das möchten, gerne. Standardmässig bringen wir eigenes, ökologisch zertifiziertes Material mit; das ist im Stundenansatz enthalten."),
            ("Wie ist die Kündigungsfrist?",
             "Ein Monat auf Monatsende, ohne Mindestlaufzeit. Wer bleibt, soll das freiwillig tun."),
        ],
    ),
    dict(
        file="bueroreinigung.html", key="bueroreinigung", icon="office", name="Büroreinigung",
        short="Arbeitsplätze, Sitzungszimmer, Sanitär und Teeküche – ausserhalb Ihrer Bürozeiten, nach fixem Reinigungsplan.",
        title="Büroreinigung Luzern &amp; Zug | Cleeno Reinigungen",
        desc="Büroreinigung in Luzern, Zug und dem Rontal: Reinigung ausserhalb der Bürozeiten, fixer Reinigungsplan, feste Ansprechperson, monatliche Pauschale. Offerte in 24 Stunden.",
        lead="Ihre Mitarbeitenden sollen sich um ihre Arbeit kümmern, nicht um die Teeküche. Wir reinigen Ihre Geschäftsräume ausserhalb der Betriebszeiten – zuverlässig, diskret und nach einem Plan, den Sie kennen.",
        pills=["Ausserhalb der Bürozeiten", "Feste Ansprechperson", "3 Monate Testphase"],
        intro_h2="Ein Reinigungsplan, den alle Beteiligten kennen",
        intro_p=("Bei Geschäftskunden legen wir vor dem Start fest, welche Arbeiten täglich, wöchentlich, monatlich "
                 "oder jährlich anfallen. Dieser Plan hängt im Putzraum, die Objektleitung kontrolliert stichprobenartig "
                 "und Sie erhalten eine feste Ansprechperson mit Direktnummer – kein Callcenter, keine Warteschlaufe."),
        bullets=[
            ("Ausserhalb Ihrer Bürozeiten", "Früh morgens, abends oder am Wochenende – der Betrieb wird nicht gestört."),
            ("Feste Ansprechperson", "Eine Person, die Ihr Gebäude kennt und direkt erreichbar ist."),
            ("Dokumentierte Qualität", "Regelmässige Kontrollen mit Protokoll, das Sie auf Wunsch erhalten."),
            ("Verbrauchsmaterial", "Seife, Papier und Hygieneartikel auf Wunsch inklusive Nachfüllservice."),
        ],
        table_head=["Bereich", "Täglich / wöchentlich", "Periodisch"],
        table_rows=[
            ["Arbeitsplätze", "Abfall leeren, freie Flächen abstauben, Böden saugen", "Grundreinigung Böden, Bürostühle, Storen"],
            ["Sitzungszimmer und Empfang", "Tische, Gläser, Böden, Glastüren", "Polster- und Teppichreinigung"],
            ["Sanitäranlagen", "WC, Urinale, Lavabos, Spiegel, Desinfektion, Verbrauchsmaterial", "Entkalkung, Fugenreinigung"],
            ["Teeküche", "Spüle, Arbeitsflächen, Geräte aussen, Abfalltrennung", "Kühlschrank und Kaffeemaschine innen"],
            ["Verkehrsflächen", "Eingang, Korridore, Treppen, Lift", "Glasflächen, Fenster innen und aussen"],
        ],
        price="Nach Fläche und Frequenz, in der Regel als monatliche Pauschale. Grundlage ist eine kostenlose Besichtigung vor Ort.",
        faqs=[
            ("Wie kommen Ihre Mitarbeitenden ins Gebäude?",
             "Über Schlüssel oder Badge, dessen Übergabe protokolliert wird. Alarmcodes behandeln wir vertraulich; alle Mitarbeitenden unterschreiben eine Geheimhaltungsvereinbarung."),
            ("Was passiert bei Ferien oder Krankheit?",
             "Wir stellen eine eingearbeitete Vertretung. Da mindestens zwei Personen jedes Objekt kennen, fällt keine Reinigung aus."),
            ("Übernehmen Sie auch das Verbrauchsmaterial?",
             "Ja. Auf Wunsch liefern und füllen wir Seife, Papierhandtücher, WC-Papier und Hygienebeutel nach und verrechnen sie zum Einstandspreis."),
            ("Ist eine Probezeit möglich?",
             "Ja. Die ersten drei Monate gelten als Testphase mit 14-tägiger Kündigungsfrist – so können Sie uns ohne Risiko ausprobieren."),
        ],
    ),
    dict(
        file="fensterreinigung.html", key="fensterreinigung", icon="window", name="Fensterreinigung",
        short="Streifenfreie Scheiben inklusive Rahmen, Falze und Storen – auch in Höhe mit Teleskopsystem.",
        title="Fensterreinigung Luzern &amp; Zug | Cleeno Reinigungen",
        desc="Fensterreinigung für Privat und Gewerbe in Luzern, Zug und dem Rontal: Glas, Rahmen, Falze und Storen, auch in Höhe mit osmotischem Wasser. Jetzt Offerte anfordern.",
        lead="Saubere Fenster verändern einen Raum sofort. Wir reinigen Glas, Rahmen, Falze und Sims – innen wie aussen, in jeder erreichbaren Höhe und ohne Streifen.",
        pills=["Rahmen und Falze inklusive", "Bis 12 Meter Höhe", "Ab CHF 6.– pro Flügel"],
        intro_h2="Sauber bis in die Ecke – und ohne Wasserränder",
        intro_p=("Zu einer richtigen Fensterreinigung gehört mehr als die Glasfläche: Erst mit gereinigten Falzen, "
                 "Rahmen und Simsen bleibt das Resultat länger schön, weil kein Schmutzwasser nachläuft. Für höher "
                 "gelegene Fenster arbeiten wir mit Teleskopstangen und entmineralisiertem Wasser, das rückstandsfrei "
                 "abtrocknet – ganz ohne Leitern am Fassadensims."),
        bullets=[
            ("Glas innen und aussen", "Von Hand gewaschen und abgezogen, ohne Schlieren und Wasserränder."),
            ("Rahmen, Falze und Sims", "Standardmässig enthalten – nicht als Zusatzposition auf der Rechnung."),
            ("Storen und Rollläden", "Lamellenreinigung auf Wunsch, inklusive Führungsschienen."),
            ("Höhe bis 12 Meter", "Teleskopsystem mit osmotischem Wasser; darüber mit Hebebühne nach Absprache."),
        ],
        table_head=["Objekt", "Enthaltene Arbeiten"],
        table_rows=[
            ["Wohnung oder Haus", "Alle Fenster innen und aussen, Rahmen, Falze, Fenstersimse, Balkontüren"],
            ["Büro und Gewerbe", "Fensterfronten, Trennwände aus Glas, Eingangstüren, Schaufenster"],
            ["Storen und Beschattung", "Lamellenstoren, Rollläden, Führungsschienen, Fensterläden"],
            ["Spezialflächen", "Wintergärten, Glasdächer, Balkonverglasungen, Lichtschächte"],
        ],
        price="Ab CHF 6.– pro Fensterflügel (beidseitig, inklusive Rahmen). Für Storen und Spezialflächen offerieren wir separat.",
        faqs=[
            ("Was passiert bei schlechtem Wetter?",
             "Leichter Regen ist kein Problem – das Resultat leidet nicht. Bei Sturm oder Frost verschieben wir den Termin kostenlos."),
            ("Wie oft sollten Fenster gereinigt werden?",
             "Für Wohnräume genügen meist zwei Reinigungen pro Jahr, für Ladenlokale und Bürofronten empfehlen wir vier bis zwölf. Den Rhythmus hinterlegen wir gern fix in der Jahresplanung."),
            ("Reinigen Sie auch Fenster, die nicht zu öffnen sind?",
             "Ja, mit Teleskopstange und osmotischem Wasser vom Boden aus oder – wo nötig – mit Hebebühne. Beides klären wir vor der Offerte ab."),
            ("Muss ich zu Hause sein?",
             "Für die Aussenreinigung nicht, sofern der Zugang gewährleistet ist. Für Fenster innen brauchen wir Zutritt oder einen hinterlegten Schlüssel."),
        ],
    ),
    dict(
        file="umzugsreinigung.html", key="umzugsreinigung", icon="truck", name="Umzugsreinigung",
        short="Wohnungsübergabe ohne Stress: gereinigt bis abnahmebereit – mit Garantie und kostenloser Nachreinigung.",
        title="Umzugsreinigung mit Abnahmegarantie | Cleeno Reinigungen",
        desc="Umzugsreinigung in Luzern und Zug zum Pauschalpreis mit Abnahmegarantie: Küche, Bad, Böden, Fenster und Storen inklusive. Kostenlose Nachreinigung.",
        lead="Der Umzug ist stressig genug. Wir übernehmen die Endreinigung Ihrer Wohnung zum Pauschalpreis – inklusive Fenster, Storen und Abnahmegarantie gegenüber Verwaltung oder Vermieterschaft.",
        pills=["Abnahmegarantie", "Fenster und Storen inklusive", "Kurzfristige Termine"],
        intro_h2="Mit Abnahmegarantie: Wir bleiben dran, bis die Übergabe sitzt",
        intro_p=("Bei jeder Umzugsreinigung gilt unsere Abnahmegarantie: Wird bei der Wohnungsabgabe etwas beanstandet, "
                 "das in unseren Auftrag fällt, reinigen wir kostenlos nach – in der Regel noch am selben oder am "
                 "folgenden Tag. Auf Wunsch ist eine Person von uns bei der Abnahme dabei und klärt Beanstandungen direkt "
                 "mit der Verwaltung."),
        bullets=[
            ("Fixer Pauschalpreis", "Nach Zimmerzahl und Zustand – nicht nach Stunden, damit Sie sicher rechnen können."),
            ("Fenster und Storen inklusive", "Beides ist Teil der Pauschale und keine Zusatzposition."),
            ("Abnahmegarantie", "Kostenlose Nachreinigung bei Beanstandungen im vereinbarten Umfang."),
            ("Begleitung bei der Abgabe", "Auf Wunsch sind wir bei der Übergabe anwesend."),
        ],
        table_head=["Bereich", "Enthaltene Arbeiten"],
        table_rows=[
            ["Küche", "Schränke innen und aussen, Backofen, Dampfabzug inkl. Filter, Kühlschrank, Steamer, Spüle entkalkt"],
            ["Bad und WC", "Dusche, Badewanne, WC, Lavabo, Spiegelschrank, Armaturen und Plättli entkalkt, Fugen"],
            ["Böden und Wände", "Alle Bodenbeläge gereinigt, Sockelleisten, Türen und Türrahmen, Lichtschalter, Steckdosen"],
            ["Fenster", "Glas innen und aussen, Rahmen, Falze, Fenstersimse, Lamellenstoren und Rollläden"],
            ["Nebenräume", "Keller, Estrich, Balkon oder Sitzplatz, Waschturm und Waschküchenanteil"],
        ],
        price="Richtpreise siehe Tabelle unten – der definitive Preis steht nach kurzer Besichtigung oder anhand von Fotos fest.",
        extra_table=(["Wohnungsgrösse", "Richtpreis inkl. Fenster, Storen und Abnahmegarantie"],
                     [["1,5 Zimmer", "ab CHF 390.–"],
                      ["2,5 Zimmer", "ab CHF 490.–"],
                      ["3,5 Zimmer", "ab CHF 690.–"],
                      ["4,5 Zimmer", "ab CHF 890.–"],
                      ["5,5 Zimmer und grösser", "auf Anfrage"]]),
        faqs=[
            ("Was bedeutet Abnahmegarantie genau?",
             "Beanstandet die Verwaltung bei der Abgabe eine Position aus unserem Auftrag, reinigen wir sie kostenlos nach. Nicht abgedeckt sind Schäden, Abnutzung und Reparaturen – dafür ist die Vermieterschaft oder Ihre Haftpflicht zuständig."),
            ("Muss die Wohnung leer sein?",
             "Ja, für die Endreinigung sollten alle Möbel und persönlichen Gegenstände draussen sein. Einzelne Möbel können stehen bleiben, wenn Sie uns das vorher sagen – wir halten es in der Offerte fest."),
            ("Wie kurzfristig können Sie kommen?",
             "Wir halten pro Woche Termine für kurzfristige Anfragen frei. In dringenden Fällen lohnt sich ein Anruf – häufig finden wir innert weniger Tage einen Slot."),
            ("Reinigen Sie auch nur einzelne Teile?",
             "Ja. Manche Kundinnen und Kunden übernehmen die Böden selbst und lassen nur Küche, Bad und Fenster machen. Die Abnahmegarantie gilt dann für den beauftragten Teil."),
        ],
    ),
    dict(
        file="bauendreinigung.html", key="bauendreinigung", icon="hat", name="Bauendreinigung",
        short="Grob-, Fein- und Endreinigung nach Umbau oder Neubau – inklusive Zement-, Farb- und Kleberesten.",
        title="Bauendreinigung Luzern &amp; Zug | Cleeno Reinigungen",
        desc="Bauendreinigung in Luzern, Zug und dem Rontal für Neubau und Umbau: Grob-, Fein- und Endreinigung vor Übergabe, inklusive Zement- und Farbresten. Offerte nach Begehung.",
        lead="Nach dem letzten Handwerker kommen wir: Wir bringen Neubauten und umgebaute Objekte in den Zustand, in dem sie übergeben werden können – etappenweise und termingerecht.",
        pills=["Direkt mit der Bauleitung", "Auch am Wochenende", "Pauschale pro Etappe"],
        intro_h2="Drei Etappen, ein Ergebnis",
        intro_p=("Bauendreinigung ist Terminarbeit. Wir stimmen uns direkt mit der Bauleitung ab, arbeiten – wenn nötig – "
                 "abends oder samstags und stellen bei grossen Objekten mehrere Teams gleichzeitig. Nach der Endreinigung "
                 "übergeben wir das Objekt besichtigungs- und bezugsbereit."),
        bullets=[
            ("Direkt mit der Bauleitung", "Ein Ansprechpartner, klare Etappen, verlässliche Termine."),
            ("Spezialreinigung", "Zementschleier, Farb- und Kleberreste, Silikon, Aufkleber und Schutzfolien."),
            ("Eigene Maschinen", "Industriesauger, Einscheibenmaschine, Nass-Trocken-Sauger, Hebebühne nach Bedarf."),
            ("Auch am Wochenende", "Wir richten uns nach dem Bauprogramm, nicht umgekehrt."),
        ],
        table_head=["Etappe", "Umfang", "Zeitpunkt"],
        table_rows=[
            ["Grobreinigung", "Baustellenabfall zusammentragen, grobe Verschmutzung entfernen, Böden saugen und wischen", "Nach Rohbau bzw. vor dem Innenausbau"],
            ["Feinreinigung", "Schutzfolien und Aufkleber, Zement- und Gipsreste, Fenster, Nassbereiche, Einbauten innen", "Nach Abschluss der Handwerkerarbeiten"],
            ["Endreinigung", "Alle Oberflächen bezugsbereit, Böden versiegelungsbereit, Glas streifenfrei, Detailkontrolle", "Unmittelbar vor Übergabe"],
        ],
        price="Nach Fläche und Verschmutzungsgrad, üblicherweise als Pauschale pro Etappe. Grundlage ist eine Begehung mit der Bauleitung.",
        faqs=[
            ("Entsorgen Sie auch Bauschutt?",
             "Kleinmengen nehmen wir mit. Für Mulden und Sondermüll organisieren wir auf Wunsch die Entsorgung und verrechnen sie nach Aufwand."),
            ("Können Sie mehrere Wohnungen gleichzeitig übernehmen?",
             "Ja. Für Überbauungen stellen wir mehrere Teams und eine Person, die die Etappen mit Ihrem Bauprogramm abgleicht."),
            ("Übernehmen Sie auch die Ersteinstellung von Böden?",
             "Ja, Grundreinigung und Erstpflege von Parkett, Linoleum oder Plattenböden gehören zum Angebot – das Produkt stimmen wir mit dem Bodenleger ab."),
            ("Wie schnell erhalte ich eine Offerte?",
             "Nach der Begehung innert 24 bis 48 Stunden, mit Etappen, Terminen und Preisen pro Position."),
        ],
    ),
    dict(
        file="liegenschaftsreinigung.html", key="liegenschaftsreinigung", icon="building", name="Liegenschaftsreinigung",
        short="Treppenhaus, Waschküche, Lift und Aussenbereich – für Eigentümer und Verwaltungen, das ganze Jahr über.",
        title="Liegenschaftsreinigung Luzern &amp; Zug | Cleeno",
        desc="Liegenschafts- und Treppenhausreinigung in Luzern, Zug und dem Rontal: fixer Turnus, ausgehängter Reinigungsplan, Umgebungspflege und Winterdienst auf Wunsch.",
        lead="Für Verwaltungen und Eigentümerschaften halten wir Liegenschaften das ganze Jahr in Form – vom Treppenhaus über die Waschküche bis zur Umgebung.",
        pills=["Fixer Turnus", "Mängel werden gemeldet", "Winterdienst möglich"],
        intro_h2="Eine Liegenschaft, ein Team, ein fixer Plan",
        intro_p=("Wir betreuen Mehrfamilienhäuser mit einem festen Turnus und einem Reinigungsplan, der im Eingang "
                 "aushängt – so wissen auch die Bewohnerinnen und Bewohner, wann was gemacht wird. Die Verwaltung "
                 "erhält eine feste Ansprechperson und auf Wunsch ein jährliches Reporting über ausgeführte Arbeiten "
                 "und festgestellte Mängel."),
        bullets=[
            ("Fixer Turnus", "Wöchentlich, alle zwei Wochen oder monatlich – je nach Grösse und Nutzung."),
            ("Sichtbarer Reinigungsplan", "Aushang im Eingangsbereich schafft Transparenz gegenüber den Mietenden."),
            ("Mängel melden", "Defekte Lampen, verstopfte Abläufe oder Schäden melden wir der Verwaltung sofort."),
            ("Umgebung und Winterdienst", "Auf Wunsch inklusive Hauswartung, Grünpflege und Schneeräumung."),
        ],
        table_head=["Bereich", "Enthaltene Arbeiten"],
        table_rows=[
            ["Treppenhaus und Korridore", "Treppen und Podeste feucht reinigen, Geländer, Briefkastenanlage, Eingangstüren, Glasflächen"],
            ["Lift", "Kabine, Spiegel, Bedienpanel, Türschwellen und Schienen"],
            ["Waschküche und Trocknungsraum", "Geräte aussen, Ablagen, Flusensiebe, Boden, Lüftungsgitter"],
            ["Neben- und Aussenräume", "Veloraum, Kellergänge, Einstellhalle, Entsorgungsplatz, Vordächer"],
            ["Umgebung (optional)", "Wege wischen, Grünpflege, Laubentfernung, Winterdienst mit Bereitschaft"],
        ],
        price="Monatliche Pauschale nach Anzahl Wohnungen, Stockwerken und Turnus. Für Verwaltungen mit mehreren Objekten offerieren wir Rahmenverträge.",
        faqs=[
            ("Wie oft sollte ein Treppenhaus gereinigt werden?",
             "Bei Mehrfamilienhäusern mit sechs bis zwölf Wohnungen hat sich ein 14-tägiger Turnus bewährt, bei stark genutzten Eingängen ein wöchentlicher. Wir empfehlen nach der Besichtigung eine konkrete Variante."),
            ("Übernehmen Sie auch die Hauswartung?",
             "Ja, technische Hauswartung und Umgebungspflege decken wir mit demselben Team ab – so haben Sie nur eine Ansprechperson für die ganze Liegenschaft."),
            ("Bieten Sie Winterdienst an?",
             "Ja, mit Bereitschaftsdienst ab dem ersten Schnee, inklusive Splitt und Räumung der Zugänge bis zum Beginn der ortsüblichen Zeiten."),
            ("Erhalten wir als Verwaltung eine Übersicht?",
             "Auf Wunsch dokumentieren wir jeden Einsatz und stellen Ihnen jährlich ein Reporting mit Leistungen und gemeldeten Mängeln zu."),
        ],
    ),
]


ILLU = {
    "unterhaltsreinigung": ("assets/illu-wohnung.svg", "Illustration eines frisch gereinigten Wohnraums"),
    "bueroreinigung": ("assets/illu-buero.svg", "Illustration eines gereinigten Büroarbeitsplatzes"),
    "fensterreinigung": ("assets/illu-fenster.svg", "Illustration einer streifenfrei gereinigten Fensterfront"),
    "umzugsreinigung": ("assets/illu-umzug.svg", "Illustration gestapelter Umzugskartons in einer leeren Wohnung"),
    "bauendreinigung": ("assets/illu-bau.svg", "Illustration eines Rohbaus vor der Endreinigung"),
    "liegenschaftsreinigung": ("assets/illu-liegenschaft.svg", "Illustration eines gepflegten Mehrfamilienhauses"),
}


def service_card(s):
    return ('<a class="card" href="' + s["file"] + '">\n'
            '          <div class="card__icon">' + icon(s["icon"]) + '</div>\n'
            '          <h3>' + s["name"] + '</h3>\n'
            '          <p>' + s["short"] + '</p>\n'
            '          <span class="card__more">Mehr erfahren ' + ICON_ARROW + '</span>\n'
            '        </a>')


# ============================================================
# Leistungsseiten
# ============================================================
for s in SERVICES:
    others = [o for o in SERVICES if o["file"] != s["file"]][:3]
    offer_link = "kontakt.html?leistung=" + s["key"]

    extra = ""
    if s.get("extra_table"):
        head, rows = s["extra_table"]
        extra = """
  <section class="section section--tight" id="preise">
    <div class="container">
      <div class="section-head reveal">
        <h2>Richtpreise</h2>
        <p>Alle Preise inklusive Material, Anfahrt und Mehrwertsteuer. Massgebend ist immer die schriftliche Offerte.</p>
      </div>
      <div class="reveal">
        """ + table(head, rows) + """
      </div>
      <div class="btn-row mt-24 reveal">
        <a class="btn btn--grad" href=\"""" + offer_link + """\">Festpreis für meine Wohnung anfordern """ + ICON_ARROW + """</a>
      </div>
    </div>
  </section>"""

    calc_link = "preisrechner.html?leistung=" + s["key"]
    marken = [("ueberblick", "Überblick"), ("umfang", "Leistungsumfang")]
    if s.get("extra_table"):
        marken.append(("preise", "Preise"))
    marken += [("ablauf", "Ablauf"), ("garantien", "Garantien"), ("faq", "Fragen")]
    subnav = ('  <nav class="subnav" aria-label="Abschnitte dieser Seite">\n    <div class="container"><ul>\n'
              + "\n".join('      <li><a href="#%s">%s</a></li>' % m for m in marken)
              + '\n    </ul></div>\n  </nav>\n')

    body = (pagehead([(s["name"], s["file"])], s["name"], s["lead"], eyebrow="Leistung",
                     cta_href=offer_link, extra="\n      " + pills(s["pills"]),
                     second=(calc_link, "Richtpreis berechnen")) + "\n" + subnav + """

  <section class="section" id="ueberblick">
    <div class="container split split--wide-left">
      <div class="reveal">
        <h2>""" + s["intro_h2"] + """</h2>
        <p>""" + s["intro_p"] + """</p>
        """ + checklist(s["bullets"], "checklist mt-24") + """
      </div>
      <div class="media reveal"><img src=\"""" + ILLU[s["key"]][0] + """\" alt=\"""" + ILLU[s["key"]][1] + """\" width="800" height="600" loading="lazy"></div>
    </div>
  </section>

  <section class="section section--soft" id="umfang">
    <div class="container">
      <div class="section-head reveal">
        <span class="eyebrow">Leistungsumfang</span>
        <h2>Das ist bei der """ + s["name"] + """ enthalten</h2>
        <p>Der genaue Umfang wird in der Offerte festgehalten – zusätzliche Wünsche lassen sich jederzeit ergänzen.</p>
      </div>
      <div class="reveal">
        """ + table(s["table_head"], s["table_rows"]) + """
      </div>
      <p class="muted mt-24"><strong>Preis:</strong> """ + s["price"] + """</p>
    </div>
  </section>
""" + extra + """

  <section class="section" id="ablauf">
    <div class="container">
      <div class="section-head reveal">
        <span class="eyebrow">Ablauf</span>
        <h2>So läuft Ihr Auftrag ab</h2>
      </div>
      <ol class="steps reveal">
        <li>
          <h3>Anfrage und Besichtigung</h3>
          <p>Sie melden sich telefonisch oder über das Formular. Wir schauen uns das Objekt an oder beurteilen es anhand von Fotos.</p>
        </li>
        <li>
          <h3>Offerte mit Festpreis</h3>
          <p>Innert 24 Stunden erhalten Sie eine Offerte mit klarem Leistungsumfang und fixem Preis – unverbindlich.</p>
        </li>
        <li>
          <h3>Ausführung und Kontrolle</h3>
          <p>Das Team arbeitet nach dem vereinbarten Plan. Zum Schluss kontrollieren wir das Resultat und beheben offene Punkte sofort.</p>
        </li>
      </ol>
    </div>
  </section>

""" + GUARANTEES + """

  <section class="section" id="faq">
    <div class="container">
      <div class="section-head reveal">
        <span class="eyebrow">Häufige Fragen</span>
        <h2>Fragen zur """ + s["name"] + """</h2>
      </div>
      """ + faq(s["faqs"]) + """
    </div>
  </section>

  <section class="section section--soft">
    <div class="container">
      <div class="section-head reveal">
        <span class="eyebrow">Weitere Leistungen</span>
        <h2>Das könnte ebenfalls passen</h2>
      </div>
      <div class="grid grid--3 reveal">
        """ + "\n        ".join(service_card(o) for o in others) + """
      </div>
      <p class="mt-24"><a href="leistungen.html">Alle Leistungen im Überblick """ + ICON_ARROW + """</a></p>
    </div>
  </section>

""" + cta(href=offer_link))

    daten = ld(
        ld_breadcrumb([("Leistungen", "leistungen.html"), (s["name"], s["file"])]),
        ld_service(s["name"], s["lead"], s["file"]),
        ld_faq(s["faqs"]),
    )
    page(s["file"], s["title"], s["desc"], "leistungen.html", body, jsonld=daten)


# ============================================================
# Leistungsübersicht
# ============================================================
extras = [
    ("carpet", "Teppich- und Polsterreinigung", "Sprühextraktion für Teppiche, Sofas und Bürostühle – Flecken raus, Fasern geschont."),
    ("sparkle", "Grund- und Sonderreinigung", "Einmalige Tiefenreinigung nach Renovation, langer Abwesenheit oder vor besonderen Anlässen."),
    ("tools", "Hauswartung", "Kleine Reparaturen, Lampen- und Filterwechsel, Kontrollgänge und Mängelmeldung."),
    ("snow", "Winterdienst", "Schneeräumung und Splittstreuung mit Bereitschaft ab dem ersten Schneefall."),
]

body = (pagehead([("Leistungen", "leistungen.html")],
                 "Unsere Reinigungsleistungen im Überblick",
                 "Ob Privathaushalt, Büro, Baustelle oder Mehrfamilienhaus: Wir stellen ein Team zusammen, das zu Ihrem Objekt passt – mit klarem Leistungsumfang und fixem Preis.",
                 eyebrow="Leistungen") + """

  <section class="section">
    <div class="container">
      <div class="section-head reveal">
        <span class="eyebrow">Kernleistungen</span>
        <h2>Sechs Bereiche, die wir täglich ausführen</h2>
        <p>Jede Leistung hat ihre eigene Seite mit detailliertem Umfang, Richtpreisen und den häufigsten Fragen.</p>
      </div>
      <div class="grid grid--3 reveal">
        """ + "\n        ".join(service_card(s) for s in SERVICES) + """
      </div>
    </div>
  </section>

  <section class="section section--soft">
    <div class="container">
      <div class="section-head reveal">
        <span class="eyebrow">Zusatzleistungen</span>
        <h2>Ergänzend buchbar</h2>
        <p>Diese Arbeiten kombinieren wir auf Wunsch mit einem bestehenden Auftrag oder führen sie einmalig aus.</p>
      </div>
      <div class="grid grid--4 reveal">
        """ + "\n        ".join(
    '<div class="card"><div class="card__icon">' + icon(i) + '</div><h3>' + t + '</h3><p>' + d + '</p></div>'
    for i, t, d in extras) + """
      </div>
    </div>
  </section>

  <section class="section">
    <div class="container">
      <div class="section-head reveal">
        <span class="eyebrow">Preisorientierung</span>
        <h2>Was eine Reinigung ungefähr kostet</h2>
        <p>Erfahrungswerte inklusive Material, Anfahrt und Mehrwertsteuer. Verbindlich ist immer die schriftliche Offerte nach Besichtigung.</p>
      </div>
      <div class="reveal">
        """ + table(["Leistung", "Abrechnung", "Richtwert"], [
    ["Unterhaltsreinigung Privat", "pro Stunde", "CHF 45.– bis 55.–"],
    ["Büroreinigung", "monatliche Pauschale", "nach Fläche und Frequenz"],
    ["Fensterreinigung", "pro Fensterflügel", "ab CHF 6.– beidseitig inkl. Rahmen"],
    ["Umzugsreinigung", "Pauschale nach Zimmerzahl", "ab CHF 390.– (1,5 Zimmer)"],
    ["Bauendreinigung", "Pauschale pro Etappe", "nach Fläche und Zustand"],
    ["Liegenschaftsreinigung", "monatliche Pauschale", "nach Wohnungen und Turnus"],
]) + """
      </div>
      <div class="btn-row mt-40 reveal">
        <a class="btn btn--grad" href="preisrechner.html">Richtpreis berechnen """ + ICON_ARROW + """</a>
        <a class="btn btn--ghost" href="kontakt.html">Verbindliche Offerte anfordern</a>
        <span class="muted">Kostenlos, unverbindlich, Antwort innert 24 Stunden.</span>
      </div>
    </div>
  </section>

  <section class="section section--soft">
    <div class="container split">
      <div class="reveal">
        <span class="eyebrow">Immer inklusive</span>
        <h2>Was bei jedem Auftrag dazugehört</h2>
        <p>Unabhängig davon, welche Leistung Sie buchen: Diese Punkte sind bei uns nie eine Zusatzposition auf der Rechnung.</p>
      </div>
      <div class="reveal">
        """ + checklist([
    ("Material und Maschinen", "Reinigungsmittel, Geräte und Verbrauchsmaterial sind im Preis enthalten."),
    ("Anfahrt im Einsatzgebiet", "In der Region Luzern, im Rontal und im Kanton Zug verrechnen wir keine Anfahrt."),
    ("Versicherungsschutz", "Betriebshaftpflicht für Schäden am Objekt."),
    ("Schlusskontrolle", "Wir prüfen das Resultat und beheben offene Punkte sofort."),
]) + """
      </div>
    </div>
  </section>

""" + cta("Nicht sicher, welche Leistung Sie brauchen?",
          "Beschreiben Sie uns Ihre Situation – wir schlagen vor, was sinnvoll ist, und sagen auch, wenn weniger genügt."))

page("leistungen.html", "Leistungen – Privat, Gewerbe, Liegenschaften | Cleeno",
     "Alle Reinigungsleistungen von Cleeno Reinigungen in Perlen, Luzern und Zug: Unterhalts-, Büro-, Fenster-, Umzugs-, Bauend- und Liegenschaftsreinigung inklusive Richtpreisen.",
     "leistungen.html", body,
     jsonld=ld(ld_breadcrumb([("Leistungen", "leistungen.html")])))


# ============================================================
# Über uns
# ============================================================
usps = [
    ("users", "Familienbetrieb", "Geführt von der Inhaberfamilie – wer den Auftrag schreibt, ist auch bei Fragen erreichbar."),
    ("wallet", "Festpreis statt Schätzung", "Sie wissen vor dem ersten Einsatz, was es kostet. Fehlkalkulationen gehen zu unseren Lasten."),
    ("shield", "Abnahmegarantie", "Bei Umzugsreinigungen inklusive kostenloser Nachreinigung, falls etwas beanstandet wird."),
    ("heart", "Dieselben Leute", "Kein wechselndes Personal, keine Subunternehmer – Ihr Objekt wird von Bekannten gereinigt."),
    ("leaf", "Ökologisch dosiert", "Mikrofaser statt Chemie, wo es geht; zertifizierte Mittel, wo sie gleich gut wirken."),
    ("clock", "Kurze Wege", "Sitz in Perlen: Im Einsatzgebiet sind wir in der Regel in unter 30 Minuten vor Ort."),
]

body = (pagehead([("Über uns", "ueber-uns.html")],
                 "Ein Familienbetrieb, der seinen Namen auf jede Rechnung setzt",
                 "Cleeno Reinigungen ist ein Familienbetrieb mit Sitz in Perlen. Mehrjährige Erfahrung in der Gebäudereinigung, ein bewusst überschaubares Einsatzgebiet – und die Haltung, dass Reinigung Vertrauenssache ist.",
                 eyebrow="Über uns") + """

  <section class="section">
    <div class="container split split--wide-left">
      <div class="reveal">
        <h2>Klein genug, um jeden Auftrag selbst zu kennen</h2>
        <p>Cleeno Reinigungen wird als Familienbetrieb geführt und ist als Einzelfirma eingetragen. Das ist keine Randnotiz, sondern der Grund, warum bei uns vieles einfacher läuft: Es gibt keine Zwischenebene zwischen Ihnen und den Leuten, die reinigen.</p>
        <p>Wir haben uns bewusst gegen schnelles Wachstum entschieden. Lieber betreuen wir weniger Objekte richtig, als viele nur halb. Deshalb hört bei uns dieselbe Person zu, die später die Offerte schreibt – und die auch dann noch erreichbar ist, wenn einmal etwas nicht passt.</p>
        <p>Unser Einsatzgebiet reicht von Perlen aus über das Rontal in die Region Luzern und in den Kanton Zug. Kurze Wege bedeuten pünktliche Teams und kurzfristige Termine, wenn es einmal pressiert.</p>
      </div>
      <div class="media reveal">""" + icon("users", "1.2") + """</div>
    </div>
  </section>

  <section class="section section--soft">
    <div class="container">
      <div class="section-head section-head--center reveal">
        <span class="eyebrow">Was uns ausmacht</span>
        <h2>Sechs Gründe, warum Kundinnen und Kunden bleiben</h2>
        <p>Reinigung kann jeder anbieten. Der Unterschied liegt darin, was passiert, wenn der erste Einsatz vorbei ist.</p>
      </div>
      <div class="grid grid--3 reveal">
        """ + "\n        ".join(
    '<div class="card"><div class="card__icon">' + icon(i) + '</div><h3>' + t + '</h3><p>' + d + '</p></div>'
    for i, t, d in usps) + """
      </div>
    </div>
  </section>

  <section class="section">
    <div class="container split">
      <div class="reveal">
        <span class="eyebrow">Auf einen Blick</span>
        <h2>Cleeno in Kürze</h2>
        <p>Ein Betrieb, der bewusst in der Region bleibt: kurze Wege, schnelle Reaktionszeiten und Mitarbeitende, die hier wohnen.</p>
        """ + checklist([
    ("Familienbetrieb", "Geführt von der Inhaberfamilie, eingetragen als Einzelfirma."),
    ("Mehrjährige Erfahrung", "Praxis in Unterhalts-, Umzugs- und Bauendreinigung."),
    ("Sitz in Perlen", "Am Kanal 30, 6035 Perlen – im Rontal, zwischen Luzern und Zug."),
    ("Versichert", "Betriebshaftpflicht für Schäden am Objekt."),
]) + """
      </div>
      <div class="stats reveal">
        <div class="stat"><span class="stat__value">24 h</span><span class="stat__label">bis zur schriftlichen Offerte</span></div>
        <div class="stat"><span class="stat__value">0</span><span class="stat__label">Subunternehmer im Einsatz</span></div>
        <div class="stat"><span class="stat__value">3</span><span class="stat__label">Garantien in jeder Offerte</span></div>
        <div class="stat"><span class="stat__value">6</span><span class="stat__label">Leistungen aus einer Hand</span></div>
      </div>
    </div>
  </section>

  <!-- Platzhalter: Sobald Fotos vom Team und von Referenzobjekten vorliegen,
       gehört hier eine Bildstrecke hin (siehe README, Abschnitt «Bilder»). -->

  <section class="section section--tint">
    <div class="container split">
      <div class="reveal">
        <span class="eyebrow">Offene Stellen</span>
        <h2>Verstärkung willkommen</h2>
        <p>Wir suchen immer wieder Reinigungskräfte für Unterhalts- und Umzugsreinigungen in Teil- oder Vollzeit. Faire Anstellung, Einarbeitung durch das Team, geregelte Arbeitszeiten und Einsätze in der näheren Umgebung.</p>
        <div class="btn-row mt-24">
          <a class="btn btn--grad" href="mailto:jobs@cleeno-reinigungen.ch">Initiativbewerbung senden</a>
        </div>
      </div>
      <div class="media media--flat reveal">""" + icon("calendar", "1.2") + """</div>
    </div>
  </section>

""" + cta("Lernen wir uns kennen?",
          "Wir schauen uns Ihr Objekt an, hören zu und sagen ehrlich, was sinnvoll ist – auch wenn das weniger ist, als Sie erwartet haben."))

page("ueber-uns.html", "Über uns – Familienbetrieb aus Perlen | Cleeno",
     "Cleeno Reinigungen ist ein Familienbetrieb mit Sitz in Perlen: mehrjährige Erfahrung, feste Teams, Festpreis- und Abnahmegarantie. Lernen Sie den Betrieb kennen.",
     "ueber-uns.html", body,
     jsonld=ld(ld_breadcrumb([("Über uns", "ueber-uns.html")])))


# ============================================================
# Kontakt
# ============================================================
options = "\n            ".join(
    '<option value="' + s["key"] + '">' + s["name"] + '</option>' for s in SERVICES)

body = (pagehead([("Kontakt", "kontakt.html")],
                 "Kontakt und kostenlose Offerte",
                 "Schildern Sie uns kurz, worum es geht. Sie erhalten innert 24 Stunden eine schriftliche Offerte mit fixem Preis – unverbindlich, kostenlos und ohne Anzahlung.",
                 eyebrow="Kontakt", cta_href="#offerte-form", cta_label="Zum Formular") + """

  <section class="section">
    <div class="container split split--wide-left">

      <div class="reveal">
        <h2>Offerte anfordern</h2>
        <p>Je mehr wir über das Objekt wissen, desto genauer wird die Offerte. Fotos können Sie uns anschliessend per E-Mail nachreichen.</p>

        <div class="form__status" id="form-status" hidden role="status" aria-live="polite"></div>

        <form class="form mt-24" id="offerte-form" novalidate>
          <div class="hp" aria-hidden="true">
            <label>Bitte leer lassen <input type="text" name="website" tabindex="-1" autocomplete="off"></label>
          </div>

          <div class="form__row form__row--2">
            <div class="field">
              <label for="name">Name <span class="req" aria-hidden="true">*</span></label>
              <input type="text" id="name" name="name" autocomplete="name" required>
              <span class="error-msg" data-error-for="name"></span>
            </div>
            <div class="field">
              <label for="firma">Firma <span class="hint">(optional)</span></label>
              <input type="text" id="firma" name="firma" autocomplete="organization">
            </div>
          </div>

          <div class="form__row form__row--2">
            <div class="field">
              <label for="email">E-Mail <span class="req" aria-hidden="true">*</span></label>
              <input type="email" id="email" name="email" autocomplete="email" required>
              <span class="error-msg" data-error-for="email"></span>
            </div>
            <div class="field">
              <label for="telefon">Telefon <span class="req" aria-hidden="true">*</span></label>
              <input type="tel" id="telefon" name="telefon" autocomplete="tel" required>
              <span class="error-msg" data-error-for="telefon"></span>
            </div>
          </div>

          <div class="form__row form__row--2">
            <div class="field">
              <label for="leistung">Gewünschte Leistung <span class="req" aria-hidden="true">*</span></label>
              <select id="leistung" name="leistung" required>
                <option value="">Bitte wählen</option>
                """ + options + """
                <option value="andere">Etwas anderes</option>
              </select>
              <span class="error-msg" data-error-for="leistung"></span>
            </div>
            <div class="field">
              <label for="objekt">Objekt und Fläche</label>
              <input type="text" id="objekt" name="objekt" placeholder="z. B. 3,5-Zimmer-Wohnung, 84 m²">
            </div>
          </div>

          <div class="field">
            <label for="termin">Wunschtermin oder Zeitraum</label>
            <input type="text" id="termin" name="termin" placeholder="z. B. ab Mitte Oktober, jeweils freitags">
          </div>

          <div class="field">
            <label for="nachricht">Ihre Nachricht <span class="req" aria-hidden="true">*</span></label>
            <textarea id="nachricht" name="nachricht" required placeholder="Was sollen wir für Sie reinigen? Gibt es Besonderheiten wie Haustiere, Zugang oder feste Zeitfenster?"></textarea>
            <span class="error-msg" data-error-for="nachricht"></span>
          </div>

          <div class="field">
            <label class="check">
              <input type="checkbox" name="datenschutz" id="datenschutz" required>
              <span>Ich bin damit einverstanden, dass meine Angaben zur Bearbeitung meiner Anfrage verwendet werden. Details in der <a href="datenschutz.html">Datenschutzerklärung</a>. <span class="req" aria-hidden="true">*</span></span>
            </label>
            <span class="error-msg" data-error-for="datenschutz"></span>
          </div>

          <div class="btn-row">
            <button class="btn btn--grad" type="submit">Offerte anfordern</button>
          </div>
          <p class="muted" style="font-size:.9rem">Felder mit <span class="req">*</span> sind erforderlich. Wir melden uns innert 24 Stunden an Werktagen.</p>
        </form>
      </div>

      <div class="reveal">
        <div class="contact-panel">
          <h2>Direkter Draht</h2>
          <ul class="contact-list">
            <li>""" + icon("phone") + """<div><strong>Telefon</strong><a href="tel:""" + TEL + """\">""" + PHONE + """</a></div></li>
            <li>""" + icon("mail") + """<div><strong>E-Mail</strong><a href="mailto:offerte@cleeno-reinigungen.ch">offerte@cleeno-reinigungen.ch</a></div></li>
            <li>""" + icon("pin") + """<div><strong>Adresse</strong>Cleeno Reinigungen<br>Am Kanal 30<br>6035 Perlen</div></li>
            <li>""" + icon("clock") + """<div><strong>Erreichbarkeit</strong>Mo–Fr 07:00–18:00 Uhr<br>Sa 08:00–12:00 Uhr<br>Einsätze auch ausserhalb dieser Zeiten</div></li>
          </ul>
        </div>

        <div class="contact-panel mt-24">
          <h2>Einsatzgebiet</h2>
          <p class="mb-0">Rontal, Region Luzern und Kanton Zug: unter anderem Perlen, Root, Ebikon, Buchrain, Dierikon, Gisikon, Inwil, Emmen, Luzern, Kriens, Horw, Rotkreuz, Cham, Baar, Zug, Hochdorf und Sursee. Ausserhalb dieses Gebiets fragen Sie bitte kurz an.</p>
        </div>
      </div>

    </div>
  </section>

  <section class="section section--soft">
    <div class="container">
      <div class="section-head reveal">
        <span class="eyebrow">Vor der Anfrage</span>
        <h2>Häufige Fragen zur Offerte</h2>
      </div>
      """ + faq(FAQ_KONTAKT := [
    ("Kostet die Offerte etwas?",
     "Nein. Anfrage, Besichtigung und Offerte sind kostenlos und unverbindlich – auch wenn Sie sich danach für einen anderen Anbieter entscheiden."),
    ("Wie schnell erhalte ich eine Antwort?",
     "An Werktagen innert 24 Stunden. Für dringende Fälle – etwa eine kurzfristige Wohnungsabgabe – rufen Sie am besten direkt an."),
    ("Ist eine Besichtigung nötig?",
     "Bei kleineren Aufträgen genügen ein paar Fotos und Angaben zur Fläche. Für Büros, Liegenschaften und Baustellen schauen wir das Objekt vorher an."),
    ("Was passiert mit meinen Angaben?",
     "Wir verwenden sie ausschliesslich zur Bearbeitung Ihrer Anfrage und geben sie nicht weiter. Details stehen in der Datenschutzerklärung."),
]) + """
    </div>
  </section>
""")

page("kontakt.html", "Kontakt und kostenlose Offerte | Cleeno Reinigungen",
     "Kontaktieren Sie Cleeno Reinigungen in Perlen: Telefon " + PHONE + " oder Offertformular. Antwort innert 24 Stunden, Besichtigung und Offerte kostenlos.",
     "kontakt.html", body,
     jsonld=ld(ld_breadcrumb([("Kontakt", "kontakt.html")]), ld_faq(FAQ_KONTAKT)))


# ============================================================
# Impressum
# ============================================================
body = (pagehead([("Impressum", "impressum.html")], "Impressum",
                 "Angaben zum Betreiber dieser Website gemäss den geltenden Bestimmungen.", cta_href=None) + """

  <section class="section">
    <div class="container prose">
      <h2 class="mt-0">Verantwortlich für den Inhalt</h2>
      <p>
        Cleeno Reinigungen<br>
        Am Kanal 30<br>
        6035 Perlen<br>
        Schweiz
      </p>
      <p>
        Telefon: <a href="tel:""" + TEL + """\">""" + PHONE + """</a><br>
        E-Mail: <a href="mailto:info@cleeno-reinigungen.ch">info@cleeno-reinigungen.ch</a>
      </p>

      <h2>Rechtsform und Mehrwertsteuer</h2>
      <p>
        Rechtsform: Einzelfirma<br>
        Inhaber: [Vor- und Nachname eintragen]<br>
        UID / MWST-Nummer: [CHE-000.000.000 eintragen]
      </p>

      <h2>Haftungsausschluss</h2>
      <p>Die Inhalte dieser Website werden mit grösstmöglicher Sorgfalt erstellt. Für Richtigkeit, Vollständigkeit und Aktualität der Inhalte kann jedoch keine Gewähr übernommen werden. Preisangaben sind Richtwerte; verbindlich ist ausschliesslich die schriftliche Offerte.</p>
      <p>Haftungsansprüche wegen Schäden materieller oder immaterieller Art, die aus dem Zugriff auf die veröffentlichten Informationen beziehungsweise durch deren Nutzung entstehen, sind ausgeschlossen, soweit kein nachweislich vorsätzliches oder grobfahrlässiges Verschulden vorliegt.</p>

      <h2>Verweise auf Websites Dritter</h2>
      <p>Verweise auf Websites Dritter liegen ausserhalb unseres Verantwortungsbereichs. Für deren Inhalte wird jede Verantwortung abgelehnt. Der Zugriff und die Nutzung solcher Websites erfolgen auf eigene Gefahr.</p>

      <h2>Urheberrecht</h2>
      <p>Die Urheber- und alle anderen Rechte an Inhalten, Bildern und Dateien auf dieser Website gehören ausschliesslich Cleeno Reinigungen oder den namentlich genannten Rechteinhabern. Für die Reproduktion von Elementen ist die schriftliche Zustimmung der Rechteinhaber im Voraus einzuholen.</p>

      <h2>Anwendbares Recht und Gerichtsstand</h2>
      <p>Es gilt ausschliesslich schweizerisches Recht. Gerichtsstand ist Luzern, soweit nicht zwingende gesetzliche Bestimmungen etwas anderes vorsehen.</p>

      <p class="muted mt-40">Hinweis für die Redaktion: Firmenname, Rechtsform und Adresse sind eingetragen. Noch zu ergänzen sind der Name des Inhabers, die UID- beziehungsweise MWST-Nummer sowie die definitive Telefonnummer und E-Mail-Adresse. Eine Einzelfirma muss im Firmennamen den Familiennamen des Inhabers führen – die vollständige Firmenbezeichnung gehört deshalb ins Impressum, auch wenn nach aussen die Marke «Cleeno Reinigungen» auftritt.</p>
    </div>
  </section>
""")

page("impressum.html", "Impressum | Cleeno Reinigungen",
     "Impressum von Cleeno Reinigungen, Am Kanal 30, 6035 Perlen: Kontaktangaben, Rechtsform, Haftungsausschluss und Urheberrecht.",
     None, body,
     jsonld=ld(ld_breadcrumb([("Impressum", "impressum.html")])))


# ============================================================
# Datenschutz
# ============================================================
body = (pagehead([("Datenschutz", "datenschutz.html")], "Datenschutzerklärung",
                 "Wie wir mit Ihren Daten umgehen – im Sinne des Schweizer Datenschutzgesetzes (DSG).", cta_href=None) + """

  <section class="section">
    <div class="container prose">
      <h2 class="mt-0">1. Verantwortliche Stelle</h2>
      <p>
        Cleeno Reinigungen, Am Kanal 30, 6035 Perlen<br>
        E-Mail: <a href="mailto:datenschutz@cleeno-reinigungen.ch">datenschutz@cleeno-reinigungen.ch</a><br>
        Telefon: <a href="tel:""" + TEL + """\">""" + PHONE + """</a>
      </p>
      <p>Wir bearbeiten Personendaten im Einklang mit dem Schweizer Bundesgesetz über den Datenschutz (DSG) sowie – soweit anwendbar – der Datenschutz-Grundverordnung der EU (DSGVO).</p>

      <h2>2. Bearbeitung beim Besuch der Website</h2>
      <p>Beim Aufruf dieser Website werden durch den Hosting-Anbieter automatisch Server-Logdaten erfasst. Dazu gehören in der Regel:</p>
      <ul>
        <li>gekürzte IP-Adresse des zugreifenden Geräts</li>
        <li>Datum und Uhrzeit des Zugriffs</li>
        <li>aufgerufene Seite und übertragene Datenmenge</li>
        <li>Browsertyp, Version und Betriebssystem</li>
      </ul>
      <p>Diese Daten dienen ausschliesslich dem sicheren und stabilen Betrieb der Website sowie der Fehleranalyse. Eine Zusammenführung mit anderen Datenquellen findet nicht statt. Die Logdaten werden nach spätestens 90 Tagen gelöscht.</p>

      <h2>3. Kontakt- und Offertformular</h2>
      <p>Wenn Sie uns über das Formular oder per E-Mail kontaktieren, bearbeiten wir die von Ihnen angegebenen Daten (Name, Firma, E-Mail-Adresse, Telefonnummer, Angaben zum Objekt und Ihre Nachricht) zur Beantwortung Ihrer Anfrage und zur Erstellung einer Offerte.</p>
      <p>Rechtsgrundlage ist die Anbahnung beziehungsweise Erfüllung eines Vertrags sowie unser berechtigtes Interesse an der Beantwortung von Anfragen. Kommt kein Auftrag zustande, löschen wir die Anfragedaten nach zwölf Monaten. Bei einem Vertragsabschluss gelten die gesetzlichen Aufbewahrungsfristen von zehn Jahren.</p>

      <h2>4. Cookies, Schriften und Analyse</h2>
      <p>Diese Website verwendet keine Tracking-Cookies und bindet keine Analyse- oder Werbedienste von Drittanbietern ein. Auch die Schriften werden von unserem eigenen Server geladen – es entsteht also keine Verbindung zu externen Anbietern. Verarbeitet werden ausschliesslich technisch notwendige Daten.</p>
      <p class="muted">Sollten später Dienste wie Google Analytics, Google Maps oder ein Bewertungs-Widget eingebunden werden, muss dieser Abschnitt entsprechend ergänzt werden.</p>

      <h2>5. Weitergabe von Daten</h2>
      <p>Ihre Daten werden nicht verkauft. Eine Weitergabe erfolgt nur, soweit dies zur Vertragserfüllung notwendig ist (etwa an das Treuhandbüro für die Rechnungsstellung oder an den Hosting-Anbieter als Auftragsbearbeiter) oder wir gesetzlich dazu verpflichtet sind. Alle Auftragsbearbeiter sind vertraglich zur Vertraulichkeit verpflichtet.</p>

      <h2>6. Datensicherheit</h2>
      <p>Die Website wird über eine verschlüsselte TLS-Verbindung (HTTPS) ausgeliefert. Wir treffen angemessene technische und organisatorische Massnahmen, um Ihre Daten gegen Verlust, Missbrauch und unberechtigten Zugriff zu schützen.</p>

      <h2>7. Ihre Rechte</h2>
      <p>Sie haben im Rahmen der gesetzlichen Bestimmungen das Recht auf Auskunft über die zu Ihrer Person bearbeiteten Daten sowie auf Berichtigung, Löschung oder Herausgabe. Zudem können Sie der Bearbeitung widersprechen. Eine kurze E-Mail an die oben genannte Adresse genügt; zur Identifikation können wir einen Nachweis verlangen.</p>
      <p>Sie haben ausserdem das Recht, sich beim Eidgenössischen Datenschutz- und Öffentlichkeitsbeauftragten (EDÖB) zu beschweren.</p>

      <h2>8. Änderungen</h2>
      <p>Wir können diese Datenschutzerklärung jederzeit anpassen. Massgebend ist die jeweils auf dieser Seite veröffentlichte Fassung.</p>

      <p class="muted mt-40">Hinweis für die Redaktion: Dieser Text ist eine Vorlage und ersetzt keine Rechtsberatung. Er muss an die tatsächlich eingesetzten Dienste (Hosting, Formularversand, Karten) angepasst und vor der Veröffentlichung geprüft werden.</p>
    </div>
  </section>
""")

page("datenschutz.html", "Datenschutzerklärung | Cleeno Reinigungen",
     "Datenschutzerklärung von Cleeno Reinigungen: Welche Daten beim Besuch der Website und bei Offertanfragen bearbeitet werden und welche Rechte Sie haben.",
     None, body,
     jsonld=ld(ld_breadcrumb([("Datenschutz", "datenschutz.html")])))


# ============================================================
# 404
# ============================================================
body = """  <section class="pagehead">
    <div class="container">
      <span class="eyebrow">Fehler 404</span>
      <h1>Diese Seite konnten wir nicht finden</h1>
      <p>Möglicherweise wurde die Seite verschoben oder der Link enthält einen Tippfehler. Hier geht es weiter:</p>
      <div class="btn-row mt-24">
        <a class="btn btn--grad" href="index.html">Zur Startseite """ + ICON_ARROW + """</a>
        <a class="btn btn--ghost" href="kontakt.html">Kontakt aufnehmen</a>
      </div>
    </div>
  </section>

  <section class="section">
    <div class="container">
      <div class="section-head reveal">
        <h2>Unsere Leistungen</h2>
      </div>
      <div class="grid grid--3 reveal">
        """ + "\n        ".join(service_card(s) for s in SERVICES) + """
      </div>
    </div>
  </section>
"""

page("404.html", "Seite nicht gefunden | Cleeno Reinigungen",
     "Die aufgerufene Seite existiert nicht. Hier finden Sie zurück zur Startseite und zu unseren Reinigungsleistungen.",
     None, body, noindex=True)

print("fertig")


# ============================================================
# Preisrechner
# ============================================================
choices = "\n          ".join(
    '<label class="choice"><input type="radio" name="leistung" value="' + s["key"] + '"'
    + (' checked' if s["key"] == "umzugsreinigung" else '') + '><span>' + icon(s["icon"])
    + '<span>' + s["name"] + '</span></span></label>'
    for s in SERVICES)

body = (pagehead([("Preisrechner", "preisrechner.html")],
                 "Was kostet die Reinigung? Rechnen Sie es aus.",
                 "Drei Angaben genügen für einen realistischen Richtpreis – ohne Adresse, ohne Anmeldung, ohne Anruf. Wenn der Rahmen passt, machen wir daraus auf Knopfdruck eine verbindliche Offerte.",
                 eyebrow="Preisrechner", cta_href=None) + """

  <section class="section">
    <div class="container">
      <noscript>
        <p class="form__status form__status--err">Der Preisrechner braucht JavaScript. Richtpreise finden Sie auch auf der Seite
        <a href="leistungen.html">Leistungen</a> – oder fordern Sie direkt eine <a href="kontakt.html">kostenlose Offerte</a> an.</p>
      </noscript>

      <div class="calc">
        <form class="calc__panel" id="calc" novalidate>
          <ol class="calc__steps">
            <li aria-current="step">Leistung</li>
            <li>Objekt</li>
            <li>Extras</li>
          </ol>

          <fieldset class="calc__step">
            <legend>Was sollen wir reinigen?</legend>
            <p class="calc__hint">Wählen Sie die Leistung, die am ehesten passt – Kombinationen klären wir in der Offerte.</p>
            <div class="choices">
              """ + choices + """
            </div>
          </fieldset>

          <fieldset class="calc__step" hidden>
            <legend>Angaben zum Objekt</legend>
            <p class="calc__hint">Je genauer die Angaben, desto näher liegt der Richtwert am späteren Festpreis.</p>
            <div id="calc-details"></div>
          </fieldset>

          <fieldset class="calc__step" hidden>
            <legend>Zusätzliche Wünsche</legend>
            <p class="calc__hint">Alles freiwillig. Was Sie hier weglassen, lässt sich später jederzeit ergänzen.</p>
            <div id="calc-extras"></div>
          </fieldset>

          <div class="calc__nav">
            <button type="button" class="btn btn--ghost" id="calc-back" hidden>Zurück</button>
            <button type="button" class="btn btn--grad" id="calc-next">Weiter """ + ICON_ARROW + """</button>
            <a class="btn btn--grad" id="calc-finish" href="kontakt.html" hidden>Offerte anfordern """ + ICON_ARROW + """</a>
          </div>
        </form>

        <aside class="calc__result" aria-live="polite">
          <h2 class="calc__title">Ihr Richtpreis</h2>
          <p class="calc__price" id="calc-price"><small>Richtpreis</small>CHF –</p>
          <p class="calc__unit" id="calc-unit"></p>
          <ul class="calc__list" id="calc-list"></ul>
          <p class="calc__note" id="calc-note"></p>
          <a class="btn btn--light btn--block" id="calc-cta" href="kontakt.html">Daraus eine Offerte machen</a>
        </aside>
      </div>
    </div>
  </section>

  <section class="section section--soft">
    <div class="container">
      <div class="section-head reveal">
        <span class="eyebrow">Transparenz</span>
        <h2>Wie dieser Preis zustande kommt</h2>
        <p>Wir legen offen, womit wir rechnen. So sehen Sie, ob eine Offerte fair ist – auch die von anderen Anbietern.</p>
      </div>
      """ + faq(FAQ_RECHNER := [
    ("Wie verbindlich ist der Richtpreis?",
     "Er ist eine Schätzung auf Basis von Erfahrungswerten und ersetzt keine Offerte. In den allermeisten Fällen liegt der spätere Festpreis innerhalb der angezeigten Spanne. Weicht er ab, sagen wir das vor dem Start – nicht auf der Rechnung."),
    ("Warum eine Spanne statt eines fixen Betrags?",
     "Zwei gleich grosse Wohnungen können unterschiedlich viel Aufwand bedeuten: Zustand, Bodenbeläge, Kalk, Erreichbarkeit. Die Spanne bildet diesen Unterschied ehrlich ab, statt eine Genauigkeit vorzutäuschen, die es vor der Besichtigung nicht gibt."),
    ("Was ist im Preis enthalten?",
     "Arbeitszeit, Reinigungsmittel, Maschinen und die Anfahrt im Einsatzgebiet. Bei Umzugsreinigungen zusätzlich Fenster, Storen und die Abnahmegarantie. Nicht enthalten sind Entsorgungskosten für Mulden und Sondermüll."),
    ("Verrechnen Sie Zuschläge?",
     "Für Einsätze am Samstag, an Sonn- und Feiertagen sowie nach 20 Uhr. Diese Zuschläge weisen wir in der Offerte separat aus – sie tauchen nie überraschend auf der Rechnung auf."),
    ("Was passiert nach dem Absenden?",
     "Sie erhalten innert 24 Stunden an Werktagen eine schriftliche Offerte mit fixem Preis. Bei grösseren Objekten schauen wir vorher kurz vorbei – kostenlos und unverbindlich."),
]) + """
    </div>
  </section>

""" + cta("Aus dem Richtpreis eine verbindliche Offerte machen",
          "Sie erhalten den Festpreis schriftlich – mit Leistungsumfang, Terminvorschlag und allen drei Garantien."))

page("preisrechner.html",
     "Preisrechner – Richtpreis in 30 Sekunden | Cleeno",
     "Richtpreis für Umzugs-, Unterhalts-, Büro-, Fenster- oder Bauendreinigung in Luzern und Zug berechnen – kostenlos, ohne Anmeldung, in 30 Sekunden.",
     "preisrechner.html", body,
     scripts='<script src="js/preisrechner.js" defer></script>\n',
     jsonld=ld(ld_breadcrumb([("Preisrechner", "preisrechner.html")]), ld_faq(FAQ_RECHNER)))


# ============================================================
# Ratgeber
# ============================================================
def toc_nav(items):
    return ('  <nav class="subnav" aria-label="Abschnitte dieses Beitrags">\n    <div class="container"><ul>\n'
            + "\n".join('      <li><a href="#%s">%s</a></li>' % it for it in items)
            + '\n    </ul></div>\n  </nav>\n')


RATGEBER = [
    dict(
        file="ratgeber-wohnungsabgabe.html", icon="doc",
        title="Wohnungsabgabe: Checkliste für die Übergabe | Cleeno",
        h1="Wohnungsabgabe ohne Abzüge: die Checkliste",
        desc="Checkliste für die Wohnungsübergabe in der Schweiz: Zeitplan, Kontrollpunkte Raum für Raum, häufige Beanstandungen und was als normale Abnützung gilt.",
        lead="Bei der Wohnungsabgabe entscheidet sich, ob Sie Ihr Depot vollständig zurückerhalten. Diese Checkliste geht Raum für Raum durch, was Verwaltungen tatsächlich prüfen – und was Sie getrost ignorieren können.",
        teaser="Zeitplan, Kontrollpunkte Raum für Raum und die zehn Stellen, an denen es bei der Übergabe am häufigsten hängt.",
        toc=[("zeitplan", "Zeitplan"), ("checkliste", "Checkliste"),
             ("pruefpunkte", "Häufige Beanstandungen"), ("abnuetzung", "Normale Abnützung"),
             ("selber", "Selber oder Firma?")],
        body="""
      <p>Die meisten Beanstandungen bei der Wohnungsabgabe entstehen nicht aus Nachlässigkeit, sondern aus einem Missverständnis: Mietende reinigen so, wie sie es zu Hause tun. Verwaltungen prüfen dagegen nach einer Liste – und die enthält Stellen, an die im Alltag niemand denkt. Wer diese Liste kennt, ist im Vorteil.</p>

      <h2 id="zeitplan">Der Zeitplan: was wann passieren muss</h2>
      <p>Die häufigste Ursache für Stress ist ein zu spät gebuchter Termin. Reinigungsfirmen sind Ende Monat und besonders per Ende März, Juni und September ausgebucht.</p>
      """ + table(["Zeitpunkt", "Was zu tun ist"], [
            ["4 Wochen vorher", "Abgabetermin schriftlich bestätigen lassen, Offerten für die Endreinigung einholen, Termin fix buchen"],
            ["2 Wochen vorher", "Kleinreparaturen klären: Storenband, Duschschlauch, Backblech, Lampenfassungen, fehlende Schlüssel nachbestellen"],
            ["1 Woche vorher", "Umzug abschliessen, Keller, Estrich, Garage und Briefkasten leeren, Möbel entsorgen"],
            ["1–2 Tage vorher", "Endreinigung – die Wohnung muss dafür vollständig leer sein"],
            ["Am Abgabetag", "Zählerstände notieren, alle Schlüssel zählen, Protokoll gemeinsam ausfüllen und unterschreiben"],
        ]) + """

      <h2 id="checkliste">Checkliste Raum für Raum</h2>
      <p>Diese Liste können Sie ausdrucken und abhaken. Sie deckt den Umfang ab, den eine übliche Abgabe verlangt.</p>
      <div class="btn-row mt-24">
        <a class="btn btn--grad" href="checkliste.html">Checkliste zum Abhaken öffnen """ + ICON_ARROW + """</a>
        <span class="muted">47 Punkte, Fortschritt wird gespeichert, druckbar.</span>
      </div>

      <h3>Küche</h3>
      """ + checklist([
            "Backofen, Backblech und Roste fettfrei – auch die Scheibe innen",
            "Dampfabzug samt Fettfilter gereinigt oder Filter ersetzt",
            "Kühlschrank abgetaut, Dichtungen und Gemüsefach gereinigt",
            "Schränke innen und aussen, auch die Oberkanten",
            "Spüle, Armatur und Siphon entkalkt",
            "Steamer, Geschirrspüler und Sieb entkalkt",
        ], "checklist checklist--2") + """

      <h3>Bad und WC</h3>
      """ + checklist([
            "Duschtrennwand und Plättli kalkfrei",
            "WC innen, unter dem Rand und hinter dem Spülkasten",
            "Armaturen, Brausekopf und Ablaufsieb entkalkt",
            "Silikonfugen ohne Schimmel",
            "Spiegelschrank innen, Ablagen und Lüftungsgitter",
            "Boden inklusive Ecken und Sockelleisten",
        ], "checklist checklist--2") + """

      <h3>Wohnräume, Fenster und Nebenräume</h3>
      """ + checklist([
            "Böden gereinigt, Parkett nicht nass, sondern nebelfeucht",
            "Fenster innen und aussen, Rahmen und Falze",
            "Storen, Rollläden und Führungsschienen",
            "Türen, Türrahmen, Lichtschalter und Steckdosen",
            "Heizkörper inklusive Zwischenräume, Radiatorennischen",
            "Keller, Estrich, Balkon, Waschküchenanteil und Flusensieb",
        ], "checklist checklist--2") + """

      <h2 id="pruefpunkte">Die zehn Punkte, an denen es am häufigsten hängt</h2>
      <ol>
        <li>Backofenscheibe innen – wird beim Putzen fast immer vergessen</li>
        <li>Fettfilter des Dampfabzugs</li>
        <li>Kalkränder an der Duschtrennwand</li>
        <li>Fensterfalze mit Schmutzwasser vom letzten Regen</li>
        <li>Storenlamellen und deren Führungsschienen</li>
        <li>Silikonfugen in Dusche und Küche</li>
        <li>Flusensieb der Waschmaschine und Trocknerfilter</li>
        <li>Rollladen- und Lüftungsgitter</li>
        <li>Sockelleisten und Türrahmen-Oberkanten</li>
        <li>Keller und Estrich – oft schlicht vergessen</li>
      </ol>

      <h2 id="abnuetzung">Was normale Abnützung ist – und was nicht</h2>
      <p>Nicht alles, was nach Gebrauch aussieht, geht zu Ihren Lasten. Gewöhnliche Abnützung durch vertragsgemässen Gebrauch muss die Vermieterschaft tragen: verblasste Farbe, kleine Kratzer im Parkett, altersbedingt matte Oberflächen.</p>
      <p>Für Schäden, die darüber hinausgehen, gilt in der Schweiz die Lebensdauertabelle des Mieterverbands: Ist ein Bauteil am Ende seiner Lebensdauer angelangt, zahlen Sie auch bei einem Schaden nichts mehr. Ein zwölfjähriger Teppich zum Beispiel ist in der Regel abgeschrieben.</p>
      <p><strong>Wichtig:</strong> Reinigung fällt nie unter Abnützung. Eine ungenügend gereinigte Wohnung dürfen Verwaltungen immer beanstanden – unabhängig vom Alter der Einrichtung.</p>

      <h2 id="selber">Selber reinigen oder eine Firma beauftragen?</h2>
      <p>Beides ist legitim. Der Entscheid hängt vor allem davon ab, wie viel Zeit Sie neben dem Umzug haben und wie hoch Ihr Risiko ist, ein zweites Mal anreisen zu müssen.</p>
      """ + table(["", "Selber reinigen", "Firma mit Abnahmegarantie"], [
            ["Zeitaufwand", "10 bis 20 Stunden für eine 3,5-Zimmer-Wohnung", "Kein eigener Aufwand"],
            ["Materialkosten", "CHF 60 bis 120 für Entkalker, Reiniger, Zubehör", "im Preis enthalten"],
            ["Risiko", "Nachreinigung auf eigene Kosten, zweiter Termin", "Nachreinigung ist Teil des Auftrags"],
            ["Sinnvoll wenn", "kleine Wohnung, viel Zeit, guter Zustand", "Termindruck, grosse Wohnung, harte Verwaltung"],
        ]) + """
      <p class="mt-24">Wenn Sie sich für eine Firma entscheiden: Achten Sie darauf, dass Fenster, Storen und eine Abnahmegarantie ausdrücklich in der Offerte stehen. Genau daran scheitern günstige Angebote am häufigsten.</p>
""",
    ),

    dict(
        file="ratgeber-umzugsreinigung-kosten.html", icon="wallet",
        title="Was kostet eine Umzugsreinigung? | Cleeno",
        h1="Was kostet eine Umzugsreinigung in der Schweiz?",
        desc="Preise für die Umzugsreinigung nach Wohnungsgrösse, die wichtigsten Preisfaktoren, was in eine seriöse Offerte gehört und woran Sie zu günstige Angebote erkennen.",
        lead="Zwischen der günstigsten und der teuersten Offerte für dieselbe Wohnung liegen schnell 60 Prozent. Dieser Beitrag erklärt, woher der Unterschied kommt und wie Sie Angebote wirklich vergleichen.",
        teaser="Preisspannen nach Wohnungsgrösse, die entscheidenden Kostenfaktoren und fünf Warnsignale bei zu günstigen Offerten.",
        toc=[("preise", "Preisspannen"), ("faktoren", "Preisfaktoren"),
             ("offerte", "Seriöse Offerte"), ("warnsignale", "Warnsignale"), ("sparen", "Sinnvoll sparen")],
        body="""
      <p>Die Umzugsreinigung ist für viele der grösste einzelne Posten beim Wohnungswechsel. Anders als beim Umzug selbst lässt sich der Preis aber gut einschätzen – wenn man weiss, welche Faktoren dahinterstehen.</p>

      <h2 id="preise">Was eine Umzugsreinigung kostet</h2>
      <p>Die folgenden Spannen entsprechen dem, was in der Zentralschweiz üblich ist – inklusive Fenster, Storen und Abnahmegarantie. Wohnungen in sehr gutem Zustand liegen am unteren Rand, stark verkalkte oder verrauchte Wohnungen darüber.</p>
      """ + table(["Wohnungsgrösse", "Übliche Spanne", "Dauer"], [
            ["1,5 Zimmer", "CHF 390 – 550", "4 bis 6 Stunden"],
            ["2,5 Zimmer", "CHF 490 – 700", "6 bis 8 Stunden"],
            ["3,5 Zimmer", "CHF 690 – 950", "8 bis 11 Stunden"],
            ["4,5 Zimmer", "CHF 890 – 1200", "10 bis 14 Stunden"],
            ["5,5 Zimmer und mehr", "ab CHF 1100", "nach Besichtigung"],
        ]) + """
      <p class="muted mt-24">Die Stundenangaben beziehen sich auf die gesamte Arbeitszeit; ein Zweierteam ist entsprechend schneller fertig.</p>

      <h2 id="faktoren">Was den Preis wirklich beeinflusst</h2>
      <ul>
        <li><strong>Zustand:</strong> Kalk, Fett und Nikotin sind die grössten Kostentreiber – hier geht Zeit weg, nicht Material.</li>
        <li><strong>Anzahl Fenster und Storen:</strong> Eine Wohnung mit zwölf Fenstern kostet spürbar mehr als eine mit sechs, bei gleicher Fläche.</li>
        <li><strong>Bodenbeläge:</strong> Parkett und Naturstein brauchen andere Mittel und mehr Sorgfalt als Plättli.</li>
        <li><strong>Nebenräume:</strong> Keller, Estrich, Balkon, Garage und Waschküchenanteil werden oft vergessen und dann nachverrechnet.</li>
        <li><strong>Termin:</strong> Ende Monat und per Quartalsende ist die Nachfrage am höchsten. Wer zwei Wochen früher bucht, hat mehr Auswahl.</li>
        <li><strong>Zugang:</strong> Fehlender Lift oder enge Treppenhäuser kosten Zeit beim Materialtransport.</li>
      </ul>

      <h2 id="offerte">Was in einer seriösen Offerte steht</h2>
      """ + checklist([
            ("Fixer Preis statt Stundenschätzung", "Sonst tragen Sie das Risiko einer Fehleinschätzung."),
            ("Vollständiger Leistungsumfang", "Fenster, Rahmen, Storen, Nebenräume und Geräte einzeln aufgeführt."),
            ("Abnahmegarantie mit Frist", "Wie lange gilt sie, und was ist ausgeschlossen?"),
            ("Firmenangaben", "Adresse, UID- oder MWST-Nummer, Haftpflichtversicherung."),
            ("Termin und Dauer", "Wann wird gereinigt, wie viele Personen kommen?"),
        ]) + """

      <h2 id="warnsignale">Fünf Warnsignale bei zu günstigen Angeboten</h2>
      <ol>
        <li><strong>Pauschalpreis ohne Rückfragen.</strong> Wer nicht nach Zustand, Fensterzahl und Nebenräumen fragt, kann nicht kalkulieren – die Nachverrechnung ist einprogrammiert.</li>
        <li><strong>Keine Abnahmegarantie.</strong> Oder eine, die nur wenige Stunden gilt.</li>
        <li><strong>Fenster und Storen als Zusatzposition.</strong> Das ist der häufigste Trick, um eine Offerte optisch günstig zu halten.</li>
        <li><strong>Keine UID-Nummer, keine Adresse.</strong> Ohne diese Angaben haben Sie im Streitfall kein Gegenüber.</li>
        <li><strong>Nur Barzahlung, keine Quittung.</strong> Dann fehlt auch der Nachweis gegenüber der Verwaltung.</li>
      </ol>

      <h2 id="sparen">Wo Sie sinnvoll sparen können</h2>
      <p>Sparen lohnt sich dort, wo Sie das Risiko kontrollieren – nicht beim Leistungsumfang:</p>
      <ul>
        <li>Früh buchen: ausserhalb der Monatsenden sind Termine besser verfügbar.</li>
        <li>Wohnung vollständig leeren – jedes stehengebliebene Möbel kostet Zeit.</li>
        <li>Kleinreparaturen selbst erledigen: Storenband, Duschschlauch, Backblech.</li>
        <li>Keller und Estrich selber räumen und wischen.</li>
        <li>Mehrere Offerten einholen, aber auf gleichen Umfang achten – sonst vergleichen Sie Äpfel mit Birnen.</li>
      </ul>
""",
    ),

    dict(
        file="ratgeber-reinigungsplan-buero.html", icon="office",
        title="Reinigungsplan fürs Büro: Vorlage und Turnus | Cleeno",
        h1="Reinigungsplan fürs Büro: Vorlage, Turnus und typische Fehler",
        desc="Wie ein Reinigungsplan für Büro und Gewerbe aufgebaut ist: Turnus je Bereich, Vorlage zum Übernehmen, was vertraglich geregelt sein muss und welche Fehler teuer werden.",
        lead="Ein Reinigungsplan ist kein bürokratisches Beiwerk, sondern die Grundlage jeder Qualitätskontrolle. Ohne ihn diskutieren Auftraggeber und Reinigungsfirma über Eindrücke statt über Vereinbartes.",
        teaser="Turnus je Bereich, eine Vorlage zum Übernehmen und fünf Fehler, die in Reinigungsverträgen regelmässig teuer werden.",
        toc=[("warum", "Warum schriftlich"), ("turnus", "Turnus je Bereich"),
             ("vorlage", "Vorlage"), ("regeln", "Was geregelt sein muss"), ("fehler", "Typische Fehler")],
        body="""
      <p>«Die Reinigung wird nach Bedarf ausgeführt» – dieser Satz steht in erstaunlich vielen Verträgen und ist die Ursache fast aller späteren Reklamationen. Denn Bedarf beurteilt jede Seite anders.</p>

      <h2 id="warum">Warum ein Plan schriftlich sein muss</h2>
      <p>Ein Reinigungsplan macht drei Dinge messbar: was gemacht wird, wie oft, und wer es kontrolliert. Erst damit lässt sich sagen, ob eine Leistung erbracht wurde oder nicht. Für die Reinigungsfirma ist das genauso wertvoll wie für den Auftraggeber – sie kann kalkulieren, statt zu raten.</p>
      <p>In der Praxis hängt der Plan im Putzraum aus. Bei Liegenschaften gehört er zusätzlich in den Eingangsbereich, damit auch Mietende wissen, wann was gemacht wird.</p>

      <h2 id="turnus">Welcher Turnus für welchen Bereich</h2>
      <p>Die folgende Aufteilung hat sich für Büros mit 10 bis 60 Arbeitsplätzen bewährt.</p>
      """ + table(["Bereich", "Täglich bis wöchentlich", "Monatlich", "Ein- bis zweimal jährlich"], [
            ["Arbeitsplätze", "Abfall, freie Flächen, Böden saugen", "Böden feucht, Bürostühle", "Grundreinigung Bodenbelag"],
            ["Sitzungszimmer", "Tische, Gläser, Glastüren", "Polster absaugen", "Polsterreinigung"],
            ["Sanitär", "WC, Lavabo, Spiegel, Desinfektion, Material auffüllen", "Entkalkung, Fugen", "Grundreinigung Plättli"],
            ["Teeküche", "Spüle, Flächen, Geräte aussen", "Kühlschrank innen, Kaffeemaschine", "Backofen, Schränke innen"],
            ["Verkehrsflächen", "Eingang, Korridore, Lift", "Treppenhaus feucht", "Fenster innen und aussen"],
        ]) + """

      <h2 id="vorlage">Vorlage zum Übernehmen</h2>
      <p>Übernehmen Sie die Tabelle oben und ergänzen Sie pro Zeile zwei Spalten: <strong>Wer</strong> (Reinigungsfirma oder eigenes Personal) und <strong>Kontrolle</strong> (Datum, Kürzel). Mehr braucht ein funktionierender Plan nicht. Wichtig ist nur, dass er tatsächlich aushängt und nicht im Ordner verschwindet.</p>

      <h2 id="regeln">Was zusätzlich geregelt sein muss</h2>
      """ + checklist([
            ("Zeitfenster", "Vor 7 Uhr, nach 18 Uhr oder am Wochenende – und wer im Gebäude sein darf."),
            ("Zutritt", "Schlüssel oder Badge, Alarmcode, protokollierte Übergabe."),
            ("Ansprechperson", "Auf beiden Seiten je eine Person mit Direktnummer."),
            ("Verbrauchsmaterial", "Wer liefert Seife, Papier und Hygieneartikel – und zu welchem Preis?"),
            ("Kontrolle", "Wie oft prüft die Objektleitung, und erhält der Auftraggeber das Protokoll?"),
            ("Reklamationsweg", "An wen, bis wann, und in welcher Frist wird nachgebessert?"),
        ]) + """

      <h2 id="fehler">Fünf Fehler, die teuer werden</h2>
      <ol>
        <li><strong>Sanitär zu selten.</strong> Der Bereich prägt den Eindruck von Gästen stärker als jeder andere – hier zu sparen fällt sofort auf.</li>
        <li><strong>Verbrauchsmaterial nicht geregelt.</strong> Führt zu leeren Spendern und gegenseitigen Schuldzuweisungen.</li>
        <li><strong>Reinigung während der Bürozeiten.</strong> Stört den Betrieb und liefert schlechtere Resultate.</li>
        <li><strong>Keine periodischen Arbeiten eingeplant.</strong> Ohne Grundreinigung sieht der Boden nach zwei Jahren alt aus, egal wie oft gewischt wurde.</li>
        <li><strong>Nur der Preis entscheidet.</strong> Wer eine Offerte 30 Prozent unter dem Marktpreis annimmt, bezahlt die Differenz später über Reklamationen und Personalwechsel.</li>
      </ol>
""",
    ),
]


for i, r in enumerate(RATGEBER):
    andere = [x for x in RATGEBER if x["file"] != r["file"]]
    body = (pagehead([("Ratgeber", "ratgeber.html"), (r["h1"], r["file"])],
                     r["h1"], r["lead"], eyebrow="Ratgeber", cta_href=None)
            + "\n\n" + toc_nav(r["toc"]) + """
  <article class="section">
    <div class="container prose">
""" + r["body"] + """
    </div>
  </article>

  <section class="section section--soft">
    <div class="container">
      <div class="section-head reveal">
        <span class="eyebrow">Weiterlesen</span>
        <h2>Passt ebenfalls zum Thema</h2>
      </div>
      <div class="grid grid--2 reveal">
        """ + "\n        ".join(
        '<a class="card" href="' + o["file"] + '"><div class="card__icon">' + icon(o["icon"]) + '</div>'
        '<h3>' + o["h1"] + '</h3><p>' + o["teaser"] + '</p>'
        '<span class="card__more">Beitrag lesen ' + ICON_ARROW + '</span></a>' for o in andere) + """
      </div>
    </div>
  </section>

""" + cta("Lieber gleich einen Festpreis?",
          "Wir schauen uns Ihr Objekt an und halten den Umfang schriftlich fest – inklusive der Punkte aus diesem Beitrag."))

    page(r["file"], r["title"], r["desc"], "ratgeber.html", body,
         jsonld=ld(ld_breadcrumb([("Ratgeber", "ratgeber.html"), (r["h1"], r["file"])]),
                   ld_article(r["h1"], r["desc"], r["file"])))


# Ratgeber-Übersicht
body = (pagehead([("Ratgeber", "ratgeber.html")],
                 "Ratgeber rund um Reinigung",
                 "Wissen aus der Praxis: Was Verwaltungen bei der Wohnungsabgabe prüfen, was eine Umzugsreinigung kostet und wie ein Reinigungsplan aufgebaut ist. Ohne Verkaufsgerede, damit Sie selbst entscheiden können.",
                 eyebrow="Ratgeber", cta_href=None) + """

  <section class="section section--tint">
    <div class="container">
      <div class="cta-band reveal">
        <div>
          <h2>Checkliste für die Wohnungsabgabe</h2>
          <p>47 Kontrollpunkte zum Abhaken – am Bildschirm mit gespeichertem Fortschritt oder ausgedruckt für den Wohnungsrundgang. Kostenlos, ohne Anmeldung.</p>
        </div>
        <div class="btn-row">
          <a class="btn btn--light" href="checkliste.html">Checkliste öffnen</a>
        </div>
      </div>
    </div>
  </section>

  <section class="section">
    <div class="container">
      <div class="section-head reveal">
        <span class="eyebrow">Beiträge</span>
        <h2>Drei Themen, die im Alltag am häufigsten auftauchen</h2>
        <p>Geschrieben aus der Praxis – mit den Punkten, die in Offerten und bei Übergaben tatsächlich zu Diskussionen führen.</p>
      </div>
      <div class="grid grid--3 reveal">
        """ + "\n        ".join(
    '<a class="card" href="' + r["file"] + '"><div class="card__icon">' + icon(r["icon"]) + '</div>'
    '<h3>' + r["h1"] + '</h3><p>' + r["teaser"] + '</p>'
    '<span class="card__more">Beitrag lesen ' + ICON_ARROW + '</span></a>' for r in RATGEBER) + """
      </div>
      <p class="muted mt-40">Wir erweitern den Ratgeber laufend. Fehlt ein Thema, das Sie beschäftigt? Schreiben Sie uns – wir greifen es gerne auf.</p>
    </div>
  </section>

""" + cta("Von der Theorie zur Offerte",
          "Sie wissen jetzt, worauf es ankommt. Wir halten es für Ihr Objekt schriftlich fest – mit Festpreis und Abnahmegarantie."))

page("ratgeber.html", "Ratgeber Reinigung: Wohnungsabgabe, Preise, Pläne | Cleeno",
     "Praxiswissen rund um Reinigung: Checkliste für die Wohnungsabgabe, Kosten einer Umzugsreinigung und Aufbau eines Reinigungsplans fürs Büro.",
     "ratgeber.html", body,
     jsonld=ld(ld_breadcrumb([("Ratgeber", "ratgeber.html")])))


# ============================================================
# Druckbare Checkliste für die Wohnungsabgabe
# ============================================================
CL_GRUPPEN = [
    ("kueche", "Küche", [
        "Backofen innen, Backblech und Roste",
        "Backofenscheibe innen",
        "Dampfabzug und Fettfilter",
        "Kochfeld und Kochfeldrahmen",
        "Kühlschrank abgetaut, Dichtungen und Fächer",
        "Geschirrspüler innen, Sieb entkalkt",
        "Schränke innen, aussen und Oberkanten",
        "Spüle, Armatur und Siphon entkalkt",
        "Steamer und Mikrowelle",
        "Boden inklusive Sockelleisten",
    ]),
    ("bad", "Bad und WC", [
        "WC innen, unter dem Rand, hinter dem Spülkasten",
        "Dusche, Duschtrennwand und Plättli entkalkt",
        "Badewanne inklusive Überlauf",
        "Lavabo, Armaturen und Brausekopf entkalkt",
        "Spiegelschrank innen und aussen",
        "Silikonfugen ohne Schimmel",
        "Lüftungsgitter und Ablaufsiebe",
        "Boden inklusive Ecken",
    ]),
    ("wohnen", "Wohn- und Schlafräume", [
        "Alle Böden gesaugt und feucht gereinigt",
        "Parkett nebelfeucht, nicht nass",
        "Sockelleisten und Türrahmen-Oberkanten",
        "Türen, Griffe, Lichtschalter und Steckdosen",
        "Einbauschränke innen",
        "Heizkörper inklusive Zwischenräume",
        "Spiegel und Glasflächen streifenfrei",
        "Deckenlampen und Fassungen",
    ]),
    ("fenster", "Fenster und Storen", [
        "Glas innen und aussen",
        "Rahmen, Falze und Dichtungen",
        "Fenstersimse innen und aussen",
        "Lamellenstoren oder Rollläden",
        "Führungsschienen der Storen",
        "Balkon- und Terrassentüren",
        "Fensterläden",
    ]),
    ("neben", "Keller, Estrich und Aussenbereich", [
        "Keller geleert und gewischt",
        "Estrich geleert und gewischt",
        "Balkon oder Sitzplatz gereinigt",
        "Garage oder Einstellhallenplatz",
        "Waschküchenanteil, Flusensieb und Trocknerfilter",
        "Velokeller und persönliche Gegenstände entfernt",
        "Briefkasten geleert und Namensschild entfernt",
    ]),
    ("uebergabe", "Am Tag der Übergabe", [
        "Zählerstände Strom, Wasser und Gas notiert",
        "Alle Schlüssel gezählt, auch Zusatzschlüssel",
        "Storen- und Fensterkurbeln vorhanden",
        "Ersatzteile ersetzt: Storenband, Duschschlauch, Backblech",
        "Abnahmeprotokoll gemeinsam ausgefüllt",
        "Protokoll fotografiert oder Kopie verlangt",
        "Neue Adresse für die Depotrückzahlung angegeben",
    ]),
]

CL_ICONS = {"kueche": "home", "bad": "sparkle", "wohnen": "home",
            "fenster": "window", "neben": "building", "uebergabe": "doc"}

anzahl = sum(len(g[2]) for g in CL_GRUPPEN)

gruppen_html = "\n        ".join(
    '<section class="cl__group">\n'
    '          <h2>' + icon(CL_ICONS[key]) + titel + '</h2>\n'
    '          <ul class="cl__list">\n            '
    + "\n            ".join(
        '<li><label class="cl__item"><input type="checkbox" id="cl-%s-%d"><span>%s</span></label></li>'
        % (key, i, text) for i, text in enumerate(punkte))
    + '\n          </ul>\n        </section>'
    for key, titel, punkte in CL_GRUPPEN)

body = (pagehead([("Ratgeber", "ratgeber.html"), ("Checkliste Wohnungsabgabe", "checkliste.html")],
                 "Checkliste für die Wohnungsabgabe",
                 "Alle " + str(anzahl) + " Punkte, die bei einer Wohnungsübergabe in der Schweiz kontrolliert werden – zum Abhaken am Bildschirm oder zum Ausdrucken. Ihr Fortschritt bleibt auf diesem Gerät gespeichert.",
                 eyebrow="Werkzeug", cta_href=None) + """

  <div class="cl__bar">
    <div class="container">
      <span class="cl__count">0 von """ + str(anzahl) + """ erledigt</span>
      <span class="cl__meter" role="progressbar" aria-label="Fortschritt der Checkliste"><span></span></span>
      <span class="cl__actions">
        <button class="btn btn--ghost btn--sm" type="button" id="cl-print">Drucken</button>
        <button class="btn btn--ghost btn--sm" type="button" id="cl-reset">Zurücksetzen</button>
      </span>
    </div>
  </div>

  <section class="section">
    <div class="container">
      <div class="cl__print-head">
        <img src="assets/logo.svg" alt="Cleeno Reinigungen" width="140" height="32">
        <p>Checkliste für die Wohnungsabgabe · cleeno-reinigungen.ch · """ + PHONE + """</p>
      </div>

      <div class="cl__groups" data-checkliste>
        """ + gruppen_html + """
      </div>

      <p class="muted mt-40">Die Liste deckt den Umfang ab, den Verwaltungen in der Deutschschweiz üblicherweise prüfen. Einzelne Objekte haben zusätzliche Punkte – der Mietvertrag und das Übergabeprotokoll gehen immer vor.</p>
    </div>
  </section>

""" + cta("Keine Lust auf 47 Häkchen?",
          "Wir übernehmen die Endreinigung zum Festpreis – inklusive Fenster, Storen und Abnahmegarantie. Wird etwas beanstandet, kommen wir kostenlos zurück.",
          href="kontakt.html?leistung=umzugsreinigung"))

page("checkliste.html", "Checkliste Wohnungsabgabe zum Ausdrucken | Cleeno",
     "Checkliste für die Wohnungsübergabe in der Schweiz mit " + str(anzahl) + " Kontrollpunkten: zum Abhaken am Bildschirm, zum Ausdrucken, mit gespeichertem Fortschritt.",
     "ratgeber.html", body,
     jsonld=ld(ld_breadcrumb([("Ratgeber", "ratgeber.html"), ("Checkliste Wohnungsabgabe", "checkliste.html")])))


# ============================================================
# Danke-Seite nach dem Absenden
# ============================================================
body = ("""  <section class="pagehead">
    <div class="container">
      <span class="eyebrow">Anfrage eingegangen</span>
      <h1>Danke – wir haben Ihre Anfrage.</h1>
      <p>Sie erhalten innert 24 Stunden an Werktagen eine schriftliche Offerte mit fixem Preis. Falls es dringend ist, rufen Sie uns direkt an – wir schauen dann, was sich noch einrichten lässt.</p>
      <div class="btn-row mt-24">
        <a class="btn btn--grad" href="tel:""" + TEL + """\">""" + PHONE + """ anrufen</a>
        <a class="btn btn--ghost" href="index.html">Zur Startseite</a>
      </div>
    </div>
  </section>

  <section class="section">
    <div class="container">
      <div class="section-head reveal">
        <span class="eyebrow">Wie es weitergeht</span>
        <h2>Drei Schritte bis zum Termin</h2>
      </div>
      <ol class="steps reveal">
        <li>
          <h3>Wir melden uns</h3>
          <p>Meist noch am selben Werktag, spätestens innert 24 Stunden – per E-Mail oder Telefon, ganz wie Sie es angegeben haben.</p>
        </li>
        <li>
          <h3>Kurze Rückfragen</h3>
          <p>Bei grösseren Objekten schauen wir vorbei, sonst genügen ein paar Fotos. Beides ist kostenlos und unverbindlich.</p>
        </li>
        <li>
          <h3>Offerte mit Festpreis</h3>
          <p>Sie erhalten den Leistungsumfang schriftlich, mit fixem Preis, Terminvorschlag und allen drei Garantien.</p>
        </li>
      </ol>
    </div>
  </section>

  <section class="section section--soft">
    <div class="container">
      <div class="section-head reveal">
        <span class="eyebrow">Bis dahin</span>
        <h2>Das könnte Ihnen jetzt helfen</h2>
      </div>
      <div class="grid grid--3 reveal">
        <a class="card" href="checkliste.html"><div class="card__icon">""" + icon("doc") + """</div>
          <h3>Checkliste zur Wohnungsabgabe</h3>
          <p>47 Kontrollpunkte zum Abhaken oder Ausdrucken – damit bei der Übergabe nichts vergessen geht.</p>
          <span class="card__more">Checkliste öffnen """ + ICON_ARROW + """</span></a>
        <a class="card" href="ratgeber-umzugsreinigung-kosten.html"><div class="card__icon">""" + icon("wallet") + """</div>
          <h3>Offerten richtig vergleichen</h3>
          <p>Woher die grossen Preisunterschiede kommen und woran Sie zu günstige Angebote erkennen.</p>
          <span class="card__more">Beitrag lesen """ + ICON_ARROW + """</span></a>
        <a class="card" href="leistungen.html"><div class="card__icon">""" + icon("sparkle") + """</div>
          <h3>Weitere Leistungen</h3>
          <p>Vom Treppenhaus bis zur Bauendreinigung – vieles lässt sich mit einem Auftrag kombinieren.</p>
          <span class="card__more">Übersicht ansehen """ + ICON_ARROW + """</span></a>
      </div>
    </div>
  </section>
""")

page("danke.html", "Vielen Dank für Ihre Anfrage | Cleeno Reinigungen",
     "Ihre Anfrage bei Cleeno Reinigungen ist eingegangen. Sie erhalten innert 24 Stunden eine schriftliche Offerte mit Festpreis.",
     None, body, noindex=True)
