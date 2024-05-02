import core

import ctypes
import sys
import pymsgbox
import os
import tkinter as tk
from tkinter.filedialog import askopenfilename
from tkinter.filedialog import askdirectory
from typing import Union

def find_spe_file() -> Union[str, str]:
    """Finder method for target .spe file.

    :raises TypeError: Checks for .spe file
    :return: both file path and file name
    :rtype: Union[str, str]
    """

    try:
        tk.Tk().withdraw()
        file = askopenfilename()
        fileBase, fileName = os.path.split(file)

        if not fileName.endswith('.spe'):
            raise TypeError(f"Can't process {fileName[-3:]} files.")
        
    except BaseException as b:
        ctypes.windll.user32.MessageBoxW(0, f"find_spe_file() error encountered. {b}", (sys.exc_info()[1]), "Warning!", 16)

    
    return file, fileName

def find_spe_folder_files() -> Union[list, list]:

    filePath_list = []
    fileName_list = []

    try:
        tk.Tk().withdraw()
        folder = askdirectory()
        
        for file in os.listdir(folder):
            if file.endswith(".spe"):
                filePath = os.path.join(folder, file)
                filePath_list.append(os.path.abspath(filePath))
                fileName_list.append(file)

    except BaseException as b:
        ctypes.windll.user32.MessageBoxW(0, f"find_spe_folder_files() error encountered. {b}", (sys.exc_info()[1]), "Warning!", 16)

    return filePath_list, fileName_list

def run_target(file: str, fileName: str, key: int, apps: int) -> None:
    """Second run method for all types of .spe files. Targets a specific
    type of application and student.

    :param key: type of application
    :type key: int
    :param apps: student index
    :type apps: int
    """

    try:
        print('\n' + file)
        current_dir = os.getcwd()
        csv_folder= os.path.abspath(f'{current_dir}/core/csv')

        if not os.path.exists(csv_folder):
                os.makedirs(csv_folder)

        csv_file = os.path.abspath(f'{csv_folder}/all.csv')
        in_file = f"{current_dir}/core/templates/template_empty.pdf"

        c = core.CSVGen(file, csv_file)
        c.spe_to_csv()

        p = core.Process(csv_file)
        p.read_csv_file()
        foreign, domestic = p.create_data_list(p.data)

        app_types = {
            "foreign": foreign, 
            "domestic": domestic
            }
        
        output_folder = os.path.abspath(f"{current_dir}/core/output")

        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        out_folder = os.path.abspath(f"{output_folder}/{fileName[:-4]}")

        report = core.ReportGen(in_file, app_types[key], apps, key)
        report.capture_student_names(apps)
        print(report.names)
        report.create_pages_structure(apps)
        report.create_canvas(out_folder, apps)
    
    except BaseException as b:
        print(report.names)
        ctypes.windll.user32.MessageBoxW(0, f"run_target() error encountered. {b}", (sys.exc_info()[1]), "Warning!", 16)

def run(file: str, fileName: str) -> None:
    """Main run method for all types of .spe files.

    :param file: target file location
    :type file: str
    :param fileName: name of the .spe file
    :type fileName: str
    """

    try:
        print('\n' + file)
        current_dir = os.getcwd()
        csv_folder= os.path.abspath(f'{current_dir}/core/csv')

        if not os.path.exists(csv_folder):
            os.makedirs(csv_folder)

        csv_file = os.path.abspath(f'{csv_folder}/all.csv')
        in_file = f"{current_dir}/core/templates/template_empty.pdf"

        c = core.CSVGen(file, csv_file)
        c.spe_to_csv()

        p = core.Process(csv_file)
        p.read_csv_file()
        foreign, domestic = p.create_data_list(p.data)

        app_types = {
            "foreign": foreign, 
            "domestic": domestic
            }

        for key in app_types:
            print(key, len(app_types[key]))
            for apps in range(len(app_types[key])):

                output_folder = os.path.abspath(f"{current_dir}/core/output")

                if not os.path.exists(output_folder):
                    os.makedirs(output_folder)

                out_folder = os.path.abspath(f"{output_folder}/{fileName[:-4]}")

                report = core.ReportGen(in_file, app_types[key], apps, key)
                report.capture_student_names(apps)
                print(report.names)
                report.create_pages_structure(apps)
                report.create_canvas(out_folder, apps)

    except BaseException as b:
        print(report.names)
        ctypes.windll.user32.MessageBoxW(0, "run() error encountered.", (sys.exc_info()[1]), "Warning!", 16)


if __name__ == "__main__":
    file, fileName = find_spe_file()
    run(file, fileName)

    # file, fileName = find_spe_file()
    # run_target(file, fileName, 'domestic', 12)

    # filePath_list, fileName_list = find_spe_folder_files()
    # for idx in range(len(filePath_list)):
    #     run(filePath_list[idx], fileName_list[idx])