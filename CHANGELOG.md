# Changelog

## [1.3.0] - 2026-07-10

### Fixed
- Renamed `taboo_cards.json` → `tabou_cards.json` so the game can find the default English deck
  when no other card file is present.

### Added
- More themed French card packs (`gen/cards_104.json` to `gen/cards_160.json`).
- `tabou_cards_fr.lua` — Lua-format version of the French deck for faster loading.
- `gen/to_lua.py` — utility script to convert JSON card packs to Lua format.

## [1.2.0] - 2026-07-09

### Added
- `tabou_cards_fr.json`: 713 KB of French-language taboo cards (101 themed packs).
- `gen/`: card generation scripts and source JSON packs for reproducible card building.

## [1.1.0] - 2026-07-08

### Added
- FR/EN translation via shared `i18n` module: buttons, menus, and status messages
  now appear in French when KOReader language is set to French.

## [1.0.0]

### Added
- Initial release.
