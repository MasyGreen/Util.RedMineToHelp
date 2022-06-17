SET PYNAME=RedMineDownloadToHelp
rmdir /s /q build
if exist %PYNAME%.exe del %PYNAME%.exe
if exist *.log del *.log
if exist *.spec del *.spec
pyinstaller -F -i "Icon.ico" %PYNAME%.py
if exist *.log del *.log
if exist *.spec del *.spec
rmdir /s /q build