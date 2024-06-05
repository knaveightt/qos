# qos
> Configuration for my "Qtile-Oriented System", one of my default desktop config setups for linux.

## Required Prerequsites
To use this desktop setup for linux, a few prerequisites need to be met or are assumed to be present. 
Of course, it is assumed the user is using a display server or the like (e.g. X11, Wayland, etc).
Beyond that, a few assumptions are made in this setup.

**Text Editing Environment**
It is assumed the user has access to a text editor, such as Vim, Emacs, Nano, etc.
This setup assumes the user is using my configuration of Emacs, named ["Knavemacs"](https://github.com/knaveightt/knavemacs)

**Terminal Emulator**
It is assumed the user is using a terminal emulator, such as xterm that comes with X11.
This configuration has options to two alternatives that I like to use.

`sakura` is a terminal emulator that is quick and functional. My configuration for this terminal emulator (along with any future patches I may add to the current source code) is present in the *sakura* subdirectory.

`gnome-terminal` is also a terminal emulator that is tried and tested, coming from prior versions of the gnome desktop environment. My configuration for this terminal emulator is present in the *gnome-terimal* subdirectory. To load this configuration, you will also need `dconf`, and will need to use a command such as `dconf load /org/gnome/terminal/legacy/profiles:/ < gnome-term-profiles.dconf`
