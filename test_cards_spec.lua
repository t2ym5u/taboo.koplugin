-- The bundled deck is 1,000+ hand-written cards and the loader in screen.lua
-- only type-checks the first pair it sees, so a malformed card further down
-- loads fine and only surfaces when a player draws it mid-round. These tests
-- read the whole deck. The forbidden-word count matters too: a card with fewer
-- taboos is simply easier than the rest, which the players cannot see coming.
local DIR = debug.getinfo(1, "S").source:sub(2):match("(.*[/\\])") or "./"

package.path = DIR .. "?.lua;" .. package.path

local function strip_accents(s)
    local map = {
        ["à"]="a", ["â"]="a", ["ä"]="a", ["ç"]="c", ["é"]="e", ["è"]="e",
        ["ê"]="e", ["ë"]="e", ["î"]="i", ["ï"]="i", ["ô"]="o", ["ö"]="o",
        ["ù"]="u", ["û"]="u", ["ü"]="u", ["ÿ"]="y", ["œ"]="oe", ["æ"]="ae",
    }
    return (s:lower():gsub("[\194-\244][\128-\191]*", function(c)
        return map[c] or c
    end))
end

local function deck_spec(module)
describe("taboo card deck " .. module, function()
    local deck

    setup(function()
        deck = require(module)
    end)

    it("is a theme-keyed dict, the shape _filterByTheme expects", function()
        assert.is_table(deck)
        local themes = 0
        for key, cards in pairs(deck) do
            assert.is_string(key)
            assert.is_table(cards)
            themes = themes + 1
        end
        assert.is_true(themes > 0)
    end)

    it("has no holes: #list reaches every card", function()
        -- _filterByTheme walks each theme with ipairs, which stops at the first
        -- nil, silently dropping the rest of that theme.
        for theme, cards in pairs(deck) do
            local counted = 0
            for _ in pairs(cards) do counted = counted + 1 end
            assert.are.equal(counted, #cards,
                "theme " .. theme .. " has a hole in its array")
        end
    end)

    it("gives every card a word and a list of forbidden words", function()
        for theme, cards in pairs(deck) do
            for i, card in ipairs(cards) do
                local where = theme .. " #" .. i
                assert.is_table(card, where .. " is not a table")
                assert.is_string(card.word, where .. " has no word")
                assert.is_true(#card.word > 0, where .. " has an empty word")
                assert.is_table(card.forbidden, where .. " has no forbidden list")
                for j, f in ipairs(card.forbidden) do
                    assert.is_string(f, where .. " forbidden #" .. j .. " is not a string")
                    assert.is_true(#f > 0, where .. " forbidden #" .. j .. " is empty")
                end
            end
        end
    end)

    it("gives every card the same number of forbidden words", function()
        local expected, from
        for theme, cards in pairs(deck) do
            for i, card in ipairs(cards) do
                local n = #card.forbidden
                if expected == nil then
                    expected, from = n, theme .. " #" .. i
                else
                    assert.are.equal(expected, n, theme .. " #" .. i .. " has "
                        .. n .. " forbidden words, " .. from .. " has " .. expected)
                end
            end
        end
    end)

    it("never lists the card's own word among its taboos", function()
        -- A card that forbids its own word cannot be described at all.
        for theme, cards in pairs(deck) do
            for i, card in ipairs(cards) do
                local word = card.word:lower()
                for _, f in ipairs(card.forbidden) do
                    assert.are_not.equal(word, f:lower(),
                        theme .. " #" .. i .. " forbids its own word: " .. card.word)
                end
            end
        end
    end)

    it("repeats no forbidden word within a card", function()
        for theme, cards in pairs(deck) do
            for i, card in ipairs(cards) do
                local seen = {}
                for _, f in ipairs(card.forbidden) do
                    local k = f:lower()
                    assert.is_nil(seen[k], theme .. " #" .. i
                        .. " lists " .. f .. " twice")
                    seen[k] = true
                end
            end
        end
    end)

    it("uses one difficulty vocabulary throughout", function()
        local allowed = { easy = true, medium = true, hard = true }
        for theme, cards in pairs(deck) do
            for i, card in ipairs(cards) do
                assert.is_true(allowed[card.difficulty] == true,
                    theme .. " #" .. i .. " has difficulty " .. tostring(card.difficulty))
            end
        end
    end)

    it("deals no word twice", function()
        -- Accent-insensitive, because the defect this catches is one word typed
        -- two ways ("Poseidon" and "Poséidon" as separate cards). French does
        -- have real pairs that differ only by an accent, and those are deliberate
        -- cards, so they are listed here rather than weakening the check.
        local homographs = {
            ["poire"]  = true,  -- Poire (the fruit) / Poiré (the cider)
            ["paris"]  = true,  -- Paris (the city) / Pâris (the Trojan prince)
            ["granite"]= true,  -- Granite (the rock) / Granité (the dessert)
            ["traite"] = true,  -- Traite (milking) / Traité (the treaty)
            ["gaia"]   = true,  -- Gaia (the ESA probe) / Gaïa (the goddess)
        }
        local seen = {}
        for theme, cards in pairs(deck) do
            for i, card in ipairs(cards) do
                local k = strip_accents(card.word)
                if not homographs[k] then
                    assert.is_nil(seen[k], "duplicate word in " .. theme .. " #" .. i
                        .. ", first seen in " .. tostring(seen[k]) .. ": " .. card.word)
                    seen[k] = theme
                end
            end
        end
    end)

    it("leaves no theme empty", function()
        for theme, cards in pairs(deck) do
            assert.is_true(#cards > 0, "theme " .. theme .. " is empty")
        end
    end)
end)
end

deck_spec("taboo_cards_fr")
deck_spec("taboo_cards_en")

-- The English deck is written from scratch (gen/en/*.txt -> gen/build_en.py),
-- so it is held to a few rules the older French deck predates.
describe("English deck", function()
    local deck
    local THEMES = {
        "fun", "action", "alimentation", "animaux", "arts", "cinéma",
        "géographie", "histoire", "jeuxvideo", "maison", "médecine", "métiers",
        "mode", "musique", "nature", "sciences", "société", "sports",
        "technologies", "transports",
    }

    setup(function()
        deck = require("taboo_cards_en")
    end)

    it("covers every theme id of the French deck, and only those", function()
        -- Same ids in both decks: the theme filter and the saved selection
        -- ("selected_themes_<lang>") are keyed by them.
        local known = {}
        for _, t in ipairs(THEMES) do known[t] = true end
        for theme in pairs(deck) do
            assert.is_true(known[theme] == true, "unknown theme id " .. theme)
        end
        for _, t in ipairs(THEMES) do
            assert.is_table(deck[t], "missing theme " .. t)
            assert.is_true(#deck[t] >= 70, t .. " has only " .. #deck[t] .. " cards")
        end
    end)

    it("has 2,000+ cards", function()
        local n = 0
        for _, cards in pairs(deck) do n = n + #cards end
        assert.is_true(n >= 2000, n .. " cards")
    end)

    it("gives every card exactly five forbidden words", function()
        for theme, cards in pairs(deck) do
            for _, card in ipairs(cards) do
                assert.are.equal(5, #card.forbidden, theme .. ": " .. card.word)
            end
        end
    end)

    it("never forbids a word that is part of the guess word", function()
        -- "Hot dog" forbidding "Dogs" wastes a slot: saying part of the
        -- word is against the rules anyway. Plural-insensitive.
        local STOP = { a=1, an=1, the=1, of=1, ["and"]=1, ["in"]=1, on=1, at=1,
            to=1, ["for"]=1, de=1, la=1, le=1, du=1, des=1, with=1, by=1, ["or"]=1 }
        local function stems(s)
            local out = {}
            for tok in s:lower():gmatch("[%a%d]+") do
                local t = tok
                if #t >= 3 and not STOP[t] then
                    if #t > 4 and t:sub(-3) == "ies" then t = t:sub(1, -4) .. "y"
                    elseif #t > 3 and t:sub(-1) == "s" and t:sub(-2) ~= "ss" then t = t:sub(1, -2) end
                    out[t] = true
                end
            end
            return out
        end
        for theme, cards in pairs(deck) do
            for _, card in ipairs(cards) do
                local w = stems(card.word)
                for _, f in ipairs(card.forbidden) do
                    for t in pairs(stems(f)) do
                        assert.is_nil(w[t], theme .. ": " .. card.word .. " / " .. f)
                    end
                end
            end
        end
    end)

    it("is plain ASCII-or-UTF-8 text with no stray separators", function()
        for theme, cards in pairs(deck) do
            for _, card in ipairs(cards) do
                assert.is_nil(card.word:find("[|\n]"), theme .. ": " .. card.word)
                assert.are.equal(card.word, card.word:match("^%s*(.-)%s*$"))
            end
        end
    end)
end)
