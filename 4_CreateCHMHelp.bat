@ECHO OFF
CHCP 65001
CLS

rem "Тихий" режим формирования CHM файла без ручного открытия проекта, средствами коммандной строки
rem Полный путь к WinCHMPortable.exe
SET ProgrammPath=e:\Work\Pyton\Util.RedMineToHelp\dist\WinCHM\
rem Полный путь к проекту CHM справки
SET ProjectPath=e:\Work\Pyton\Util.RedMineToHelp\dist\WinCHM_Project\help.wcp
%ProgrammPath%\WinCHMPortable.exe "%ProjectPath%" /h
