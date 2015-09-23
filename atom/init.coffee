# 保存とノーマルモードへの回帰を同時に行う
atom.commands.add 'atom-text-editor.vim-mode', 'custom:save-and-normalmode', ->
  view = atom.views.getView atom.workspace.getActiveTextEditor()
  atom.commands.dispatch view, 'core:save'
  atom.commands.dispatch view, 'vim-mode:reset-normal-mode'
