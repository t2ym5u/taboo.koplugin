-- Cards already shown, remembered across sessions (game-common
-- seen_history, one history per deck language), so the next evening starts
-- with cards not played yet instead of the same random openers.
--
-- Pure Lua, no UI, so the specs can drive it. Cards are identified by their
-- word, which also works for a deck file put in the documents folder.

local TabooHistory = {}

-- The French deck has 8,402 cards, the English one 2,445. Remembering all
-- of them would put ~100 KB in the settings, rewritten at every card; 3,000
-- words (~35 KB) is several dozen evenings of play. With the full French deck
-- selected, a card older than the last 3,000 is forgotten and may come back
-- before the never-shown ones; any single theme (1,538 cards at most) and the
-- whole English deck are remembered in full.
TabooHistory.MAX = 3000

function TabooHistory.open(plugin, lang)
    local SeenHistory = require("seen_history")
    return SeenHistory.open(plugin, "cards_" .. lang, { max = TabooHistory.MAX })
end

local function shuffle(t, rng)
    for i = #t, 2, -1 do
        local j = rng(i)
        t[i], t[j] = t[j], t[i]
    end
    return t
end

-- Reorders `cards` in place: cards not seen yet first, then those seen in
-- earlier sessions, each part shuffled. Nothing is marked here (the screen
-- marks a card when it is shown). When every card of `cards` has been seen,
-- their history is forgotten and a new random cycle starts.
function TabooHistory.order(seen, cards, rng)
    rng = rng or math.random
    if not seen then return shuffle(cards, rng) end
    local fresh, old = {}, {}
    for _i, c in ipairs(cards) do
        if seen:has(c) then old[#old + 1] = c else fresh[#fresh + 1] = c end
    end
    if #fresh == 0 then
        seen:forgetPool(cards)
        fresh, old = old, {}
    end
    shuffle(fresh, rng)
    shuffle(old, rng)
    for i = 1, #fresh do cards[i] = fresh[i] end
    for i = 1, #old do cards[#fresh + i] = old[i] end
    return cards
end

return TabooHistory
