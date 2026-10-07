# Changelog

## [1.5.14] - 2026-10-07

### Fixed
- The Tools menu entry is translated again. `main.lua` took `_` from
  KOReader's `gettext`, which knows nothing of this plugin's strings, so the
  menu label stayed English while the game's own screen, which goes through
  `i18n`, was translated. `_` now comes from `i18n` here too.
- `i18n_fr.lua` shipped to the device but was never loaded: nothing called
  `i18n.extend()` on it, so the whole table was dead weight. main.lua now
  merges it in before the menu entry is built.


## [1.5.13] - 2026-10-01

### Fixed
- Picks up game-common v1.5.0. Play statistics were recorded under a key no
  tool could match: `ReaderUI`/`FileManager:registerModule()` rewrite a plugin
  instance's `name` to `reader<id>` / `filemanager<id>` right after it is
  built, so this game's sessions were split across two rows and neither
  carried its plugin id. Rows written under the old keys are merged back on
  first read. The same release brings the `stopPlugin()` /
  `deletePluginSettings()` hooks KOReader 2026.07 calls when a plugin is
  deleted from the device (PR #15240).

  No change to this plugin's own code -- it inherits all of it from the
  shared library.

## [1.5.12] - 2026-09-30

### Fixed
- Repair 35 broken cards: 10 listed their own word among the taboos, which
  makes them impossible to describe; 12 listed the same taboo twice, so they
  were quietly easier than the rest; 1 carried six taboos where every other
  card has five; and 11 words appeared twice under two spellings.

### Added
- A spec over the whole 8,419-card deck. The five French pairs that differ
  only by an accent -- Poire/Poiré, Traite/Traité, Granite/Granité,
  Paris/Pâris, Gaia/Gaïa -- are deliberate cards and are listed in the spec
  rather than loosening the check.

### Changed
- README: the plugin ships 8,419 French cards. The old text said there was no
  bundled deck and that you had to supply your own.

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
