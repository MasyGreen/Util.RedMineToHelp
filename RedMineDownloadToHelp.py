import configparser
import os
import re

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
    with open(filename, 'a', encoding='utf-8') as f:
        f.write(f"{description}")


#  1) Delete empty string
#  2) LowDown <hX> on 1 livel
def EditBlock(curblok):
    sresult = ""
    for curstr in curblok.split('\n'):
        if curstr.strip() != '':
            hlist = re.findall(r'<h\d*', curstr)
            if len(hlist) > 0:
                hitem = hlist[0].replace("<h", "").strip()
                try:
                    newhitem = int(hitem) + 1
                    curstr = curstr.replace(f"<h{hitem}", f"<h{newhitem}").replace(f"/h{hitem}>", f"/h{newhitem}>")
                except:
                    curstr = curstr
            sresult = sresult + curstr + '\n'

    return sresult


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
        print(f'{curId=}')
        if curId != "":
            indx = indx + 1
            print(f'{Fore.GREEN}Process {indx}: {curId=}')

            if curId.isdigit():
                print(f'Get RedMine Issue Description: {curId=}')

                # 1 Get RedMine Issue Description
                issue = redmine.issue.get(curId, include=[])
                issueDescription = issue.description

                print()

                exportfilename = os.path.join(downloadDirectory, f'Issue - {curId}.html')
                WriteHtml(issueDescription, exportfilename)
            else:
                print(f'Get RedMine Wiki Description: {curId=}')

                wikiId = curId.split('/')
                if len(wikiId) == 3:
                    projectid = wikiId[0]
                    wikiname = wikiId[2]

                    # 1 Get RedMine Wiki Description
                    wiki = redmine.wiki_page.get(wikiname, project_id=projectid, include=[])
                    wikiDescription = wiki.text

                    print()

                    exportfilename = os.path.join(downloadDirectory, f'Wiki - {wikiname}.html')
                    WriteHtml(wikiDescription, exportfilename)
                else:
                    print(f"Skip wiki {wikiId=}")

        print(f'{Fore.CYAN}_________________________________________________________')

    print(f'{Fore.CYAN}Process completed, press Space...')
    keyboard.wait("space")


if __name__ == "__main__":
    print(f"{Fore.CYAN}Last update: Cherepanov Maxim masygreen@gmail.com (c), 06.2022")
    print(f"{Fore.CYAN}Convert table to *.html")

    currentDirectory = os.getcwd()
    configfilepath = os.path.join(currentDirectory, 'config.cfg')

    if ReadConfig(configfilepath):
        idList = glid.split(';')
        print(f'{idList=}')

        main()
    else:
        print(f'{Fore.RED}Pleas edit default Config value: {Fore.BLUE}{configfilepath}')
        print(f'{Fore.CYAN}Process completed, press Space...')
        keyboard.wait("space")
