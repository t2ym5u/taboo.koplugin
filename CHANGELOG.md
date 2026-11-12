# Changelog

## [1.8.4] - 2026-11-12

### Changed
- Picks up game-common 1.16.0: games for two readers (new Two readers
  category) and the shared Start / Join dialog.

## [1.8.3] - 2026-11-09

### Fixed
- A language tried once in the game no longer sticks for good: the game
  now starts in KOReader's language (French when KOReader is in French),
  and a language picked in the game holds until KOReader's language changes.
- Changing the deck language in the menu now deals the new language's cards
  straight away, instead of the previous deck until the game was reopened.

## [1.8.2] - 2026-11-04

### Fixed
- A game no longer crashes when an outdated plugin is installed alongside:
  shared modules left behind by an older plugin are replaced by this
  plugin's own copy instead of being used as they are.

## [1.8.1] - 2026-11-04

### Changed
- Uses less memory: the game loads when you open it, not when KOReader
  starts, so it no longer takes memory or startup time while unplayed.

## [1.8.0] - 2026-11-03

### Added
- 100 new English cards, for the themes that had the fewest: Games
  (82 → 108), Medicine (84 → 105), Technology (77 → 100), Transport
  (88 → 111) and Fashion (99 → 106). The English deck now has 2,545 cards.

### Changed
- Cards no longer come back from one evening to the next: the game remembers
  the last 3,000 cards played (per deck language) and deals the ones not seen
  yet first. A card returns only once every card of the chosen themes has
  been played (with the whole 8,402-card French deck, cards older than the
  last 3,000 may come back a little earlier). This also works with your own
  deck file.
- Needs game-common 1.11.0.

## [1.7.0] - 2026-11-02

### Added
- An English deck: 2,445 cards written for English speakers (not translated
  from French) across the same 20 theme ids as the French deck — Sherlock
  Holmes, Big Ben, Fish and chips, Muhammad Ali, Pac-Man… English readers
  used to get the French fallback deck. Theme names in the theme filter now
  follow the deck language.
- The deck language now defaults to KOReader's language (French → French
  deck, anything else → English) until it is picked in Options → Language.

### Changed
- Renamed from "Taboo Party" to "Forbidden Words" (FR « Mots interdits »): it is listed under Tools → Games → Party & quiz, so "Party" said nothing, and the new name is not a trademark. The plugin id and settings are unchanged.
- Family-friendly cards: dropped Pet, Pipi, Caca, Prout and Testicule from
  the French deck, and tapette, branle, dyke, anus, rectum and bruant zizi
  from the fallback deck (`taboo_cards.json`); swapped sexual forbidden
  words (Freud, MeToo, Simone de Beauvoir, Beauvoir, Marilyn Monroe).
- No dictators or mass murderers: removed the French cards Hitler, Adolf
  Hitler, Staline, Mussolini, Mao Zedong, Mao Tsé-Toung, Franco, Francisco
  Franco, Fidel Castro, Gengis Khan, Attila and Nazisme (and nazisme, Staline,
  Mao, Castro, Attila, Gengis from the fallback deck). Where such a name was a
  forbidden word (Hitler on Seconde Guerre mondiale, Staline on URSS and
  Yalta, Kadhafi on Libye, Pinochet on Chili, Gengis on Mongolie…), it was
  swapped for another natural clue; history topics keep their cards. A spec
  keeps these names out of every deck, as a card or a clue.

## [1.6.1] - 2026-11-02

### Changed
- Listed under **Tools → Games**, grouped by category, instead of its own
  entry in the Tools menu (game-common 1.9.1).

## [1.6.0] - 2026-10-30

### Changed
- Redesigned play screen. The card and the team name are sized to the room
  the controls leave, in portrait and landscape. The round buttons sit in a
  full-width action bar on two rows ("+1 Got it", "−1 Buzzed" / "Skip", "End
  round"), since four labels on one row did not fit a small screen.
- The "Settings" submenu is gone. The title-bar menu lists the settings
  directly, with their current value: New game, Language, Teams, Timer,
  Themes (e.g. "Themes: 3/20"), then Rules. It is the same menu during a
  round, which used to offer only Rules.
- "New game" replaces "Reset scores": it sets every score back to zero and
  hands the first turn back to the first team.
- Interface text now follows KOReader's language (with French, Spanish and
  German translations). Only the cards keep their own Language setting.

### Fixed
- The card's word, the forbidden words and the timer came out about twice
  too big on high-DPI readers and ran off the screen edges. They are now
  sized to the screen, and a long word shrinks to fit the card.

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
