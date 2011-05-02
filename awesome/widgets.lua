-- {{{ kushou's widgets using vicious }}}
require("vicious")
require("naughty")

-- {{{ Global Values
popup_percent = 100
notice = nil
-- }}}

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
vicious.register(batterywidget, vicious.widgets.bat,
		 function (widget, args)
		    -- Init
		    if args[1] == "⌁" then
		       if notice then
			  naughty.destroy(notice)
		       end
		       batterylabel.image = image(beautiful.widget_bat_rcp)
		       return ""
		    else
		       batterylabel.image = image(beautiful.widget_bat_std)
		       if args[1] == "-" and args[2] < 15 then
			  batterylabel.image = image(beautiful.widget_bat_crt)
			  if popup_percent > 15 then
			     popup_percent = 15
			     if notice then
				naughty.destroy(notice)
			     end
			     notice = naughty.notify({
							title = "Critical Battery State",
							text = "The percentage of battery is now lower than <b>15</b> percents.",
							timeout = 0,
							hover_timeout = 2
						     })
			  end
		       elseif args[1] == "-" and args[2] < 30 then
			  batterylabel.image = image(beautiful.widget_bat_low)
			  if popup_percent > 30 then
			     popup_percent = 30
			     if notice then
				naughty.destroy(notice)
			     end
			     notice = naughty.notify({
							title = "Dangerous Battery State",
							text = "The percentage of battery is now lower than <b>30</b> percents.",
							timeout = 0,
							hover_timeout = 2
						     })
			  end
		       else
			  popup_percent = 100
			  if notice then
			     naughty.destroy(notice)
			  end
		       end
		    end
		    return args[1] .. args[2] .. "%"
		 end,
		 2, "BAT0")
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