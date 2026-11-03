local _dir = debug.getinfo(1, "S").source:sub(2):match("(.*[/\\])") or "./"

local Blitbuffer      = require("ffi/blitbuffer")
local CenterContainer = require("ui/widget/container/centercontainer")
local DataStorage     = require("datastorage")
local Device          = require("device")
local Font            = require("ui/font")
local FrameContainer  = require("ui/widget/container/framecontainer")
local Geom            = require("ui/geometry")
local HorizontalGroup = require("ui/widget/horizontalgroup")
local HorizontalSpan  = require("ui/widget/horizontalspan")
local InfoMessage     = require("ui/widget/infomessage")
local LineWidget      = require("ui/widget/linewidget")
local RenderText      = require("ui/rendertext")
local Size            = require("ui/size")
local TextBoxWidget   = require("ui/widget/textboxwidget")
local TextWidget      = require("ui/widget/textwidget")
local UIManager       = require("ui/uimanager")
local VerticalGroup   = require("ui/widget/verticalgroup")
local VerticalSpan    = require("ui/widget/verticalspan")
local _               = require("i18n")
local T               = require("ffi/util").template

local MenuHelper  = require("menu_helper")
local ScreenBase  = require("screen_base")

local DeviceScreen = Device.screen

-- ---------------------------------------------------------------------------
-- Text sizing helpers
--
-- Font:getFace() scales its size by the screen DPI, so a size worked out from
-- pixel dimensions has to be divided back first, or every line comes out
-- about twice too big on a 300 dpi reader and runs off the screen edges.
-- ---------------------------------------------------------------------------

local DPI_SCALE = DeviceScreen:scaleBySize(1000) / 1000

local function pxFace(px)
    return Font:getFace("cfont", math.max(8, math.floor(px / DPI_SCALE)))
end

-- One line of text at up to `px` pixels, shrunk until it fits `max_w`.
local function fitLine(text, px, max_w)
    local face = pxFace(px)
    while px > 12 do
        local m = RenderText:sizeUtf8Text(0, max_w * 10, face, text, true, false)
        if m.x <= max_w then break end
        px   = math.floor(px * 0.9)
        face = pxFace(px)
    end
    return TextWidget:new{ text = text, face = face, max_width = max_w }
end

-- A paragraph wrapped to `width`, centred.
local function wrapText(text, face, width)
    return TextBoxWidget:new{ text = text, face = face, width = width, alignment = "center" }
end

local DEFAULT_DURATION = 60
local DEFAULT_NB_TEAMS = 2

-- Display labels for each theme id (used in the theme-picker menu), per deck
-- language: the label follows the deck, not the KOReader UI, so an English
-- deck lists "Food" even under a French interface. The ids are the same in
-- both decks (taboo_cards_fr.lua / taboo_cards_en.lua), so a saved theme
-- selection means the same thing in either. Canonical source: gen/themes.json
-- -- keep this table in sync by hand, the shipped plugin doesn't load gen/.
local THEME_LABELS = {
    fr = {
        action         = "Action & Verbes",
        alimentation   = "Alimentation",
        animaux        = "Animaux",
        arts           = "Arts & Littérature",
        ["cinéma"]     = "Cinéma & Séries",
        fun            = "Fun & Décalé",
        ["géographie"] = "Géographie",
        histoire       = "Histoire",
        jeuxvideo      = "Jeux vidéo",
        maison         = "Maison & Objets",
        ["médecine"]   = "Médecine",
        ["métiers"]    = "Métiers",
        mode           = "Mode & Beauté",
        musique        = "Musique",
        nature         = "Nature",
        sciences       = "Sciences",
        ["société"]    = "Société",
        sports         = "Sports",
        technologies   = "Technologies",
        transports     = "Transports",
    },
    en = {
        action         = "Actions & Verbs",
        alimentation   = "Food & Drink",
        animaux        = "Animals",
        arts           = "Arts & Literature",
        ["cinéma"]     = "Film & TV",
        fun            = "Fun & Quirky",
        ["géographie"] = "Geography & Landmarks",
        histoire       = "History",
        jeuxvideo      = "Games",
        maison         = "Home & Objects",
        ["médecine"]   = "Health & Body",
        ["métiers"]    = "Jobs",
        mode           = "Fashion & Beauty",
        musique        = "Music",
        nature         = "Nature",
        sciences       = "Science",
        ["société"]    = "Society",
        sports         = "Sports",
        technologies   = "Technology",
        transports     = "Transport",
    },
}

