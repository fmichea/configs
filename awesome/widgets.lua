-- {{{ kushou's widgets using vicious }}}
require("vicious")

-- {{{ Separator
separator	= widget({ type = "imagebox" })
separator.image = image(beautiful.widget_sep)
-- }}}

-- {{{ Battery widget
-- Label
batterylabel	= widget({ type = "imagebox"})
batterylabel.image = image(beautiful.widget_bat_std)
-- Widget + Update Function
batterywidget	= widget({ type = "textbox" })
vicious.register(batterywidget, vicious.widgets.bat, "$1$2%",
--		 function (widget, args)
--		    if args["{state}"] == "⌁" then
--		       batterylabel.image = image(beautiful.widget_bat_rcp)
--		       return "-"
--		    else
--		       batterylabel.image = image(beautiful.widget_bat_std)
--		       if args["{state}"] == "-" and args["{percent}"] < 15 then
--			  batterylabel.image = image(beautiful.widget_bat_crt)
--		       elseif args["{state}"] == "-" and args["{percent}"] < 30 then
--			  batterylabel.image = image(beautiful.widget_bat_low)
--		       end
--		    end
--		    return args["{state}"] .. args["{percent}"] .. "%"
--		 end,
		 10, "BAT0")
-- }}}

-- {{{ CPU Usage Widget
-- Label
cpulabel	= widget({ type = "imagebox" })
cpulabel.image	= image(beautiful.widget_cpu)
-- Widget
cpuwidget	= widget({ type = "textbox" })
vicious.register(cpuwidget, vicious.widgets.cpu, "$1%") 
-- }}}

-- {{{ Memory Usage Widget
-- Label
memlabel	= widget({ type = "imagebox" })
memlabel.image	= image(beautiful.widget_mem)
-- Widget
memwidget	= widget({ type = "textbox" })
vicious.register(memwidget, vicious.widgets.mem, "$1%")
-- }}}

-- {{{ MPD widget
-- Label
mpdlabel	= widget({ type = "imagebox" })
mpdlabel.image	= image(beautiful.widget_mpd)
-- Widget + Update Function
mpdwidget = widget({ type = "textbox" })
function mpdfun (widget, args)
   if not (args["{state}"] == "Stop") then
      return args["{state}"] .. ": " .. args["{Artist}"] .. " - " .. args["{Title}"]
   end
   return " - MPD - "
end
vicious.register(mpdwidget, vicious.widgets.mpd,
		 function (widget, args)
		    if not (args["{state}"] == "Stop") then
		       return args["{state}"] .. ": " .. args["{Artist}"] .. " - " .. args["{Title}"]
		    end
		    return " - MPD - "
		 end)
-- }}}

-- {{{ Network Usage Widget
-- Labels
netuplabel		= widget({ type = "imagebox" })
netdownlabel		= widget({ type = "imagebox" })
netuplabel.image	= image(beautiful.widget_net_up)
netdownlabel.image	= image(beautiful.widget_net_down)
-- Widgets
-- {{ Ethernet
netwidget		= widget({ type = "textbox" })
vicious.register(netwidget, vicious.widgets.net, "${eth0 down_kb} - ${eth0 up_kb}")
-- }}
-- {{ Wifi
wifiupdownwidget	= widget({ type = "textbox" })
wifisignwidget		= widget({ type = "textbox" })
vicious.register(wifiupdownwidget, vicious.widgets.net, "${wlan0 down_kb} - ${wlan0 up_kb}")
vicious.register(wifisignwidget, vicious.widgets.wifi, "{ssid}: {sign}%")
-- }}
-- }}}

-- {{{ Including config file
local function widget_filepath(filename)
   return (awful.util.getdir("config") .. "/widgets.d/" .. filename .. ".lua")
end

local filename = widget_filepath(string.sub (io.popen("hostname"):read(), 0, -1))
local file, msg
file, msg = io.open(filename, "r")
if not file then
   dofile(widget_filepath("default"))
else
   dofile(filename)
end
-- }}}