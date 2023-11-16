import json
import os
import re
from lxml import html

import keyboard
import requests  # request img from web
from bs4 import BeautifulSoup
from colorama import Fore
from redminelib import Redmine
# pip name Python-Redmine

# Read config
def ReadConfig(filepath):
    print(f'{Fore.YELLOW}Start ReadConfig')
    try:
        if os.path.exists(filepath):
            json_from_file: str = ""
            with open(filepath, 'r', encoding='utf-8-sig') as file:
                json_from_file = file.read()

            settings_json = json.loads(json_from_file)

            global glhost
            glhost = settings_json.get('host', None)

            global glapikey
            glapikey = settings_json.get('apikey', None)

            global glid
            glid = settings_json.get('list', [])

            global glclear
            glclear = settings_json.get('clear', False)

            global gllogon
            gllogon = settings_json.get('logon', 0)

            return True
        else:
            print(f'{Fore.YELLOW}Start create config')
            content_json = '''
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
            '''

            with open(filepath, 'w', encoding='utf-8-sig') as file:
                file.write(content_json)

            print(f'{Fore.GREEN}Create config: {Fore.BLUE}{filepath}\n{content_json}')
            return False
    except Exception as err:
        print(f'{Fore.RED}Delete config file, struct error...\n{err}')
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


# Delete inline link (#[digit])
def ClearRedmineLink(description):
    sresult = description
    if glclear and sresult.find('(#') != -1:
        if gllogon == 3:
            print(f'{Fore.YELLOW}--------------ClearRedmineLink---------------')
            print(f'{Fore.YELLOW}In: {sresult}')
        match = re.findall(r'\(\#\d*\)', description)
        for el in match:
            if gllogon == 3:
                print(f'{Fore.GREEN}{el =}')
            sresult = sresult.replace(el, '')

        if gllogon == 3:
            print(f'{Fore.YELLOW}Out: {sresult}')
            print(f'{Fore.YELLOW}--------------ClearRedmineLink---------------')
    return sresult


#  Get table and create file
def ProcessDescription(download_directory, description):
    description = ClearDescription(description)
    description = f'<html><body>{description}</body></html>'

    # 1 Получаем таблицы
    html_content = html.fromstring(description)
    tables = html_content.xpath(".//table")  # таблицы документа
    for table in tables:
        if gllogon >= 1:
            html_tablest = html.tostring(table, encoding='unicode')
            print(f'{Fore.BLUE}------------------TABLE------------------------')
            if gllogon >= 2:
                print(f'{Fore.WHITE}{html_tablest}')

        row_list = table.xpath(".//tr")  # строки таблицы
        rInd = 0
        isSkip: bool = True
        head_row = ""  # Заголовок таблицы
        for row in row_list:
            rInd = rInd + 1

            html_row = html.tostring(row, encoding='unicode')
            html_row = ClearRedmineLink(html_row)

            if gllogon >= 1:
                print(f'{Fore.BLUE}------------------ROW {rInd}------------------------')
                if gllogon >= 2:
                    print(f'{Fore.WHITE}{html_row}')

            col_list = row.xpath(".//th")  # все столбцы строки
            if len(col_list) == 0:
                col_list = row.xpath(".//td")  # все столбцы строки

            Article = ""
            if len(col_list) > 0:
                Article = html.tostring(col_list[0], encoding='unicode')
                Article = Article.strip('\n')
                Article = Article.strip('\r')
                Article = Article.strip('\t')
                if gllogon >= 2:
                    print(f'{Fore.WHITE}{Article=}')

            # 2 Проверка шапки таблицы на наличие в первом столбце HelpID
            if rInd == 1:
                if gllogon:
                    print(f'{Fore.WHITE}Первая строка, первый столбец: {Article=}')
                if Article.find("HelpID") > 0:
                    isSkip = False
                    head_row = html_row
            if isSkip:
                print(f'{Fore.RED}Первый столбец первой строки не HelpID')
                break

            # 3 Разбиваем таблицу построчно по наличию HelpID и записываем в файл
            if rInd > 1:
                find_id_article = ClearDescription(Article)
                ttd = re.findall('<.+?>', find_id_article)  # убираем <td>
                if len(ttd) < 2:
                    print(f'{Fore.RED}{find_id_article} не столбец, отсутствует <td>...</td>')
                    Article = ""
                else:
                    if gllogon >= 2:
                        print(f'Del ({ttd[0]}; {ttd[(len(ttd) - 1)]})')
                    find_id_article = ClearDescription(find_id_article.lstrip(ttd[0]).rstrip(ttd[(len(ttd) - 1)]))
                    Article = find_id_article
                    if gllogon >= 2:
                        print(f'{find_id_article=}')

                # Article = Article.replace()
                dgt = re.findall('(\d+)', Article)
                article_id = Article
                if len(dgt) > 0:
                    article_id = dgt[0]
                    if gllogon >= 1:
                        print(f'{article_id=}')
                if article_id.isdigit():
                    Id = int(article_id)
                    if Id > 99999:
                        ArticleFle = f'Article{article_id}.html'
                        content = f'<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">\n<html>\n'
                        content = f'{content}\n<head><title>{article_id}</title>\n<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">\n</head>'
                        content = f'{content}\n<style>table, th, td {{border: 1px solid black; border-collapse: collapse;}}</style>\n<body>'
                        content = f'{content}\n<table width="80%">\n<tbody>\n{head_row}\n{html_row}\n</tbody>\n</table>\n'
                        content = f'{content}\n</body>\n</html>'
                        content = ClearDescription(content)
                        export_file_name = os.path.join(download_directory, ArticleFle)
                        WriteHtml(content, export_file_name)
                    else:
                        print(f'{Fore.RED}HelpID меньше 999999, ({Id})')
                else:
                    print(f'{Fore.RED}HelpID не число, ({article_id})')


