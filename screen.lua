local _dir = debug.getinfo(1, "S").source:sub(2):match("(.*[/\\])") or "./"

local ButtonTable     = require("ui/widget/buttontable")
local DataStorage     = require("datastorage")
local Device          = require("device")
local Font            = require("ui/font")
local FrameContainer  = require("ui/widget/container/framecontainer")
local InfoMessage     = require("ui/widget/infomessage")
local Size            = require("ui/size")
local TextBoxWidget   = require("ui/widget/textboxwidget")
local TextWidget      = require("ui/widget/textwidget")
local UIManager       = require("ui/uimanager")
local VerticalGroup   = require("ui/widget/verticalgroup")
local VerticalSpan    = require("ui/widget/verticalspan")
local _               = require("i18n")

local MenuHelper  = require("menu_helper")
local ScreenBase  = require("screen_base")

local DeviceScreen = Device.screen

local DEFAULT_DURATION = 60
local DEFAULT_NB_TEAMS = 2

-- Display labels for each theme id (used in the theme-picker menu).
-- Canonical source: gen/themes.json — keep this table in sync by hand,
-- the shipped plugin doesn't load gen/ at runtime.
local THEME_LABELS = {
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
}

-- Preferred display order in the theme menu
local THEME_ORDER = {
    "fun", "alimentation", "animaux", "arts", "cinéma", "géographie",
    "histoire", "jeuxvideo", "maison", "médecine", "métiers", "mode",
    "musique", "nature", "sciences", "société", "sports", "technologies",
    "transports",
}

local GAME_RULES_EN = _([[
Taboo Party — Rules

Two (or more) teams take turns. Each round, one player from the active team describes as many words as possible in the time limit — without saying any of the forbidden words listed below the main word.

• ✓ +1 = teammates guessed correctly.
• ✗ Buzzed = opponent buzzed (forbidden word said) → −1.
• → Skip = pass, no penalty.

The round ends when the timer runs out or the agreed card count is reached. Teams swap roles each round.
]])

