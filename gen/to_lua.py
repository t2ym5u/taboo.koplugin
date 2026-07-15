#!/usr/bin/env python3
"""Convert taboo_cards_fr.json → taboo_cards_fr.lua (theme-keyed dict).

The Lua format is 5-10× faster to load on e-readers than JSON because
loadfile() uses the native C Lua parser instead of a pure-Lua JSON decoder.
The 'theme' field is dropped from each card (it becomes the dict key).
"""
import json, os

THEME_ORDER = [
    "fun", "alimentation", "animaux", "arts", "géographie",
    "histoire", "maison", "médecine", "métiers", "mode",
    "musique", "nature", "sciences", "société", "sports", "technologies",
]

def lua_str(s):
    s = s.replace("\\", "\\\\").replace('"', '\\"').replace("\n", "\\n")
    return '"' + s + '"'

script_dir = os.path.dirname(os.path.abspath(__file__))
src = os.path.join(script_dir, "..", "taboo_cards_fr.json")
dst = os.path.join(script_dir, "..", "taboo_cards_fr.lua")

with open(src, encoding="utf-8") as f:
    cards = json.load(f)

# Group by theme, preserve declaration order then alpha for unknowns
themes = {}
for card in cards:
    t = card.get("theme", "autres")
    themes.setdefault(t, []).append(card)

ordered_keys = [t for t in THEME_ORDER if t in themes]
ordered_keys += sorted(k for k in themes if k not in THEME_ORDER)

with open(dst, "w", encoding="utf-8") as f:
    f.write("return {\n")
    for theme in ordered_keys:
        f.write(f"  [{lua_str(theme)}]={{\n")
        for card in themes[theme]:
            word      = lua_str(card["word"])
            forbidden = "{" + ",".join(lua_str(w) for w in card.get("forbidden", [])) + "}"
            diff      = lua_str(card.get("difficulty", "medium"))
            f.write(f"    {{word={word},forbidden={forbidden},difficulty={diff}}},\n")
        f.write("  },\n")
    f.write("}\n")

total = sum(len(v) for v in themes.values())
print(f"{total} cartes → {os.path.relpath(dst)}")
for t in ordered_keys:
    print(f"  {t:<16} {len(themes[t]):>4} cartes")
