import core

class ReportStructure:

    def __init__(self, input: str):
        """Class created to house methods for PDF markdown text structure. Generates given
        strings of text and dynamically changes them based on varying elements.

        :param input: targeted string for explanation
        :type input: str
        """

        self._str = input

    def page_structure(self) -> str:
        """Main page structure creater that displays where markdown text will show up
        on a Canvas object with a short description.

        :return: string description of given markdown text
        :rtype: str
        """

        found = 0

        four_mark_structure = {
            'IN1104PG1': "Start Parent 1 Contact Info",
            'IN1104PG2': "Start Parent 2 Contact Info",
            'RQSAQZZ$  1': 'Multi type question',
            'RQSAQZZ$  2': 'Faculty Mentor ?',
            'RQSAQZZ$  3': 'Consultant Agency ?',
            'RQSAQZZ$  4': 'Multi type question',
            'RQSAQZZ$  5': 'Citzenship ?',
            'RQSAQZZ$  6': 'Text Messaging Option',
            'RQSAQZZ$  7': 'SSN Verification Notice',
            'RQSAQZZ$  8': 'Name Verification Notice',
            'RQSAQZZ$  9': 'Conduct Question: Conviction',
            'RQSAQZZ$ 10': 'Conduct Question: Expulsion',
            'RQSAQZZ$ 11': 'Conduct: Pending Action',
            'RQSAQZZ$ 12': 'Consultant/Agency',
            'RQSAQZZAPP SUBMIT/TRANSMIT': 'Submit/Transmit'
        }

        three_mark_structure = {
            'IN1104': "Start Extra Contact Info",
            'IN10104': "Start Extra Contact Info",
            'IN10102': "Start Student Contact Info",
            'IN1102': "Start Student Contact Info",
            'ATVSANZZ': "Extra Curricular Activities",
            'ATVSAOZZ': "Community or Volunteer Service",
            'ATVSBQZZ': "Award/Acheivement",
            'ATVSARZZ': "Employment/Internships/Summer Activities",
            'FOSMZZ': 'Major',
            'FOSCZZ': "Area of Interest",
            'RQSAQZZ': 'Request and/or Answer',
            'LONGR': 'Long REQ',
            'SHORTR': 'Short REQ',
            'MEDR': 'Med REQ',
            'CRSRU': "Senior Year Course(s)",
            'DTP102D8': "Issued Date"
        }

        two_mark_structure = {
            'BGN00': "Start App",
            'N1TM': "TXAPP",
            'N1AT': "AT",
            'REF48': "App ID",
            'DTP196': "Date Start",
            'DTP197': "Data End",
            'REFSY': "SSN",
            'REFZZ': "Premanent Residence status",
            'IN201': "Sir Name",
            'IN205': "Last Name",
            'IN202': "First Name",
            'IN203': "Middle Name",
            'IN207': "Middle Initial",
            'IN209': "Suffix",
            'IN216': "Representative Name",
            'IN218': "Preferred Name",
            'DMGD8': "Student Gender",
            'COMTE': "Phone",
            'COMAP': "Phone",
            'COMEM': "Email",
            'MSGYes': "Question Answer",
            'MSGNo': "Question Answer",
            'MSGYes - I am a RELLIS student': "Question Answer",
            'SSTB18': "Graduation Date",
            'N1HS': "High School Info",
            'CRSR': "Current enrolled course",
            'REFPSM': "Previous Applicant",
            'REFV2': "VISA Info",
            'DTP036': "VISA end date"
        }

        one_mark_structure = {
            'IND': "Place of Birth",
            'NTE': "Ethnicity/Race",
            'N3': "Address One",
            'N4': "Address Two",
            'SSE': "Semester",
            'MSG': "Question statement",
            'SES': "Grade level",
            'TST': "Admissions Test",
            'PCL': "Post-Secondary Colleges/Universities",
            'SUM': "Hours Earned",
            'SE': "End of App",
            'DEG': "Degree Earned",
            'SST': "Skip",
            'GE': 'Transfer Information',
            'IEA': 'Transfer Information',
            'ISA': "Transfer Information",
            'GS': "Transfer Information",
            'LUI': "Language",
            'SRE': "Old Admission Test Score",
            'SBT': "Old Admission Test",
            'SHORTM': "Short MSG"
        }

        converted_mark = ""

        dictionaries = [four_mark_structure, three_mark_structure, two_mark_structure, one_mark_structure]

        for idx in range(len(dictionaries)):
            total = len(dictionaries)
            search_key = "".join(self._str[0:(total-idx)])
            for key, value in dictionaries[idx].items():
                if key == search_key and found == 0:
                    found += 1
                    if search_key == 'MSG' and len(self._str) == 2:
                        converted_mark = 'Short MSG'
                    elif search_key == 'RQSAQZZ' and len(self._str) == 6:
                        converted_mark = 'Long REQ'
                    elif search_key == 'RQSAQZZ' and len(self._str) == 5:
                        converted_mark = 'Med REQ'
                    elif search_key == 'RQSAQZZ' and len(self._str) <= 2:
                        converted_mark = 'Short REQ'
                    else: 
                        converted_mark = value
                    break

        return converted_mark
    

    def transform_page(self, val: str) -> str:
        """Structure syntax replacer method. Meant to find the final display text
        for the Canvas object.

        :param val: strucutre markdown text
        :type val: str
        :return: new plain text string
        :rtype: str
        """

        _list = str(self._str).split("!")

        four_mark_syntax = {
            "Start Parent 1 Contact Info": "First Guardian/Parent Information:",
            "Start Parent 2 Contact Info": "Second Guardian/Parent Information:",
            'Multi type question': 'Multi type question',
            'Faculty Mentor ?': 'Faculty Mentor ?',
            'Consultant Agency ?': 'Consultant Agency ?',
            'Alumni ?': 'Alumni ?',
            'Citzenship ?': 'Citzenship ?',
            'Text Messaging Option': 'Text Messaging Option',
            'SSN Verification Notice': _list[-1],
            'Name Verification Notice': f'{_list[-1]}',
            'Conduct Question: Conviction': f'{_list[-1]}',
            'Conduct Question: Expulsion':'Conduct Question: Expulsion',
            'Conduct: Pending Action': 'Conduct: Pending Action',
            'Consultant/Agency': 'Consultant/Agency',
            'Submit/Transmit': _list[-1]
        }

        three_mark_syntax  = {
            "Start Extra Contact Info": None,
            "Start Student Contact Info": "Student Information:",
            "Extra Curricular Activities": f"{_list[-5:-4]}",
            "Community or Volunteer Service": f"{_list[-4:-2]}",
            "Award/Acheivement": f"{_list[-5:-4]}",
            "Employment/Internships/Summer Activities":f"{_list[-4:-3]}",
            'Major': f"Major: {_list[-1]}",
            "Area of Interest": f"Area of Interest: {_list[-1]}",
            'Request and/or Answer': _list[-1],
            'Long REQ': _list,
            'Short REQ': _list[-1],
            'Med REQ': _list,
            "Senior Year Course(s)": None,
            "Issued Date": f"Issued: {_list[-1]}"
        }

        two_mark_syntax  = {
            "Start App": "Start of App",
            "TXAPP": "ApplyTexas Application",
            "AT": None,
            "App ID": None,
            "Date Start": f"Date Start: {_list[-1][:4]}-{_list[-1][4:]}",
            "Data End": f"Date End: {_list[-1][:4]}-{_list[-1][4:]}",
            "SSN": None,
            "Premanent Residence status": _list[-1],
            "Sir Name": _list[-1],
            "Last Name": f"Last: {_list[-1]}",
            "First Name": f"First: {_list[-1]}",
            "Middle Name": f"Middle: {_list[-1]}",
            "Middle Initial": f"MIddle Initial: {_list[-1]}",
            "Suffix": f"Suffix: {_list[-1]}",
            "Representative Name": f"Rep Name: {_list[-1]}",
            "Preferred Name": f"Preferred: {_list[-1]}",
            "Student Gender": None,
            "Phone": f"Phone: {_list[-1]}",
            "Email": f"Email: {_list[-1]}",
            "Question Answer": _list[-2:-1],
            "Graduation Date": f"Expected Graduation Date: {_list[-1][:-3]}-{_list[-1][-3:]}",
            "High School Info": None,
            "Current enrolled course": None,
            "Previous Applicant": f"Previous Applicant: Yes",
            "VISA Info": f"Visa: {_list[-1]}",
            "VISA end date": f"End date: {_list[-1][:4]}-{_list[-1][4:]}"
        }

        one_mark_syntax  = {
            "Place of Birth": f"Place of Birth: {_list[-3:]}",
            "Ethnicity/Race": _list[-1],
            "Address One": f"Address: {_list[-1]}",
            "Address Two": None,
            "Semester": f"Semester: {_list[-1]}",
            "Question statement": _list[-2:-1],
            "Grade level": None,
            "Admissions Test": None,
            "Post-Secondary Colleges/Universities": None,
            "Hours Earned": f"Hours Earned: {_list[-1]}",
            "End of App": "End of App",
            "Degree Earned": f"Degree: {_list[-1]}",
            "Skip": f'Expected Graduation Date: {_list[-1][:4]}-{_list[-1][4:]}',
            'Transfer Information': None,
            "Language": _list,
            "Old Admission Test Score": _list,
            "Old Admission Test": _list,
            "Short MSG": None
        }
        
        converted_mark = ""

        dictionaries = [four_mark_syntax, three_mark_syntax, two_mark_syntax, one_mark_syntax]

        v = core.Values()

        for idx in range(len(dictionaries)):
            for key, value in dictionaries[idx].items():
                if key == val:
                    req_start = {
                        'Med REQ': v.long_med_req_value(_list, key),
                        'Long REQ': v.long_med_req_value(_list, key),
                        'Request and/or Answer': v.req_and_or_answer_value(_list, key),
                        'Multi type question': v.additional_value(_list, key),
                        'Degree Earned': v.additional_value(_list, key),
                        'Semester': v.additional_value(_list, key),
                        'Ethnicity/Race': v.ethnicity_race_value(_list, key),
                        'Address Two': v.address_value(_list, key),
                        'Student Gender': v.gender_value(_list, key),
                        'Start Extra Contact Info': v.extra_value(_list, key),
                        'App ID': v.app_value(_list, key),
                        'SSN': v.ssn_value(_list, key),
                        'Short MSG': v.short_msg_value(_list, key),
                        'Grade level': v.grade_level_value(_list, key),
                        'High School Info': v.high_school_value(_list, key),
                        'Admissions Test': v.admissions_value(_list, key)
                    }
                    
                    if key in req_start:
                        value = req_start[key]

                    converted_mark = str(value).replace("\\", "")
                    break

        return "".join(converted_mark).translate(str.maketrans("", "", "[],'{}"))
        
