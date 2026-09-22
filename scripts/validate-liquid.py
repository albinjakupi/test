#!/usr/bin/env python3
"""Parst alle Liquid-Dateien des Repos mit einem echten Liquid-Parser.

Prueft die Syntax (Tag-Paare, Filter-Argumente, Ausdruecke), nicht das Ergebnis.
Shopify-eigene Tags und Filter werden dafuer neutralisiert bzw. als Attrappen
registriert.

    pip install python-liquid
    python3 scripts/validate-liquid.py
"""
import glob
import re
import sys

from liquid import Environment

SHOPIFY_FILTERS = [
    "money", "money_with_currency", "money_without_currency", "image_url", "image_tag",
    "handle", "handleize", "t", "asset_url", "asset_img_url", "file_url", "stylesheet_tag",
    "script_tag", "json", "within", "link_to", "weight_with_unit", "camelize",
    "highlight", "payment_type_img_url", "placeholder_svg_tag", "inline_asset_content",
    "structured_data", "metafield_tag", "metafield_text", "format_address",
]


def strip_shopify_only(src: str) -> str:
    """Entfernt Konstrukte, die nur die Shopify-Engine kennt."""
    # {% schema %} ... {% endschema %} -> ganz raus (ist JSON, kein Liquid)
    src = re.sub(r"\{%-?\s*schema\s*-?%\}.*?\{%-?\s*endschema\s*-?%\}", "", src, flags=re.S)
    # {% style %} / {% javascript %} umschliessen reines CSS/JS -> nur die Tags entfernen,
    # der Inhalt darin wird weiter geparst (dort stehen ja {{ }}-Ausgaben drin).
    for tag in ("style", "javascript", "stylesheet"):
        src = re.sub(rf"\{{%-?\s*(end)?{tag}\s*-?%\}}", "", src)
    return src


def main() -> int:
    env = Environment()
    for name in SHOPIFY_FILTERS:
        env.filters.setdefault(name, lambda v, *a, **k: v)

    paths = sorted(glob.glob("sections/*.liquid") + glob.glob("snippets/*.liquid")
                   + glob.glob("custom-liquid/*.liquid") + glob.glob("product-block/*.liquid"))
    failures = []
    for path in paths:
        source = strip_shopify_only(open(path, encoding="utf-8").read())
        # Einzelne when-Zweige ohne umgebendes case sind als Datei-Fragment gedacht
        if re.match(r"\s*\{%-?\s*when\b", source):
            source = "{% case block.type %}" + source + "{% endcase %}"
        try:
            env.from_string(source)
            print(f"  OK       {path}")
        except Exception as exc:  # noqa: BLE001 - jede Parser-Ausnahme ist ein Fund
            print(f"  FEHLER   {path}: {type(exc).__name__}: {exc}")
            failures.append(path)

    print()
    if failures:
        print(f"{len(failures)} von {len(paths)} Dateien mit Syntaxfehler.")
        return 1
    print(f"Alle {len(paths)} Liquid-Dateien parsen sauber.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
