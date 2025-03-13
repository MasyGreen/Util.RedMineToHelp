import json
import os
import re
from lxml import html

import keyboard
from colorama import Fore
from redminelib import Redmine
# pip name Python-Redmine

# Read config
def read_config(filepath):
    print(f'{Fore.YELLOW}Start ReadConfig')
    try:
        if os.path.exists(filepath):
            json_from_file: str = ""
            with open(filepath, 'r', encoding='utf-8-sig') as file:
                json_from_file = file.read()

            settings_json = json.loads(json_from_file)

            global settings_host
            settings_host = settings_json.get('host', None)

            global settings_apikey
            settings_apikey = settings_json.get('apikey', None)

            global settings_id
            settings_id = settings_json.get('list', [])

            global settings_clear
            settings_clear = settings_json.get('clear', False)

            global settings_logon_level
            settings_logon_level = settings_json.get('logon', 0)

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
def write_html(description, filename):
    print(f'{Fore.YELLOW}File save as: {filename}')
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(f"{description}")


#  Delete empty string
def clear_description(description):
    str_result = ""
    for cur_str in description.split('\n'):
        if cur_str.strip() != '':
            cur_str = cur_str.strip('\n')
            cur_str = cur_str.strip('\r')
            cur_str = cur_str.strip('\t')
            str_result = str_result + cur_str + '\n'
    return str_result


# Delete inline link (#[digit])
def clear_redmine_link(description):
    str_result = description
    if settings_clear and str_result.find('(#') != -1:
        if settings_logon_level == 3:
            print(f'{Fore.YELLOW}--------------ClearRedmineLink---------------')
            print(f'{Fore.YELLOW}In: {str_result}')
        match = re.findall(r'\(\#\d*\)', description)
        for el in match:
            if settings_logon_level == 3:
                print(f'{Fore.GREEN}{el =}')
            str_result = str_result.replace(el, '')

        if settings_logon_level == 3:
            print(f'{Fore.YELLOW}Out: {str_result}')
            print(f'{Fore.YELLOW}--------------ClearRedmineLink---------------')
    return str_result

# Check Is HelpID Table?
def check_table(row):
    check_val = ""
    item0 = row.xpath('./th')
    if len(item0) == 0:
        item0 = row.xpath('./td')
        if len(item0) > 0:
            check_val = html.tostring(item0[0], encoding='unicode')
    else:
        check_val = html.tostring(item0[0], encoding='unicode')

    if check_val.lower().find("helpid") > 0:
        if settings_logon_level >= 1:
            print(f'{Fore.GREEN}: {check_val=}')
        return True
    else:
        if settings_logon_level >= 1:
            print(f'{Fore.RED}: {check_val=}')
        return False