local GAME_RULES_FR = [[
Taboo Party — Règles

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
    self.lang     = self.plugin:getSetting("lang", "fr")
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
        local default = self.lang == "fr" and ("Équipe " .. i) or ("Team " .. i)
        self.teams[i] = { name = self.plugin:getSetting("team_name_" .. i, default), score = 0 }
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
    local is_fr = self.lang == "fr"
    local msg = is_fr
        and string.format("Temps écoulé ! +%d −%d = %+d points", self.round_correct, self.round_buzzed, delta)
        or  string.format("Time's up! +%d −%d = %+d points",     self.round_correct, self.round_buzzed, delta)
    UIManager:show(InfoMessage:new{ text = msg, timeout = 3 })
end

-- ---------------------------------------------------------------------------
-- Game actions
-- ---------------------------------------------------------------------------

function TabooScreen:onStartRound()
    if #self.cards == 0 then
        local is_fr = self.lang == "fr"
        UIManager:show(InfoMessage:new{
            text = is_fr
                and "Aucune carte chargée.\n\nCopiez taboo_cards_fr.lua (ou .json)\ndans le dossier documents de KOReader."
                or  "No cards loaded.\n\nCopy taboo_cards_en.lua (or .json)\nto KOReader's documents folder.",
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

function TabooScreen:openOptionsMenu()
    local is_fr = self.lang == "fr"
    local items = {
        { id = "lang",     text = is_fr and "Langue…"                   or "Language…" },
        { id = "themes",   text = is_fr and "Thèmes…"                   or "Themes…" },
        { id = "teams",    text = is_fr and "Nombre d'équipes…"         or "Number of teams…" },
        { id = "duration", text = is_fr and "Durée du chrono…"          or "Timer duration…" },
        { id = "reset",    text = is_fr and "Remettre les scores à zéro" or "Reset scores" },
    }
    MenuHelper.openPickerMenu{
        title     = "Options",
        items     = items,
        parent    = self,
        on_select = function(id)
            if     id == "lang"     then self:openLangMenu()
            elseif id == "themes"   then self:openThemeMenu()
            elseif id == "teams"    then self:openTeamsMenu()
            elseif id == "duration" then self:openDurationMenu()
            elseif id == "reset"    then self:onResetScores()
            end
        end,
    }
end

function TabooScreen:openLangMenu()
    MenuHelper.openPickerMenu{
        title      = "Language / Langue",
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
    local is_fr = self.lang == "fr"

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
            text    = is_fr
                and "Aucun thème disponible.\nChargez d'abord un fichier de cartes."
                or  "No themes available.\nLoad a card file first.",
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
               .. (is_fr and "Tous les thèmes" or "All themes")
               .. string.format("  (%d)", #self.cards),
    }
    for _, tid in ipairs(available) do
        local label = THEME_LABELS[tid] or tid
        local count = self.all_themes[tid] or 0
        local sel   = all_selected or (self.selected_themes[tid] == true)
        items[#items + 1] = {
            id   = tid,
            text = (sel and "✓ " or "○ ") .. label
                   .. string.format("  (%d)", count),
        }
    end

    MenuHelper.openPickerMenu{
        title     = is_fr and "Thèmes" or "Themes",
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
    local is_fr = self.lang == "fr"
    local items = {}
    for n = 2, 6 do
        items[#items + 1] = { id = n, text = n .. " " .. (is_fr and "équipes" or "teams") }
    end
    MenuHelper.openPickerMenu{
        title      = is_fr and "Équipes" or "Teams",
        items      = items,
        current_id = #self.teams,
        parent     = self,
        on_select  = function(n)
            self.plugin:saveSetting("nb_teams", n)
            while #self.teams < n do
                local i = #self.teams + 1
                self.teams[i] = { name = (self.lang == "fr" and "Équipe " or "Team ") .. i, score = 0 }
            end
            while #self.teams > n do table.remove(self.teams) end
            if self.current_team > #self.teams then self.current_team = 1 end
            self:buildLayout()
            UIManager:setDirty(self, function() return "ui", self.dimen end)
        end,
    }
end

function TabooScreen:openDurationMenu()
    local items = {
        { id = 30,  text = "0:30" }, { id = 45,  text = "0:45" },
        { id = 60,  text = "1:00" }, { id = 90,  text = "1:30" },
        { id = 120, text = "2:00" },
    }
    MenuHelper.openPickerMenu{
        title      = self.lang == "fr" and "Durée" or "Duration",
        items      = items,
        current_id = self.duration,
        parent     = self,
        on_select  = function(dur)
            self.duration = dur
            self.plugin:saveSetting("duration", dur)
        end,
    }
end

function TabooScreen:onResetScores()
    for _, t in ipairs(self.teams) do t.score = 0 end
    self.current_team = 1
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

function TabooScreen:_buildIdleLayout()
    local sw    = DeviceScreen:getWidth()
    local sh    = DeviceScreen:getHeight()
    local is_fr = self.lang == "fr"
    local team  = self.teams[self.current_team]

    local btn_w = math.floor(sw * 0.92)
    local buttons = ButtonTable:new{
        shrink_unneeded_width = true,
        width   = btn_w,
        buttons = {{
            { text = is_fr and "Commencer la manche" or "Start round",
              callback = function() self:onStartRound() end },
            { text = "Options", callback = function() self:openOptionsMenu() end },
            self:makeRulesButtonConfig(GAME_RULES_EN, GAME_RULES_FR),
            self:makeCloseButtonConfig(),
        }},
    }

    -- Scores
    local score_parts = {}
    for _, t in ipairs(self.teams) do
        score_parts[#score_parts + 1] = t.name .. " : " .. t.score
    end
    local score_w = TextWidget:new{
        text = table.concat(score_parts, "   "),
        face = Font:getFace("smallinfofont"),
    }

    -- Active team
    local team_fs = math.max(24, math.floor(math.min(sw, sh) * 0.08))
    local team_w  = TextWidget:new{
        text = team.name:upper(),
        face = Font:getFace("cfont", team_fs),
    }

    local sub_w = TextWidget:new{
        text = is_fr and "C'est votre tour de faire deviner" or "It's your turn to describe",
        face = Font:getFace("smallinfofont"),
    }

    -- Card / theme info
    local deck_line
    if #self.cards == 0 then
        deck_line = is_fr and "⚠ Aucune carte — voir Options" or "⚠ No cards — see Options"
    elseif self.selected_themes == nil then
        local nb_themes = 0
        for _ in pairs(self.all_themes) do nb_themes = nb_themes + 1 end
        deck_line = is_fr
            and string.format("Tous les thèmes (%d) · %d cartes", nb_themes, #self.cards)
            or  string.format("All themes (%d) · %d cards",       nb_themes, #self.cards)
    else
        local nb_sel = 0
        for _ in pairs(self.selected_themes) do nb_sel = nb_sel + 1 end
        deck_line = is_fr
            and string.format("%d thème(s) sélectionné(s) · %d cartes", nb_sel, #self.cards)
            or  string.format("%d theme(s) selected · %d cards",         nb_sel, #self.cards)
    end
    local deck_w = TextWidget:new{
        text = deck_line,
        face = Font:getFace("smallinfofont"),
    }

    local vs  = VerticalSpan:new{ width = Size.span.vertical_large }
    local vs2 = VerticalSpan:new{ width = Size.span.vertical_large * 4 }

    self.timer_widget = nil
    local content = VerticalGroup:new{
        align = "center",
        score_w,
        vs2,
        team_w,
        vs,
        sub_w,
        vs2,
        deck_w,
    }
    self:buildPortraitLayout(nil, content, buttons)
end

function TabooScreen:_buildPlayLayout()
    local sw    = DeviceScreen:getWidth()
    local sh    = DeviceScreen:getHeight()
    local is_fr = self.lang == "fr"
    local card  = self:_currentCard()

    local btn_w = math.floor(sw * 0.92)
    local action_btns = ButtonTable:new{
        shrink_unneeded_width = true,
        width   = btn_w,
        buttons = {{
            { text = is_fr and "✓  +1 Trouvé" or "✓  +1 Got it",
              callback = function() self:onCorrect() end },
            { text = is_fr and "✗  −1 Grillé"  or "✗  −1 Buzzed",
              callback = function() self:onBuzzed() end },
            { text = is_fr and "→  Passer"     or "→  Skip",
              callback = function() self:onSkip() end },
            { text = is_fr and "■  Fin de manche" or "■  End round",
              callback = function() self:onStopRound() end },
        }},
    }

    local timer_fs = math.max(20, math.floor(math.min(sw, sh) * 0.09))
    self.timer_widget = TextWidget:new{
        text = self:_timerText(),
        face = Font:getFace("cfont", timer_fs),
    }

    local stats_w = TextWidget:new{
        text = string.format("✓ %d   ✗ %d", self.round_correct, self.round_buzzed),
        face = Font:getFace("smallinfofont"),
    }

    local card_group
    if not card then
        card_group = TextWidget:new{
            text = is_fr and "Aucune carte." or "No cards.",
            face = Font:getFace("cfont", 24),
        }
    else
        local word    = card.word or card[1] or "?"
        local wlen    = #word
        local word_fs = wlen > 12 and math.floor(math.min(sw, sh) * 0.08)
                     or wlen > 8  and math.floor(math.min(sw, sh) * 0.10)
                     or               math.floor(math.min(sw, sh) * 0.13)
        word_fs = math.max(22, math.min(word_fs, 110))

        local word_w = TextWidget:new{
            text = word,
            face = Font:getFace("cfont", word_fs),
        }

        local forbidden = card.forbidden or card[2] or {}
        local forb_lines = {}
        for _, fw in ipairs(forbidden) do
            forb_lines[#forb_lines + 1] = "× " .. fw
        end
        local forb_w = TextBoxWidget:new{
            text  = table.concat(forb_lines, "\n"),
            face  = Font:getFace("cfont", math.max(16, math.floor(math.min(sw, sh) * 0.045))),
            width = math.floor(sw * 0.7),
        }

        local sep_w = TextWidget:new{
            text = string.rep("─", 24),
            face = Font:getFace("smallinfofont"),
        }

        card_group = VerticalGroup:new{
            align = "center",
            word_w,
            VerticalSpan:new{ width = Size.span.vertical_large },
            sep_w,
            VerticalSpan:new{ width = Size.span.vertical_large },
            forb_w,
        }
    end

    local card_frame = FrameContainer:new{
        padding = Size.padding.large,
        margin  = Size.margin.default,
        card_group,
    }

    local vs  = VerticalSpan:new{ width = Size.span.vertical_large }
    local vs2 = VerticalSpan:new{ width = Size.span.vertical_large * 2 }

    local content = VerticalGroup:new{
        align = "center",
        self.timer_widget,
        vs,
        stats_w,
        vs2,
        card_frame,
    }
    self:buildPortraitLayout(nil, content, action_btns)
end

-- ---------------------------------------------------------------------------
-- Status bar
-- ---------------------------------------------------------------------------

function TabooScreen:updateStatus(msg)
    if msg then ScreenBase.updateStatus(self, msg); return end
    local parts = {}
    for _, t in ipairs(self.teams) do
        parts[#parts + 1] = t.name .. " " .. t.score
    end
    ScreenBase.updateStatus(self, table.concat(parts, "  |  "))
end

function TabooScreen:onClose()
    self:_stopCountdown()
    ScreenBase.onClose(self)
end

return TabooScreen