-- Preferred display order in the theme menu
local THEME_ORDER = {
    "fun", "action", "alimentation", "animaux", "arts", "cinéma", "géographie",
    "histoire", "jeuxvideo", "maison", "médecine", "métiers", "mode",
    "musique", "nature", "sciences", "société", "sports", "technologies",
    "transports",
}

local GAME_RULES_EN = _([[
Forbidden Words — Rules

Two (or more) teams take turns. Each round, one player from the active team describes as many words as possible in the time limit — without saying any of the forbidden words listed below the main word.

• ✓ +1 = teammates guessed correctly.
• ✗ Buzzed = opponent buzzed (forbidden word said) → −1.
• → Skip = pass, no penalty.

The round ends when the timer runs out or the agreed card count is reached. Teams swap roles each round.
]])

local GAME_RULES_FR = [[
Mots interdits — Règles

Deux équipes (ou plus) jouent à tour de rôle. Chaque manche, un joueur de l'équipe active fait deviner le maximum de mots dans le temps imparti — sans prononcer les mots interdits listés sous le mot principal.

• ✓ +1 = l'équipe a deviné correctement.
• ✗ Grillé = l'adversaire a buzzé (mot interdit prononcé) → −1.
• → Passer = on passe, sans pénalité.

La manche se termine quand le chrono sonne ou quand le nombre de cartes convenu est atteint. Les équipes échangent les rôles à chaque manche.
]]

-- ---------------------------------------------------------------------------
-- JSON loader (fallback path)
-- ---------------------------------------------------------------------------

local function jsonDecode(s)
    local ok, json = pcall(require, "json")
    if ok then
        local ok2, result = pcall(json.decode, s)
        if ok2 then return result end
    end
    return nil
end

-- ---------------------------------------------------------------------------
-- TabooScreen
-- ---------------------------------------------------------------------------

local TabooScreen = ScreenBase:extend{}

function TabooScreen:init()
    -- Deck language. Until the player picks one in the menu it follows the
    -- KOReader UI: French readers get the French deck, everyone else the
    -- English one (there is no other bundled deck).
    self.lang     = self.plugin:getSetting("lang", _.lang() == "fr" and "fr" or "en")
    self.duration = self.plugin:getSetting("duration", DEFAULT_DURATION)
    local nb      = self.plugin:getSetting("nb_teams", DEFAULT_NB_TEAMS)
    self.cards_path = self.plugin:getSetting("cards_path", "")

    -- selected_themes: nil = all; {theme_id = true, ...} = subset
    self.selected_themes = self:_loadThemeSelection()
    self.all_themes      = {}   -- theme_id → card count, filled by _loadCards
    self._raw_data       = nil  -- cached raw data for re-filtering without I/O
    self._data_is_lua    = false

    self.teams = {}
    for i = 1, nb do
        self.teams[i] = { name = self.plugin:getSetting("team_name_" .. i, T(_("Team %1"), i)), score = 0 }
    end
    self.current_team   = 1
    self.phase          = "idle"
    self.cards          = {}
    self.card_index     = 1
    self.time_remaining = self.duration
    self.round_correct  = 0
    self.round_buzzed   = 0

    self:_loadCards()
    ScreenBase.init(self)
end

-- ---------------------------------------------------------------------------
-- Theme-selection persistence (stored as "theme1,theme2,..." or "" = all)
-- ---------------------------------------------------------------------------

function TabooScreen:_loadThemeSelection()
    local saved = self.plugin:getSetting("selected_themes_" .. self.lang, "")
    if not saved or saved == "" then return nil end
    local sel = {}
    for theme in saved:gmatch("[^,]+") do
        sel[theme] = true
    end
    return sel
end

