#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Vektorisiert das gelieferte Logo-PNG zu einer SVG-Datei.

Die Form wird aus dem Alphakanal nachgezeichnet, die Farben werden
spaltenweise aus dem Original gemittelt und als linearer Verlauf gesetzt.
"""

import os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + "/"

import numpy as np
from PIL import Image
import potrace

SRC = ROOT + "assets/logo-original.png"   # Vorlage, aus der vektorisiert wird

im = Image.open(SRC).convert("RGBA")
arr = np.array(im)
alpha = arr[..., 3]
h, w = alpha.shape

# --- Form nachzeichnen ---
mask = alpha > 128
bmp = potrace.Bitmap(~mask)   # potracer behandelt True als Hintergrund
path = bmp.trace(turdsize=4, alphamax=1.0, opticurve=True, opttolerance=0.2)


def f(v):
    return ("%.1f" % v).rstrip("0").rstrip(".")


parts = []
for curve in path:
    p = curve.start_point
    parts.append("M%s %s" % (f(p.x), f(p.y)))
    for seg in curve:
        end = seg.end_point
        if seg.is_corner:
            parts.append("L%s %sL%s %s" % (f(seg.c.x), f(seg.c.y), f(end.x), f(end.y)))
        else:
            parts.append("C%s %s %s %s %s %s" % (f(seg.c1.x), f(seg.c1.y),
                                                 f(seg.c2.x), f(seg.c2.y),
                                                 f(end.x), f(end.y)))
    parts.append("Z")
d = "".join(parts)

# --- Farbverlauf aus dem Original ableiten ---
xs = np.where(mask.any(axis=0))[0]
x0, x1 = int(xs.min()), int(xs.max())
stops = []
for i in range(7):
    xa = x0 + (x1 - x0) * i // 6
    xb = min(x1, xa + max(4, (x1 - x0) // 40))
    col = mask[:, xa:xb + 1]
    if not col.any():
        continue
    rgb = arr[:, xa:xb + 1, :3][col]
    r, g, b = rgb.mean(axis=0).round().astype(int)
    stops.append((i / 6.0, "#%02X%02X%02X" % (r, g, b)))

stop_xml = "\n      ".join(
    '<stop offset="%s" stop-color="%s"/>' % (("%.3f" % o).rstrip("0").rstrip(".") or "0", c)
    for o, c in stops)

svg = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" role="img" aria-label="Cleeno">
  <title>Cleeno</title>
  <defs>
    <linearGradient id="cleeno-grad" x1="%d" y1="0" x2="%d" y2="0" gradientUnits="userSpaceOnUse">
      %s
    </linearGradient>
  </defs>
  <path fill="url(#cleeno-grad)" fill-rule="evenodd" d="%s"/>
</svg>
""" % (w, h, x0, x1, stop_xml, d)

open(OUT, "w", encoding="utf-8").write(svg)
print("Pfadlänge:", len(d), "Zeichen")

print("Farbstopps:", stops)
