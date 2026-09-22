#!/usr/bin/env python3
"""Prueft die {% schema %}-Bloecke aller Section-Dateien gegen die Regeln,
die Shopify beim Speichern im Theme-Editor durchsetzt.

    python3 scripts/validate-schema.py
"""
import re, json, sys, glob

VALID = {"text","textarea","richtext","html","article","blog","checkbox","collection",
         "collection_list","color","color_background","color_scheme","font_picker","image_picker",
         "inline_richtext","link_list","liquid","number","page","product","product_list","radio",
         "range","select","url","video","video_url","header","paragraph"}

def check(settings, where, problems):
    ids = []
    for s in settings:
        t = s.get("type")
        sid = s.get("id", "?")
        tag = f"{where}/{sid}"
        if t not in VALID:
            problems.append(f"{tag}: unbekannter Typ '{t}'")
            continue
        if t in ("header", "paragraph"):
            if not s.get("content"):
                problems.append(f"{where}/{t}: 'content' fehlt oder leer")
            for k in s:
                if k not in ("type", "content", "info"):
                    problems.append(f"{where}/{t}: unerwarteter Schluessel '{k}'")
            continue
        ids.append(sid)
        if not s.get("id"):
            problems.append(f"{where}: Einstellung ohne id")
        elif not re.fullmatch(r"[a-z0-9_]+", sid):
            problems.append(f"{tag}: ungueltige Zeichen in der id")
        if not s.get("label"):
            problems.append(f"{tag}: 'label' fehlt oder leer")
        for k, v in s.items():
            if isinstance(v, str) and v == "" and k != "default":
                problems.append(f"{tag}: '{k}' ist ein leerer String — Shopify lehnt das ab")
        if t == "range":
            mn, mx, st, df = s.get("min"), s.get("max"), s.get("step"), s.get("default")
            if None in (mn, mx, st):
                problems.append(f"{tag}: min/max/step unvollstaendig"); continue
            if mx <= mn:
                problems.append(f"{tag}: max <= min")
            steps = (mx - mn) / st
            if abs(steps - round(steps)) > 1e-9:
                problems.append(f"{tag}: (max-min)/step = {steps} ist nicht ganzzahlig")
            if steps > 101:
                problems.append(f"{tag}: {steps:.0f} Schritte (Shopify erlaubt max. 101)")
            if isinstance(st, float) or isinstance(mn, float) or isinstance(mx, float):
                problems.append(f"{tag}: Dezimalwerte in range — Rundungsrisiko, besser ganzzahlig")
            if df is None:
                problems.append(f"{tag}: 'default' fehlt")
            else:
                if not (mn <= df <= mx):
                    problems.append(f"{tag}: default {df} liegt ausserhalb {mn}..{mx}")
                off = (df - mn) / st
                if abs(off - round(off)) > 1e-9:
                    problems.append(f"{tag}: default {df} liegt nicht auf einem Schritt")
        if t in ("select", "radio"):
            opts = s.get("options") or []
            if not opts:
                problems.append(f"{tag}: keine options")
            vals = [o.get("value") for o in opts]
            for o in opts:
                if not o.get("label"):
                    problems.append(f"{tag}: option '{o.get('value')}' ohne label")
            if len(vals) != len(set(vals)):
                problems.append(f"{tag}: doppelte option-values")
            if "default" in s and s["default"] not in vals:
                problems.append(f"{tag}: default '{s['default']}' ist keine der options")
        if t == "checkbox" and not isinstance(s.get("default", False), bool):
            problems.append(f"{tag}: default muss true/false sein")
        if t == "image_picker" and "default" in s:
            problems.append(f"{tag}: image_picker darf kein default haben")
    dupes = {i for i in ids if ids.count(i) > 1}
    if dupes:
        problems.append(f"{where}: doppelte ids {sorted(dupes)}")

problems = []
for path in sorted(glob.glob("sections/*.liquid")):
    src = open(path, encoding="utf-8").read()
    m = re.search(r"\{%\s*schema\s*%\}(.*?)\{%\s*endschema\s*%\}", src, re.S)
    if not m:
        problems.append(f"{path}: kein schema-Block"); continue
    try:
        sc = json.loads(m.group(1))
    except json.JSONDecodeError as e:
        problems.append(f"{path}: JSON ungueltig — {e}"); continue

    name = sc.get("name", "")
    if len(name) > 25:
        problems.append(f"{path}: name '{name}' laenger als 25 Zeichen")
    check(sc.get("settings", []), path, problems)
    for b in sc.get("blocks", []):
        if len(b.get("name", "")) > 25:
            problems.append(f"{path}: Block-name '{b['name']}' zu lang")
        check(b.get("settings", []), f"{path}:block/{b.get('type')}", problems)

    block_types = {b.get("type") for b in sc.get("blocks", [])}
    for pr in sc.get("presets", []):
        for pb in pr.get("blocks", []):
            if pb.get("type") not in block_types:
                problems.append(f"{path}: Preset nutzt unbekannten Block '{pb.get('type')}'")
            bdef = next((b for b in sc["blocks"] if b["type"] == pb["type"]), {})
            known = {s.get("id") for s in bdef.get("settings", [])}
            for k in pb.get("settings", {}):
                if k not in known:
                    problems.append(f"{path}: Preset setzt unbekannte Einstellung '{k}'")
    print(f"geprueft: {path} ({len(sc.get('settings', []))} Einstellungen)")

print()
if problems:
    print(f"{len(problems)} PROBLEM(E):")
    for p in problems:
        print("  -", p)
    sys.exit(1)
print("Alle Schemas sauber.")
