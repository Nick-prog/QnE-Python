import core

import re
from datetime import datetime

class ReportSyntax(object):

    def __init__(self, input: str):
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
    
    def long_med_req_value(self, _str: str) -> str:
        """Long and Med REQ value output replacers based on given text.

        :param _str: full string of Long or Med REQ
        :type _str: str
        :return: updated string value for proper display
        :rtype: str
        """

        target = _str[3]

        output = str(_str[-1]).replace('Y', 'Yes').replace('N', 'No')

        parent_value = {
            '32\\' : 'Mother',
            '33\\' : 'Father',
            '49\\' : "High School Diploma or GED",
            '26\\' : "Bachelor's/Four-year Degree",
            '34\\' : "Other Adult",
            '48\\' : "Stepmother",
            'PG1YY\\': 'Some College/No High School',
            'PG1YN\\': 'No College',
            'PG1N\\': 'Parent/Guardian 1',
            'PG2N\\': 'Parent/Guardian 2',
            'PG2YY\\': 'Some College',
            'PG2YN\\': 'No College',
            'ZZ\\': "Unknown",
        }

        med_value = {
            'DUAL CREDIT': "",
            'IB DIPLOMA': f'IB Diploma? {output}',
            'RESUME SWITCH': f'Resume? {output}',
            'PRE-PROFESSIONAL PGMZ': f'Do you plan to pursue a preprofessional program? {output}',
            'CURRENT ACADEMIC SUSP': f'Are you currently on academic suspension from the last college or univeristy attended? {output}',
            'HOME SCHOOLED': f'Where you home schooled? {output}',
            'COLLEGE WORK': f'Number of college credit hours by high school graduation date: {output}',
            'RES: DETERM': f'Applytexas Residency Determination: {output}',
            'REVERSE TRANSFER': f'Reverse transfer? {output}',
            'FAMILY OBLIGATIONS': f'Do you have family obligations that keep you from participating in extracurricular activities? {output}',
            'APPLICATION SHARING': f'Application sharing on denied admission? {output}',
            'FORMER STUDENT': '',
            'VET STATUS': f'U.S. Military-Veteran Status? {output}',
            'PHI THETA KAPPA': f'Are you a Phi Theta Kappa? {output}',
            'INT CURR RESIDE IN US': f'Are you currently residing in the U.S.? {output}',
            'ULTIMATE DEGREE SOUGHT': f'Ultimate degree you wish to seek in this major from this institution? ',
            'PAYMENT RECONCILIATION': "Billing Information:", #Next line info, displayed on reportgen.py
            'GRADUATE AWARD': "", #Skipped
            'TEST1 SENT': "", #Skipped
            'TEST2 SENT': "", #Skipped
            'CUR COLLEGE CRS': f"Present semester course to be completed: {output}",
            'CUR COLLEGE ATT': f"Current college attending code: {output}",
            'COLLEGE WORK IN CLASSROOM': ""
        }

        long_value = {
            'COUNSELOR OPT IN': f'Opt-In for Counselor? {output}',
            'PERM COUNTY INFO' : f'Permanent County Info--{output}',
            'PERM COUNTRY INFO' : f'Permanent Country Info--{output}',
            'PERM ADDR STND' : f'Mailing/Permanent Address Standardized: {output}',
            'CURR COUNTY INFO' : f'Current County CODE Info--{output}',
            'CURR COUNTRY INFO' : f'Current Country Info--{output}',
            'PHYS ADDR STND' : f'Physical Address Standardized: {output}',
            'FERPA CERT SWITCH' : f'FERPA Certification box checked on: {output}',
            'MENINGITIS CERT SWITCH' : f'MENINGITIS Certification box checked on: {output}',
            'TRUTH CERT SWITCH' : f'TRUTH Certification box checked on: {output}',
            'CONSERVATORSHIP SWITCHES' : "",
            'TEACHING CERTIFICATE TYPE' : f'Will you seek Teacher Certification? {output}',
            'HS GED TYPE': '',
            'PARENT 1 ED LEVEL RELATIONSHIP': f'Parent Relationship\t',
            'PARENT 2 ED LEVEL RELATIONSHIP': f'Parent Relationship\t',
            'PARENT OR GUARDIAN INFO': f'Education Level: ',
            'CTRY SELF': f'Country: {output}',
            'FAMILY': f'Family? {output}',
            'RES: PREVIOUS ENROLLMENT': "",
            'RES: RESIDENCY CLAIM': f'Of what state or country are you a resident? {output}',
            'RES: HS DIPLOMA OR GED': f'High school atteneded: {output}',
            'RES: BASIS OF CLAIM': '',
            'RES: SELF': _str, # f'{_str[-1]}',
            'RES: GUAR': _str, # f'{_str[-1]}',
            'SPOKEN LANGUAGES': f"In addition to English, what languages do you speak fluently? {output}",
            'PRE-PROFESSIONAL PGMC': f'Do you plan to pursue a preprofessional program? {output}',
            'PRE-PROFESSIONAL PGMN': f'Do you plan to pursue a preprofessional program? {output}',
            'PRE-PROFESSIONAL PGMD': f'Do you plan to pursue a preprofessional program? {output}',
            'APP TYPE INFO': f'You are applying as a/an TRANSFER. Total hours earned: {output}',
            'AUTO TRANSFER ADM': f'Automatic Admission for Transfer Applicants Based on Texas Law? {output}',
        }

        dictionaries = [med_value, long_value]
        parent_check = ['PARENT 1 ED LEVEL RELATIONSHIP', 'PARENT 2 ED LEVEL RELATIONSHIP', 'PARENT OR GUARDIAN INFO']
        
        for syntax in dictionaries:
            for key, value in syntax.items():
                if key == target:
                    if key in parent_check:
                        value = value + parent_value[_str[-1]]
                    elif target == 'ULTIMATE DEGREE SOUGHT':
                        value = value + self.additional_value(_str, value)
                    return value
            
        return _str
    
    def payment_syntax(self, _str: str) -> list:
        """Text fully listing the question given for payment information from students
        on ApplyTexas.

        :param _str: string from designated markdown text
        :type _str: str
        :return: list of strings to display proper output
        :rtype: list
        """

        target = _str[-1]

        transaction_time = target[0:8]
        payment_status = target[15:19]
        payment_amount = target[19:24]
        transaction_trace = target[24:36]
        customer_ref = target[36:48]
        card_type = target[48]
        last_4 = target[49:53]
        card_exp = target[53:57]


        payment_list = [f"Transcation Time: {transaction_time}",
                        f"Payment Status: {payment_status}",
                        f"Payment Amount: {payment_amount}",
                        f"Transcation Trace: {transaction_trace}",
                        f"Customer Reference: {customer_ref}",
                        f"Card Type: {card_type}",
                        f"Last 4 digit card number: {last_4}",
                        f"Card Expiration Date: {card_exp}"]
        
        return payment_list
    
    def hs_ged_syntax(self, _str: str) -> list:
        """Text fully listing the question given for HS GED information from students 
        on ApplyTexas.

        :param _str: string from designated markdown text
        :type _str: str
        :return: list of strings to display proper output
        :rtype: list
        """

        target = "".join(_str[4]).translate(str.maketrans("", "", "\\0"))

        target = target.replace('N', "No").replace('Y', "Yes")


        hs_list = ['If you did not graduate from high school, do you have a DEG or have you completed',
                   'another high school equivalency program?',
                   f'{target}']
        
        return hs_list
    
    def prev_syntax(self, _str: str) -> list:
        """Text fully listing the question given from previous college information from
        students on ApplyTexas.

        :param _str: string from designated markdown text
        :type _str: str
        :return: list of strings to display proper output
        :rtype: list
        """

        target = "".join(_str[-1]).translate(str.maketrans("", "", "\\0"))

        target = target.replace('N', "No").replace('Y', "Yes")

        prev_list = ['During the 12 months prior to you applying, did you register',
                     'for a public college or university in Texas?',
                     f'{target}']
        
        return prev_list
    
    def basis_syntax(self, _str: str) -> list:
        """Text fully listing the question given from basis of claim information from
        students on ApplyTexas.

        :param _str: string from designated markdown text
        :type _str: str
        :return: list of strings to display proper output
        :rtype: list
        """

        target = "".join(_str[-1]).translate(str.maketrans("", "", "\\0"))

        target = target.replace('NN', "No, No").replace('YY', "Yes, Yes").replace('YN', 'Yes, No').replace('NY', 'No, Yes')

        basis_list = ['Do you file your own federal income tax as an independent tax payer?',
                      'Are you claimed as a dependent or are you eligible to be claimed as a dependent',
                      'by a parent or court-appointed legal guardian?',
                      f'{target}']
        
        return basis_list
    
    def comment_syntax(self) -> list:
        """Text fully listing the question given from resident comments information from
        students on ApplyTexas.

        :return: list of strings to display proper output
        :rtype: list
        """

        com_list = ['Is there any additional information that you believe your college should know in', 
                    'evaluating your eligibility to be classified as a resident? If so, please provide.']
        
        return com_list
    
    def dual_syntax(self, _str: str) -> list:
        """Text fully listing the question given from dual credit information from students
        on ApplyTexas.

        :param _str: string from designated markdown text
        :type _str: str
        :return: list of strings to display proper output
        :rtype: list
        """

        target = "".join(_str[-1]).translate(str.maketrans("", "", "\\0"))
        
        target = target.replace('N', "No").replace('Y', "Yes")

        dual_list = ['Are you applyting to take college courses to be completed while you are still', 
                     'a high school student (Dual Credit or Concurrent Enrollment)?',
                     f'{target}']
        
        return dual_list
    
    def conservator_syntax(self, _str: str) -> list:
        """Text fully listing the question given from conservator information from students
        on ApplyTexas.

        :param _str: string from designated markdown text
        :type _str: str
        :return: list of strings to display proper output
        :rtype: list
        """

        target = "".join(_str[-1]).translate(str.maketrans("", "", "\\0"))

        target = target.replace('N', "No").replace('Y', "Yes")

        conserv_list = ['At anytime in your life were you placed in foster care or adopted from foster care in Texas?',
                        'If admitted, would your like to receive student foster care info and benefits?',
                        f'{target}']
        
        return conserv_list
    
    def alien_syntax(self, _str: str) -> list:
        """Text fully listing the question given from alien applicaiton information from
        students on ApplyTexas.

        :param _str: string from designated markdown text 
        :type _str: str
        :return: list of strings to display proper output
        :rtype: list
        """
        
        target = "".join(_str[-1]).translate(str.maketrans("", "", "\\0"))

        alien_list = ['Is this parent or legal guardian a foreign national whose application',
                      'for Permanent Resident Status has been preliminarily reviewed?',
                      f'{target}']
        
        return alien_list
    
    def former_syntax(self, _str: str) -> list:
        """Text fully listing the question given from former student information from
        students on ApplyTexas.

        :param _str: string from designated markdown text
        :type _str: str
        :return: list of strings to display proper output
        :rtype: list
        """

        target = "".join(_str[-1]).translate(str.maketrans("", "", "\\0"))

        target = target.replace('NN', "No, No").replace('YY', "Yes, Yes").replace('YN', 'Yes, No').replace('NY', 'No, Yes')

        former_list = ['Are you a former student of this institution?',
                       'Have you previously applied?',
                       f'{target}']
        
        return former_list
    
    def req_and_or_answer_value(self, _str: str, val: str) -> str:
        """Request and or Answer value markdown replacement text. Gives a clearer representation of
        the original question asked.

        :param _str: string from designated markdown text
        :type _str: str
        :param val: preivous string for designated markdown text
        :type val: str
        :return: new or previous string based on dict
        :rtype: str
        """

        target = _str[3]

        req_syntax = {
            'ALIEN APP/INT\\': "",
            'RES: COMMENTS\\': "",
            'FAMILY OBLIGATION INCOME\\': f"Please indicate, for the most recent tax year, your family's gross income. Include both untaxed and taxed income: {_str[-1]}",
            'FAMILY OBLIGATION CARE\\': f'How many people, including yourself, live in your household? (include brothers and sisiters attending college): {_str[-1]}',
            'FAMILY OBLIGATION OTHER\\': f'{_str[-1]}',
            'TREX TRANSCRIPT REQUESTED\\': f'Transcript sharing consent? {_str[-1]}',
            'FUNDS SUPPORT\\': "Do you have a source of financial suppport if your are, or will be, in F-1 or J-1 status?",
            'CONTACT AT WORK\\': "", # Skipped
        }

        for key, value in req_syntax.items():
            if key == target:
                return value
            
        return val
    
    def additional_value(self, _str: str, val: str) -> str:
        """Additional value markdown replacement text. Meant for markdown text that have more than one 
        option to be or semester information.

        :param _str: string from designated markdown text
        :type _str: str
        :param val: previous string for designated markdown text
        :type val: str
        :return: new or previous string based on dicts
        :rtype: str
        """

        target = _str[-1]

        semester = target[-5:]
        
        additional_syntax = {
            'Area of Emphasis/Concentration\\': "Area of Emphasis/Concentartion",
            'Pre-Veterinary Medicine\\': "Pre-Veterinary Medicine",
            'RELLIS Academic Alliance\\': "'RELLIS Academic Alliance ?'",
            '4.2\\': 'Degree: Masters (M.)',
            '4.4\\': 'Degree: Doctoral (PhD)',
        }

        semester_syntax = {
            '0901\\': 'Semester: Fall',
            '0601\\': 'Semester: Summer',
        }

        for key, value in additional_syntax.items():
            if key == target:
                return value
            
        for key, value in semester_syntax.items():
            if key == semester:
                output = f"{value} {target[:-5]}"
                return output

        return val
    
    def ethnicity_race_value(self, _str: str, val: str) -> str:
        """Ethnicity and Race value markdown replacement  text. Gives a clearer representation of the 
        different options students can choose from.

        :param _str: string from designated markdown text
        :type _str: str
        :param val: previous string for designated markdown text
        :type val: str
        :return: new or previous string based on dicts
        :rtype: str
        """

        target = _str[-1]

        hispanic_syntax = {
            "Ethnicity=R;Race=S\\": "Ethnicity=Hispanic or Latino. Race=White.",
            "Ethnicity=R;Race=T\\": "Ethnicity=Hispanic or Latino. Race=American Indian or Alaska Native.",
            "Ethnicity=R;Race=Q\\": "Hispanic or Latino ethnicity. Race=Black or African American.",
            "Ethnicity=R;Race=U\\": "Hispanic or Latino ethnicity. Race=Asian.",
            "Ethnicity=R;Race=V\\": "Hispanic or Latino ethnicity. Race=Native Hawaiian or Other Pacific Islander.",
            "Ethnicity=R;Race=QS\\": "Hispanic or Latino ethnicity. Race=Black or African American or White.",
            "Ethnicity=R;Race=US\\": "Hispanic or Latino ethnicity. Race=Asian or White.",
            "Ethnicity=R;Race=UV\\": "Hispanic or Latino ethnicity. Race=Asian, Native Hawaiian or Other Pacific Islander.",
            "Ethnicity=R;Race=TS\\": "Hispanic or Latino ethnicity. Race=American Indian, Alaska Native or White.",
            "Ethnicity=R;Race=ST\\": "Hispanic or Latino ethnicity. Race=American Indian, Alaska Native or White.",
            "Ethnicity=R;Race=UST\\": "Hispanic or Latino ethnicity. Race=Asian, White, American Indian or Alaska Native.",
        }

        not_hispanic_syntax = {
            "Ethnicity=W\\": "Ethnicity=Not Hispanic or Latino ethnicity. Race=N/A.",
            "Ethnicity=W;Race=S\\": "Ethnicity=Not Hispanic or Latino ethnicity. Race=White.",
            "Ethnicity=W;Race=T\\": "Ethnicity=Not Hispanic or Latino ethnicity. Race=American Indian or Alaska Native.",
            "Ethnicity=W;Race=Q\\": "Ethnicity=Not Hispanic or Latino ethnicity. Race=Black or African American.",
            "Ethnicity=W;Race=U\\": "Ethnicity=Not Hispanic or Latino ethnicity. Race=Asian.",
            "Ethnicity=W;Race=V\\": "Ethnicity=Not Hispanic or Latino ethnicity. Race=Native Hawaiian or Other Pacific Islander.",
            "Ethnicity=W;Race=QS\\": "Ethnicity=Not Hispanic or Latino ethnicity. Race=Black, African American or White.",
            "Ethnicity=W;Race=US\\": "Ethnicity=Not Hispanic or Latino ethnicity. Race=Asian or White.",
            "Ethnicity=W;Race=UV\\": "Ethnicity=Not Hispanic or Latino ethnicity. Race=Asian, Native Hawaiian or Other Pacific Islander.",
            "Ethnicity=W;Race=TS\\": "Ethnicity=Not Hispanic or Latino ethnicity. Race=American Indian, Alaska Native or White.",
            "Ethnicity=W;Race=ST\\": "Ethnicity=Not Hispanic or Latino ethnicity. Race=American Indian, Alaska Native or White.",
            "Ethnicity=W;Race=UST\\": "Ethnicity=Not Hispanic or Latino ethnicity. Race=Asian, White, American Indian or Alaska Native.",
        }

        other_syntax = {
            "Ethnicity=\\": "Ethnicity=N/A. Race=N/A.",
            "Ethnicity=R\\": "Ethnicity=Hispanic or Latino. Race=N/A.",
        }

        dictionaries = [hispanic_syntax, not_hispanic_syntax, other_syntax]

        for dicts in dictionaries:
            for key, value in dicts.items():
                if key == target:
                    return value

        return val
    
    def gender_value(self, _str: str, val: str) -> str:
        """Gender value markdown replacement  text. Gives a clearer representation of the 
        different options students can choose from.

        :param _str: string from designated markdown text
        :type _str: str
        :param val: previous string for designated markdown text
        :type val: str
        :return: new or previous string based on dicts
        :rtype: str
        """
        
        target = "".join(_str[3]).translate(str.maketrans("", "", "\\0"))

        gender_syntax = {
            'F': 'Gender=Female',
            'M': 'Gender=Male'
        }

        for key, value in gender_syntax.items():
           if key == target:
               return value
           
        return val
        

    def find_page_syntax(self, val: str) -> str:
        """Structure syntax replacer method. Meant to find the final display text
        for the Canvas object.

        :param val: strucutre markdown text
        :type val: str
        :return: new plain text string
        :rtype: str
        """

        _str = str(self._str).split("!")

        four_mark_syntax = {
            "Start Parent 1 Contact Info": "First Guardian/Parent Information:",
            "Start Parent 2 Contact Info": "Second Guardian/Parent Information:",
            'Multi type question': 'Multi type question',
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
            "Start Extra Contact Info": "Emergency Contact Information:",
            "Start Student Contact Info": "Student Information:",
            "Extra Curricular Activities": f"{_str[-5:-4]}",
            "Community or Volunteer Service": f"{_str[-4:-2]}",
            "Award/Acheivement": f"{_str[-5:-4]}",
            "Employment/Internships/Summer Activities":f"{_str[-4:-3]}",
            'Major': f"Major: {_str[-1]}",
            "Area of Interest": f"Area of Interest: {_str[-1]}",
            'Request and/or Answer': _str[-1],
            'Long REQ': _str,
            'Short REQ': _str[-1],
            'Med REQ': _str,
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
            "Student Gender": "",
            "Phone": f"Phone: {_str[-1]}",
            "Email": f"Email: {_str[-1]}",
            "Question Answer": _str[-2:-1],
            "Graduation Date": f"Expected Graduation Date: {_str[-1]}",
            "High School Info": f"School Code: {_str[-1]}",
            "Current enrolled course": _str,
            "Previous Applicant": f"Previous Applicant: {_str[-1]}",
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
            "Grade level": f"Date: {_str[1]}",
            "Admissions Test": _str,
            "Post-Secondary Colleges/Universities": f"Name of Institution: {_str[-1]}",
            "Hours Earned": f"Hours Earned: {_str[-1]}",
            "End of App": "End of App",
            "Degree Earned": f"Degree: {_str[-1]}",
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
                    if key == "Med REQ" or key == "Long REQ":
                        value = self.long_med_req_value(_str)
                    elif key == "Request and/or Answer":
                        value = self.req_and_or_answer_value(_str, value)
                    elif key == 'Multi type question' or key == "Degree Earned" or key == 'Semester':
                        value = self.additional_value(_str, value)
                    elif key == 'Ethnicity/Race':
                        value = self.ethnicity_race_value(_str, value)
                    elif key == 'Student Gender':
                        value = self.gender_value(_str, value)
                    converted_mark = str(value).replace("\\", "")
                    break

        output = "".join(converted_mark).translate(str.maketrans("", "", "[],'{}"))

        return output
        
