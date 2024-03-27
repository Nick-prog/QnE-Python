import core

import ctypes
import sys
import pymsgbox
import os
import tkinter as tk
from pprint import pprint
from tkinter.filedialog import askopenfilename
from pathlib import Path

def run_target(key, apps):

    current_dir = os.getcwd()
    csv_file = os.path.abspath(f'{current_dir}/core/csv/all.csv')
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
    report.create_pages_structure(apps)
    report.create_canvas(out_folder, apps)

def find_spe_file():

    try:
        tk.Tk().withdraw()
        file = askopenfilename()
        fileBase, fileName = os.path.split(file)

        if not fileName.endswith('.spe'):
            raise TypeError(f"Can't process {fileName[-3:]} files.")
        
    except BaseException as b:
        ctypes.windll.user32.MessageBoxW(0, f"Error encountered. {b}", (sys.exc_info()[1]), "Warning!", 16)

    
    return file, fileName

def run(file, fileName):

    try:
        current_dir = os.getcwd()
        csv_file = os.path.abspath(f'{current_dir}/core/csv/all.csv')
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
                report.create_pages_structure(apps)
                report.create_canvas(out_folder, apps)

    except BaseException as b:
        ctypes.windll.user32.MessageBoxW(0, f"Error encountered. {b}", (sys.exc_info()[1]), "Warning!", 16)


if __name__ == "__main__":
    file, fileName = find_spe_file()
    # run(file, fileName)
    run_target("domestic", 144)