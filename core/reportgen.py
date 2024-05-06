import core

import os
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.colors import HexColor
from pdfrw import PdfReader
from pdfrw.buildxobj import pagexobj
from pdfrw.toreportlab import makerl
from reportlab.lib.units import inch

from typing import Union

class ReportGen:

    def __init__(self, in_file: str, nested_list: list, file_count: int, key: str):
        """Class created to house methods for PDF creation. Generates each line of text and
        dynamically inputs them at desired locations.

        :param in_file: path to the template used for all PDFs
        :type in_file: str
        :param nested_list: list of all rows from the generated .csv file
        :type nested_list: list
        :param file_count: current index of student selected
        :type file_count: int
        :param key: application type (ex: Domestic or Foreign)
        :type key: str
        """

        self.in_file = in_file
        self.nested_list = nested_list
        self.file_count = file_count
        self.key = key

        self.ystart = 1250
        self.xstart = 50

        self.names = []

        self.page_1 = []
        self.page_2 = []
        self.page_3 = []

        self.page_1_idx = []
        self.page_2_idx = []
        self.page_3_idx = []

    def generate_new_points(self, xstart: int, ystart: int, yadd: int) -> Union[int, int, int]:
        return self.xstart+xstart, self.ystart+ystart, yadd

    def capture_student_names(self, select_app: int) -> None:
        """Captures student names for file descriptions based on the given
        student information.

        :param select_app: target application index
        :type select_app: int
        """

        name = []
        break_found = 0

        for col in range(len(self.nested_list[select_app])):
            _str = str(self.nested_list[select_app][col]).split("!")

            syntax = core.ReportStructure(_str)
            conv = syntax.page_structure()

            if conv in ['Start Student Contact Info', 'Start Extra Contact Info','Start Parent 1 Contact Info', 'Start Parent 2 Contact Info']:
                break_found += 1

            if break_found == 1 and conv in ["First Name", "Last Name", "Middle Name", "Middle Initial", "Suffix"]:
                current = "".join(_str[-1]).replace("\\", "")
                name.append(current)

            if break_found > 1:
                name.append(str(self.file_count))
                self.names = name
                name = []
                break

    def create_pages_structure(self, select_app: int) -> None:
        """Creates pages structure based on distinct separation markdown text.

        :param select_app: target application index
        :type select_app: int
        """

        page_count = 0
        pend_sep = 0

        page_list = [self.page_1, self.page_2, self.page_3]
        page_idx = [self.page_1_idx, self.page_2_idx, self.page_3_idx]

        for col in range(len(self.nested_list[select_app])):
            _str = str(self.nested_list[select_app][col]).split("!")
            
            syntax = core.ReportStructure(_str)
            conv = syntax.page_structure()

            if conv == "Submit/Transmit": # first page cutoff
                page_count += 1
            elif conv == "Conduct: Pending Action" and pend_sep == 0: # second page cutoff
                page_count += 1
                pend_sep = 1 # May appear more than once

            target_list = page_list[page_count]
            target_list.append(conv)

            target_idx = page_idx[page_count]
            target_idx.append(col)

    def create_canvas(self, out_folder: str, select_app: int) -> None:
        """Creates a canvas object to manipulate our PdfReader targetlate and add given information.

        :param out_folder: string location to designated folder
        :type out_folder: str
        :param select_app: target application index
        :type select_app: int
        """

        if not os.path.exists(out_folder):
            os.mkdir(out_folder)

        out_folder = os.path.join(out_folder, self.key)

        if not os.path.exists(out_folder):
            os.mkdir(out_folder)

        name = "_".join(self.names)
        out_file = os.path.join(out_folder, f"{name}.pdf")

        page_count = 0
        targetlate = PdfReader(self.in_file, decompress=False)
        canvas = Canvas(out_file)

        for page in targetlate.pages:
            page_count += 1
            # Extract the page and convert it into a PDF xobject
            targetlate_obj = pagexobj(page)
            
            # Place the targetlate onto the canvas
            xobj_name = makerl(canvas, targetlate_obj)
            canvas.doForm(xobj_name)

            if page_count == 1:
                last_idx = self.handle_first_page(canvas, select_app)
            elif page_count == 2:
                last_idx = self.handle_second_page(canvas, select_app, last_idx)
            elif page_count == 3:
                last_idx = self.handle_third_page(canvas, select_app, last_idx)

            # Add a new page
            canvas.showPage()

        # Save the modified canvas to the output PDF file
        canvas.save()

    def handle_first_page(self, canvas: object, select_app: int) -> int:
        """Handles all information to be displayed for the first page of the pdf.

        :param canvas: PDFReader object for pdf managment
        :type canvas: object
        :param select_app: target application index
        :type select_app: int
        :return: final index reached on student's list
        :rtype: int
        """

        # Starting points
        xstart = self.xstart
        ystart = self.ystart

        #Increment
        yadd = 0

        current_idx = -1 # Allows us to target the str itself
        found = 0
        extra_found = 0


        opt_list = ["Community or Volunteer Service", "Award/Acheivement", "Employment/Internships/Summer Activities"]
        
        opt_sep = {
            "Extra Curricular Activities": 0, 
            "Community or Volunteer Service": 0, 
            "Award/Acheivement": 0, 
            "Employment/Internships/Summer Activities": 0
            }

        canvas.setFont("Courier", 7)
        canvas.setPageSize((8.5*inch, 18*inch))
        
        for val in self.page_1:
            current_idx += 1

            if val == "App ID":
                xstart, ystart, yadd = self.generate_new_points(320, 0, 0)
            elif val == "Start Student Contact Info":
                xstart, ystart, yadd = self.generate_new_points(0, -100, 0)
            elif val == "Start Extra Contact Info":
                if extra_found == 0:
                    extra_found = 1
                    xstart, ystart, yadd = self.generate_new_points(320, -100, 0)
                else:
                    yadd -= 10
            elif val == "Start Parent 1 Contact Info" or val == "Start Parent 2 Contact Info" :
                yadd -= 10
            elif val == "Extra Curricular Activities" and opt_sep[val] == 0:
                canvas.setFont("Courier", 7)
                opt_sep[val] = 1
                xstart, ystart, yadd = self.generate_new_points(0, -400, 0)
                canvas.drawString(xstart, ystart+yadd, "Extra Curricular Activite(s):")
                yadd = -10
                canvas.setFont("Courier", 6)
            elif val in opt_list and opt_sep[val] == 0:
                canvas.setFont("Courier", 7)
                xstart = self.xstart
                ystart = ystart+yadd-10
                yadd = 0
                opt_sep[val] = 1

                for key, value in opt_sep.items():
                    if key != val and value == 1:
                        found += 1

                if found == 0:
                    ystart = self.ystart-400
                
                found = 0
                canvas.drawString(xstart, ystart+yadd, f"{val}:")
                yadd = -10
                canvas.setFont("Courier", 6)
            elif val == "Semester":
                canvas.setFont("Courier", 7)
                xstart, ystart, yadd = self.generate_new_points(0, -50, 0)

            _str = self.nested_list[select_app][current_idx]
            struct = core.ReportStructure(_str)
            conv = struct.transform_page(val)

            if conv != "None":
                canvas.drawString(xstart, ystart+yadd, str(conv)) # prints syntax values
                # canvas.drawString(xstart, ystart+yadd, val + _str)
                yadd -= 10

        return current_idx

    def handle_second_page(self, canvas: list, select_app: int, last_idx: int) -> int:
        """Handles all information to be displayed for the second page of the pdf.

        :param canvas: PDFReader object for pdf managment
        :type canvas: list
        :param select_app: target application index
        :type select_app: int
        :param last_idx: last reached index
        :type last_idx: int
        :return: final index reached on student's list
        :rtype: int
        """

        s = core.Syntax()

        # Starting points
        xstart = self.xstart
        ystart = self.ystart

        #Increment
        yadd = 0

        current_idx = last_idx

        canvas.setFont("Courier", 7)
        canvas.setPageSize((8.5*inch, 18*inch))
        # canvas.setFillColor(HexColor('#FFFFFF'))

        paragraph_start = ['Alumni ?', 'Citzenship ?', 'Text Messaging Option',
                           'SSN Verification Notice', 'Name Verification Notice',
                           'Conduct Question: Conviction', 'Conduct Question: Expulsion',
                           'Multi type question', 'Faculty Mentor ?',
                           'Consultant Agency ?', 'End of App']
        
        req_start = ['Request and/or Answer', 'Long REQ', 'Med REQ']

        req_dict = {
            'DUAL CREDIT': "",
            'IB DIPLOMA': "Student Information - continued:",
            'HS GED TYPE': "Student Information - continued:",
            'FERPA CERT SWITCH': "Certification of Information:",
            'PRE-PROFESSIONAL PGMC': "Educational Information:",
            'PRE-PROFESSIONAL PGMN': "Educational Information:",
            'PRE-PROFESSIONAL PGMZ': "Educational Information:",
            'PRE-PROFESSIONAL PGMD': "Educational Information:",
            'PERM COUNTY INFO': "Mailing/Permanent Address:",
            'PERM COUNTRY INFO': "Mailing/Permanent Address:",
            'CURR COUNTY INFO': "Physical Address:",
            'CURR COUNTRY INFO': "Physical Address:",
            'CUR COLLEGE ATT': 'Educational Information (Colleges Attended):',
            'CONSERVATORSHIP SWITCHES': "",
            'FORMER STUDENT': "",
            'COUNSELOR OPT IN': "Counselor Question:"
        }
        
        _list = []

        for val in self.page_2:
            current_idx += 1
            _str = self.nested_list[select_app][current_idx]
            struct = core.ReportStructure(_str)

            if val in paragraph_start:
                yadd -= 10
            elif val in req_start:
                target = str(_str).split("!")

                req_syntax = {
                        'HS GED TYPE': s.hs_ged_syntax(target),
                        'DUAL CREDIT': s.dual_syntax(target),
                        'CONSERVATORSHIP SWITCHES': s.conservator_syntax(target),
                        'FORMER STUDENT': s.former_syntax(target),
                        'INTL EXIT US': s.exit_us_syntax(target)
                        }

                for key, value in req_dict.items():
                    if target[3] == key:
                        if value != "":
                            yadd -= 10
                            canvas.drawString(xstart, ystart+yadd, value)
                            yadd -= 10
                        else:
                            canvas.drawString(xstart, ystart+yadd, value)

                for key, value in req_syntax.items():
                    if target[3] == key:
                        _list = value
                        yadd -= 10

                if _list != None:
                    for x in range(len(_list)):
                        canvas.drawString(xstart, ystart+yadd, str(_list[x]))
                        yadd -= 10

                _list = []

            conv = struct.transform_page(val)
     
            if conv != "None":
                canvas.drawString(xstart, ystart+yadd, str(conv)) # prints syntax values
                # canvas.drawString(xstart, ystart+yadd, val + _str)
                yadd -= 10

        return current_idx

    def handle_third_page(self, canvas: object, select_app: int, last_idx: int) -> None:
        """Handles all information to be displayed for the second page of the pdf.

        :param canvas: PDFReader object for pdf managment
        :type canvas: list
        :param select_app: target application index
        :type select_app: int
        :param last_idx: last reached index
        :type last_idx: int
        """

        s = core.Syntax()

        # Starting points
        xstart = self.xstart
        ystart = self.ystart+720 # Increase by 80 every 1 inch height

        #Increment
        yadd = 0

        current_idx = last_idx

        canvas.setFont("Courier", 7)
        canvas.setPageSize((8.5*inch, 28*inch))
        # canvas.setFillColor(HexColor('#FFFFFF'))

        paragraph_start = ['Faculty Mentor ?', 'Consultant/Agency', 'Text Messaging Option',
                           'Name Verification Notice', 'Conduct Question: Conviction',
                           'Graduation Date', 'Consultant Agency ?', 'Alumni ?', 'Citzenship ?', "Post-Secondary Colleges/Universities",
                           'Conduct Question: Expulsion', 'Conduct: Pending Action', 'Multi type question',
                           'End of App']
        
        req_start = ['Request and/or Answer', 'Long REQ', 'Short REQ', 'Med REQ', "Post-Secondary Colleges/Universities"]

        _list = []

        for val in self.page_3:
            current_idx += 1
            _str = self.nested_list[select_app][current_idx]
            struct = core.ReportStructure(_str)

            if val in paragraph_start:
                yadd -= 10
            elif val in req_start:
                target = str(_str).split("!")

                req_syntax = {
                        'PAYMENT RECONCILIATION': s.payment_syntax(target),
                        'RES: PREVIOUS ENROLLMENT': s.prev_syntax(target),
                        'RES: BASIS OF CLAIM': s.basis_syntax(target),
                        'RES: HS DIPLOMA OR GED': s.hs_diploma_syntax(target),
                        'RES: SELF': s.residency_self_syntax(target),
                        'RES: GUAR': s.residency_guar_syntax(target),
                        'CTRY SELF': s.country_syntax(target),
                        'FAMILY OBLIGATION INCOME': s.family_obj_income_syntax(target),
                        'VET STATUS': s.vet_syntax(target),
                        'HOME SCHOOLED': s.home_syntax(target),
                        'RES: COMMENTS\\': s.comment_syntax(),
                        'RES: BASIS OF CLAIM\\': s.basis_syntax(target),
                        'CURRENT ACADEMIC SUSP': s.suspension_syntax(target),
                        'COLLEGE WORK': s.college_work_syntax(target),
                        'RES: RESIDENCY CLAIM': s.residency_claim_syntax(target),
                        'RES: DETERM': s.residency_determ_syntax(target),
                        'FAMILY OBLIGATIONS': s.family_obj_syntax(target),
                        'APPLICATION SHARING': s.app_share_syntax(target),
                        'PHI THETA KAPPA': s.phi_theta_kappa_syntax(target),
                        'INT CURR RESIDE IN US': s.currently_reside_syntax(target),
                        'FAMILY OBLIGATION OTHER': s.family_obj_other_syntax(target)
                        }

                for key, value in req_syntax.items():
                    if target[3] == key:
                        _list = value
                        yadd -= 10

                if _list != None:
                    for x in range(len(_list)):
                        canvas.drawString(xstart, ystart+yadd, str(_list[x]))
                        yadd -= 10

                _list = []

            conv = struct.transform_page(val)

            if conv != "None":
                canvas.drawString(xstart, ystart+yadd, str(conv)) # prints syntax values
                # canvas.drawString(xstart, ystart+yadd, val + _str)
                yadd -= 10