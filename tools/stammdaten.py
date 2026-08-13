#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Ersetzt Telefonnummer, E-Mail-Domain, Inhaber und UID im ganzen Projekt.

Die Platzhalter stecken in über zwanzig Dateien. Von Hand ersetzt man
zuverlässig eine davon zu wenig – deshalb dieses Skript.

    python3 tools/stammdaten.py --telefon "041 555 12 34"
    python3 tools/stammdaten.py --telefon "041 555 12 34" --anwenden

Ohne --anwenden wird nichts geschrieben, sondern nur gezeigt, was passieren
würde. Das Skript kann mehrfach laufen: es ersetzt jeweils den aktuellen
Stand, nicht nur den ursprünglichen Platzhalter.
"""

import os
import re
import io
import sys
import json
import argparse

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + "/"
MERKER = os.path.join(ROOT, "tools", ".stammdaten.json")

# Was im Auslieferungszustand drinsteht. Wird nach dem ersten Lauf durch die
# Werte in tools/.stammdaten.json abgelöst.
VORGABE = {
    "telefon": "041 123 45 67",
    "tel": "+41411234567",
    "domain": "cleeno-reinigungen.ch",
    "inhaber": "[Vor- und Nachname eintragen]",
    "uid": "[CHE-000.000.000 eintragen]",
}

# Dateien, die durchsucht werden. Bewusst nicht dabei:
#   *.md              – die Anleitungen erklären die Platzhalter, sie dürfen
#                       nicht mitgeändert werden, sonst erklären sie sich selbst
#   tools/vorschau.html – wird ohnehin neu erzeugt
ENDUNGEN = (".html", ".py", ".js", ".xml", ".txt", ".webmanifest")
AUSNAHMEN = {"tools/vorschau.html", "tools/stammdaten.py"}


def dateien():
    for pfad, ordner, namen in os.walk(ROOT):
        ordner[:] = [o for o in ordner if o not in (".git", "fonts")]
        for name in namen:
            if not name.endswith(ENDUNGEN):
                continue
            voll = os.path.join(pfad, name)
            rel = os.path.relpath(voll, ROOT).replace(os.sep, "/")
            if rel in AUSNAHMEN:
                continue
            yield rel, voll


def tel_aus(telefon):
    """«041 555 12 34» → «+41415551234» für href="tel:…»."""
    ziffern = re.sub(r"[^\d+]", "", telefon)
    if ziffern.startswith("+"):
        return ziffern
    if ziffern.startswith("00"):
        return "+" + ziffern[2:]
    if ziffern.startswith("0"):
        return "+41" + ziffern[1:]
    return "+41" + ziffern


def aktuell():
    if os.path.exists(MERKER):
        werte = dict(VORGABE)
        werte.update(json.load(io.open(MERKER, encoding="utf-8")))
        return werte
    return dict(VORGABE)


def main():
    alt = aktuell()

    p = argparse.ArgumentParser(
        description="Stammdaten der Website an einer Stelle pflegen.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="Aktuell hinterlegt:\n" + "\n".join(
            "  %-9s %s" % (k, v) for k, v in sorted(alt.items())))
    p.add_argument("--telefon", help='Anzeigeform, z. B. "041 555 12 34". '
                                     'Die tel:-Form wird daraus abgeleitet.')
    p.add_argument("--tel", help="tel:-Form separat setzen, falls die "
                                "Ableitung nicht passt.")
    p.add_argument("--domain", help='Domain ohne www, z. B. "cleeno.ch". '
                                    "Gilt für Adressen und E-Mail zugleich.")
    p.add_argument("--inhaber", help="Vor- und Nachname für das Impressum.")
    p.add_argument("--uid", help='UID/MWST, z. B. "CHE-123.456.789 MWST".')
    p.add_argument("--anwenden", action="store_true",
                   help="Änderungen wirklich schreiben.")
    a = p.parse_args()

    neu = dict(alt)
    if a.telefon:
        neu["telefon"] = a.telefon
        neu["tel"] = a.tel or tel_aus(a.telefon)
    elif a.tel:
        neu["tel"] = a.tel
    for feld in ("domain", "inhaber", "uid"):
        if getattr(a, feld):
            neu[feld] = getattr(a, feld)

    paare = [(alt[k], neu[k]) for k in neu if alt[k] != neu[k]]
    if not paare:
        p.print_help()
        print("\nNichts zu tun: keine neuen Werte angegeben.")
        return 0

    # Längere Suchbegriffe zuerst, damit «+41411234567» nicht von einer
    # Teilersetzung zerlegt wird.
    paare.sort(key=lambda x: -len(x[0]))

    print("Ersetzungen:")
    for a_, n_ in paare:
        print("  %s  →  %s" % (a_, n_))
    print("")

    gesamt = 0
    betroffen = []
    for rel, voll in sorted(dateien()):
        text = io.open(voll, encoding="utf-8").read()
        original = text
        anzahl = 0
        for a_, n_ in paare:
            anzahl += text.count(a_)
            text = text.replace(a_, n_)
        if text == original:
            continue
        gesamt += anzahl
        betroffen.append((rel, anzahl))
        if a.anwenden:
            io.open(voll, "w", encoding="utf-8").write(text)

    breite = max([len(r) for r, _ in betroffen] or [0])
    for rel, anzahl in betroffen:
        print("  %-*s  %3d" % (breite, rel, anzahl))
    print("\n%d Stellen in %d Dateien." % (gesamt, len(betroffen)))

    if not a.anwenden:
        print("\nProbelauf – nichts geschrieben. Mit --anwenden ausführen.")
        return 0

    json.dump(neu, io.open(MERKER, "w", encoding="utf-8"),
              ensure_ascii=False, indent=2, sort_keys=True)

    # Kontrolle: nichts vom alten Stand darf übrig bleiben.
    rest = []
    for rel, voll in sorted(dateien()):
        text = io.open(voll, encoding="utf-8").read()
        for a_, _ in paare:
            if a_ in text:
                rest.append("%s: %s" % (rel, a_))
    if rest:
        print("\nAchtung, noch vorhanden:")
        for r in rest:
            print("  " + r)
        return 1

    print("\nGeschrieben. Jetzt noch:")
    print("  python3 tools/pruefen.py")
    return 0


if __name__ == "__main__":
    sys.exit(main())
