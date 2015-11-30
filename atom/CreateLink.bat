del %HOMEPATH%\.atom\atomfile
mklink /h %HOMEPATH%\.atom\atomfile .\atomfile
del %HOMEPATH%\.atom\config.cson
mklink /h %HOMEPATH%\.atom\config.cson .\config.cson
del %HOMEPATH%\.atom\init.coffee
mklink /h %HOMEPATH%\.atom\init.coffee .\init.coffee
del %HOMEPATH%\.atom\keymap.cson
mklink /h %HOMEPATH%\.atom\keymap.cson .\keymap.cson
del %HOMEPATH%\.atom\macros.coffee
mklink /h %HOMEPATH%\.atom\macros.coffee .\macros.coffee
del %HOMEPATH%\.atom\snippets.cson
mklink /h %HOMEPATH%\.atom\snippets.cson .\snippets.cson
del %HOMEPATH%\.atom\styles.less
mklink /h %HOMEPATH%\.atom\styles.less .\styles.less
