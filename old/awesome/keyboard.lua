-- {{{ kushou's keyboard bindings in awesome
--
-- ** Notation:
-- # = Modkey
-- C = Control
-- M = Meta
-- > = Right Arrow
-- < = Left Arrow
--
-- ** Basic bindings :
-- #Ch: FIXME?
-- #Cj: Focus next screen.
-- #Ck: Foxus previous screen.
-- #C<: Previous Tag (modified)
-- #C{RET}: Get Current Client Master
-- #C>: Right: Next Tag (modified)
-- #Cr: Restart Awesome
-- #C{SPC}: Toggle Floating
-- #{ESC} : Last Tag
-- #f: FullScreen Mode
-- #h: Reduce Master Width
-- #j: Next Client
-- #k: Previous Client
-- #l: Inc Master Width
-- #Mj: Swap Current Client With Next One
-- #Mk: Swap Current Client With Previous One
-- #m: Toggle Minimized
-- #n: Toggle Minimized
-- #o: Change client of screen.
-- #{RET}: Spawn Terminal
-- #r: Run Prompt
-- #Sc: Kill Current Client
-- #Sh: FIXME?
-- #Sl: FIXME?
-- #{SPC}: Next Layout
-- #Sq: Quit Awesome
-- #Sr: Redraw Client
-- #S{SPC}: Previous Layout
-- #{TAB}: Last Client
-- #u: Jump To Urgent
-- #w: Awesome Menu [REMOVED]
-- #x: Run Lua Code Prompt
--
-- Added by me (uses ncmpcpp):
-- #p: Toggle Playback/Pause
-- #>: Next Song
-- #<: Previous Song
-- #s: Stop Music
--
-- #z: zlock
-- #t: Toggle touchpad ableness.
-- #q: Focus previous screen.
-- #w: Focus next screen.

require("settings")

touchpad_enabled = true

globalkeys = awful.util.table.join(
    awful.key({ modkey, "Control" }, "Left",   awful.tag.viewprev       ),
    awful.key({ modkey, "Control" }, "Right",  awful.tag.viewnext       ),
    awful.key({ modkey }, "Escape", awful.tag.history.restore),

    awful.key({ modkey }, "j", function ()
        awful.client.focus.byidx(1)
        if client.focus then client.focus:raise() end
    end),
    awful.key({ modkey }, "k", function ()
        awful.client.focus.byidx(-1)
        if client.focus then client.focus:raise() end
    end),
--    awful.key({ modkey }, "w", function ()
--        mymainmenu:show({ keygrabber = true })
--    end),

    -- Layout manipulation
    awful.key({ modkey, "Shift" }, "j", function ()
        awful.client.swap.byidx(1)
    end),
    awful.key({ modkey, "Shift" }, "k", function ()
        awful.client.swap.byidx(-1)
    end),
    awful.key({ modkey, "Control" }, "j", function ()
        awful.screen.focus_relative(1)
    end),
    awful.key({ modkey, "Control" }, "k", function ()
        awful.screen.focus_relative(-1)
    end),
    awful.key({ modkey }, "u", awful.client.urgent.jumpto),
    awful.key({ modkey }, "Tab", function ()
        awful.client.focus.history.previous()
        if client.focus then client.focus:raise() end
    end),

    -- Standard program
    awful.key({ modkey }, "Return", function ()
        awful.util.spawn(settings.terminal)
    end),
    awful.key({ modkey, "Control" }, "r", awesome.restart),
    awful.key({ modkey, "Shift" }, "q", awesome.quit),

    awful.key({ modkey }, "l", function () awful.tag.incmwfact(0.05) end),
    awful.key({ modkey }, "h", function () awful.tag.incmwfact(-0.05) end),
    awful.key({ modkey, "Shift" }, "h", function ()
        awful.tag.incnmaster(1)
    end),
    awful.key({ modkey, "Shift" }, "l", function ()
        awful.tag.incnmaster(-1)
    end),
    awful.key({ modkey, "Control" }, "h", function ()
        awful.tag.incncol(1)
    end),
    awful.key({ modkey, "Control" }, "l", function ()
        awful.tag.incncol(-1)
    end),
    awful.key({ modkey }, "space", function ()
        awful.layout.inc(layouts, 1)
    end),
    awful.key({ modkey, "Shift" }, "space", function ()
        awful.layout.inc(layouts, -1)
    end),

    -- Prompt
    awful.key({ modkey }, "e", function ()
        mypromptbox[mouse.screen]:run()
    end),
    awful.key({ modkey }, "r", function ()
        awful.util.spawn("dmenu_run -i -p 'Run: ' " ..
            " -fn '-misc-dejavu sans mono-medium-r-*-*-10-*-*-*-*-*-*'" ..
            " -nb '" .. beautiful.bg_normal ..
            "' -nf '" .. beautiful.fg_normal ..
            "' -sb '" .. beautiful.bg_focus ..
            "' -sf '" .. beautiful.fg_focus .. "'")
    end),

    awful.key({ modkey }, "x", function ()
        awful.prompt.run({ prompt = "Run Lua code: " },
                         mypromptbox[mouse.screen].widget,
                         awful.util.eval, nil,
                         awful.util.getdir("cache") .. "/history_eval")
    end),
    awful.key({ modkey }, "p", function ()
        awful.util.pread(settings.mpd_toggle)
    end),
    awful.key({ modkey }, "Left", function ()
        awful.util.pread(settings.mpd_previous)
    end),
    awful.key({ modkey }, "Right", function ()
        awful.util.pread(settings.mpd_next)
    end),
    awful.key({ modkey }, "s", function ()
        awful.util.pread(settings.mpd_stop)
    end),
    awful.key({ modkey }, "z", function ()
        awful.util.spawn(settings.locker)
    end),
    awful.key({ modkey }, "t", function ()
        touchpad_enabled = not touchpad_enabled
        if touchpad_enabled then
            awful.util.pread("synclient TouchpadOff=0")
        else
            awful.util.pread("synclient TouchpadOff=1")
        end
    end),
    awful.key({ modkey }, "w", function ()
        awful.screen.focus_relative(1)
    end),
    awful.key({ modkey }, "q", function ()
        awful.screen.focus_relative(-1)
    end)
)

clientkeys = awful.util.table.join(
    awful.key({ modkey }, "f", function (c)
        c.fullscreen = not c.fullscreen
    end),
    awful.key({ modkey, "Shift" }, "c", function (c) c:kill() end),
    awful.key({ modkey, "Control" }, "space",  awful.client.floating.toggle),
    awful.key({ modkey, "Control" }, "Return", function (c)
       c:swap(awful.client.getmaster())
    end),
    awful.key({ modkey }, "o", awful.client.movetoscreen),
    awful.key({ modkey, "Shift" }, "r", function (c) c:redraw() end),
    awful.key({ modkey }, "n", function (c) c.minimized = not c.minimized end),
    awful.key({ modkey }, "m", function (c)
        c.maximized_horizontal = not c.maximized_horizontal
        c.maximized_vertical   = not c.maximized_vertical
    end)
)

-- Compute the maximum number of digit we need, limited to 9
keynumber = 0
for s = 1, screen.count() do
   keynumber = math.min(9, math.max(#tags[s], keynumber));
end

-- Bind all key numbers to tags.
-- Be careful: we use keycodes to make it works on any keyboard layout.
-- This should map on the top row of your keyboard, usually 1 to 9.
for i = 1, keynumber do
    globalkeys = awful.util.table.join(globalkeys,
        awful.key({ modkey }, "#" .. i + 9, function ()
            local screen = mouse.screen
                if tags[screen][i] then
                    awful.tag.viewonly(tags[screen][i])
                end
        end),
        awful.key({ modkey, "Control" }, "#" .. i + 9, function ()
            local screen = mouse.screen
            if tags[screen][i] then
                awful.tag.viewtoggle(tags[screen][i])
            end
        end),
        awful.key({ modkey, "Shift" }, "#" .. i + 9, function ()
            if client.focus and tags[client.focus.screen][i] then
                awful.client.movetotag(tags[client.focus.screen][i])
            end
        end),
        awful.key({ modkey, "Control", "Shift" }, "#" .. i + 9, function ()
            if client.focus and tags[client.focus.screen][i] then
                awful.client.toggletag(tags[client.focus.screen][i])
            end
        end))
end

clientbuttons = awful.util.table.join(
    awful.button({ }, 1, function (c) client.focus = c; c:raise() end),
    awful.button({ modkey }, 1, awful.mouse.client.move),
    awful.button({ modkey }, 3, awful.mouse.client.resize)
)

-- Set keys
root.keys(globalkeys)
-- }}}