function TabooScreen:_saveThemeSelection()
    if self.selected_themes == nil then
        self.plugin:saveSetting("selected_themes_" .. self.lang, "")
        return
    end
    local parts = {}
    for theme in pairs(self.selected_themes) do
        parts[#parts + 1] = theme
    end
    table.sort(parts)
    self.plugin:saveSetting("selected_themes_" .. self.lang, table.concat(parts, ","))
end

-- ---------------------------------------------------------------------------
-- Lua-file loader (fast path: theme-keyed dict)
-- ---------------------------------------------------------------------------

function TabooScreen:_tryLoadLua(path)
    local f = io.open(path, "r")
    if not f then return nil end
    f:close()
    local chunk, err = loadfile(path)
    if not chunk then return nil end
    local ok, data = pcall(chunk)
    if not ok or type(data) ~= "table" then return nil end
    -- Verify it is a theme-keyed dict (not a flat array)
    for k, v in pairs(data) do
        if type(k) ~= "string" or type(v) ~= "table" then return nil end
        break
    end
    return data
end

-- ---------------------------------------------------------------------------
-- Theme filtering
-- ---------------------------------------------------------------------------

-- data is {theme_id = [{word,forbidden,difficulty}, ...], ...}
function TabooScreen:_filterByTheme(data)
    local sel   = self.selected_themes
    local cards = {}
    for theme, theme_cards in pairs(data) do
        if sel == nil or sel[theme] then
            for _, c in ipairs(theme_cards) do
                cards[#cards + 1] = c
            end
        end
    end
    return cards
end

-- data is a flat array [{word,forbidden,theme,difficulty}, ...]
function TabooScreen:_filterByThemeFlat(data)
    local sel = self.selected_themes
    if sel == nil then return data end
    local cards = {}
    for _, c in ipairs(data) do
        if sel[c.theme or "autres"] then
            cards[#cards + 1] = c
        end
    end
    return cards
end

-- Re-filter from cached raw data (called after theme selection changes)
function TabooScreen:_reloadCards()
    if self._raw_data == nil then return end
    if self._data_is_lua then
        self.cards = self:_filterByTheme(self._raw_data)
    else
        self.cards = self:_filterByThemeFlat(self._raw_data)
    end
    self:_shuffleCards()
end

-- ---------------------------------------------------------------------------
-- Card loading (Lua first, JSON fallback)
-- ---------------------------------------------------------------------------

function TabooScreen:_loadCards()
    local docs = DataStorage:getDataDir()

    -- "tabou_cards*" paths are kept as a fallback so decks players already
    -- placed in their documents folder (before the plugin was renamed from
    -- tabou.koplugin to taboo.koplugin) keep loading.
    local lua_paths = {
        docs  .. "/taboo_cards_" .. self.lang .. ".lua",
        docs  .. "/tabou_cards_" .. self.lang .. ".lua",
        _dir  .. "taboo_cards_" .. self.lang .. ".lua",
    }
    local json_paths = {
        docs  .. "/taboo_cards_" .. self.lang .. ".json",
        docs  .. "/tabou_cards_" .. self.lang .. ".json",
        docs  .. "/taboo_cards.json",
        docs  .. "/tabou_cards.json",
        _dir  .. "taboo_cards_" .. self.lang .. ".json",
        _dir  .. "taboo_cards.json",
    }
    if self.cards_path ~= "" then
        if self.cards_path:match("%.lua$") then
            table.insert(lua_paths,  1, self.cards_path)
        else
            table.insert(json_paths, 1, self.cards_path)
        end
    end

    -- Try Lua (theme-keyed dict)
    for _, path in ipairs(lua_paths) do
        local data = self:_tryLoadLua(path)
        if data then
            self._raw_data    = data
            self._data_is_lua = true
            self.cards_path   = path
            self.all_themes   = {}
            for theme, tc in pairs(data) do
                self.all_themes[theme] = #tc
            end
            self.cards = self:_filterByTheme(data)
            self:_shuffleCards()
            return
        end
    end

    -- Fallback: flat JSON array
    for _, path in ipairs(json_paths) do
        local f = io.open(path, "r")
        if f then
            local content = f:read("*all")
            f:close()
            local data = jsonDecode(content)
            if type(data) == "table" and #data > 0 then
                self._raw_data    = data
                self._data_is_lua = false
                self.cards_path   = path
                self.all_themes   = {}
                for _, card in ipairs(data) do
                    local t = card.theme or "autres"
                    self.all_themes[t] = (self.all_themes[t] or 0) + 1
                end
                self.cards = self:_filterByThemeFlat(data)
                self:_shuffleCards()
                return
            end
        end
    end

    self.cards      = {}
    self._raw_data  = nil
    self.all_themes = {}
end

function TabooScreen:_shuffleCards()
    local c = self.cards
    for i = #c, 2, -1 do
        local j = math.random(i)
        c[i], c[j] = c[j], c[i]
    end
    self.card_index = 1
end

function TabooScreen:_currentCard()
    if #self.cards == 0 then return nil end
    if self.card_index > #self.cards then
        self:_shuffleCards()
    end
    return self.cards[self.card_index]
end

-- ---------------------------------------------------------------------------
-- Timer
-- ---------------------------------------------------------------------------

function TabooScreen:_startCountdown()
    self._tick_gen = (self._tick_gen or 0) + 1
    local gen = self._tick_gen
    UIManager:scheduleIn(1, function() self:_onTick(gen) end)
end

function TabooScreen:_stopCountdown()
    self._tick_gen = (self._tick_gen or 0) + 1
end

function TabooScreen:_onTick(gen)
    if gen ~= self._tick_gen then return end
    self.time_remaining = math.max(0, self.time_remaining - 1)
    if self.timer_widget then
        self.timer_widget:setText(self:_timerText())
        UIManager:setDirty(self, function() return "fast", self.dimen end)
    end
    if self.time_remaining <= 0 then
        self:_onTimerEnd()
    else
        UIManager:scheduleIn(1, function() self:_onTick(gen) end)
    end
end

function TabooScreen:_timerText()
    local m = math.floor(self.time_remaining / 60)
    local s = self.time_remaining % 60
    return string.format("%d:%02d", m, s)
end

function TabooScreen:_onTimerEnd()
    self:_stopCountdown()
    self.phase = "idle"
    local delta = self.round_correct - self.round_buzzed
    self.teams[self.current_team].score = self.teams[self.current_team].score + delta
    self.current_team = (self.current_team % #self.teams) + 1
    self:buildLayout()
    UIManager:setDirty(self, function() return "ui", self.dimen end)
    local msg = T(_("Time's up! +%1 −%2 = %3 points"), self.round_correct, self.round_buzzed,
        string.format("%+d", delta))
    UIManager:show(InfoMessage:new{ text = msg, timeout = 3 })
end

-- ---------------------------------------------------------------------------
-- Game actions
-- ---------------------------------------------------------------------------

function TabooScreen:onStartRound()
    if #self.cards == 0 then
        UIManager:show(InfoMessage:new{
            text = T(_("No cards loaded.\n\nCopy %1\nto KOReader's documents folder."),
                "taboo_cards_" .. self.lang .. ".lua (.json)"),
            timeout = 6,
        })
        return
    end
    self.time_remaining = self.duration
    self.round_correct  = 0
    self.round_buzzed   = 0
    self.phase          = "playing"
    self:buildLayout()
    UIManager:setDirty(self, function() return "ui", self.dimen end)
    self:_startCountdown()
end

function TabooScreen:onCorrect()
    self.round_correct = self.round_correct + 1
    self.card_index    = self.card_index + 1
    self:buildLayout()
    UIManager:setDirty(self, function() return "ui", self.dimen end)
end

function TabooScreen:onBuzzed()
    self.round_buzzed = self.round_buzzed + 1
    self.card_index   = self.card_index + 1
    self:buildLayout()
    UIManager:setDirty(self, function() return "ui", self.dimen end)
end

function TabooScreen:onSkip()
    self.card_index = self.card_index + 1
    self:buildLayout()
    UIManager:setDirty(self, function() return "ui", self.dimen end)
end

function TabooScreen:onStopRound()
    self:_onTimerEnd()
end

-- ---------------------------------------------------------------------------
-- Settings
-- ---------------------------------------------------------------------------

function TabooScreen:_durationLabel(dur)
    return string.format("%d:%02d", math.floor(dur / 60), dur % 60)
end

-- "Themes: All" or "Themes: 3/20" for the title-bar menu.
function TabooScreen:_themesMenuText()
    if self.selected_themes == nil then return _("Themes: All") end
    local total, sel = 0, 0
    for tid in pairs(self.all_themes) do
        total = total + 1
        if self.selected_themes[tid] then sel = sel + 1 end
    end
    return T(_("Themes: %1"), sel .. "/" .. total)
end

function TabooScreen:openLangMenu()
    MenuHelper.openPickerMenu{
        title      = _("Language"),
        items      = { { id = "fr", text = "Français" }, { id = "en", text = "English" } },
        current_id = self.lang,
        parent     = self,
        on_select  = function(lang)
            self.lang = lang
            self.plugin:saveSetting("lang", lang)
            self.selected_themes = self:_loadThemeSelection()
            self:_loadCards()
            self:buildLayout()
            UIManager:setDirty(self, function() return "ui", self.dimen end)
        end,
    }
end

-- ---------------------------------------------------------------------------
-- Theme-picker menu (multi-select, re-opens after each toggle)
-- ---------------------------------------------------------------------------

function TabooScreen:openThemeMenu()
    -- Build sorted list of themes that actually exist in the loaded data
    local available = {}
    local in_order  = {}
    for _, tid in ipairs(THEME_ORDER) do
        if self.all_themes[tid] then
            available[#available + 1] = tid
            in_order[tid] = true
        end
    end
    for tid in pairs(self.all_themes) do
        if not in_order[tid] then
            available[#available + 1] = tid
        end
    end

    if #available == 0 then
        UIManager:show(InfoMessage:new{
            text    = _("No themes available.\nLoad a card file first."),
            timeout = 3,
        })
        return
    end

    local all_selected = (self.selected_themes == nil)

    -- Build item list
    local items = {}
    items[#items + 1] = {
        id   = "__all__",
        text = (all_selected and "★ " or "  ")
               .. _("All themes")
               .. string.format("  (%d)", #self.cards),
    }
    for _, tid in ipairs(available) do
        local labels = THEME_LABELS[self.lang] or THEME_LABELS.en
        local label = labels[tid] or tid
        local count = self.all_themes[tid] or 0
        local sel   = all_selected or (self.selected_themes[tid] == true)
        items[#items + 1] = {
            id   = tid,
            text = (sel and "✓ " or "○ ") .. label
                   .. string.format("  (%d)", count),
        }
    end

    MenuHelper.openPickerMenu{
        title     = _("Themes"),
        items     = items,
        parent    = self,
        on_select = function(id)
            if id == "__all__" then
                self.selected_themes = nil
            else
                if self.selected_themes == nil then
                    -- Was "all" → keep every theme except the one just tapped
                    self.selected_themes = {}
                    for _, tid in ipairs(available) do
                        if tid ~= id then
                            self.selected_themes[tid] = true
                        end
                    end
                else
                    -- Toggle the tapped theme
                    if self.selected_themes[id] then
                        self.selected_themes[id] = nil
                    else
                        self.selected_themes[id] = true
                    end
                    -- Collapse back to nil if every theme is now checked
                    local all_on = true
                    for _, tid in ipairs(available) do
                        if not self.selected_themes[tid] then
                            all_on = false
                            break
                        end
                    end
                    if all_on then self.selected_themes = nil end
                end
            end
            self:_reloadCards()
            self:_saveThemeSelection()
            self:buildLayout()
            UIManager:setDirty(self, function() return "ui", self.dimen end)
            -- Re-open to reflect the new state
            self:openThemeMenu()
        end,
    }
end

function TabooScreen:openTeamsMenu()
    local items = {}
    for n = 2, 6 do
        items[#items + 1] = { id = n, text = T(_("%1 teams"), n) }
    end
    MenuHelper.openPickerMenu{
        title      = _("Teams"),
        items      = items,
        current_id = #self.teams,
        parent     = self,
        on_select  = function(n)
            self.plugin:saveSetting("nb_teams", n)
            while #self.teams < n do
                local i = #self.teams + 1
                self.teams[i] = { name = T(_("Team %1"), i), score = 0 }
            end
            while #self.teams > n do table.remove(self.teams) end
            if self.current_team > #self.teams then self.current_team = 1 end
            self:buildLayout()
            UIManager:setDirty(self, function() return "ui", self.dimen end)
        end,
    }
end

function TabooScreen:openDurationMenu()
    local items = {}
    for _i, d in ipairs({ 30, 45, 60, 90, 120 }) do
        items[#items + 1] = { id = d, text = self:_durationLabel(d) }
    end
    MenuHelper.openPickerMenu{
        title      = _("Timer"),
        items      = items,
        current_id = self.duration,
        parent     = self,
        on_select  = function(dur)
            self.duration = dur
            self.plugin:saveSetting("duration", dur)
        end,
    }
end

-- New game: scores back to zero, first team to play.
function TabooScreen:onNewGame()
    self:_stopCountdown()
    for _i, t in ipairs(self.teams) do t.score = 0 end
    self.current_team = 1
    self.phase        = "idle"
    self:buildLayout()
    UIManager:setDirty(self, function() return "ui", self.dimen end)
end

-- ---------------------------------------------------------------------------
-- Layout
-- ---------------------------------------------------------------------------

function TabooScreen:buildLayout()
    if self.phase == "idle" then
        self:_buildIdleLayout()
    else
        self:_buildPlayLayout()
    end
    self[1] = self.layout
    self:updateStatus()
end

function TabooScreen:_titleBar()
    return self:buildTitleBar(_("Forbidden Words"), function()
        return {
            { text = _("New game"), callback = function() self:onNewGame() end },
            { text = T(_("Language: %1"), self.lang:upper()), callback = function() self:openLangMenu() end },
            { text = T(_("Teams: %1"), #self.teams),          callback = function() self:openTeamsMenu() end },
            { text = T(_("Timer: %1"), self:_durationLabel(self.duration)),
              callback = function() self:openDurationMenu() end },
            { text = self:_themesMenuText(), callback = function() self:openThemeMenu() end },
            self:makeRulesButtonConfig(GAME_RULES_EN, GAME_RULES_FR),
        }
    end)
end

function TabooScreen:_buildIdleLayout()
    local team  = self.teams[self.current_team]

    local title_bar = self:_titleBar()
    local controls  = self:_buildControls({
        { text = _("Start round"),
          callback = function() self:onStartRound() end },
    })
    local bw, bh = self:getBoardBudget(title_bar, controls)
    local short  = math.min(bw, bh)
    local vs     = Size.span.vertical_large

    -- Card / theme info
    local deck_line
    if #self.cards == 0 then
        deck_line = "⚠ " .. T(_("No cards loaded.\n\nCopy %1\nto KOReader's documents folder."),
            "taboo_cards_" .. self.lang .. ".lua (.json)")
    elseif self.selected_themes == nil then
        local nb_themes = 0
        for _ in pairs(self.all_themes) do nb_themes = nb_themes + 1 end
        deck_line = T(_("All themes (%1) · %2 cards"), nb_themes, #self.cards)
    else
        local nb_sel = 0
        for _ in pairs(self.selected_themes) do nb_sel = nb_sel + 1 end
        deck_line = T(_("%1 theme(s) selected · %2 cards"), nb_sel, #self.cards)
    end

    self.timer_widget = nil
    local content = VerticalGroup:new{
        align = "center",
        -- Active team
        fitLine(team.name:upper(), short * 0.14, bw),
        VerticalSpan:new{ width = vs },
        wrapText(_("It's your turn to describe"),
            Font:getFace("infofont"), bw),
        VerticalSpan:new{ width = vs * 4 },
        wrapText(deck_line, Font:getFace("smallinfofont"), bw),
    }
    self:_placeLayout(title_bar, content, controls)
end

function TabooScreen:_buildPlayLayout()
    local card  = self:_currentCard()

    -- Two rows: four labels on one row do not fit a small screen.
    local title_bar = self:_titleBar()
    local controls  = self:_buildControls({
        {
            { text = "✓  " .. _("+1 Got it"),
              callback = function() self:onCorrect() end },
            { text = "✗  " .. _("−1 Buzzed"),
              callback = function() self:onBuzzed() end },
        },
        {
            { text = "→  " .. _("Skip"),
              callback = function() self:onSkip() end },
            { text = "■  " .. _("End round"),
              callback = function() self:onStopRound() end },
        },
    })
    local bw, bh = self:getBoardBudget(title_bar, controls)
    local short  = math.min(bw, bh)
    local vs     = Size.span.vertical_large

    self.timer_widget = TextWidget:new{
        text = self:_timerText(),
        face = pxFace(short * 0.12),
    }

    local frame_pad = Size.padding.large
    local inner_w   = bw - 2 * (frame_pad + Size.border.window)
    local card_group
    if not card then
        card_group = wrapText(_("No cards."), Font:getFace("infofont"), inner_w)
    else
        local word = card.word or card[1] or "?"
        local forbidden = card.forbidden or card[2] or {}
        local forb_lines = {}
        for _, fw in ipairs(forbidden) do
            forb_lines[#forb_lines + 1] = "× " .. fw
        end

        card_group = VerticalGroup:new{
            align = "center",
            -- Word: as big as the width allows
            fitLine(word, short * 0.13, inner_w),
            VerticalSpan:new{ width = vs },
            LineWidget:new{
                background = Blitbuffer.COLOR_DARK_GRAY,
                dimen      = Geom:new{ w = math.floor(inner_w * 0.6), h = Size.line.medium },
            },
            VerticalSpan:new{ width = vs },
            wrapText(table.concat(forb_lines, "\n"), pxFace(short * 0.06), inner_w),
        }
    end

    local card_frame = FrameContainer:new{
        padding = frame_pad,
        margin  = 0,
        CenterContainer:new{
            dimen = Geom:new{ w = inner_w, h = card_group:getSize().h },
            card_group,
        },
    }

    local content = VerticalGroup:new{
        align = "center",
        self.timer_widget,
        VerticalSpan:new{ width = vs },
        TextWidget:new{
            text = string.format("✓ %d   ✗ %d", self.round_correct, self.round_buzzed),
            face = Font:getFace("smallinfofont"),
        },
        VerticalSpan:new{ width = vs * 2 },
        card_frame,
    }
    self:_placeLayout(title_bar, content, controls)
end

-- Status line + action bar, built before the content so the content can be
-- sized from what they leave over (getBoardBudget).
function TabooScreen:_buildControls(rows)
    self.status_text:setMaxWidth(self:getControlsWidth())
    return VerticalGroup:new{
        align = "center",
        self.status_text,
        VerticalSpan:new{ width = Size.span.vertical_large },
        self:buildActionBar(rows),
    }
end

function TabooScreen:_placeLayout(title_bar, content, controls)
    if self:isLandscape() then
        self:buildLandscapeLayout(title_bar, HorizontalGroup:new{
            align = "center",
            content,
            HorizontalSpan:new{ width = self:getGutter() },
            controls,
        })
    else
        self:buildPortraitLayout(title_bar, content,
            VerticalGroup:new{ align = "center", controls, VerticalSpan:new{ width = self:getGutter() } })
    end
end

-- "Team 1: 3 · Team 2: 1"
function TabooScreen:_scoreStatus(list)
    local parts = {}
    for _i, t in ipairs(list) do
        parts[#parts + 1] = T(_("%1: %2"), t.name, t.score)
    end
    return self:joinStatus((table.unpack or unpack)(parts))
end

-- ---------------------------------------------------------------------------
-- Status bar
-- ---------------------------------------------------------------------------

function TabooScreen:updateStatus(msg)
    if msg then ScreenBase.updateStatus(self, msg); return end
    ScreenBase.updateStatus(self, self:_scoreStatus(self.teams))
end

function TabooScreen:onClose()
    self:_stopCountdown()
    ScreenBase.onClose(self)
end

return TabooScreen
