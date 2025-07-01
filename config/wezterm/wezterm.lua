local wezterm = require("wezterm")
local config = wezterm.config_builder() 

-- font settings
config.font_size = 13
config.font = wezterm.font("JetBrainsMono Nerd Font")

-- colors
config.colors = {
    cursor_bg = "gray",
    cursor_border = "gray",
}

-- appearance
config.window_decorations = "RESIZE"
config.hide_tab_bar_if_only_one_tab = true
config.window_padding = {
    left = 0,
    right = 0,
    top = 0,
    bottom = 0,
}

-- misc settings
config.max_fps = 120

return config


