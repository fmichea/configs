---------------------------
-- Default awesome theme --
---------------------------

require("awful")

theme = {}
local confdir = awful.util.getdir("config")
local baseconf = "/usr/share/awesome/themes/default/"

theme.font          = "sans 7"

theme.bg_normal     = "#222222"
theme.bg_focus      = "#535d6c"
theme.bg_urgent     = "#ff0000"
theme.bg_minimize   = "#444444"

theme.fg_normal     = "#aaaaaa"
theme.fg_focus      = "#ffffff"
theme.fg_urgent     = "#ffffff"
theme.fg_minimize   = "#ffffff"

theme.border_width  = "1"
theme.border_normal = "#000000"
theme.border_focus  = "#535d6c"
theme.border_marked = "#91231c"

-- There are other variable sets
-- overriding the default one when
-- defined, the sets are:
-- [taglist|tasklist]_[bg|fg]_[focus|urgent]
-- titlebar_[bg|fg]_[normal|focus]
-- tooltip_[font|opacity|fg_color|bg_color|border_width|border_color]
-- mouse_finder_[color|timeout|animate_timeout|radius|factor]
-- Example:
--theme.taglist_bg_focus = "#ff0000"

-- Display the taglist squares
theme.taglist_squares_sel   = baseconf .. "taglist/squarefw.png"
theme.taglist_squares_unsel = baseconf .. "taglist/squarew.png"

theme.tasklist_floating_icon = baseconf .. "tasklist/floatingw.png"

-- Variables set for theming the menu:
-- menu_[bg|fg]_[normal|focus]
-- menu_[border_color|border_width]
theme.menu_submenu_icon = baseconf .. "submenu.png"
theme.menu_height = "15"
theme.menu_width  = "100"

-- You can add as many variables as
-- you wish and access them by using
-- beautiful.variable in your rc.lua
--theme.bg_widget = "#cc0000"

-- Define the image to load
theme.titlebar_close_button_normal = baseconf .. "titlebar/close_normal.png"
theme.titlebar_close_button_focus = baseconf .. "titlebar/close_focus.png"

theme.titlebar_ontop_button_normal_inactive = baseconf .. "titlebar/ontop_normal_inactive.png"
theme.titlebar_ontop_button_focus_inactive = baseconf .. "titlebar/ontop_focus_inactive.png"
theme.titlebar_ontop_button_normal_active = baseconf .. "titlebar/ontop_normal_active.png"
theme.titlebar_ontop_button_focus_active = baseconf .. "titlebar/ontop_focus_active.png"

theme.titlebar_sticky_button_normal_inactive = baseconf .. "titlebar/sticky_normal_inactive.png"
theme.titlebar_sticky_button_focus_inactive = baseconf .. "titlebar/sticky_focus_inactive.png"
theme.titlebar_sticky_button_normal_active = baseconf .. "titlebar/sticky_normal_active.png"
theme.titlebar_sticky_button_focus_active = baseconf .. "titlebar/sticky_focus_active.png"

theme.titlebar_floating_button_normal_inactive = baseconf .. "titlebar/floating_normal_inactive.png"
theme.titlebar_floating_button_focus_inactive = baseconf .. "titlebar/floating_focus_inactive.png"
theme.titlebar_floating_button_normal_active = baseconf .. "titlebar/floating_normal_active.png"
theme.titlebar_floating_button_focus_active = baseconf .. "titlebar/floating_focus_active.png"

theme.titlebar_maximized_button_normal_inactive = baseconf .. "titlebar/maximized_normal_inactive.png"
theme.titlebar_maximized_button_focus_inactive = baseconf .. "titlebar/maximized_focus_inactive.png"
theme.titlebar_maximized_button_normal_active = baseconf .. "titlebar/maximized_normal_active.png"
theme.titlebar_maximized_button_focus_active = baseconf .. "titlebar/maximized_focus_active.png"

-- You can use your own command to set your wallpaper
theme.wallpaper_cmd = { "feh --bg-scale " .. confdir .. "/wallpaper.jpg" }

-- You can use your own layout icons like this:
theme.layout_fairh = confdir ..  "/icons/layouts/fairh.png"
theme.layout_fairv = confdir .. "/icons/layouts/fairv.png"
theme.layout_floating = confdir .. "/icons/layouts/floating.png"
theme.layout_magnifier = confdir .. "/icons/layouts/magnifier.png"
theme.layout_max = confdir .. "/icons/layouts/max.png"
theme.layout_fullscreen = confdir .. "/icons/layouts/fullscreen.png"
theme.layout_tilebottom = confdir .. "/icons/layouts/tilebottom.png"
theme.layout_tileleft = confdir .. "/icons/layouts/tileleft.png"
theme.layout_tile = confdir .. "/icons/layouts/tile.png"
theme.layout_tiletop = confdir .. "/icons/layouts/tiletop.png"
theme.layout_spiral = confdir .. "/icons/layouts/spiral.png"
theme.layout_dwindle = confdir .. "/icons/layouts/dwindle.png"

theme.awesome_icon = "/usr/share/awesome/icons/awesome16.png"

-- Widget Icons
theme.widget_bat_std = confdir .. "/icons/bat.png"
theme.widget_bat_rcp = confdir .. "/icons/bat_rcp.png"
theme.widget_bat_low = confdir .. "/icons/bat_low.png"
theme.widget_bat_crt = confdir .. "/icons/bat_crt.png"
theme.widget_cpu = confdir .. "/icons/cpu.png"
theme.widget_mem = confdir .. "/icons/mem.png"
theme.widget_mpd = confdir .. "/icons/music.png"
theme.widget_sep = confdir .. "/icons/sep.png"
theme.widget_net_up = confdir .. "/icons/netup.png"
theme.widget_net_down = confdir .. "/icons/netdown.png"

return theme
-- EOF
