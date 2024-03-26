import core

from datetime import datetime

class ReportSyntax(object):

    def __init__(self, _str):
        self._str = _str

    def page_structure(self):

        found = 0

        four_mark_structure = {
            'IN1104PG1': "Start Parent 1 Contact Info",
            'IN1104PG2': "Start Parent 2 Contact Info",
            'RQSAQZZ$  1': 'Rellis Campus ?/Pre-Veterinary Medicine',
            'RQSAQZZ$  2': 'Faculty Mentor ?',
            'RQSAQZZ$  3': 'Consultant Agency ?',
            'RQSAQZZ$  4': 'Alumni ?',
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
            'DMGD8': "Extra Student SKIP",
            'COMTE': "Phone",
            'COMAP': "Phone",
            'COMEM': "Email",
            'MSGYes': "Question Answer",
            'MSGNo': "Question Answer",
            'MSGYes - I am a RELLIS student': "Question Answer",
            'SSTB18': "Graduation Date",
            'N1HS': "High School Info",
            'CRSR': "Current enrolled course",
            'REFPSM': "Extra Name",
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

    def find_page_syntax(self, val):

        _str =str(self._str).split("!")

        four_mark_syntax = {
            "Start Parent 1 Contact Info": "First Guardian/Parent:",
            "Start Parent 2 Contact Info": "Second Guardian/Parent:",
            'Rellis Campus ?/Pre-Veterinary Medicine': 'Rellis Campus ?/Pre-Veterinary Medicine',
            'Faculty Mentor ?': 'Faculty Mentor ?',
            'Consultant Agency ?': 'Consultant Agency ?',
            'Alumni ?': 'Alumni ?',
            'Citzenship ?': 'Citzenship ?',
            'Text Messaging Option': 'Text Messaging Option',
            'SSN Verification Notice': 'SSN Verification Notice',
            'Name Verification Notice': 'Name Verification Notice',
            'Conduct Question: Conviction': 'Conduct Question: Conviction',
            'Conduct Question: Expulsion':'Conduct Question: Expulsion',
            'Conduct: Pending Action': 'Conduct: Pending Action',
            'Consultant/Agency': 'Consultant/Agency',
            'Submit/Transmit': {_str[-1]}
        }

        three_mark_syntax  = {
            "Start Extra Contact Info": "Emergency Contact:",
            "Start Student Contact Info": "Student:",
            "Extra Curricular Activities": f"{_str[-5:-4]}",
            "Community or Volunteer Service": f"{_str[-4:-2]}",
            "Award/Acheivement": f"{_str[-5:-4]} \t\t{_str[-1]}",
            "Employment/Internships/Summer Activities":f"{_str[-4:-3]}",
            'Major': f"Major: {_str[-1]}",
            "Area of Interest": f"Area of Interest: {_str[-1]}",
            'Request and/or Answer': _str[-1],
            'Long REQ': _str[-3:],
            'Short REQ': _str[-1],
            'Med REQ': _str[-2:],
            "Senior Year Course(s)": _str,
            "Issued Date": f"Issued: {_str[-1]}"
        }

        two_mark_syntax  = {
            "Start App": "Start of App",
            "TXAPP": "ApplyTexas Application",
            "AT": "",
            "App ID": _str[-1],
            "Date Start": f"Date Start: {_str[-1]}",
            "Data End": f"Date End: {_str[-1]}",
            "SSN": _str[-2:],
            "Premanent Residence status": _str[-1],
            "Sir Name": _str[-1],
            "Last Name": f"Last: {_str[-1]}",
            "First Name": f"First: {_str[-1]}",
            "Middle Name": f"Middle: {_str[-1]}",
            "Middle Initial": f"MIddle Initial: {_str[-1]}",
            "Suffix": f"Suffix: {_str[-1]}",
            "Representative Name": f"Rep Name: {_str[-1]}",
            "Preferred Name": f"Preferred: {_str[-1]}",
            "Extra Student SKIP": "",
            "Phone": f"Phone: {_str[-1]}",
            "Email": f"Email: {_str[-1]}",
            "Question Answer": _str[-2:-1],
            "Graduation Date": f"Graduation Date: {_str[-1]}",
            "High School Info": f"High School: {_str[-1]}",
            "Current enrolled course": _str,
            "Extra Name": "",
            "VISA Info": f"Visa: {_str[-1]}",
            "VISA end date": f"End date: {_str[-1]}"
        }

        one_mark_syntax  = {
            "Place of Birth": f"Place of Birth: {_str[-3:]}",
            "Ethnicity/Race": _str[-1],
            "Address One": f"Address: {_str[-1]}",
            "Address Two": f"{_str[1:]}",
            "Semester": f"Semester: {_str[-1]}",
            "Question statement": _str[-2:-1],
            "Grade level": _str,
            "Admissions Test": _str,
            "Post-Secondary Colleges/Universities": _str,
            "Hours Earned": _str,
            "End of App": "End of App",
            "Degree Earned": "",
            "Skip": "",
            'Transfer Information': _str,
            "Language": _str,
            "Old Admission Test Score": _str,
            "Old Admission Test": _str,
            "Short MSG": _str[-1]
        }
        
        converted_mark = ""

        dictionaries = [four_mark_syntax, three_mark_syntax, two_mark_syntax, one_mark_syntax]

        for idx in range(len(dictionaries)):
            for key, value in dictionaries[idx].items():
                if key == val:
                    converted_mark = str(value).replace("\\", "")
                    break

        output = str("".join(converted_mark)).strip("[[']")

        return output
        