#  Get table and create file
def process_description(download_directory, description):
    description = clear_description(description)
    description = f'<html><body>{description}</body></html>'

    # 1 Получаем таблицы
    html_content = html.fromstring(description)
    tables = html_content.xpath(".//table")  # таблицы документа - все на всех уровнях (//)
    for table in tables:
        if settings_logon_level >= 1:
            html_table = html.tostring(table, encoding='unicode')
            print(f'{Fore.BLUE}------------------TABLE------------------------')
            if settings_logon_level >= 2:
                print(f'{Fore.WHITE}{html_table}')

        # необходимо исключить из разбора строки вложенных таблиц
        row_list = table.xpath("./tr")  # строки таблицы первого уровня
        row_list_th = table.xpath("./thead/tr")  # строки таблицы первого уровня
        row_list_tb = table.xpath("./tbody/tr")  # строки таблицы первого уровня

        if len(row_list_th) > 0:
            row_list.extend(row_list_th)
            print(f'{Fore.YELLOW} use ./thead {len(row_list_th)}')

        if len(row_list_tb) > 0:
            row_list.extend(row_list_tb)
            print(f'{Fore.YELLOW} use ./tbody {len(row_list_tb)}')

        # Если в таблице меньше 2 строк т.е. только заголовок - нет смысла разбирать
        is_parce = False
        if len(row_list) >= 2:
            if settings_logon_level >= 1:
                print(f'{Fore.RED}CHEK: {len(row_list)=}')
            is_parce = check_table(row_list[0])
        else:
            if settings_logon_level >= 1:
                print(f'{Fore.RED}SKIP: {len(row_list)=}')

        if is_parce:
            cur_row_index = 0
            head_row = ""  # Заголовок таблицы
            for row in row_list:
                cur_row_index = cur_row_index + 1

                if settings_logon_level >= 1:
                    print(f'{Fore.YELLOW} {cur_row_index=}')

                html_row = html.tostring(row, encoding='unicode')
                html_row = clear_redmine_link(html_row)

                col_list = row.xpath("./th")  # все столбцы из строки первого уровня (заголовок)
                if len(col_list) == 0:
                    col_list = row.xpath("./td")  # все столбцы из строки первого уровня (обычные строки)

                article = ""
                if len(col_list) > 0:
                    article = html.tostring(col_list[0], encoding='unicode')
                    article = article.strip('\n')
                    article = article.strip('\r')
                    article = article.strip('\t')
                    if settings_logon_level >= 2:
                        print(f'{Fore.WHITE}{article=}')

                # 2 Сохраняем первую строку для вставки в шапку новой таблицы
                if cur_row_index == 1:
                    head_row = html_row

                # 3 Разбиваем таблицу построчно по наличию HelpID и записываем в файл
                if cur_row_index > 1:
                    find_id_article = clear_description(article)
                    ttd = re.findall('<.+?>', find_id_article)  # убираем <td>
                    if len(ttd) < 2:
                        print(f'{Fore.RED}{find_id_article} не столбец, отсутствует <td>...</td>')
                        article = ""
                    else:
                        if settings_logon_level >= 2:
                            print(f'Del ({ttd[0]}; {ttd[(len(ttd) - 1)]})')
                        find_id_article = clear_description(find_id_article.lstrip(ttd[0]).rstrip(ttd[(len(ttd) - 1)]))
                        article = find_id_article
                        if settings_logon_level >= 2:
                            print(f'{find_id_article=}')

                    # Article = Article.replace()
                    dgt = re.findall('(\d+)', article)
                    article_id = article
                    if len(dgt) > 0:
                        # Some value can be color or another digit - get only >= 99999
                        article_id = dgt[0]
                        for dg in dgt:
                            if int(dg) > 99999:
                                article_id = dg

                        if settings_logon_level >= 1:
                            print(f'{article_id=}')
                    if article_id.isdigit():
                        Id = int(article_id)
                        if Id > 99999:
                            article_fle = f'Article{article_id}.html'
                            content = f'<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">\n<html>\n'
                            content = f'{content}\n<head><title>{article_id}</title>\n<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">\n</head>'
                            content = f'{content}\n<style>table, th, td {{border: 1px solid black; border-collapse: collapse;}}</style>\n<body>'
                            content = f'{content}\n<table width="80%">\n<tbody>\n{head_row}\n{html_row}\n</tbody>\n</table>\n'
                            content = f'{content}\n</body>\n</html>'
                            content = clear_description(content)
                            export_file_name = os.path.join(download_directory, article_fle)
                            write_html(content, export_file_name)
                        else:
                            print(f'{Fore.RED}HelpID меньше 99999, ({Id})')
                    else:
                        print(f'{Fore.RED}HelpID не число, ({article_id})')

def main():
    redmine = Redmine(settings_host, key=settings_apikey)
    print(f'{Fore.CYAN}{settings_host=}')
    print(f'{Fore.CYAN}{settings_apikey=}')
    print(f'{Fore.CYAN}{currentDirectory=}')
    print(f'{Fore.CYAN}{settings_logon_level=}')

    download_directory = os.path.join(currentDirectory, "Dowload")
    if not os.path.exists(download_directory):
        os.makedirs(download_directory)
        print(f"{Fore.CYAN}{download_directory=}")
    print()
    print(f'{Fore.CYAN}===========================================================================')
    index = 0

    for curId in idList:
        try:
            if curId != "":
                index = index + 1
                print(f'{Fore.GREEN}Process {index}: {curId=}')

                if curId.isdigit():
                    print(f'Get RedMine Issue Description: {curId=}')
                    # 1 Get RedMine Issue Description
                    issue = redmine.issue.get(curId, include=['watchers'])
                    issue_description = issue.description
                    try:
                        process_description(download_directory, issue_description)
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
                            process_description(download_directory, wiki_description)
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

    if read_config(configFilePath):
        idList = settings_id
        print(f'{idList=}')

        main()
    else:
        print(f'{Fore.RED}Pleas edit default Config value: {Fore.BLUE}{configFilePath}')
        print(f'{Fore.CYAN}Process completed, press Space...')
        keyboard.wait("space")
