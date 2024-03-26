import core

import os
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.colors import HexColor
from pdfrw import PdfReader
from pdfrw.buildxobj import pagexobj
from pdfrw.toreportlab import makerl
from reportlab.lib.units import mm, inch

class ReportGen(object):

    def __init__(self, in_file, nested_list, file_count, key):
        self.in_file = in_file
        self.nested_list = nested_list
        self.file_count = file_count
        self.key = key

        self.names = []

        self.page_1 = []
        self.page_2 = []
        self.page_3 = []

        self.page_1_idx = []
        self.page_2_idx = []
        self.page_3_idx = []

    def capture_student_names(self, select_app):

        name = []

        for col in range(len(self.nested_list[select_app])):
            _str = str(self.nested_list[select_app][col]).split("!")

            syntax = core.ReportSyntax(_str)
            conv = syntax.page_structure()


            if conv == "First Name" or conv == "Last Name" or conv == "Middle Name" or conv == "Middle Initial":
                current = "".join(_str[-1]).replace("\\", "")
                name.append(current)

            if conv == "Place of Birth":
                name.append(str(self.file_count))
                self.names = name
                name = []


    def create_pages_structure(self, select_app):

        page_count = 0
        pend_sep = 0
        extra_sep = 0

        page_list = [self.page_1, self.page_2, self.page_3]
        page_idx = [self.page_1_idx, self.page_2_idx, self.page_3_idx]

        for col in range(len(self.nested_list[select_app])):
            _str = str(self.nested_list[select_app][col]).split("!")
            
            syntax = core.ReportSyntax(_str)
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

    def create_canvas(self, out_folder, select_app):
        '''
        Create a canvas object to manipulate our PdfReader template and add given information.
        Returns None.
        '''

        if not os.path.exists(out_folder):
            os.mkdir(out_folder)

        out_folder = os.path.join(out_folder, self.key)

        if not os.path.exists(out_folder):
            os.mkdir(out_folder)

        name = "_".join(self.names)
        out_file = os.path.join(out_folder, f"{name}.pdf")
        # out_file = os.path.join(out_folder, f"result_{self.file_count}.pdf")

        page_count = 0
        template = PdfReader(self.in_file, decompress=False)
        canvas = Canvas(out_file)

        for page in template.pages:
            page_count += 1
            # Extract the page and convert it into a PDF xobject
            template_obj = pagexobj(page)
            
            # Place the template onto the canvas
            xobj_name = makerl(canvas, template_obj)
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

    def handle_first_page(self, canvas, select_app):
        '''
        Handles all information for the first page of the pdf.
        Returns None.
        '''

        # Starting points
        xstart = 50
        ystart = 960

        #Increment
        yadd = 0

        current_idx = -1 # Allows us to target the str itself
        extra_sep = 0 # temp val to capture a one time move for extra curriculars
        award_sep = 0 # temp val to capture a one time move for awards
        vol_sep = 0 # temp val to capture a one time move for vol
        other_sep = 0 # "temp val to campture a one time move for Employment/Internships/Summer Activities"

        canvas.setFont("Helvetica", 7)
        canvas.setPageSize((8.5*inch, 14*inch))
        # canvas.setFillColor(HexColor('#FFFFFF'))
        
        for val in self.page_1:
            current_idx += 1

            if val == "App ID":
                xstart = 400
                ystart = 960
                yadd = 0
            elif val == "Start Student Contact Info":
                xstart = 50
                ystart = 880
                yadd = 0
            elif val == "Start Extra Contact Info":
                xstart = 400
                ystart = 880
                yadd = 0
            elif val == "Start Parent 1 Contact Info" or val == "Start Parent 2 Contact Info" :
                yadd -= 10
            elif val == "Extra Curricular Activities" and extra_sep == 0:
                canvas.setFont("Helvetica", 7)
                extra_sep = 1
                xstart = 50
                ystart = 720
                yadd = 0
                canvas.drawString(xstart, ystart+yadd, "Extra Curricular Activite(s):")
                yadd = -10
                canvas.setFont("Helvetica", 6 )
            elif val == "Community or Volunteer Service" and vol_sep == 0:
                canvas.setFont("Helvetica", 7)
                vol_sep = 1
                xstart = 50
                if extra_sep == 0:
                    ystart = 720
                else:
                    ystart = ystart+yadd-10
                yadd = 0
                canvas.drawString(xstart, ystart+yadd, "Community/Volunteer Service(s):")
                yadd = -10
                canvas.setFont("Helvetica", 6)
            elif val == "Award/Acheivement" and award_sep == 0:
                canvas.setFont("Helvetica", 7)
                award_sep = 1
                xstart = 50
                if extra_sep == 0 and vol_sep == 0:
                    ystart = 720
                else:
                    ystart = ystart+yadd-10
                yadd = 0
                canvas.drawString(xstart, ystart+yadd, "Award(s)/Achievement(s):")
                yadd = -10
                canvas.setFont("Helvetica", 6)
            elif val == "Employment/Internships/Summer Activities" and other_sep == 0:
                canvas.setFont("Helvetica", 7)
                other_sep = 1
                xstart = 50
                if extra_sep == 0 and vol_sep == 0 and award_sep == 0:
                    ystart = 720
                else:
                    ystart = ystart+yadd-10
                yadd = 0
                canvas.drawString(xstart, ystart+yadd, "Employment/Internships/Summer Activities:")
                yadd = -10
                canvas.setFont("Helvetica", 6)
            elif val == "Semester":
                canvas.setFont("Helvetica", 7)
                xstart = 50
                ystart = 930
                yadd = 0

            _str = self.nested_list[select_app][current_idx]
            syntax = core.ReportSyntax(_str)
            conv = syntax.find_page_syntax(val)

            canvas.drawString(xstart, ystart+yadd, str(conv)) # prints syntax values
            # canvas.drawString(xstart, ystart+yadd, _str) # prints natural values
            # canvas.drawString(xstart, ystart+yadd, val) # prints structure values
            
            yadd -= 10 # clear separation

        return current_idx

    def handle_second_page(self, canvas, select_app, last_idx):
        '''
        Handles all information for the second page of the pdf.
        Returns None.
        '''

        # Starting points
        xstart = 50
        ystart = 800

        #Increment
        yadd = 0

        req_sep = 0

        current_idx = last_idx

        canvas.setFont("Helvetica", 7)
        canvas.setPageSize((8.5*inch, 12*inch))
        # canvas.setFillColor(HexColor('#FFFFFF'))

        paragraph_start = ['Alumni ?', 'Citzenship ?', 'Text Messaging Option',
                           'SSN Verification Notice', 'Name Verification Notice',
                           'Conduct Question: Conviction', 'Conduct Question: Expulsion',
                           'Rellis Campus ?/Pre-Veterinary Medicine', 'Faculty Mentor ?',
                           'Consultant Agency ?', 'End of App']
        
        req_start = ['Request and/or Answer', 'Long REQ', 'Med REQ']
        
        for val in self.page_2:
            current_idx += 1

            if val in paragraph_start:
                yadd -= 10
            if val in req_start and req_sep == 0:
                req_sep = 1
                yadd -= 10


            _str = self.nested_list[select_app][current_idx]
            syntax = core.ReportSyntax(_str)
            conv = syntax.find_page_syntax(val)
    
            canvas.drawString(xstart, ystart+yadd, str(conv)) # prints syntax values
            # canvas.drawString(xstart, ystart+yadd, _str)
            # canvas.drawString(xstart, ystart+yadd, val)
            yadd -= 10

        return current_idx

    def handle_third_page(self, canvas, select_app, last_idx):
        '''
        Handles all information for the third page of the pdf.
        Returns None.
        '''

        # Starting points
        xstart = 50
        ystart = 800

        #Increment
        yadd = 0

        current_idx = last_idx
        req_sep = 0

        canvas.setFont("Helvetica", 7)
        canvas.setPageSize((8.5*inch, 12*inch))
        # canvas.setFillColor(HexColor('#FFFFFF'))

        paragraph_start = ['Faculty Mentor ?', 'Consultant/Agency', 
                           'Name Verification Notice', 'Conduct Question: Conviction',
                           'Graduation Date', 'Consultant Agency ?', 'Alumni ?', 'Citzenship ?',
                           'Conduct Question: Expulsion', 'Conduct: Pending Action', 'Rellis Campus ?/Pre-Veterinary Medicine',
                           'End of App']
        
        req_start = ['Request and/or Answer', 'Short REQ', 'Med REQ']
        
        for val in self.page_3:
            current_idx += 1

            if val in paragraph_start:
                yadd -= 10
            elif val in req_start and req_sep == 0:
                req_sep = 1
                yadd -= 10

            _str = self.nested_list[select_app][current_idx]
            syntax = core.ReportSyntax(_str)
            conv = syntax.find_page_syntax(val)
    
            canvas.drawString(xstart, ystart+yadd, str(conv)) # prints syntax values
            # canvas.drawString(xstart, ystart+yadd, _str)
            # canvas.drawString(xstart, ystart+yadd, val + _str)
            yadd -= 10