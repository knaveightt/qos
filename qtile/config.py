# Copyright (c) 2010 Aldo Cortesi
# Copyright (c) 2010, 2014 dequis
# Copyright (c) 2012 Randall Ma
# Copyright (c) 2012-2014 Tycho Andersen
# Copyright (c) 2012 Craig Barnes
# Copyright (c) 2013 horsik
# Copyright (c) 2013 Tao Sauvage
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import os
import subprocess
from libqtile import bar, layout, qtile, widget, hook
from libqtile.config import Click, Drag, Group, Key, KeyChord, Match, Screen, ScratchPad, DropDown
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal

mod = "mod4"
#terminal = guess_terminal()
terminal = "wezterm"

keys = [
    # Window Switching, Movement, Sizing
    Key([mod], "j", lazy.layout.next(), desc="Move focus to next window"),
    Key([mod], "k", lazy.layout.previous(), desc="Move focus to prev window"),
    Key([mod], "h", lazy.layout.shrink_main(), desc="Decrease Master Size"),
    Key([mod], "l", lazy.layout.grow_main(), desc="Increase Master Size"),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down(), desc="Move window down"),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up(), desc="Move window up"),
    Key([mod], "g", lazy.layout.swap_main(), desc="Increase Master Size"),
    Key([mod], "r", lazy.layout.reset(), desc="Decrease Master Size"),    
    Key([mod], "q", lazy.window.kill(), desc="Kill focused window"),
    Key([mod], "z", lazy.screen.toggle_group(), desc="Focus on prior group"),
    
    # Layout Switching
    Key([mod], "t", lazy.to_layout_index(0), desc="Increase Master Size"),
    Key([mod], "d", lazy.to_layout_index(1), desc="Increase Master Size"),
    Key([mod], "c", lazy.to_layout_index(2), desc="Increase Master Size"),
    Key([mod], "v", lazy.window.toggle_floating(), desc="Toggle floating on the focused window"),
    Key([mod], "f", lazy.window.toggle_fullscreen(), desc="Toggle fullscreen on the focused window"),
    Key([mod], "b", lazy.hide_show_bar(), desc="Increase Master Size"),

    # TreeTab Layout Navigation
    Key([mod], "o", lazy.layout.move_right(), desc="Increase Master Size"),
    Key([mod], "i", lazy.layout.move_left(), desc="Increase Master Size"),
    Key([mod], "y", lazy.layout.move_down(), desc="Increase Master Size"),
    Key([mod], "u", lazy.layout.move_up(), desc="Increase Master Size"),
    Key([mod, "shift"], "i", lazy.layout.collapse_branch(), desc="Increase Master Size"),
    Key([mod, "shift"], "o", lazy.layout.expand_branch(), desc="Increase Master Size"),
    Key([mod, "shift"], "u", lazy.layout.section_up(), desc="Increase Master Size"),
    Key([mod, "shift"], "y", lazy.layout.section_down(), desc="Increase Master Size"),

    # Launchers and Applications
    Key([mod], "Return", lazy.spawn(terminal), desc="Launch terminal"),
    Key([mod], "space", lazy.spawn("emacsclient -c"), desc="Launch Emacs"),
    Key([mod], "p", lazy.spawncmd(), desc="Launch Program Launcher"),
    Key([mod, "shift"], "p", lazy.spawn(terminal), desc="Spawn a command using a prompt widget"),
    Key([mod], "e", lazy.spawn(terminal), desc="Launch Terminal File Explorer"),
    Key([mod], "w", lazy.spawn(terminal), desc="Launch Window Switcher"),
    Key([mod, "shift"], "x", lazy.spawn(terminal), desc="Launch X Kill"),
    Key([mod, "shift"], "z", lazy.spawn("xscreensaver-command --lock"), desc="Lock Screen"),
    Key([mod], "x", lazy.spawncmd(), desc="Launch Extended Prompt"),

    # ScratchPad
    Key([mod], "s", lazy.group["scratchterm"].dropdown_toggle("term"), desc="Launch Extended Prompt"),
    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),

    # Laptop Special Keys
    # (for Chromebook. You can use Shift+Key to send original Function Key)
    Key([], "F1", lazy.layout.previous(), desc="Toggle"),
    Key([], "F2", lazy.layout.next(), desc="Toggle"),
    Key([], "F3", lazy.screen.toggle_group(), desc="Toggle"),
    Key([], "F4", lazy.window.toggle_fullscreen(), desc="Toggle"),
    Key([], "F5", lazy.to_layout_index(1), desc="Toggle"),
    Key([], "F6", lazy.layout.next(), desc="Toggle"),
    Key([], "F7", lazy.layout.next(), desc="Toggle"),
    Key([], "F8", lazy.layout.next(), desc="Toggle"),
    Key([], "F9", lazy.layout.next(), desc="Toggle"),
    Key([], "F10", lazy.layout.next(), desc="Toggle"),
    Key([], "XF86Tools", lazy.spawn(terminal), desc="Toggle"),
  
    # Control Keybinds
    Key([mod, "control"], "r", lazy.reload_config(), desc="Reload the config"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
]

# Custom TreeTab Control Keybinds
def prompt_get_notify(qtile):
    try:
        mb = qtile.widgets_map["prompt"]
        mb.start_input("Echo", notif, None)
    except:
        mb = None

def notif(args):
    qtile.cmd_spawn('dunstify "%s"' % args)

#keys.append(Key([mod], "z", lazy.function(prompt_get_notify)))

def sectionadd(args):
    qtile.current_layout.cmd_add_section(args)

