# Changelog

## [1.5.0] - 2026-07-15

### Added
- `gen/CARD_FORMAT.md` — documents the card JSON schema and includes a
  ready-to-use AI prompt template for generating new card batches.
- `gen/themes.json` — canonical theme list (id + French label), extracted
  from what was previously duplicated between `screen.lua` and
  `gen/to_lua.py`. `to_lua.py` now reads theme order from this file.
- 3 new theme ids: `transports`, `jeuxvideo`, `cinéma` (no cards tagged
  with them yet — they were already anticipated as sub-themes in
  `gen/themes.md` but never promoted to a top-level theme).

## [1.4.0] - 2026-07-15

### Changed
- Plugin renamed `tabou.koplugin` → `taboo.koplugin` (repo, id, class names, card
  file naming: `tabou_cards*` → `taboo_cards*`). The game still reads
  `tabou_cards*` files from KOReader's documents folder as a fallback, so decks
  placed there before this rename keep working.

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
