import core

import os
import sys
import tkinter as tk
from tkinter.filedialog import askopenfilename
from tkinter.filedialog import askdirectory
from typing import Union
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

def find_spe_files() -> Union[list, list]:

    try:
        spe_default = find_initial_dir()

        tk.Tk().withdraw()
        dir = askdirectory(initialdir = spe_default, title='Select a folder with SPE files')

        file_paths = []
        file_names = []

        for file in os.listdir(dir):
            fileBase, fileName = os.path.split(file)

            if not fileName.endswith('.spe'):
                raise TypeError(f"Can't process {fileName[-3:]} files.")
            
            file_paths.append(os.path.abspath(os.path.join(dir, file)))
            file_names.append(fileName)
            
        return [file_paths, file_names]

    except BaseException as b:
        tk.messagebox.showerror("find_spe_files() error", f"{sys.exc_info()[1]}")

def find_spe_file() -> Union[str, str]:
    """Finder method for target .spe file.

    :raises TypeError: Checks for .spe file
    :return: both file path and file name
    :rtype: Union[str, str]
    """

    try:
        spe_default = find_initial_dir()

        tk.Tk().withdraw()
        file = askopenfilename(initialdir = spe_default, title='Select an SPE file')
        file_base, file_name = os.path.split(file)

        if not file_name.endswith('.spe'):
            raise TypeError(f"Can't process {file_name[-3:]} files.")
        
    except BaseException as b:
        tk.messagebox.showerror("find_spe_file() error", f"{sys.exc_info()[1]}")

    
    return [file, file_name]

def run(file_path: str, file_name: str) -> None:
    """Main run method for all types of .spe files.

    :param file: target file location
    :type file: str
    :param fileName: name of the .spe file
    :type fileName: str
    """

    try:
        download_default = str(os.path.join(Path.home(), "Downloads"))
        tk.Tk().withdraw()
        folder = askdirectory(initialdir=download_default, title='Select Download Path')

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

        for idx, item in enumerate(translated_spe):
            _list = r.fit_student_data(item)
            r.create_page_structure(folder, file_name, _list, idx)

    except BaseException as b:
        tk.messagebox.showerror("run() error", f"{sys.exc_info()[1]}")

if __name__ == "__main__":

    # files = find_spe_files()
    # for idx, file in enumerate(files):
    #     print(file[1])
    #     run(file[0], file[1])

    file = find_spe_file()
    print(file[1])
    run(file[0], file[1])

    print('Done')