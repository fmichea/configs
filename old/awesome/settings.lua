-- settings.lua - Several settings that can be used everywhere in the
--                configuration.

require("awful")

settings = {}

-- Constants
settings.hostname = io.popen("echo -n $HOSTNAME"):read()
settings.terminal = "urxvt"
settings.editor = os.getenv("EDITOR") or "nano"
settings.editor_cmd = settings.terminal .. " -e " .. settings.editor

-- Widgets filepath.
local function widget_filepath(filename)
   return (awful.util.getdir("config") .. "/widgets.d/" .. filename .. ".lua")
end

local filename = widget_filepath(settings.hostname)
local file, msg
file, msg = io.open(filename, "r")
if not file then
   settings.widget_config = widget_filepath("default")
else
   settings.widget_config = filename
end
-- }}}

if settings.hostname == "pc-michea-f" then
    settings.locker = "zlock -immed"
else
    confdir = awful.util.getdir("config")
    settings.locker = "i3lock -t -i " .. confdir .. "/locker.png"
end

-- {{{ MPD Client Config
settings.mpd_toggle = "ncmpcpp toggle"
settings.mpd_previous = "ncmpcpp prev"
settings.mpd_next = "ncmpcpp next"
settings.mpd_stop = "ncmpcpp stop"
-- }}}

return settings
-- EOF
