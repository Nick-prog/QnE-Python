import core

import os
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.colors import HexColor
from pdfrw import PdfReader
from pdfrw.buildxobj import pagexobj
from pdfrw.toreportlab import makerl
from reportlab.lib.units import inch

class Report:

    def __init__(self, nested_list: list):

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

    def capture_student_name(self) -> None:

        name = ''

        for idx, app in enumerate(self.nested_list):
            student_check = 0
            for item in app:
                if item == ['', 'Student Contact:']:
                    student_check = 1

                if student_check == 1 and str(item).startswith(tuple(['First', 'Middle', 'Last', 'Initial','Suffix'])):
                    colon_idx = item.find(':') # Find the position of the colon
                    input = item[colon_idx + 2:]  # Extract the part after the colon, +2 to skip the colon and the space after it
                    name += f'{input}_' # Add an underscore before each new item

                elif student_check == 1 and str(item).startswith(tuple(['Nickname', 'Place of Birth', 'Date of Birth'])):
                    name += str(idx)
                    self.student_name.append(name)
                    name = ''
                    student_check = 0

    def capture_app_type(self) -> None:

        for idx, app in enumerate(self.nested_list):
            for item in app:
                if str(item).startswith('App ID'):
                    app_type = str(item).split('| ')
                    self.app_type.append(app_type[-1])

    def fit_student_data(self, app_data: list) -> list:

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

        if len(_list)/65 > round(len(_list)/65):
            return round(len(_list)/65)+1
        
        return round(len(_list)/65)
    
    def create_page_structure(self, folder: str, file_name: str,  _list: list, idx: int) -> None:

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

        canvas.setFont(self.font_type, self.font_size)
        canvas.setPageSize(self.page_size)

        self.start = 65*page_num
        self.end = 65*(page_num+1)

        for idx, items in enumerate(_list):
            if self.start <= idx < self.end:
                canvas.drawString(self.x_start, self.y_start, items)
                self.y_start = self.y_start - 10

        self.y_start = 750