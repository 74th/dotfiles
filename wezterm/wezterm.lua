local wezterm = require 'wezterm';

local c = {}
local keys = {}
local launch_menu = {}

table.insert(keys, {key="t", mods="CTRL", action="ShowLauncher"})

table.insert(launch_menu, {
  label = "bash",
  args = {"/usr/bin/bash"},
})
table.insert(launch_menu, {
  label = "xonsh",
  args = {"xonsh"},
})
table.insert(launch_menu, {
  label = "lewill",
  args = {"ssh", "lewill", "xonsh"},
  domain = {DomainName="local"},
})

local ssh_domains = {}

table.insert(ssh_domains, {
  name = "lewill",
  remote_address = "lewill",
  username = "nnyn",
})

c.window_decorations = "RESIZE"

c.window_padding = {
  left = 3,
  right = 3,
  top = 3,
  bottom = 3,
}

c.color_scheme = "Monokai Remastered"

c.font = wezterm.font_with_fallback({
  "Liga InputMono",
  "Input Mono",
})
c.font_size = 10.5

c.default_prog = {"xonsh"}
c.launch_menu = launch_menu
c.keys = keys
c.ssh_domains = ssh_domains

return c
