-- Family-friendly words: Forbidden Words is played around a family table, so
-- no card -- neither the word to guess nor its forbidden words -- may be
-- vulgar, sexual, scatological, a slur or drug-related. Both bundled decks
-- are read: taboo_cards_fr.lua, taboo_cards_en.lua, and taboo_cards.json,
-- the JSON fallback (French) left for user decks.
local DIR = debug.getinfo(1, "S").source:sub(2):match("(.*[/\\])") or "./"

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

-- Whole words only (accent-stripped, lowercase): "Pet" is out, "Petit Pois"
-- and "Peter Pan" are fine. No "con": Comic Con, chili con carne.
local BLOCKED = {}
for w in ([[
    caca pipi pet pets prout crotte zizi bite merde putain pute salope salaud
    connard couille couilles enfoire encule branle branler tapette
    gouine pede nichons teton sperme sexe sexuel sexuelle sexualite porno
    orgasme orgie vagin penis testicule anus rectum dyke viol violer
    cocaine heroine cannabis shit fuck
]]):gmatch("%a+") do BLOCKED[w] = true end

local function offending(text)
    for w in strip_accents(text):gmatch("[%a\128-\255]+") do
        if BLOCKED[w] then return w end
    end
end

-- English blocklist, plus figures the content guidelines exclude outright
-- (dictators, terrorists, serial killers, gangsters): they may appear neither
-- as a card nor as a clue. Two-word names are matched as a phrase.
local BLOCKED_EN = {}
for w in ([[
    poop poo pee piss fart farts crap shit fuck damn bitch bastard ass arse butt
    boob boobs tits penis vagina testicle testicles nipple sex sexy sexual
    porn porno orgasm orgy erotic nude stripper condom viagra prostitute hooker
    brothel rape slut whore cock pussy bollocks bugger wank
    cocaine heroin cannabis marijuana weed meth lsd stoned junkie suicide hell
    hitler nazi nazis stalin mussolini mao genghis capone gaddafi saddam
]]):gmatch("%a+") do BLOCKED_EN[w] = true end
local BLOCKED_EN_PHRASES = { "bin laden", "pol pot", "jack the ripper", "idi amin" }

local function offending_en(text)
    local lower = " " .. text:lower():gsub("[^%a%d]+", " ") .. " "
    local prev
    for w in lower:gmatch("%a+") do
        -- Moby Dick is a novel, not a rude word.
        if BLOCKED_EN[w] then return w end
        if w == "dick" and prev ~= "moby" then return w end
        prev = w
    end
    for _, p in ipairs(BLOCKED_EN_PHRASES) do
        if lower:find(" " .. p .. " ", 1, true) then return p end
    end
end

-- Figures the content guidelines exclude outright -- known mainly for
-- dictatorship, genocide, mass murder or terrorism -- and Nazism, which is
-- described through its figure. They may be neither a card nor a clue in the
-- French decks (history topics such as the Second World War stay, with other
-- clues). Words keep their hyphens so "BD franco-belge" and "Révolution
-- maoïste" are not mistaken for Franco and Mao.
local EXCLUDED_FR = {}
for w in ([[
    hitler staline stalin mussolini duce mao gengis attila franco pinochet
    kadhafi ceausescu ceaușescu saddam castro khomeini himmler goebbels
    capone nazi nazis nazisme al-qaida
]]):gmatch("%S+") do EXCLUDED_FR[w] = true end
local EXCLUDED_FR_PHRASES = { "pol pot", "ben laden", "idi amin", "kim jong" }

local function excluded_fr(text)
    local lower = strip_accents(text)
    for tok in lower:gmatch("[%a\128-\255%-]+") do
        local w = tok:gsub("^%-+", ""):gsub("%-+$", "")
        if EXCLUDED_FR[w] then return w end
    end
    for _, p in ipairs(EXCLUDED_FR_PHRASES) do
        if (" " .. lower .. " "):find(" " .. p .. " ", 1, true) then return p end
    end
end

describe("family-friendly cards", function()
    it("the English deck has no blocked word or excluded figure on any card", function()
        local deck = dofile(DIR .. "taboo_cards_en.lua")
        local n = 0
        for theme, cards in pairs(deck) do
            for _, card in ipairs(cards) do
                n = n + 1
                assert.is_falsy(offending_en(card.word), theme .. ": " .. card.word)
                for _, f in ipairs(card.forbidden) do
                    assert.is_falsy(offending_en(f), card.word .. " / " .. f)
                end
            end
        end
        assert.is_true(n >= 2000)
    end)

    it("the French deck has no blocked word on any card", function()
        local deck = dofile(DIR .. "taboo_cards_fr.lua")
        local n = 0
        for theme, cards in pairs(deck) do
            for _, card in ipairs(cards) do
                n = n + 1
                -- "Héroïne" the protagonist is a fine card word; only the
                -- drug sense would not be, and no card uses it.
                local bad = card.word ~= "Héroïne" and offending(card.word)
                assert.is_falsy(bad, theme .. ": " .. card.word)
                for _, f in ipairs(card.forbidden) do
                    local fb = f ~= "Héroïne" and offending(f)
                    assert.is_falsy(fb, card.word .. " / " .. f)
                end
            end
        end
        assert.is_true(n > 8000)
    end)

    it("the French deck names no excluded figure, as a card or a clue", function()
        local deck = dofile(DIR .. "taboo_cards_fr.lua")
        for theme, cards in pairs(deck) do
            for _, card in ipairs(cards) do
                assert.is_falsy(excluded_fr(card.word), theme .. ": " .. card.word)
                for _, f in ipairs(card.forbidden) do
                    assert.is_falsy(excluded_fr(f), card.word .. " / " .. f)
                end
            end
        end
    end)

    it("the fallback JSON deck names no excluded figure", function()
        local f = assert(io.open(DIR .. "taboo_cards.json", "r"))
        local text = f:read("*a")
        f:close()
        for card in text:gmatch('{"word":%s*"(.-)"') do
            assert.is_falsy(excluded_fr(card), card)
        end
    end)

    it("the fallback JSON deck has no blocked word on any card", function()
        local f = assert(io.open(DIR .. "taboo_cards.json", "r"))
        local text = f:read("*a")
        f:close()
        local n = 0
        for card in text:gmatch('{"word":%s*"(.-)"') do
            n = n + 1
            assert.is_falsy(offending(card), card)
        end
        assert.is_true(n > 6000)
    end)
end)
