import os
import fitz
import pandas as pd
import tkinter as tk
from tkinter.filedialog import askdirectory
from pathlib import Path

class XLSX:

    def __init__(self):
        self.consultant_check = 0
        self.consultant_idx = 0

    def find_pdfs(self) -> list:
        _default = str(os.path.join(Path.home(), "Downloads"))

        tk.Tk().withdraw()
        folder = askdirectory(initialdir = _default, title='Select a folder with SPE files')

        pdf_files = []

        for root, dirs, files in os.walk(folder):
            root = str(root).replace('\\', '/')
            sep = str(root).split('/')
            if str(sep[-1]).startswith('International'):
                for file in files:
                    pdf_files.append(os.path.abspath(os.path.join(root, file)))

        print('Paths acquired...')

        return pdf_files
    
    def read_pdf_content(self, pdf_files: list) -> list:

        _list = []
        
        for pdf in pdf_files:
            document = fitz.open(pdf)
            content_list = []
            root = str(pdf).replace('\\', '/')
            sep = str(root).split('/')

            content_list.append(sep[-3]) # File name
            content_list.append(sep[-2]) # App Type
            content_list.append(sep[-1][:-4]) # Applicant name

            for page_num in range(len(document)):
                page = document.load_page(page_num)
                content = page.get_text()
                _lines = content.splitlines()
                for idx, line in enumerate(_lines):
                    if self.search_for_headers(line, idx):
                        if str(line).startswith('Date of Birth'):
                            content_list.append(line[15:25]) # DOB
                            content_list.append(line[33:]) # Gender
                        elif self.consultant_idx != 0 and self.consultant_check == 1:
                            content_list.append(_lines[self.consultant_idx+3]) # Consultant Answer
                            self.consultant_idx == 0
                        else: 
                            content_list.append(line) # Semester Entry
                self.consultant_check = 0

            _list.append(content_list)

        print('Lines appended to list...')

        return _list

    def search_for_headers(self, line: str, idx: int) -> bool:

        if str(line).startswith(('Fall', 'Spring', 'Date of Birth')) and idx <= 20:
            return True
        elif line == 'Consultant/Agency':
            self.consultant_check += 1
            self.consultant_idx = idx
            return True
        
        return False
    
    def generate_xlsx_sheet(self, _list: list) -> None:
            
        df = pd.DataFrame(_list)
        download_default = str(os.path.join(Path.home(), "Downloads"))
        filepath = f'{download_default}/total.xlsx'
        df.to_excel(filepath, index=False, header= ["File Name", "Type", "Name", "Semester", "DOB", "Gender", "Info"])

if __name__ == '__main__':
    x = XLSX()
    pdf_files = x.find_pdfs()
    _list = x.read_pdf_content(pdf_files)
    x.generate_xlsx_sheet(_list)