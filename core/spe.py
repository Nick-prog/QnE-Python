import os
import ctypes
import sys
from datetime import date
from fpdf import FPDF

class SPE(object):
    '''
    Class in charge of handling all processes invovled with .spe files. Opens selected file and separates each individual found into TXT files
    for data markdown text manipulation to finally be converted to PDFs.
    '''

    def __init__(self, file_path, file_out, file_name):
        self.file_path = file_path # abs file path for selected file
        self.file_out = file_out # auto download path folder
        self.file_name = file_name # name of file selected
        self.file_start = 0 # total number of individuals found

    def read_file(self):
        '''
        Reads .spe file selected and opens it in a single TXT file.
        No Returns.
        '''
        try:
            with open(self.file_path, 'r') as file:
                content = file.read()

            file = f'{self.file_name}_{self.file_start}.txt'
            txt_file = os.path.join(self.file_out, file)
            
            with open(txt_file, 'w') as out:
                out.write(content)

        except FileNotFoundError:
            ctypes.windll.user32.MessageBoxW(0, "FileNotFoundError encountered.", (sys.exc_info()[1]), "Warning!", 16)
        except Exception as e:
            ctypes.windll.user32.MessageBoxW(0, "Exception encountered.", (sys.exc_info()[1]), "Warning!", 16)

    def process_file(self):
        '''
        Reads .spe file selected and processes each line through process_line method. If output is True, create a new PDF file else
        continue writing to currently opened PDF file based on file_name and file_start count.
        Stores PDFs in folder created at same location with create_folder method. 
        No Returns.
        '''
        try:
            today = date.today()
            today_formatted = today.strftime("%m.%d.%y")
            self.create_folder(f"{today_formatted}/")

            with open(self.file_path, 'r') as file:
                for line in file:
                    line = line.strip()

                    output = self.process_line(line)

                    file = f'{self.file_name}_{self.file_start}.txt'

                    out = open(self.file_out + file, 'a')
                    if output == True:
                        out.close()
                        self.create_pdf(file)
                        self.file_start = self.file_start + 1
                    else:
                        out.write(line + '\n')

        except FileNotFoundError:
            ctypes.windll.user32.MessageBoxW(0, "FileNotFoundError encountered.", (sys.exc_info()[1]), "Warning!", 16)
        except Exception as e:
            ctypes.windll.user32.MessageBoxW(0, "Exception encountered.", (sys.exc_info()[1]), "Warning!", 16)

    def process_line(self, line):
        '''
        Line processing method for all files.
        Returns bool.
        '''
        return line.startswith('BGN!')
    
    def create_folder(self, folder):
        '''
        Folder creation method for all files.
        No Returns.
        '''
        folder = os.path.join(self.file_out, folder)
        os.mkdir(folder)
    
    def create_pdf(self, file):
        '''
        PDF creation method for all files once criteria is meet, line starts with BGN!.
        Names file based on file passed in process_file method.
        No Returns.
        '''
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", "B",7)

        txt_path = os.path.join(self.file_out, file)

        pdf_out = open(txt_path, 'r')

        for txt in pdf_out:
            pdf.cell(200, 10, txt=txt, ln=1, align='L')

        today = date.today()
        today_formatted = today.strftime("%m.%d.%y")
        pdf_path = os.path.join(self.file_out, f"{today_formatted}/{file[:-4]}.pdf")

        pdf.output(pdf_path)

    def remove_txt_files(self):
        '''
        Removes all TXT files found at download location.
        No Returns.
        '''
        directory = os.listdir(self.file_out)

        for item in directory:
            if item.endswith('.txt'):
                os.remove(f"{self.file_out}/{item}")