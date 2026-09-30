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

describe("taboo card deck", function()
    local deck

    setup(function()
        deck = require("taboo_cards_fr")
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
