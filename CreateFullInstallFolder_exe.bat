@ECHO OFF
CHCP 65001
CLS

rem ==============================================
SET EXENAME=1_RedMineDownload
SET PYNAME=RedMineDownload
rmdir /s /q build
if exist "dist\%EXENAME%.exe" del "dist\%EXENAME%.exe"
if exist *.log del *.log
if exist *.spec del *.spec
pyinstaller -F -i "Icon.ico" %PYNAME%.py
if exist *.log del *.log
if exist *.spec del *.spec
ren "dist\%PYNAME%.exe" %EXENAME%.exe
rmdir /s /q build

rem ==============================================
SET EXENAME=2_CreateWinCHMProject
SET PYNAME=CreateWinCHMProject
rmdir /s /q build
if exist "dist\%EXENAME%.exe" del "dist\%EXENAME%.exe"
if exist *.log del *.log
if exist *.spec del *.spec
pyinstaller -F -i "Icon.ico" %PYNAME%.py
if exist *.log del *.log
if exist *.spec del *.spec
ren "dist\%PYNAME%.exe" %EXENAME%.exe
rmdir /s /q build

rem ==============================================
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

rem ==============================================
rmdir /s /q "dist\Template"
rem set request xcopy as D
echo D | xcopy "Template" "dist\Template" /e /c /f /y /r

rem ==============================================
if exist "dist\DeleteTmpFolder.bat" del "dist\DeleteTmpFolder.bat"
copy DeleteTmpFolder.bat "dist\DeleteTmpFolder.bat"
if exist "dist\4_CreateCHMHelp.bat" del "dist\4_CreateCHMHelp.bat"
copy 4_CreateCHMHelp.bat "dist\4_CreateCHMHelp.bat"


