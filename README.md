# I.1 [RedMineDownload] Конвертирует Issue и Wiki записи RedMine в Html

Настроить **config.cfg** (запустить единожды *.exe для создания шаблона файла)

* [host], IP или DNS имя RedMine (например: **http://192.168.1.1**)
* [apikey], *RedMine - Моя учетная запись - Ключ доступа к API*, RESTAPI должен быть глобально включен Администратором (например: **aldjfoeiwgj9348gn348**)
* [list], список **Issue ID** и/или страниц **Wiki**, например: 
  + *["1","2","114"]*
  + *["id100/wiki/Help1","id103/wiki/Help2","114""]*
* [clear], (true) удалить внутренние ссылки RedMine по шаблону *(#[цифры])*, например: **(#3168)**
* Запустить

## I.2 Получить ключ API

![alt text](https://github.com/MasyGreen/RedMine.ToHelp/blob/master/Settings%20manual%20(config.cfg).jpg)

## I.3 Пример config.cfg
В формате JSON
```
{
    "host": "http://192.168.1.1",
    "apikey": "dq3inqgnqe8igqngninkkvekmviewrgir9384",
    "clear": false,
    "logon": 0,
    "list": [
        "1677",
        "318",
        "id103/wiki/Help2"
    ]
}
```

## I.4 Результат
Issue или Wiki должна содержать html таблицу, первый столбец первой строки которой [Help ID].

Утилита разбивает строки таблицы содержащие числовое значение [Help ID] на отдельные файлы *"Article[Help ID].htm"* в новом каталоге *Dowload*

# II.1 [CreateWinCHMProject] Конвертирует Html в проект WinCHM

1. Копирует файл шаблона из *Template* в каталог *WinCHM_Project*
2. Получает файлы *"Dowload/Article[Help ID].htm"*
3. Дополняет файл проекта *help.wcp* найденными файлами


## II.2 Результат
Настроенный *help.wcp* с метками **[Help ID]** доступный для редактирования в *WinCHM* и компиляции справки *help.chm*

По умолчанию на каталог выше от текущего *RedMine.ToHelp\HelpCHM\help.chm*

# III.1 [CreateHTMLHelp] Конвертирует Html в файл справки help.chm

1. Получает файлы *"WinCHM_Project/Article[Help ID].htm"*
2. Формирует один общий файл *WinCHM_Project/help.htm* дополняя секцию **<body>** -> **<body id="[Help ID]">**

## II.2 Результат
Настроенный *help.htm* готовый к подключению в Систему