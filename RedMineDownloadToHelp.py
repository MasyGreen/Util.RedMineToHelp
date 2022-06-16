import configparser
import os
import re
from lxml import html

import keyboard
import requests  # request img from web
from bs4 import BeautifulSoup
from colorama import Fore
from redminelib import Redmine


# Read config
def ReadConfig(filepath):
    print(f'{Fore.YELLOW}Start ReadConfig')

    if os.path.exists(filepath):
        config = configparser.ConfigParser()
        config.read(filepath, "utf8")
        config.sections()

        global glhost
        glhost = config.has_option("Settings", "host") and config.get("Settings", "host") or None

        global glapikey
        glapikey = config.has_option("Settings", "apikey") and config.get("Settings", "apikey") or None

        global glid
        glid = config.has_option("Settings", "id") and config.get("Settings", "id") or None

        return True
    else:
        print(f'{Fore.YELLOW}Start create config')
        config = configparser.ConfigParser()
        config.add_section("Settings")

        config.set("Settings", "host", 'http://192.168.1.1')
        config.set("Settings", "apikey", 'dq3inqgnqe8igqngninkkvekmviewrgir9384')
        config.set("Settings", "id", '1677;318;id103/wiki/Help2')

        with open(filepath, "w") as config_file:
            config.write(config_file)

        print(f'{Fore.GREEN}Create config: {Fore.BLUE}{filepath},{config_file}')
        return False


# Write html
def WriteHtml(description, filename):
    print(f'{Fore.YELLOW}File save as: {filename}')
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(f"{description}")


#  Delete empty string
def ClearDescription(description):
    sresult = ""
    for curstr in description.split('\n'):
        if curstr.strip() != '':
            curstr = curstr.strip('\n')
            curstr = curstr.strip('\r')
            curstr = curstr.strip('\t')
            sresult = sresult + curstr + '\n'
    return sresult


#  Get table and create file
def ProcessDescription(downloadDirectory, description):
    description = ClearDescription(description)
    description = f'<html><body>{description}</body></html>'

    # 1 Получаем таблицы
    htmlContent = html.fromstring(description)
    tables = htmlContent.xpath(".//table")  # таблицы документа
    for table in tables:
        if logOn:
            htmlTablest = html.tostring(table, encoding='unicode')
            print(f'{Fore.RED}------------------TABLE------------------------')
            print(f'{Fore.WHITE}{htmlTablest}')

        rowList = table.xpath(".//tr")  # строки таблицы
        rInd = 0
        isSkip: bool = True

        for row in rowList:
            rInd = rInd + 1
            htmlRow = html.tostring(row, encoding='unicode')

            if logOn:
                print(f'{Fore.RED}------------------ROW {rInd}------------------------')
                print(f'{Fore.WHITE}{htmlRow}')

            colList = row.xpath(".//th")  # все столбцы строки
            Article = ""

            if len(colList) > 0:
                Article = html.tostring(colList[0], encoding='unicode')

            # 2 Проверка шапки таблицы на наличие в первом столбце HelpID
            if rInd == 1:
                if logOn:
                    print(f'{Article}')
                if Article.find("HelpID") > 0:
                    isSkip = False
            if isSkip:
                break

            # 3 Разбиваем таблицу построчно по наличию HelpID и записываем в файл
            if rInd > 1:
                content = f'<html>\n'
                content = f'{content}\n<style>table, th, td {{border: 1px solid black; border-collapse: collapse;}}</style>\n<body>'
                content = f'{content}\n<table width="80%">\n<tbody>\n{htmlRow}\n</tbody>\n</table>\n</body>\n</html>'
                # content = f'<html><body><table style="width: 80%; border=".5">\n<tbody>\n{htmlRow}\n</tbody>\n</table></body></html>'
                content = ClearDescription(content)
                exportFileName = os.path.join(downloadDirectory, f'Article{rInd}.html')
                WriteHtml(content, exportFileName)

    #
    # txt_link = html.tostring(link_tablebg, encoding='unicode')
    # print(f'{Fore.WHITE}{htmlTablest}')
    # print(f'{Fore.WHITE}{rowList}')
    # exportFileName = os.path.join(downloadDirectory, f'Issue.html')
    # WriteHtml(description, exportFileName)


def main():
    redmine = Redmine(glhost, key=glapikey)
    print(f'{Fore.CYAN}{glhost=}')
    print(f'{Fore.CYAN}{glapikey=}')
    print(f'{Fore.CYAN}{currentDirectory=}')

    downloadDirectory = os.path.join(currentDirectory, "Dowload")
    if not os.path.exists(downloadDirectory):
        os.makedirs(downloadDirectory)
        print(f"{Fore.CYAN}{downloadDirectory=}")
    print()
    print(f'{Fore.CYAN}===========================================================================')
    indx = 0

    for curId in idList:
        if curId != "":
            indx = indx + 1
            print(f'{Fore.GREEN}Process {indx}: {curId=}')

            if curId.isdigit():
                print(f'Get RedMine Issue Description: {curId=}')

                # 1 Get RedMine Issue Description
                issue = redmine.issue.get(curId, include=[])
                issueDescription = issue.description
                ProcessDescription(downloadDirectory, issueDescription)

            else:
                print(f'Get RedMine Wiki Description: {curId=}')

                wikiId = curId.split('/')
                if len(wikiId) == 3:
                    projectId = wikiId[0]
                    wikiName = wikiId[2]

                    # 1 Get RedMine Wiki Description
                    wiki = redmine.wiki_page.get(wikiName, project_id=projectId, include=[])
                    wikiDescription = wiki.text
                    ProcessDescription(downloadDirectory, wikiDescription)
                else:
                    print(f"Skip wiki {wikiId=}")

        print(f'{Fore.CYAN}_________________________________________________________')

    print(f'{Fore.CYAN}Process completed, press Space...')
    keyboard.wait("space")


if __name__ == "__main__":
    print(f"{Fore.CYAN}Last update: Cherepanov Maxim masygreen@gmail.com (c), 06.2022")
    print(f"{Fore.CYAN}Convert table to *.html")
    global logOn
    logOn = True
    currentDirectory = os.getcwd()
    configFilePath = os.path.join(currentDirectory, 'config.cfg')

    if ReadConfig(configFilePath):
        idList = glid.split(';')
        print(f'{idList=}')

        main()
    else:
        print(f'{Fore.RED}Pleas edit default Config value: {Fore.BLUE}{configFilePath}')
        print(f'{Fore.CYAN}Process completed, press Space...')
        # keyboard.wait("space")
