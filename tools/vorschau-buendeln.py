#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Bündelt die statische Website zu einer einzelnen Vorschau-Seite.

Die echte Website bleibt unverändert – hier werden alle Seiten in ein Dokument
gelegt, die Navigation auf Hash-Routen umgestellt und Schriften, Logo und
Stylesheet eingebettet, damit die Vorschau unter einer einzigen URL läuft.
"""

import os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + "/"

import io, os, re, base64


PAGES = [
    ("start", "index.html"),
    ("leistungen", "leistungen.html"),
    ("preisrechner", "preisrechner.html"),
    ("unterhaltsreinigung", "unterhaltsreinigung.html"),
    ("bueroreinigung", "bueroreinigung.html"),
    ("fensterreinigung", "fensterreinigung.html"),
    ("umzugsreinigung", "umzugsreinigung.html"),
    ("bauendreinigung", "bauendreinigung.html"),
    ("liegenschaftsreinigung", "liegenschaftsreinigung.html"),
    ("ratgeber", "ratgeber.html"),
    ("checkliste", "checkliste.html"),
    ("danke", "danke.html"),
    ("ratgeber-wohnungsabgabe", "ratgeber-wohnungsabgabe.html"),
    ("ratgeber-umzugsreinigung-kosten", "ratgeber-umzugsreinigung-kosten.html"),
    ("ratgeber-reinigungsplan-buero", "ratgeber-reinigungsplan-buero.html"),
    ("ueber-uns", "ueber-uns.html"),
    ("kontakt", "kontakt.html"),
    ("impressum", "impressum.html"),
    ("datenschutz", "datenschutz.html"),
]
FILE_TO_KEY = {f: k for k, f in PAGES}


OUT = ROOT + "tools/vorschau.html"


def read(p):
    return io.open(os.path.join(ROOT, p), encoding="utf-8").read()


def rewrite_links(html):
    """Interne Seitenlinks auf Hash-Routen umstellen, Anker unberührt lassen.
       Ein ?leistung=… wandert in ein data-Attribut, damit die Vorschau das
       Auswahlfeld auf der Kontaktseite trotzdem vorbelegen kann."""
    def sub(m):
        attr, target, query = m.group(1), m.group(2), m.group(3) or ""
        key = FILE_TO_KEY.get(target)
        if not key:
            return m.group(0)
        out = attr + '="#/' + key + '"'
        wanted = re.search(r'leistung=([a-z\-]+)', query)
        if wanted:
            out += ' data-leistung="' + wanted.group(1) + '"'
        return out
    return re.sub(r'(href|action)="([a-z0-9\-]+\.html)(\?[^"]*)?"', sub, html)


index = read("index.html")
header = re.search(r'(<a class="skip-link".*?</header>)', index, re.S).group(1)
footer = re.search(r'(<footer class="site-footer">.*?</footer>)', index, re.S).group(1)
mobile = re.search(r'(<div class="mobile-cta">.*?\n</div>)', index, re.S).group(1)

header = rewrite_links(header.replace(' aria-current="page"', ''))
footer = rewrite_links(footer)
mobile = rewrite_links(mobile)

# ---------- Assets einbetten ----------
css = read("css/style.css")
for name in os.listdir(os.path.join(ROOT, "assets/fonts")):
    if not name.endswith(".woff2"):
        continue
    data = open(os.path.join(ROOT, "assets/fonts", name), "rb").read()
    uri = "data:font/woff2;base64," + base64.b64encode(data).decode()
    css = css.replace('url("../assets/fonts/' + name + '")', 'url("' + uri + '")')
assert "../assets/fonts" not in css, "Schrift nicht eingebettet"

def inline_svgs(html):
    """<img src="assets/x.svg"> durch eingebettete Daten ersetzen."""
    def sub(m):
        path = os.path.join(ROOT, "assets", m.group(1))
        if not os.path.exists(path):
            return m.group(0)
        data = base64.b64encode(open(path, "rb").read()).decode()
        return 'src="data:image/svg+xml;base64,' + data + '"'
    return re.sub(r'src="assets/([a-z0-9\-]+\.svg)"', sub, html)

header = inline_svgs(header)
footer = inline_svgs(footer)

js = read("js/main.js")
calc_js = read("js/preisrechner.js")
js = js.replace(
    "      showStatus('Ihr E-Mail-Programm öffnet sich mit der fertigen Anfrage. "
    "Alternativ erreichen Sie uns telefonisch.', true);\n"
    "      window.location.href = buildMailto(data);\n",
    "      showStatus('Vorschau: Die Eingaben sind vollständig. Auf der echten Website "
    "geht die Anfrage jetzt raus – hier wird nichts versendet.', true);\n"
    "      void buildMailto;\n")
assert "window.location.href = buildMailto" not in js, "Mailto-Fallback nicht ersetzt"

DUP_IDS = ("ueberblick|umfang|preise|ablauf|garantien|faq|vergleich|zeitplan|checkliste|pruefpunkte|abnuetzung|selber|faktoren|offerte|warnsignale|sparen|warum|turnus|vorlage|regeln|fehler")

sections = []
for key, filename in PAGES:
    body = re.search(r'<main id="main">(.*?)</main>', read(filename), re.S).group(1)
    body = rewrite_links(inline_svgs(body))
    # In der gebündelten Vorschau liegen alle Seiten in einem Dokument –
    # gleichnamige Sprungmarken werden deshalb pro Seite eindeutig gemacht.
    body = re.sub(r'id="(' + DUP_IDS + r')"', lambda m: 'id="' + key + '-' + m.group(1) + '"', body)
    body = re.sub(r'href="#(' + DUP_IDS + r')"', lambda m: 'href="#' + key + '-' + m.group(1) + '"', body)
    sections.append('<div class="pv-page" id="pv-' + key + '" hidden>\n' + body + '\n</div>')

PREVIEW_CSS = """
/* ---------- Nur für die Vorschau ---------- */
.pv-bar { background: var(--bg-deep); color: rgba(255,255,255,.8); font-family: var(--font-body); font-size: .89rem; line-height: 1.45; }
.pv-bar__inner { max-width: var(--container); margin-inline: auto; padding: 11px var(--gutter); display: flex; flex-wrap: wrap; align-items: center; gap: 8px 14px; }
.pv-chip { background: var(--grad); color: #fff; font-family: var(--font-display); font-weight: 700; font-size: .72rem; letter-spacing: .1em; text-transform: uppercase; padding: 5px 11px; border-radius: 999px; flex: none; }
/* Einblende-Animation abschalten: Inhalte liegen in ausgeblendeten Containern,
   die der IntersectionObserver nie zu sehen bekommt. */
.js .reveal { opacity: 1 !important; transform: none !important; }
"""

PREVIEW_JS = """
(function () {
  'use strict';
  var DEFAULT = 'start';
  var SERVICES = ['unterhaltsreinigung', 'bueroreinigung', 'fensterreinigung',
                  'umzugsreinigung', 'bauendreinigung', 'liegenschaftsreinigung'];
  var pages = {};
  document.querySelectorAll('.pv-page').forEach(function (el) {
    pages[el.id.replace('pv-', '')] = el;
  });

  var navLinks = Array.prototype.slice.call(
    document.querySelectorAll('.nav__link, .nav__drawer a[href^="#/"]')
  );

  function show(key) {
    if (!pages[key]) { key = DEFAULT; }
    Object.keys(pages).forEach(function (k) { pages[k].hidden = (k !== key); });

    var navKey = SERVICES.indexOf(key) > -1 ? 'leistungen'
      : (key.indexOf('ratgeber-') === 0 || key === 'checkliste' ? 'ratgeber' : key);
    navLinks.forEach(function (a) {
      if (a.getAttribute('href') === '#/' + navKey) { a.setAttribute('aria-current', 'page'); }
      else { a.removeAttribute('aria-current'); }
    });

    window.scrollTo(0, 0);
  }

  function route() {
    var hash = window.location.hash;
    if (hash.indexOf('#/') !== 0) { return; }   // normale Anker wie #offerte-form
    show(hash.slice(2) || DEFAULT);
  }

  window.addEventListener('hashchange', route);

  // Gewünschte Leistung auf der Kontaktseite vorbelegen
  function preselect(value) {
    var select = document.getElementById('leistung');
    if (!select || !value) { return; }
    Array.prototype.forEach.call(select.options, function (o) {
      if (o.value === value) { select.value = value; }
    });
  }

  function preselectCalc(value) {
    var radio = document.querySelector('#calc input[name="leistung"][value="' + value + '"]');
    if (!radio) { return; }
    radio.checked = true;
    radio.dispatchEvent(new Event('change', { bubbles: true }));
  }

  document.addEventListener('click', function (e) {
    var link = e.target.closest ? e.target.closest('[data-leistung]') : null;
    if (!link) { return; }
    var value = link.getAttribute('data-leistung');
    var ziel = link.getAttribute('href');
    setTimeout(function () {
      if (ziel === '#/preisrechner') { preselectCalc(value); } else { preselect(value); }
    }, 0);
  });

  // Schnellofferte aus dem Hero
  var quick = document.getElementById('quick-form');
  if (quick) {
    quick.addEventListener('submit', function (e) {
      e.preventDefault();
      var value = document.getElementById('quick-leistung').value;
      window.location.hash = '#/preisrechner';
      show('preisrechner');
      preselectCalc(value);
    });
  }

  show(window.location.hash.indexOf('#/') === 0
    ? window.location.hash.slice(2) || DEFAULT
    : DEFAULT);
})();
"""

html = ("<title>Cleeno Reinigungen</title>\n"
        "<style>\n" + css + PREVIEW_CSS + "</style>\n\n"
        '<div class="pv-bar"><div class="pv-bar__inner">'
        '<span class="pv-chip">Vorschau</span>'
        '<span>Alle Seiten sind verlinkt und anklickbar. Telefonnummer, E-Mail-Adresse und Domain '
        'sind noch Platzhalter – das Formular versendet nichts.</span>'
        '</div></div>\n\n'
        + header + "\n\n<main id=\"main\">\n\n"
        + "\n\n".join(sections)
        + "\n\n</main>\n\n" + footer + "\n\n" + mobile
        + "\n\n<script>\n" + js + "\n" + calc_js + "\n" + PREVIEW_JS + "\n</script>\n")

io.open(OUT, "w", encoding="utf-8").write(html)
print("geschrieben:", OUT, round(len(html.encode("utf-8")) / 1024), "KB,", len(sections), "Seiten")
