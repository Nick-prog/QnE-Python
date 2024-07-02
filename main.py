import core

import os
import sys
import tkinter as tk
import glob
import pandas as pd
from tkinter.filedialog import askopenfilename
from tkinter.filedialog import askdirectory
from pathlib import Path

def find_initial_dir() -> str:

    dl = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    drives = ['%s:' % d for d in dl if os.path.exists('%s:' % d)]

    for idx in range(len(drives)):
        path = os.path.join(drives[idx], '/Applications')
        if os.path.exists(os.path.abspath(path)):
            return path
        else:
            return str(os.path.join(Path.home(), "Downloads"))

def find_spe_files() -> None:

    try:
        spe_default = find_initial_dir()

        tk.Tk().withdraw()
        dir = askdirectory(initialdir = spe_default, title='Select a folder with SPE files')

        for file in os.listdir(dir):
            fileBase, fileName = os.path.split(file)

            if not fileName.endswith('.spe'):
                raise TypeError(f"Can't process {fileName[-3:]} files.")

            print(os.path.join(dir, file), fileName)
            run(os.path.join(dir, file), fileName)

    except BaseException as b:
        tk.messagebox.showerror("find_spe_files() error", f"{sys.exc_info()[1]}")

def find_spe_file() -> None:
    """Finder function for target .spe file.

    :raises TypeError: Checks for .spe file
    """

    try:
        spe_default = find_initial_dir()

        tk.Tk().withdraw()
        file = askopenfilename(initialdir = spe_default, title='Select an SPE file')
        file_base, file_name = os.path.split(file)

        if not file_name.endswith('.spe'):
            raise TypeError(f"Can't process {file_name[-3:]} files.")
        
        print(file, file_name)
        run(file, file_name)
        
    except BaseException as b:
        tk.messagebox.showerror("find_spe_file() error", f"{sys.exc_info()[1]}")

def run(file_path: str, filename: str) -> None:
    """Main run function for all types of .spe files.

    :param file: target file location
    :type file: str
    :param fileName: name of the .spe file
    :type fileName: str
    """

    try:
        folder = str(os.path.join(Path.home(), "Downloads"))
        p = core.Process(file_path)
        spe_list = p.read_spe_file()

        translated_spe = []
        markdown_spe = []

        for idx, item in enumerate(spe_list):
            s = core.Structure(item, idx)
            translated_spe.append(s.translate())
            markdown_spe.append(s.markdown)
    
        r = core.Report(translated_spe)
        r.capture_student_name()
        r.capture_app_type()

        create_xlsx(translated_spe, filename)

        for idx, item in enumerate(translated_spe):
            _list = r.fit_student_data(item)
            r.create_page_structure(folder, filename, _list, idx)

    except BaseException as b:
        tk.messagebox.showerror("run() error", f"{sys.exc_info()[1]}")

def create_xlsx(translated_spe: list, filename: str)-> None:

    _xlsx = []

    r = core.Report(translated_spe)
    r.capture_student_name()
    r.capture_app_type()

    for idx, item in enumerate(translated_spe):
        _list = r.fit_student_data(item)
        _xlsx.append(r.find_consultant_agency(_list, filename))

    for idx, item in enumerate(r.student_name):
            _xlsx[idx] = (_xlsx[idx], item)

    r.generate_xlsx_sheet(_xlsx, filename[:-4])

def merge_xlsx()-> None:
    # specifying the path to csv files
    input_folder = str(os.path.join(Path.home(), "Downloads"))
    output_file = str(os.path.join(input_folder, 'total.xlsx'))
    
    # Create a list to hold the dataframes
    dfs = []

    # Iterate over all Excel files in the specified folder
    for file_name in os.listdir(input_folder):
        if file_name.endswith('.xlsx') or file_name.endswith('.xls'):
            file_path = os.path.join(input_folder, file_name)
            # Read all sheets from the Excel file
            xls = pd.ExcelFile(file_path, engine='openpyxl')
            for sheet_name in xls.sheet_names:
                df = pd.read_excel(file_path, sheet_name=sheet_name)
                dfs.append(df)

    # Concatenate all dataframes into one
    merged_df = pd.concat(dfs, ignore_index=True)

    # Drop duplicate rows
    merged_df = merged_df.drop_duplicates()

    # Save the merged dataframe to a new Excel file
    merged_df.to_excel(output_file, index=False, engine='openpyxl')

if __name__ == "__main__":

    # find_spe_files() # Multiple .spe files
    # find_spe_file() # Singluar .spe file
    # print('Done')
    merge_xlsx()
    print('Done Done')