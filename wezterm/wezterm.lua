local wezterm = require 'wezterm';

launch_menu = {}

table.insert(launch_menu, {
  label = "bash",
  args = {"/usr/local/bin/bash"},
})
table.insert(launch_menu, {
  label = "xonsh",
  args = {"/usr/local/bin/xonsh"},
})

return {
  launch_menu = launch_menu,
  -- default_prog = {"/usr/local/bin/xonsh"},
  color_scheme = "Monokai Remastered",
  font = wezterm.font_with_fallback({
    "Liga InputMono",
    "Input Mono",
  }),
}
