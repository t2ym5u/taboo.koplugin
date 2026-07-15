#!/usr/bin/env python3
"""
Fusionne tous les fichiers cards_NNN.json en un seul taboo_cards_fr.json.
Usage : python3 merge.py
Produit : ../taboo_cards_fr.json
"""
import json, os, sys, glob

script_dir = os.path.dirname(os.path.abspath(__file__))
output     = os.path.join(script_dir, "..", "taboo_cards_fr.json")

files = sorted(glob.glob(os.path.join(script_dir, "cards_*.json")))
if not files:
    print("Aucun fichier cards_*.json trouvé.")
    sys.exit(1)

all_cards = []
seen      = set()
dupes     = 0

for path in files:
    with open(path, encoding="utf-8") as f:
        cards = json.load(f)
    for c in cards:
        word = c.get("word", "").strip()
        if not word:
            continue
        key = word.lower()
        if key in seen:
            dupes += 1
            continue
        seen.add(key)
        all_cards.append(c)

with open(output, "w", encoding="utf-8") as f:
    json.dump(all_cards, f, ensure_ascii=False, separators=(",", ":"))

print(f"{len(all_cards)} cartes uniques écrites → {output}")
if dupes:
    print(f"  ({dupes} doublons ignorés)")
