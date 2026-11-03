-- Cards played in one session do not come back in the next one until the rest
-- of the selection has been played (taboo_history.lua + game-common
-- seen_history).
local DIR = debug.getinfo(1, "S").source:sub(2):match("(.*[/\\])") or "./"
package.path = DIR .. "?.lua;" .. DIR .. "common/?.lua;" .. package.path

local TabooHistory = require("taboo_history")

local function fakePlugin()
    local store = {}
    return {
        store = store,
        getSetting  = function(_self, k, d) if store[k] == nil then return d end return store[k] end,
        saveSetting = function(_self, k, v) store[k] = v end,
    }
end

local function theme(lang, id)
    local deck = dofile(DIR .. "taboo_cards_" .. lang .. ".lua")
    if id then return deck[id] end
    local all = {}
    for _t, cards in pairs(deck) do
        for _i, c in ipairs(cards) do all[#all + 1] = c end
    end
    return all
end

-- One evening: reopen the history, order the selection, play `n` cards.
local function session(plugin, lang, cards, n)
    local seen = TabooHistory.open(plugin, lang)
    local copy = {}
    for i, c in ipairs(cards) do copy[i] = c end
    TabooHistory.order(seen, copy)
    local shown = {}
    for i = 1, n do
        shown[i] = copy[i]
        seen:mark(copy[i])
    end
    return shown
end

describe("taboo history across sessions", function()
    it("plays a whole small theme before any card comes back (en technologies)", function()
        local p = fakePlugin()
        local cards = theme("en", "technologies")
        local got = {}
        for _s = 1, 4 do
            for _i, c in ipairs(session(p, "en", cards, math.floor(#cards / 4))) do
                assert.is_nil(got[c.word], "repeated: " .. c.word)
                got[c.word] = true
            end
        end
        -- Used up: the next evening starts a new cycle.
        local rest = #cards - 4 * math.floor(#cards / 4)
        session(p, "en", cards, rest)
        assert.equals(10, #session(p, "en", cards, 10))
    end)

    it("keeps one history per language, capped", function()
        local p = fakePlugin()
        local all = theme("fr")
        for _s = 1, 4 do session(p, "fr", all, 1000) end
        assert.equals(TabooHistory.MAX, #p.store.seen_cards_fr)
        assert.is_nil(p.store.seen_cards_en)
    end)

    it("remembers the whole English deck and any single French theme", function()
        assert.is_true(TabooHistory.MAX >= #theme("en"))
        for id, cards in pairs(dofile(DIR .. "taboo_cards_fr.lua")) do
            assert.is_true(TabooHistory.MAX >= #cards, id)
        end
    end)

    it("works for a user's own deck (cards keyed by word)", function()
        local p = fakePlugin()
        local cards = {}
        for i = 1, 8 do cards[i] = { word = "W" .. i, forbidden = { "a" } } end
        local got = {}
        for _i, c in ipairs(session(p, "fr", cards, 4)) do got[c.word] = true end
        for _i, c in ipairs(session(p, "fr", cards, 4)) do assert.is_nil(got[c.word]) end
    end)
end)
