# I.1 [RedMineDownloadToHelp] Конвертирует Issue и Wiki записи RedMine в Html

1. Настроить **config.cfg** (запустить единожды *.exe для создания шаблона файла)
   1. [host], IP или DNS имя RedMine (например: **http://192.168.1.1**)
   2. [apikey], *RedMine - Моя учетная запись - Ключ доступа к API*, RESTAPI должен быть глобально включен Администратором (например: **aldjfoeiwgj9348gn348**)
   3. [id], список Issue ID и/или страниц Wiki разделенных *";"* (например: **1;2;114;9123** и/или **id100/wiki/Help1;id103/wiki/Help2**)
   4. Запустить

## I.2 Получить ключ API

![alt text](https://github.com/MasyGreen/RedMine.ToHelp/blob/master/Settings%20manual%20(config.cfg).jpg)

## I.3 Пример config.cfg
```
[Settings]
host = http://192.168.1.1
apikey = dq3inqgnqe8igqngninkkvekmviewrgir9384
id = 1677;318;id100/wiki/Help1
```

## I.4 Результат
Issue или Wiki должна содержать html таблицу, первый столбец которой является [Help ID].

Утилита разбивает строки таблицы содержащие числовое значение [Help ID] на отдельные файлы *"Article[Help ID].htm"* в новом каталоге *Dowload*

# II.1 [CreateWinCHMProject] Конвертирует Html в проект WinCHM

1. Копирует файл шаблона из *Template* в каталог *WinCHM_Project*
2. Получает файлы *"Dowload/Article[Help ID].htm"*
3. Дополняет файл проекта *help.wcp* найденными файлами


## II.2 Результат
Настроенный *help.wcp* с метками [Help ID] доступный для редактирования в *WinCHM* и компиляции справки *help.chm*

По умолчанию на каталог выше от текущего *RedMine.ToHelp\HelpCHM\help.chm*

# III.1 [CreateHTMLHelp] Конвертирует Html в файл справки help.chm

1. Получает файлы *"WinCHM_Project/Article[Help ID].htm"*
2. Формирует один общий файл *WinCHM_Project/help.htm* дополняя секцию **<body>** -> **<body id="[Help ID]">**

## II.2 Результат
Настроенный *help.htm* готовый к подключению в Систему