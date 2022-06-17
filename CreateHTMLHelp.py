import shutil
import configparser
import os
import re
from lxml import html

import keyboard
import requests  # request img from web
from bs4 import BeautifulSoup
from colorama import Fore
from redminelib import Redmine


def main():
    print(f'{Fore.CYAN}{currentDirectory=}')

    projectDirectory = os.path.join(currentDirectory, "WinCHM_Project")
    print(f'{Fore.CYAN}{projectDirectory=}')
    if not os.path.exists(projectDirectory):
        print(f'{Fore.RED}Folder {projectDirectory} not found')
        exit(0)

    hlpFile = os.path.join(projectDirectory, "help.htm")
    with open(hlpFile, 'w', encoding='utf-8') as wf:
        wf.write(f'<html>\n')
        for file in os.listdir(projectDirectory):
            if file.startswith("Article"):
                curFile = os.path.join(projectDirectory, file)
                curIndex = file.strip("Article").strip(".html")
                with open(curFile, 'r', encoding='utf-8') as rf:
                    description = rf.read()
                    htmlContent = html.fromstring(description)
                    bodys = htmlContent.xpath(".//body")  # содержимое документа
                    for body in bodys:
                        htmlBody = html.tostring(body, encoding='unicode')
                        htmlBody = htmlBody.replace('<body>',f"<body id='{curIndex}'>")
                        wf.write(f'{htmlBody}\n')
        wf.write(f'</html>')


if __name__ == "__main__":
    print(f"{Fore.CYAN}Last update: Cherepanov Maxim masygreen@gmail.com (c), 06.2022")
    print(f"{Fore.CYAN}Create HTML help from Download/Article*.html")
    global logOn
    logOn = True
    currentDirectory = os.getcwd()
    main()