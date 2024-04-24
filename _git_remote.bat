@ECHO =====================Attention!!!============================
@ECHO Remote add
@ECHO =====================Attention!!!============================
CHCP 65001
pause
@ECHO =====================Список существующих============================
git remote -v
@ECHO =====================Удаление============================
git remote rm origingit
git remote rm originbit
git remote rm origin
git remote -v
@ECHO =====================Добавление============================
git remote add origingit git@github.com:MasyGreen/Util.RedMineToHelp.git
git remote add originbit git@bitbucket.org:masygreen/Util.RedMineToHelp.git
git remote add origin git@192.168.177.75:masygreen/Util.RedMineToHelp.git
@ECHO =====================Список существующих============================
git remote -v
pause