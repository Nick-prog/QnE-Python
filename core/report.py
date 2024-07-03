import os
import pandas as pd
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.colors import HexColor
from pdfrw import PdfReader
from pdfrw.buildxobj import pagexobj
from pdfrw.toreportlab import makerl
from reportlab.lib.units import inch
from pathlib import Path

class Report:

    def __init__(self, nested_list: list):
        """Report class handles all PDF generation methods and fits the translated list (nested_list)
        into line by line inputs. Student name and app types are also captured for later storing methods.

        :param nested_list: translated nested list of inputs such as: strings and lists
        :type nested_list: list
        """

        self.nested_list = nested_list
        self.student_name = []
        self.app_type = []

        self.start = 0
        self.end = 0

        self.y_start = 750
        self.x_start = 50
        self.page_size = (8.5*inch, 11*inch)
        self.font_type = "Courier"
        self.font_size = 7

        self.student_flag = 0

    def capture_student_name(self) -> None:
        """Method for capturing the student names from the given nested list. Locates the start of student information
        ['Student Contact:'] and captures the next several lines in the list until it reaches an indicator to stop 
        ['Nickname', 'Place of Birth', ...]
        """

        name = ''

        for idx, app in enumerate(self.nested_list):
            student_check = 0
            for item in app:
                if item == ['', 'Student Contact:']:
                    student_check = 1

                if student_check == 1 and str(item).startswith(tuple(['First', 'Middle', 'Last', 'Initial','Suffix'])):
                    colon_idx = item.find(':') # Find the position of the colon
                    input = item[colon_idx + 2:]  # Extract the part after the colon, +2 to skip the colon and the space after it
                    if str(item).startswith('Last'):
                        name += f'{input}, ' # Add a comma after the last name for each new item
                    else:
                        name += f'{input} '

                elif student_check == 1 and str(item).startswith(tuple(['Nickname', 'Place of Birth', 'Date of Birth'])):
                    # name += str(idx)
                    self.student_name.append(name)
                    name = ''
                    student_check = 0

    def capture_app_type(self) -> None:
        """Method for capturing the app types from the given nested list. Locates the start of app information
        ['App ID'] and captures the portion of the list after a certain indicator '|'
        """

        for idx, app in enumerate(self.nested_list):
            for item in app:
                if str(item).startswith('App ID'):
                    app_type = str(item).split('| ')
                    self.app_type.append(app_type[-1])

    def fit_student_data(self, app_data: list) -> list:
        """Method for fitting the nested lists data of list and strings into a coherent list of strings.
        Ex: list = ['input1', 'input2', ['input3', 'input4', ''], 'input5'] -> list = ['input1', 'input2','input3', 'input4', '', 'input5']

        :param app_data: selected nested list
        :type app_data: list
        :return: decoupled nested list
        :rtype: list
        """

        _list = []

        for idx, items in enumerate(app_data):
            if items != None:
                if type(items) == list:
                    for nested in items:
                        _list.append(nested)
                else:
                    _list.append(items)

        return _list

    def find_total_pages(self, _list: list) -> int:
        """Method to find the total number of pages needed to be used to display all of the student's app data. Divides by
        65 lines to determine when to cutoff each list of data.

        :param _list: selected list
        :type _list: list
        :return: number of pages
        :rtype: int
        """

        if len(_list)/65 > round(len(_list)/65):
            return round(len(_list)/65)+1
        
        return round(len(_list)/65)
    
    def create_page_structure(self, folder: str, file_name: str,  _list: list, idx: int) -> None:
        """Method that handles the creation of pdf pages and storage. Creates pdf objects based on the number of pages
        needed and feeds the current list of data through the generate_pdf_page method to write each input line by line.

        :param folder: current folder path
        :type folder: str
        :param file_name: name of selected spe file
        :type file_name: str
        :param _list: selected list of data
        :type _list: list
        :param idx: current nested list idx
        :type idx: int
        """

        current_dir = os.getcwd()
        pdf_pages = self.find_total_pages(_list)
        template = f"{current_dir}/templates/template_{pdf_pages}.pdf"

        full_path = os.path.abspath(f'{folder}/{file_name[:-4]}/{self.app_type[idx]}')

        if not os.path.exists(full_path):
            os.makedirs(full_path)

        student_file = os.path.abspath(os.path.join(full_path, f'{self.student_name[idx]}.pdf'))

        pdf = PdfReader(template, decompress=False)
        canvas = Canvas(student_file)

        for idx, page in enumerate(pdf.pages):
            pdf_obj = pagexobj(page)
            xpdf_name = makerl(canvas, pdf_obj)
            canvas.doForm(xpdf_name)
            self.generate_pdf_page(canvas, _list, idx)
            canvas.showPage()

        canvas.save()

    def generate_pdf_page(self, canvas: object, _list: list, page_num: int) -> None:
        """Nethod for handling all page writing in any given pdf generation. Write line by line and 
        slices the list of data based on the number of lines able to fit on the self.page_size parameters.

        :param canvas: PDF canvas object
        :type canvas: object
        :param _list: selected list of data
        :type _list: list
        :param page_num: current page number
        :type page_num: int
        """

        canvas.setFont(self.font_type, self.font_size)
        canvas.setPageSize(self.page_size)

        self.start = 65*page_num
        self.end = 65*(page_num+1)

        for idx, items in enumerate(_list):
            if self.start <= idx < self.end:
                if str(items).startswith('\t'):
                    canvas.setFont(self.font_type, 6)
                else:
                    canvas.setFont(self.font_type, self.font_size)

                canvas.drawString(self.x_start, self.y_start, items)
                self.y_start = self.y_start - 10

        self.y_start = 750

    def find_consultant_agency(self, app_data: list, filename: str) -> list:

        _list = []

        for idx, items in enumerate(app_data):
            if items == 'Spring 2025':
                _list.append(items)
            elif str(items) == 'Consultant/Agency':
                _list.append(app_data[idx+3])
            elif str(items).startswith('Student Contact'):
                self.student_flag = 1
            elif self.student_flag == 1 and str(items).startswith('Date of Birth'):
                self.student_flag = 0
                _list.append(items[15:25])
                _list.append(items[33:])
        _list.append(filename)

        return _list
    
    def generate_xlsx_sheet(self, _list: list, filename: str) -> None:
        _temp = []

        for idx, items in enumerate(_list):
            if len(items[0]) >= 5:
                _temp.append([items[0][0], items[0][1], items[0][2], items[0][3], items[0][4], items[1]])

        if len(_temp) != 0:
            df = pd.DataFrame(_temp)
            download_default = str(os.path.join(Path.home(), "Downloads"))
            filepath = f'{download_default}/{filename}.xlsx'
            df.to_excel(filepath, index=False, header= ["Semester", "DOB", "Gender", "Info", "Filename", "Name"])