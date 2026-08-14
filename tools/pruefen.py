#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Qualitätskontrolle für alle Seiten: Struktur, Verlinkung, Barrierefreiheit, SEO."""

import os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + "/"

import glob, os, re, json, sys

issues = []


def add(f, kind, msg):
    issues.append((f, kind, msg))


os.chdir(ROOT)
for f in sorted(glob.glob("*.html")):
    h = open(f, encoding="utf-8").read()

    # --- Struktur ---
    if h.count("<h1") != 1:
        add(f, "Struktur", "%d h1-Elemente" % h.count("<h1"))
    if '<html lang="de-CH">' not in h:
        add(f, "Struktur", "lang-Attribut fehlt")
    if '<meta charset="utf-8">' not in h:
        add(f, "Struktur", "charset fehlt")

    # Überschriftenreihenfolge
    levels = [int(m) for m in re.findall(r"<h([1-4])[ >]", h)]
    for a, b in zip(levels, levels[1:]):
        if b > a + 1:
            add(f, "Struktur", "Sprung von h%d zu h%d" % (a, b))
            break

    # --- IDs ---
    ids = re.findall(r'\sid="([^"]+)"', h)
    dup = {i for i in ids if ids.count(i) > 1}
    if dup:
        add(f, "IDs", "doppelt: " + ", ".join(sorted(dup)))

    # --- Verweise innerhalb der Seite ---
    for ref in re.findall(r'href="#([^"]+)"', h):
        if ref not in ids:
            add(f, "Anker", "#%s existiert nicht" % ref)
    for ref in re.findall(r'aria-controls="([^"]+)"', h):
        if ref not in ids:
            add(f, "ARIA", "aria-controls=%s zeigt ins Leere" % ref)
    for ref in re.findall(r'aria-labelledby="([^"]+)"', h):
        if ref not in ids:
            add(f, "ARIA", "aria-labelledby=%s zeigt ins Leere" % ref)
    for ref in re.findall(r'<label[^>]+for="([^"]+)"', h):
        if ref not in ids:
            add(f, "Formular", "label for=%s ohne Feld" % ref)

    # --- Dateien ---
    for ref in re.findall(r'(?:href|src)="([^"#?]+\.(?:html|css|js|svg|png|jpg|webp|woff2))"', h):
        if not ref.startswith(("http", "data:")) and not os.path.exists(ref):
            add(f, "Datei", "fehlt: " + ref)

    # --- Symbole: ohne eigene Masse blähen sich SVG im Fliesstext auf ---
    for svg in re.findall(r"<svg[^>]*>", h):
        if "width=" not in svg or "height=" not in svg:
            add(f, "Symbol", "svg ohne width/height: " + svg[:70])

    # --- Bilder ---
    for img in re.findall(r"<img[^>]*>", h):
        if "alt=" not in img:
            add(f, "Bild", "alt fehlt: " + img[:70])
        if "width=" not in img or "height=" not in img:
            add(f, "Bild", "width/height fehlt: " + img[:70])

    # --- Buttons und Links mit Text ---
    for a in re.findall(r"<a\b[^>]*>(.*?)</a>", h, re.S):
        text = re.sub(r"<[^>]+>", "", a).strip()
        if not text and "aria-label" not in a:
            add(f, "Link", "ohne Text und ohne aria-label")

    # --- SEO ---
    title = re.search(r"<title>(.*?)</title>", h, re.S)
    if not title:
        add(f, "SEO", "kein title")
    elif not (15 <= len(title.group(1)) <= 65):
        add(f, "SEO", "title %d Zeichen: %s" % (len(title.group(1)), title.group(1)[:60]))

    desc = re.search(r'<meta name="description" content="(.*?)">', h, re.S)
    if not desc:
        add(f, "SEO", "keine description")
    elif not (70 <= len(desc.group(1)) <= 175):
        add(f, "SEO", "description %d Zeichen" % len(desc.group(1)))

    if 'name="robots"' not in h and "<link rel=\"canonical\"" not in h:
        add(f, "SEO", "kein canonical")
    if 'property="og:image"' not in h:
        add(f, "SEO", "kein og:image")
    if 'name="theme-color"' not in h:
        add(f, "SEO", "kein theme-color")

    # --- JSON-LD prüfen ---
    for block in re.findall(r'<script type="application/ld\+json">(.*?)</script>', h, re.S):
        try:
            json.loads(block)
        except ValueError as e:
            add(f, "JSON-LD", "ungültig: %s" % e)

    # --- Tags ausgeglichen ---
    for tag in ["div", "section", "ul", "ol", "li", "a", "p", "table", "form", "details",
                "main", "header", "footer", "svg", "fieldset", "aside", "nav", "button",
                "label", "figure", "article", "h1", "h2", "h3", "span"]:
        o = len(re.findall(r"<" + tag + r"[\s>]", h))
        c = len(re.findall(r"</" + tag + r">", h))
        if o != c:
            add(f, "HTML", "%s: %d offen / %d geschlossen" % (tag, o, c))

if issues:
    by_kind = {}
    for f, kind, msg in issues:
        by_kind.setdefault(kind, []).append((f, msg))
    for kind in sorted(by_kind):
        print("\n== %s (%d) ==" % (kind, len(by_kind[kind])))
        for f, msg in by_kind[kind][:14]:
            print("  %-28s %s" % (f, msg))
        if len(by_kind[kind]) > 14:
            print("  … %d weitere" % (len(by_kind[kind]) - 14))
    print("\nGesamt: %d Befunde" % len(issues))
else:
    print("Keine Befunde.")
