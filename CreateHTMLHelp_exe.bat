SET EXENAME=3_CreateHTMLHelp
SET PYNAME=CreateHTMLHelp
rmdir /s /q build
if exist "dist\%EXENAME%.exe" del "dist\%EXENAME%.exe"
if exist *.log del *.log
if exist *.spec del *.spec
pyinstaller -F -i "Icon.ico" %PYNAME%.py
if exist *.log del *.log
if exist *.spec del *.spec
ren "dist\%PYNAME%.exe" %EXENAME%.exe
rmdir /s /q build