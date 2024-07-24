import core

import os
import sys
import tkinter as tk
import pandas as pd
from tkinter.filedialog import askopenfilename
from tkinter.filedialog import askdirectory
from pathlib import Path

def find_spe_files() -> None:

    try:
        spe_default = str(os.path.join(Path.home(), "Downloads"))

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
        spe_default = str(os.path.join(Path.home(), "Downloads"))

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

        new_list = p.rearrange_markdown_list(spe_list)

        from pprint import pprint
        pprint(new_list)

        for idx, item in enumerate(new_list):
            s = core.Structure(item, idx)
            translated_spe.append(s.translate())
            markdown_spe.append(s.markdown)
    
        r = core.PDF(translated_spe)
        r.capture_student_name()
        r.capture_app_type()

        for idx, item in enumerate(translated_spe):
            _list = r.fit_student_data(item)
            r.create_page_structure(folder, filename, _list, idx)

    except BaseException as b:
        tk.messagebox.showerror("run() error", f"{sys.exc_info()[1]}")

if __name__ == "__main__":

    # find_spe_files() # Multiple .spe files
    find_spe_file() # Singluar .spe file
    print('Done')