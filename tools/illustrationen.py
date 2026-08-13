#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Erzeugt flache Szenen-Illustrationen im Markenstil (800 x 600).

Bewusst reduziert und ohne Menschen: Die Bilder sollen Kontext geben und
später problemlos durch echte Fotos ersetzt werden können.
"""

import os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + "/"

import io

W, H = 800, 600
OUT = ROOT + "assets/"

# Markenpalette
MINT, SKY, BLUE, DEEP = "#26CEB1", "#26AFD0", "#2581FF", "#0C1B33"
BG, BG2, LIGHT, WHITE = "#EAF3FC", "#D6E8F8", "#BBDCF7", "#FFFFFF"
WARM, WARM2 = "#E6EDF5", "#CBD9E8"


def head(label):
    return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" role="img" aria-label="%s">'
            '<defs><linearGradient id="bg" x1="0" y1="0" x2="0" y2="1">'
            '<stop offset="0" stop-color="%s"/><stop offset="1" stop-color="%s"/></linearGradient>'
            '<linearGradient id="mb" x1="0" y1="0" x2="1" y2="1">'
            '<stop offset="0" stop-color="%s"/><stop offset="1" stop-color="%s"/></linearGradient></defs>'
            '<rect width="%d" height="%d" fill="url(#bg)"/>' % (W, H, label, BG, BG2, MINT, BLUE, W, H))


def sparkle(x, y, s, fill=WHITE, o=".9"):
    return ('<g transform="translate(%d %d) scale(%s)" fill="%s" opacity="%s">'
            '<path d="M0 -22 L5.5 -5.5 L22 0 L5.5 5.5 L0 22 L-5.5 5.5 L-22 0 L-5.5 -5.5 Z"/></g>'
            % (x, y, s, fill, o))


scenes = {}

# ---------- Büro ----------
scenes["illu-buero.svg"] = head("Illustration eines gereinigten Büroarbeitsplatzes") + f'''
<rect y="430" width="{W}" height="170" fill="{WARM}"/>
<rect x="500" y="70" width="250" height="230" rx="10" fill="{LIGHT}"/>
<rect x="500" y="70" width="250" height="230" rx="10" fill="{WHITE}" opacity=".45"/>
<path d="M500 300 L610 70 h70 L560 300 Z" fill="{WHITE}" opacity=".5"/>
<rect x="618" y="70" width="7" height="230" fill="{WARM2}"/>
<rect x="500" y="182" width="250" height="7" fill="{WARM2}"/>
<rect x="120" y="430" width="420" height="16" rx="6" fill="{DEEP}"/>
<rect x="146" y="446" width="16" height="120" rx="6" fill="{DEEP}" opacity=".8"/>
<rect x="498" y="446" width="16" height="120" rx="6" fill="{DEEP}" opacity=".8"/>
<rect x="250" y="300" width="200" height="120" rx="8" fill="{DEEP}"/>
<rect x="262" y="312" width="176" height="96" rx="4" fill="url(#mb)"/>
<rect x="335" y="420" width="30" height="12" fill="{DEEP}"/>
<rect x="300" y="428" width="100" height="10" rx="5" fill="{DEEP}"/>
<rect x="150" y="352" width="86" height="26" rx="12" fill="{SKY}"/>\n<rect x="182" y="378" width="16" height="52" rx="8" fill="{DEEP}"/>\n<rect x="150" y="290" width="20" height="70" rx="10" fill="{SKY}" opacity=".8"/>\n<rect x="160" y="392" width="70" height="24" rx="6" fill="{WHITE}" opacity=".9"/>
<rect x="168" y="380" width="54" height="14" rx="4" fill="{SKY}"/>
<circle cx="640" cy="470" r="46" fill="{MINT}" opacity=".25"/>
<path d="M640 430c26 22 34 44 22 62-14 20-44 20-58 0-12-18-4-40 36-62Z" fill="{MINT}"/>
<rect x="620" y="492" width="42" height="60" rx="8" fill="{WHITE}"/>
{sparkle(200, 150, "1.1", MINT, ".55")}
{sparkle(300, 90, ".7", BLUE, ".35")}
</svg>'''

# ---------- Umzug ----------
scenes["illu-umzug.svg"] = head("Illustration gestapelter Umzugskartons in einer leeren Wohnung") + f'''
<rect y="430" width="{W}" height="170" fill="{WARM}"/>
<rect x="70" y="120" width="150" height="200" rx="8" fill="{LIGHT}" opacity=".8"/>
<rect x="230" y="300" width="200" height="130" rx="6" fill="#E4B98A"/>
<rect x="230" y="300" width="200" height="130" rx="6" fill="{DEEP}" opacity=".08"/>
<rect x="310" y="300" width="40" height="130" fill="{WHITE}" opacity=".55"/>
<rect x="230" y="296" width="200" height="14" rx="5" fill="{WHITE}" opacity=".6"/>
<rect x="258" y="180" width="150" height="120" rx="6" fill="#EFC79B"/>
<rect x="316" y="180" width="34" height="120" fill="{WHITE}" opacity=".55"/>
<rect x="258" y="176" width="150" height="12" rx="4" fill="{WHITE}" opacity=".6"/>
<rect x="452" y="340" width="160" height="90" rx="6" fill="#E4B98A"/>
<rect x="514" y="340" width="34" height="90" fill="{WHITE}" opacity=".55"/>
<rect x="600" y="250" width="52" height="180" rx="26" fill="{SKY}" opacity=".55"/>
<rect x="612" y="250" width="28" height="180" rx="14" fill="{WHITE}" opacity=".5"/>
<circle cx="700" cy="392" r="38" fill="{MINT}" opacity=".3"/>
<path d="M700 352c22 20 30 38 20 54-12 18-38 18-50 0-10-16-4-34 30-54Z" fill="{MINT}"/>
<rect x="684" y="408" width="34" height="46" rx="7" fill="{WHITE}"/>
{sparkle(150, 250, "1", BLUE, ".3")}
{sparkle(520, 150, ".8", MINT, ".5")}
</svg>'''

# ---------- Liegenschaft ----------
scenes["illu-liegenschaft.svg"] = head("Illustration eines gepflegten Mehrfamilienhauses") + (
    f'''
<rect y="470" width="{W}" height="130" fill="{WARM}"/>
<rect x="170" y="96" width="460" height="374" rx="12" fill="{WHITE}"/>
<rect x="170" y="96" width="460" height="54" rx="12" fill="url(#mb)"/>
<rect x="170" y="140" width="460" height="10" fill="{DEEP}" opacity=".08"/>
'''
    + "".join(
        f'<rect x="{x}" y="{y}" width="74" height="62" rx="6" fill="{LIGHT}"/>'
        f'<path d="M{x} {y+62} L{x+42} {y} h30 v16 L{x+30} {y+62} Z" fill="{WHITE}" opacity=".55"/>'
        f'<rect x="{x-6}" y="{y+62}" width="86" height="7" rx="3" fill="{WARM2}"/>'
        for y in (192, 300)
        for x in (206, 316, 426, 536)
    )
    + f'''
<rect x="344" y="392" width="96" height="78" rx="8" fill="{DEEP}"/>
<rect x="356" y="404" width="72" height="66" rx="5" fill="{SKY}" opacity=".85"/>
<circle cx="418" cy="440" r="5" fill="{WHITE}"/>
<rect x="316" y="466" width="152" height="10" rx="5" fill="{WARM2}"/>
<rect x="664" y="336" width="18" height="134" rx="9" fill="#8A6A4E"/>
<circle cx="673" cy="304" r="60" fill="{MINT}" opacity=".85"/>
<circle cx="634" cy="340" r="36" fill="{MINT}" opacity=".7"/>
<circle cx="714" cy="340" r="32" fill="{MINT}" opacity=".6"/>
<rect x="92" y="392" width="58" height="78" rx="8" fill="{SKY}" opacity=".6"/>
<rect x="92" y="382" width="58" height="14" rx="6" fill="{DEEP}" opacity=".45"/>
''' + sparkle(118, 190, "1.1", WHITE, ".85") + sparkle(700, 168, ".8", WHITE, ".6") + "</svg>")

# ---------- Bauendreinigung ----------
scenes["illu-bau.svg"] = head("Illustration eines Rohbaus vor der Endreinigung") + (
    f'''
<rect y="430" width="{W}" height="170" fill="{WARM}"/>
<rect x="470" y="90" width="260" height="240" rx="8" fill="{LIGHT}"/>
<path d="M470 330 L590 90 h64 L534 330 Z" fill="{WHITE}" opacity=".5"/>
<rect x="596" y="90" width="8" height="240" fill="{WARM2}"/>
<path d="M96 566 L300 566 L262 430 L134 430 Z" fill="{WHITE}" opacity=".55"/>
<rect x="150" y="150" width="17" height="286" rx="7" fill="{DEEP}"/>
<rect x="256" y="150" width="17" height="286" rx="7" fill="{DEEP}"/>
'''
    + "".join(f'<rect x="150" y="{y}" width="123" height="14" rx="6" fill="{DEEP}" opacity=".78"/>'
              for y in (198, 256, 314, 372))
    + f'''
<rect x="330" y="356" width="88" height="78" rx="9" fill="{BLUE}"/>
<rect x="330" y="356" width="88" height="19" rx="9" fill="{WHITE}" opacity=".5"/>
<path d="M352 354c0-17 44-17 44 0" fill="none" stroke="{DEEP}" stroke-width="7" stroke-linecap="round"/>
<rect x="440" y="392" width="134" height="42" rx="11" fill="{MINT}"/>
<rect x="452" y="402" width="110" height="18" rx="9" fill="{WHITE}" opacity=".55"/>
<rect x="500" y="330" width="14" height="66" rx="7" fill="{DEEP}"/>
<path d="M614 434 q64 -34 128 0" fill="none" stroke="{WHITE}" stroke-width="15" stroke-linecap="round" opacity=".75"/>
''' + sparkle(660, 208, "1", MINT, ".6") + sparkle(210, 118, ".7", BLUE, ".3") + "</svg>")

# ---------- Fenster ----------
scenes["illu-fenster.svg"] = head("Illustration einer streifenfrei gereinigten Fensterfront") + f'''
<rect x="90" y="60" width="620" height="480" rx="14" fill="{WHITE}"/>
<rect x="112" y="82" width="576" height="436" rx="8" fill="{LIGHT}"/>
<path d="M112 518 L392 82 h150 L262 518 Z" fill="{WHITE}" opacity=".55"/>
<path d="M540 518 L688 288 v130 L640 518 Z" fill="{WHITE}" opacity=".35"/>
<rect x="392" y="82" width="14" height="436" fill="{WHITE}"/>
<rect x="112" y="292" width="576" height="14" fill="{WHITE}"/>
<rect x="90" y="60" width="620" height="480" rx="14" fill="none" stroke="{WARM2}" stroke-width="18"/>
<rect x="470" y="120" width="150" height="26" rx="13" fill="{DEEP}"/>
<rect x="470" y="146" width="150" height="16" rx="6" fill="{MINT}"/>
<rect x="536" y="162" width="18" height="86" rx="9" fill="{DEEP}" opacity=".9"/>
<path d="M470 176 q76 26 150 0" fill="none" stroke="{WHITE}" stroke-width="12" stroke-linecap="round" opacity=".85"/>
{sparkle(230, 200, "1.2", WHITE, ".95")}
{sparkle(320, 400, ".9", WHITE, ".8")}
{sparkle(600, 420, "1", WHITE, ".7")}
</svg>'''

# ---------- Wohnung / Unterhaltsreinigung ----------
scenes["illu-wohnung.svg"] = head("Illustration eines frisch gereinigten Wohnraums") + f'''
<rect y="430" width="{W}" height="170" fill="{WARM}"/>
<ellipse cx="400" cy="500" rx="290" ry="52" fill="{LIGHT}" opacity=".8"/>
<rect x="520" y="80" width="220" height="220" rx="10" fill="{LIGHT}"/>
<path d="M520 300 L620 80 h60 L580 300 Z" fill="{WHITE}" opacity=".5"/>
<rect x="626" y="80" width="7" height="220" fill="{WARM2}"/>
<rect x="170" y="330" width="340" height="26" rx="13" fill="{DEEP}"/>
<rect x="182" y="252" width="316" height="86" rx="18" fill="{BLUE}"/>
<rect x="196" y="266" width="136" height="68" rx="14" fill="{WHITE}" opacity=".35"/>
<rect x="348" y="266" width="136" height="68" rx="14" fill="{WHITE}" opacity=".35"/>
<rect x="182" y="356" width="26" height="60" rx="10" fill="{DEEP}" opacity=".85"/>
<rect x="472" y="356" width="26" height="60" rx="10" fill="{DEEP}" opacity=".85"/>
<rect x="556" y="250" width="18" height="180" rx="9" fill="{DEEP}"/>
<path d="M510 250 h110 l-30 -70 h-50 Z" fill="{BLUE}" opacity=".85"/>
<circle cx="120" cy="404" r="40" fill="{MINT}" opacity=".28"/>
<path d="M120 366c24 20 32 40 21 57-13 19-41 19-54 0-11-17-3-37 33-57Z" fill="{MINT}"/>
<rect x="102" y="422" width="38" height="52" rx="8" fill="{WHITE}"/>
{sparkle(300, 150, "1.1", MINT, ".5")}
{sparkle(430, 200, ".7", BLUE, ".3")}
</svg>'''

for name, svg in scenes.items():
    io.open(OUT + name, "w", encoding="utf-8").write(svg)
    print("%-26s %5.1f KB" % (name, len(svg) / 1024))