def prompt_get_sectionadd(qtile):
    try:
        mb = qtile.widgets_map["prompt"]
        mb.start_input("Section", sectionadd, None)
    except:
        mb = None

keys.append(Key([mod, "control"], "o", lazy.function(prompt_get_sectionadd)))

def sectiondel(args):
    qtile.current_layout.cmd_del_section(args)

def prompt_get_sectiondel(qtile):
    try:
        mb = qtile.widgets_map["prompt"]
        mb.start_input("Section", sectiondel, None)
    except:
        mb = None

keys.append(Key([mod, "control"], "i", lazy.function(prompt_get_sectiondel)))

# Add key bindings to switch VTs in Wayland.
# We can't check qtile.core.name in default config as it is loaded before qtile is started
# We therefore defer the check until the key binding is run by using .when(func=...)
for vt in range(1, 8):
    keys.append(
        Key(
            ["control", "mod1"],
            f"f{vt}",
            lazy.core.change_vt(vt).when(func=lambda: qtile.core.name == "wayland"),
            desc=f"Switch to VT{vt}",
        )
    )

groups = [
    Group("", layout="max"),
    Group("", layout="max"),
    Group("", layout="max"),
    Group("", layout="max"),
    Group("", layout="monadtall"),
    ScratchPad("scratchterm",[DropDown("term","wezterm", x=0.12, y=0.02, width=0.75, height=0.6, on_focus_lost_hide=False)]),
]

from libqtile.dgroups import simple_key_binder
dgroups_key_binder = simple_key_binder("mod4")

layouts = [
    layout.MonadTall(),
    layout.Max(),
    layout.TreeTab(),
]

widget_defaults = dict(
    font="JetBrainsMono Nerd Font",
    fontsize=12,
    padding=3,
)
extension_defaults = widget_defaults.copy()

def init_widgets_list():
    widgets_list = [
        widget.TextBox(
            text="",
            foreground = "#00AA00",
            background = "#666666",
            fontsize=12,
            padding = 10,
            markup = True,
            fmt='<span font_size="130%">{}</span>',
            ),
        widget.Sep(
            linewidth=0,
            padding=0,
            foreground = "#666666",
            background = "#666666",
            ),
        widget.TextBox(
            text="",
            foreground = "#666666",
            background = "#333333",
            fontsize=22,
            padding=0,
            ),
        widget.Sep(
            linewidth=3,
            padding=0,
            foreground = "#333333",
            background = "#333333",
            ),
        widget.GroupBox(
            highlight_method='block',
            foreground = "#0000AA",
            background = "#333333",
            fontsize = 12,
            margin_x = 3,
            padding = 6,
            markup = True,
            fmt='<tt>{}</tt>',
            ),
        widget.Sep(
            linewidth=0,
            padding=0,
            foreground = "#333333",
            background = "#333333",
            ),
        widget.Prompt(
            background = "#333333",
            prompt = 'Command: ',
            ),
        widget.TextBox(
            text="",
            foreground = "#333333",
            background = "#000000",
            fontsize=22,
            padding=0,
            ),
        widget.Sep(
            linewidth=3,
            padding=0,
            foreground = "#000000",
            background = "#000000",
            ),
        widget.WindowName(),
        widget.Sep(
            linewidth=0,
            padding=0,
            foreground = "#000000",
            background = "#000000",
            ),
        widget.TextBox(
            text="",
            foreground = "#333333",
            background = "#000000",
            fontsize=22,
            padding=0,
            ),
        widget.Sep(
            linewidth=3,
            padding=0,
            foreground = "#333333",
            background = "#333333",
            ),
        widget.Clock(
            format="%Y-%m-%d %a %I:%M %p",
            background="#333333",
            ),
        widget.Sep(
            linewidth=3,
            padding=0,
            foreground = "#333333",
            background = "#333333",
            ),
        widget.TextBox(
            text="",
            foreground = "#666666",
            background = "#333333",
            fontsize=22,
            padding=0,
            ),
        widget.Sep(
            linewidth=3,
            padding=0,
            foreground = "#666666",
            background = "#666666",
            ),
        widget.Systray(),
        ]
    return widgets_list

screens = [
    Screen(
        top=bar.Bar(
            widgets=init_widgets_list(),
            size=24,
            # border_width=[2, 0, 2, 0],  # Draw top and bottom borders
            # border_color=["ff00ff", "000000", "ff00ff", "000000"]  # Borders are magenta
        ),
        # You can uncomment this variable if you see that on X11 floating resize/moving is laggy
        # By default we handle these events delayed to already improve performance, however your system might still be struggling
        # This variable is set to None (no cap) by default, but you can set it to 60 to indicate that you limit it to 60 events per second
        # x11_drag_polling_rate = 60,
    ),
]

# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(), start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front()),
]


dgroups_app_rules = []  # type: list
follow_mouse_focus = True
bring_front_click = False
floats_kept_above = True
cursor_warp = False
floating_layout = layout.Floating(
    float_rules=[
        # Run the utility of `xprop` to see the wm class and name of an X client.
        *layout.Floating.default_float_rules,
        Match(wm_class="confirmreset"),  # gitk
        Match(wm_class="makebranch"),  # gitk
        Match(wm_class="maketag"),  # gitk
        Match(wm_class="ssh-askpass"),  # ssh-askpass
        Match(title="branchdialog"),  # gitk
        Match(title="pinentry"),  # GPG key password entry
    ]
)
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = True

# When using the Wayland backend, this can be used to configure input devices.
wl_input_rules = None

# setup startup script
@hook.subscribe.startup_once
def start_once():
    home = os.path.expanduser('~/.config/qtile/autostart.sh')
    subprocess.Popen([home])

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "Qtile"
