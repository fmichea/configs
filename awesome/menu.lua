-- menu.lua - Main menu is implemented here.

require("awful")
require("beautiful")
require("settings")

-- Edit Configuration Command
ecc = settings.editor_cmd .. " " .. awful.util.getdir("config") .. "/rc.lua"

myawesomemenu = {
   { "manual", settings.terminal .. " -e man awesome" },
   { "edit config", },
   { "restart", awesome.restart },
   { "quit", awesome.quit }
}

mymainmenu = awful.menu({
    items = {
        { "awesome", myawesomemenu, beautiful.awesome_icon },
        { "open terminal", terminal }
    }
})

mylauncher = awful.widget.launcher({
    image = image(beautiful.awesome_icon),
    menu = mymainmenu
})

return mylauncher
