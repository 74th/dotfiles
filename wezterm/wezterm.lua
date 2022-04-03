local wezterm = require 'wezterm';

local function startswith(text, prefix)
  return text:find(prefix, 1, true) == 1
end

local function get_hostname()
    local f = io.popen ("/bin/hostname")
    local hostname = f:read("*a") or ""
    f:close()
    hostname =string.gsub(hostname, "\n$", "")
    return hostname
end

local c = {}
local keys = {}
local launch_menu = {}

local home_dir = os.getenv("HOME")
local hostname = get_hostname()

local is_linux = true
local is_macos = false
local is_m1mac = false
if startswith(home_dir, "/Users") then
  is_linux = false
  is_macos = true
  if hostname == "kukrushka" then
    is_m1mac = true
  end
end


if is_macos then
  table.insert(keys, {key="t", mods="CMD", action="ShowLauncher"})
else
  table.insert(keys, {key="t", mods="CTRL", action="ShowLauncher"})
end

if is_linux then
  table.insert(launch_menu, {
    label = "bash",
    args = {"/usr/bin/bash"},
  })
end
if is_macos then
  if is_m1mac then
    table.insert(launch_menu, {
      label = "bash",
      args = {"/opt/homebrew/bin/bash"},
    })
  else
    table.insert(launch_menu, {
      label = "bash",
      args = {"/usr/local/bin/bash"},
    })
  end
end

table.insert(launch_menu, {
  label = "xonsh",
  args = {"xonsh"},
})
table.insert(launch_menu, {
  label = "ssh lewill",
  args = {"ssh", "lewill", "xonsh"},
  domain = {DomainName="local"},
})

local ssh_domains = {}

table.insert(ssh_domains, {
  name = "lewill",
  remote_address = "lewill",
  username = "nnyn",
})
table.insert(ssh_domains, {
  name = "ciel",
  remote_address = "192.168.64.8",
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
if hostname == "kukrushka" then
  c.font_size = 12
end

local xonsh_path = home_dir.."/.local/bin/xonsh"
c.default_prog = {xonsh_path}

c.launch_menu = launch_menu
c.keys = keys
c.ssh_domains = ssh_domains

return c
