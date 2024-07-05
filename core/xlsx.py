import os
import tkinter as tk
from tkinter.filedialog import askdirectory
from pathlib import Path
from pdfrw import PdfReader

class XLSX:

    def __init__(self):
        self.temp = 1

    def find_pdfs_in_downloads(self):
        _default = str(os.path.join(Path.home(), "Downloads"))

        tk.Tk().withdraw()
        folder = askdirectory(initialdir = _default, title='Select a folder with SPE files')

        pdf_files = []

        for root, dirs, files in os.walk(folder):
            sep = str(root).split('\\')
            if str(sep[-1]).startswith('International'):
                for file in files:
                    pdf_files.append(os.path.abspath(os.path.join(root, file)))

        return pdf_files
    
    def read_pdf_content(self, pdf_files):

        content_list = []
        
        for pdf in pdf_files:
            with open(pdf, 'rb') as file:
                for line in file:
                    print(line)



if __name__ == '__main__':
    x = XLSX()
    pdf_files = x.find_pdfs_in_downloads()
    x.read_pdf_content(pdf_files)