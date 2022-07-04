import shutil
import os

import keyboard
from colorama import Fore


def main():
    print(f'{Fore.CYAN}{currentDirectory=}')

    downloadDirectory = os.path.join(currentDirectory, "Dowload")
    print(f'{Fore.CYAN}{downloadDirectory=}')
    if not os.path.exists(downloadDirectory):
        print(f'{Fore.RED}Folder {downloadDirectory} not found')
        exit(0)

    templateDirectory = os.path.join(currentDirectory, "Template")
    print(f'{Fore.CYAN}{templateDirectory=}')
    if not os.path.exists(templateDirectory):
        print(f'{Fore.RED}Folder {templateDirectory} not found')
        exit(0)

    projectDirectory = os.path.join(currentDirectory, "WinCHM_Project")
    print(f'{Fore.CYAN}{projectDirectory=}')
    if not os.path.exists(projectDirectory):
        os.makedirs(projectDirectory)

    # 1 Переносим шаблон проекта
    shutil.copytree(templateDirectory, projectDirectory, symlinks=False, ignore=None,ignore_dangling_symlinks=False, dirs_exist_ok=True)

    # 2 Переносим статьи
    shutil.copytree(downloadDirectory, projectDirectory, symlinks=False, ignore=None, ignore_dangling_symlinks=False, dirs_exist_ok=True)

    # 3 Формирование файла проекта
    ind=2
    prjFile = os.path.join(projectDirectory,"help.wcp")
    with open(prjFile, 'a', encoding='utf-16') as f:
        f.write(f"\n")
        for file in os.listdir(downloadDirectory):
            if file.startswith("Article"):
                print(f"{Fore.YELLOW}Process {ind}: {file}")
                curIndex = file.strip("Article").strip(".html")
                f.write(f"TitleList.Title.{ind}={curIndex}\n")
                f.write(f"TitleList.Level.{ind}=1\n")
                f.write(f"TitleList.Url.{ind}={file}\n")
                f.write(f"TitleList.Icon.{ind}=0\n")
                f.write(f"TitleList.Status.{ind}=0\n")
                f.write(f"TitleList.Keywords.{ind}=\n")
                f.write(f"TitleList.ContextNumber.{ind}={curIndex}\n")
                f.write(f"TitleList.ApplyTemp.{ind}=0\n")
                f.write(f"TitleList.Expanded.{ind}=0\n")
                f.write(f"TitleList.Kind.{ind}=0\n")
                ind = ind + 1

        f.write(f"TitleList.Title.{ind}=Фиксированная вверху\n")
        f.write(f"TitleList.Level.{ind}=0\n")
        f.write(f"TitleList.Url.{ind}=template2\\fixedtop.htm\n")
        f.write(f"TitleList.Icon.{ind}=0\n")
        f.write(f"TitleList.Status.{ind}=0\n")
        f.write(f"TitleList.Keywords.{ind}=\n")
        f.write(f"TitleList.ContextNumber.{ind}=\n")
        f.write(f"TitleList.ApplyTemp.{ind}=0\n")
        f.write(f"TitleList.Expanded.{ind}=0\n")
        f.write(f"TitleList.Kind.{ind}=2\n")

    # 4 Исправление количества секций ([TOPICS]) для полного отображения
    prjFileT = os.path.join(projectDirectory, "help.tmp")
    with open(prjFile, 'r', encoding='utf-16') as f1, open(prjFileT, 'w', encoding='utf-16') as f2:
        lines = f1.readlines()
        for line in lines:
            if 'TitleList=' in line:
                f2.write(f'TitleList={ind+1}\n')
            else:
                f2.write(f'{line}\n')

    os.remove(prjFile)  # удаляем основной файл
    shutil.copy(prjFileT, prjFile) # переименовываем временный в основной
    os.remove(prjFileT)  # удаляем основной файл

    print(f'{Fore.CYAN}Process completed, press Space...')
    keyboard.wait("space")

if __name__ == "__main__":
    print(f"{Fore.CYAN}Last update: Cherepanov Maxim masygreen@gmail.com (c), 06.2022")
    print(f"{Fore.CYAN}Create WinCHM project from Download/Article*.html")
    currentDirectory = os.getcwd()
    main()
