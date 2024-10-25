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

html1 = """
<h1>Коды базовых объектов</h1>
<table>
<thead>
<tr><th scope="col">HELPID 1</th> <th scope="col">

<table>
<tr><th scope="col">INSIDE</th><th scope="col">ROW1 COl2</th></tr>
</table>

</th></tr>
<tr><td scope="col">ROW2 COl1</td><td scope="col">ROW2 COl2</td></tr>
</thead>
</table>

<table>
<thead>
<tr><th scope="col">HELPID 2</th><th scope="col">ROW1 COl2 T2</th></tr>
</thead>
<tbody>
<tr><th scope="col">ROW1 COl2 T2</th><th scope="col">ROW1 COl2 T2</th></tr>
</tbody>
</table>
"""

html2 = """
<table>
<tr>
<th scope="col">ROW1COl1 T2</th>
<th scope="col">ROW1COl2 T2</th>
</tr>
"""

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
        print(f'{Fore.GREEN}: {check_val=}')
        return True
    else:
        print(f'{Fore.RED}: {check_val=}')
        return False


def process_description(description):
    description = f'<html><body>{description}</body></html>'

    # 1 Получаем таблицы
    html_content = html.fromstring(description)
    tables = html_content.xpath(".//table")  # таблицы документа
    for table in tables:
        s = html.tostring(table, encoding='unicode')
        print(f'{Fore.WHITE}MT: {s}\n---------------------------')

        row_list = []
        row_list = table.xpath("./tr")  # строки таблицы
        print(f"{row_list=}")

        row_list_th = table.xpath("./thead/tr")  # строки таблицы
        print(f"{row_list_th=}")

        row_list_tb = table.xpath("./tbody/tr")  # строки таблицы
        print(f"{row_list_tb=}")

        if len(row_list_th)>0:
            row_list.extend(row_list_th)
        if len(row_list_tb)>0:
            row_list.extend(row_list_tb)

        print(f"EXT: {row_list=}")

        is_parce = False
        if len(row_list)>=2:
            is_parce = check_table(row_list[0])
        else:
            print(f'{Fore.RED}SKIP: {len(row_list)=}')


        if is_parce:
            for row in row_list:
                s = html.tostring(row)
                print(f'{Fore.BLUE}WORK: {s}')


        print(f'{Fore.WHITE}================================================')
if __name__ == "__main__":
    process_description(html1)