import datetime
import shutil
import os

import keyboard
from colorama import Fore


def main():
    print(f'{Fore.CYAN}{currentDirectory=}')

    download_directory = os.path.join(currentDirectory, "Dowload")
    print(f'{Fore.CYAN}{download_directory=}')
    if not os.path.exists(download_directory):
        print(f'{Fore.RED}Folder {download_directory} not found')
        exit(0)

    template_directory = os.path.join(currentDirectory, "Template")
    print(f'{Fore.CYAN}{template_directory=}')
    if not os.path.exists(template_directory):
        print(f'{Fore.RED}Folder {template_directory} not found')
        exit(0)

    project_directory = os.path.join(currentDirectory, "WinCHM_Project")
    print(f'{Fore.CYAN}{project_directory=}')
    if not os.path.exists(project_directory):
        os.makedirs(project_directory)

    # 1 Переносим шаблон проекта
    shutil.copytree(template_directory, project_directory, symlinks=False, ignore=None,ignore_dangling_symlinks=False, dirs_exist_ok=True)

    # 2 Переносим статьи
    shutil.copytree(download_directory, project_directory, symlinks=False, ignore=None, ignore_dangling_symlinks=False, dirs_exist_ok=True)

    # 3 Формирование файла проекта
    ind=2
    prj_file = os.path.join(project_directory,"help.wcp")
    with open(prj_file, 'a', encoding='utf-16') as f:
        f.write(f"\n")
        for file in os.listdir(download_directory):
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

    # 4 Исправление количества секций ([TOPICS]) для полного отображения (временный файл для замены help.wcp)
    prj_file_temp = os.path.join(project_directory, "help.tmp")
    with open(prj_file, 'r', encoding='utf-16') as f1, open(prj_file_temp, 'w', encoding='utf-16') as f2:
        lines = f1.readlines()
        for line in lines:
            if 'TitleList=' in line:
                f2.write(f'TitleList={ind+1}\n')
            else:
                f2.write(f'{line}\n')

    # 5 Установка даты формирования файла справки (..\WinCHM_Project\template2\fixedtop.htm)
    top_file = os.path.join(project_directory, "template2/fixedtop.htm")
    cur_year = datetime.datetime.now().strftime('%m.%Y')
    with open(top_file, 'r') as file:
        filedata = file.read()
    filedata = filedata.replace('{{%Copyright%}}', f'{cur_year}')
    with open(top_file, 'w') as file:
        file.write(filedata)

    os.remove(prj_file)  # удаляем основной файл
    shutil.copy(prj_file_temp, prj_file) # переименовываем временный в основной
    os.remove(prj_file_temp)  # удаляем основной файл

    print(f'{Fore.CYAN}Process completed, press Space...')
    keyboard.wait("space")

if __name__ == "__main__":
    print(f"{Fore.CYAN}Last update: Cherepanov Maxim masygreen@gmail.com (c), 06.2022")
    print(f"{Fore.CYAN}Create WinCHM project from Download/Article*.html")
    currentDirectory = os.getcwd()
    main()
