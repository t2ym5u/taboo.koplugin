local _dir = debug.getinfo(1, "S").source:sub(2):match("(.*[/\\])") or "./"
package.path = _dir .. "?.lua;" .. _dir .. "common/?.lua;" .. package.path

local function lrequire(name)
    local key = _dir .. name
    if not package.loaded[key] then
        package.loaded[key] = assert(loadfile(_dir .. name .. ".lua"))()
    end
    return package.loaded[key]
end

local PluginBase = require("plugin_base")
local _          = require("gettext")
local Screen     = lrequire("screen")

local Taboo = PluginBase:extend{
    name      = "taboo",
    menu_text = _("Taboo Party"),
    menu_hint = "tools",
}

function Taboo:createScreen()
    return Screen:new{ plugin = self }
end

return Taboo
