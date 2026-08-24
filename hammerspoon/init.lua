local ghosttyBundleId = "com.mitchellh.ghostty"

local function positionGhostty(win)
  local screen = hs.mouse.getCurrentScreen()
  local frame = screen:frame()

  local width

  -- 大きい外部ディスプレイ
  if frame.w >= 2000 then
    width = 1300
  else
    -- Mac内蔵ディスプレイ
    width = math.floor(frame.w * 0.65)
  end

  win:setFrame({
    x = frame.x,
    y = frame.y,
    w = width,
    h = frame.h,
  })
end

hs.hotkey.bind({"cmd"}, "F2", function()
  local app = hs.application.get(ghosttyBundleId)

  if app and app:isFrontmost() and not app:isHidden() then
    app:hide()
    return
  end

  if not app then
    app = hs.application.open(ghosttyBundleId, 2, true)
  else
    app:unhide()
    app:activate()
  end

  if not app then
    return
  end

  local win = app:focusedWindow() or app:mainWindow()

  if win then
    positionGhostty(win)
    win:focus()
  end
end)
