import core
import os
import ctypes
import sys
import pymsgbox
import tkinter as tk
from tkinter.filedialog import askopenfilename
from pathlib import Path

def run(file, download, fileName):
    obj = core.SPE(file, download, fileName)
    # obj.read_file()
    obj.process_file()
    obj.remove_txt_files()
    return obj.file_start

if __name__ == "__main__":

    try:
        tk.Tk().withdraw()
        file = askopenfilename()
        fileBase, fileName = os.path.split(file)
        filepath = os.path.join(fileBase, fileName)
        downloadpath = str(os.path.join(Path.home(), "Downloads"))
        total = run(os.path.abspath(filepath), os.path.abspath(downloadpath), fileName[:-4])

        pymsgbox.alert(f"{total} file(s) created from file original .spe file ({fileName[:-4]}) stored at {fileBase}", "Complete!")

    except ValueError:
        ctypes.windll.user32.MessageBoxW(0, "ValueError encountered.", (sys.exc_info()[1]), "Warning!", 16)