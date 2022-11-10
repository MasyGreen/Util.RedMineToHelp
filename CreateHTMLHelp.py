import os
from lxml import html
from colorama import Fore

def main():
    print(f'{Fore.CYAN}{currentDirectory=}')

    projectDirectory = os.path.join(currentDirectory, "WinCHM_Project")
    print(f'{Fore.CYAN}{projectDirectory=}')
    if not os.path.exists(projectDirectory):
        print(f'{Fore.RED}Folder {projectDirectory} not found')
        exit(0)

    helpFileFolder = os.path.join(currentDirectory, "HelpCHM")
    if not os.path.exists(helpFileFolder):
        os.mkdir(helpFileFolder)
    print(f'{Fore.CYAN}{helpFileFolder=}')

    hlpFile = os.path.join(helpFileFolder, "help.htm")
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
    currentDirectory = os.getcwd()
    main()