def main():
    redmine = Redmine(glhost, key=glapikey)
    print(f'{Fore.CYAN}{glhost=}')
    print(f'{Fore.CYAN}{glapikey=}')
    print(f'{Fore.CYAN}{currentDirectory=}')
    print(f'{Fore.CYAN}{gllogon=}')

    download_directory = os.path.join(currentDirectory, "Dowload")
    if not os.path.exists(download_directory):
        os.makedirs(download_directory)
        print(f"{Fore.CYAN}{download_directory=}")
    print()
    print(f'{Fore.CYAN}===========================================================================')
    indx = 0

    for curId in idList:
        try:
            if curId != "":
                indx = indx + 1
                print(f'{Fore.GREEN}Process {indx}: {curId=}')

                if curId.isdigit():
                    print(f'Get RedMine Issue Description: {curId=}')
                    # 1 Get RedMine Issue Description
                    issue = redmine.issue.get(curId, include=['watchers'])
                    issue_description = issue.description
                    try:
                        ProcessDescription(download_directory, issue_description)
                    except Exception as err:
                        print(f'{Fore.RED}Some Issue error...\n{err}')

                    print(f'Количество наблюдателей = {len(issue.watchers)}')
                    for user in issue.watchers:
                        usr = redmine.user.get(user.id)
                        print(f'{user} = {usr.mail}')
                else:
                    print(f'Get RedMine Wiki Description: {curId=}')

                    wiki_id = curId.split('/')
                    if len(wiki_id) == 3:
                        project_id = wiki_id[0]
                        wiki_name = wiki_id[2]

                        # 1 Get RedMine Wiki Description
                        wiki = redmine.wiki_page.get(wiki_name, project_id=project_id, include=[])
                        wiki_description = wiki.text
                        try:
                            ProcessDescription(download_directory, wiki_description)
                        except Exception as err:
                            print(f'{Fore.RED}Some Wiki error...\n{err}')
                    else:
                        print(f"Skip wiki {wiki_id=}")
        except Exception as err:
            print(f'{Fore.RED}Some "{curId}" error...\n{err}')

        print(f'{Fore.CYAN}_________________________________________________________')

    print(f'{Fore.CYAN}Process completed, press Space...')
    keyboard.wait("space")


if __name__ == "__main__":
    print(f"{Fore.CYAN}Last update: Cherepanov Maxim masygreen@gmail.com (c), 07.2022-11.2023")
    print(f"{Fore.CYAN}Convert table to *.html")

    currentDirectory = os.getcwd()
    configFilePath = os.path.join(currentDirectory, 'config.cfg')

    if ReadConfig(configFilePath):
        idList = glid
        print(f'{idList=}')

        main()
    else:
        print(f'{Fore.RED}Pleas edit default Config value: {Fore.BLUE}{configFilePath}')
        print(f'{Fore.CYAN}Process completed, press Space...')
        keyboard.wait("space")
