import core

class Values:
    """Class created to house methods for in-place replacement text of varying types of markdown text in the 
    form of a string.
    """

    def long_med_req_value(self, _str: str) -> str:
        """Long and Med REQ value output replacers based on given text.

        :param _str: full string of Long or Med REQ
        :type _str: str
        :return: updated string value for proper display
        :rtype: str
        """

        target = _str[3]

        output = str(_str[-1]).replace('Y', 'Yes').replace('N', 'No')

        output = output.strip()

        med_value = {
            'DUAL CREDIT': None,
            'IB DIPLOMA': f'IB Diploma: {output}',
            'RESUME SWITCH': f'Resume: {output}',
            'PRE-PROFESSIONAL PGMZ': f'Do you plan to pursue a preprofessional program? {output}',
            'CURRENT ACADEMIC SUSP': f'Are you currently on academic suspension from the last college or univeristy attended? {output}',
            'HOME SCHOOLED': f'Where you home schooled: {output}',
            'COLLEGE WORK': f'Will you have college credit hours by high school graduation date, if so how many? {output}',
            'RES: DETERM': f'Applytexas Residency Determination: {output}',
            'REVERSE TRANSFER': f'Reverse transfer: {output}',
            'APPLICATION SHARING': f'Application sharing on denied admission: {output}',
            'FORMER STUDENT': None,
            'VET STATUS': f'U.S. Military-Veteran Status? {output}',
            'PHI THETA KAPPA': f'Are you a Phi Theta Kappa? {output}',
            'INT CURR RESIDE IN US': f'Are you currently residing in the U.S.? {output}',
            'ULTIMATE DEGREE SOUGHT': f'Ultimate degree you wish to seek in this major from this institution? ',
            'PAYMENT RECONCILIATION': "Billing Information:", 
            'GRADUATE AWARD': None, 
            'TEST1 SENT': None, 
            'TEST2 SENT': None, 
            'CUR COLLEGE CRS': f"Present semester course to be completed: {output}",
            'CUR COLLEGE ATT': f"Current college attending code: {output}",
            'COLLEGE WORK IN CLASSROOM': None,
            'FAMILY OBLIGATIONS': f'Do you have family obligations that keep you from participating in extracurricular activities? {output}',
            'EMERGENCY CONTACT HAS NO PHONE': f'Does the listed emergency contact NOT have a phone? {output}'
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
            'CONSERVATORSHIP SWITCHES' : None,
            'TEACHING CERTIFICATE TYPE' : f'Will you seek Teacher Certification? {output}',
            'HS GED TYPE': None,
            'PARENT 1 ED LEVEL RELATIONSHIP': None,
            'PARENT 2 ED LEVEL RELATIONSHIP': None,
            'PARENT OR GUARDIAN INFO': f'Education Level: ',
            'CTRY SELF': f'Country: {output}',
            'FAMILY': None, # f'Family? {output}',
            'RES: PREVIOUS ENROLLMENT': None,
            'RES: RESIDENCY CLAIM': f'What state or country are you a resident of: {output}',
            'RES: HS DIPLOMA OR GED': None,
            'RES: BASIS OF CLAIM': None,
            'RES: SELF': None,
            'RES: GUAR': None,
            'SPOKEN LANGUAGES': f"In addition to English, what languages do you speak fluently? {output}",
            'PRE-PROFESSIONAL PGMC': f'Do you plan to pursue a preprofessional program? {output}',
            'PRE-PROFESSIONAL PGMN': f'Do you plan to pursue a preprofessional program? {output}',
            'PRE-PROFESSIONAL PGMD': f'Do you plan to pursue a preprofessional program? {output}',
            'PRE-PROFESSIONAL PGMF': f'Do you plan to pursue a preprofessional program? PHARMACY--{output}',
            'PRE-PROFESSIONAL PGMB': f'Do you plan to pursue a preprofessional program? MEDICINE--{output}',
            'PRE-PROFESSIONAL PGME': f'Do you plan to pursue a preprofessional program? PHYSICAL THERAPY--{output}',
            'APP TYPE INFO': f'You are applying as a/an TRANSFER. Total hours earned: {output}',
            'AUTO TRANSFER ADM': f'Automatic Admission for Transfer Applicants Based on Texas Law: {output}',
            'OTHER FIRST NAME1': f"Other first name: {output}",
            'OTHER MIDDLE NAME1': f"Other middle name: {output}",
            'OTHER LAST NAME1': f"Other last name: {output}",
            'OTHER SUFFIX NAME1': f"Other suffix: {output}",
        }

        dictionaries = [med_value, long_value]
        parent_check = ['PARENT 1 ED LEVEL RELATIONSHIP', 'PARENT 2 ED LEVEL RELATIONSHIP', 'PARENT OR GUARDIAN INFO']
        
        for dicts in dictionaries:
            for key, value in dicts.items():
                if key == target:
                    if key in parent_check:
                        return self.parent_value(_str)
                    elif target == 'ULTIMATE DEGREE SOUGHT':
                        return value + self.additional_value(_str)
                    
                    return value
                
        return _str
    
    def parent_value(self, _str: str) -> str:
        """REMOVED too inconsistent on recording. Parent value markdown replacement text. Gives a clearer representation of
        the original question asked.

        :param _str: string from designated markdown text
        :type _str: str
        :return: new string based on dict value
        :rtype: str
        """
        
        target = _str[3]

        parent_ = {
            '32\\' : 'Mother',
            '33\\' : 'Father',
            '49\\' : "High School Diploma or GED",
            '26\\' : "Bachelor's/Four-year Degree",
            '34\\' : "Other Adult",
            '48\\' : "Stepmother",
            'PG1YY\\': 'High School Diploma or GED',
            'PG1YN\\': 'No College',
            'PG1N\\': 'Parent/Guardian 1',
            'PG2N\\': 'Parent/Guardian 2',
            'PG2YY\\': 'No High School',
            'PG2YN\\': 'Some College',
            'PG2NY\\': 'Some College',
            'ZZ\\': "Unknown",
        }

        value = parent_[_str[-1]]

        # return f"{target}: {value}"
        return None
    
    def req_and_or_answer_value(self, _str: str) -> str:
        """Request and or Answer value markdown replacement text. Gives a clearer representation of
        the original question asked.

        :param _str: string from designated markdown text
        :type _str: str
        :return: new string based on dict value
        :rtype: str
        """

        target = _str[3]

        req_ = {
            'ALIEN APP/INT\\': None,
            'RES: COMMENTS\\': None,
            'FAMILY OBLIGATION INCOME\\': None,
            'FAMILY OBLIGATION CARE\\': None,
            'FAMILY OBLIGATION OTHER\\': None, # f'{_str[-1]}',
            'TREX TRANSCRIPT REQUESTED\\': f'Transcript sharing consent: {_str[-1]}',
            'FUNDS SUPPORT\\': "Do you have a source of financial suppport if your are, or will be, in F-1 or J-1 status?",
            'CONTACT AT WORK\\': None,
            'RES: BASIS OF CLAIM\\': None,
            'REVERSE TRANSFER\\': None,
            'APPLICATION SHARING\\': None,
            'FAMILY OBLIGATIONS\\': None, # f'Do you have family obligations that keep you from participating in extracurricular activities? {_str[-1]}',
            'OTHER FIRST NAME1\\': None,
            'OTHER MIDDLE NAME1\\': None,
            'OTHER LAST NAME1\\': None,
            'OTHER SUFFIX NAME1\\': None,
            'GRADUATE AWARD\\': None
        }

        return req_[target]
    
    def additional_value(self, _str: str) -> str:
        """Additional value markdown replacement text. Meant for markdown text that have more than one 
        option to be or semester information.

        :param _str: string from designated markdown text
        :type _str: str
        :return: new string based on dict values
        :rtype: str
        """

        target = _str[-1]

        semester = target[-5:]
        
        additional_= {
            'Is Parent TAMUK Alumni?\\': "Is Parent TAMUK Alumni ?",
            'Concentration\\': 'Concentration ?',
            'RELLIS Campus\\': 'RELLIS Campus ?',
            'Area of Emphasis/Concentration\\': "Area of Emphasis/Concentartion",
            'Pre-Veterinary Medicine\\': "Pre-Veterinary Medicine",
            'RELLIS Academic Alliance\\': "'RELLIS Academic Alliance ?'",
            '4.2\\': 'Degree: Masters (M.)',
            '4.4\\': 'Degree: Doctoral (PhD)',
            ' \\': 'Degree: N/A'
        }

        semester_ = {
            '0901\\': 'Semester: Fall',
            '0601\\': 'Semester: Summer',
        }

        for key, value in additional_.items():
            if key == target:
                return value
            
        for key, value in semester_.items():
            if key == semester:
                output = f"{value} {target[:-5]}"
                return output
    
    def ethnicity_race_value(self, _str: str) -> str:
        """Ethnicity and Race value markdown replacement  text. Gives a clearer representation of the 
        different options students can choose from.

        :param _str: string from designated markdown text
        :type _str: str
        :return: new string based on dict values
        :rtype: str
        """

        target = _str[-1]

        hispanic_ = {
            "Ethnicity=R;Race=S\\": "Hispanic or Latino. White.",
            "Ethnicity=R;Race=T\\": "Hispanic or Latino. American Indian or Alaska Native.",
            "Ethnicity=R;Race=Q\\": "Hispanic or Latino. Black or African American.",
            "Ethnicity=R;Race=U\\": "Hispanic or Latino. Asian.",
            "Ethnicity=R;Race=V\\": "Hispanic or Latino. Native Hawaiian or Other Pacific Islander.",
            "Ethnicity=R;Race=QS\\": "Hispanic or Latino. Black or African American or White.",
            "Ethnicity=R;Race=US\\": "Hispanic or Latino. Asian or White.",
            "Ethnicity=R;Race=UV\\": "Hispanic or Latino. Asian, Native Hawaiian or Other Pacific Islander.",
            "Ethnicity=R;Race=TS\\": "Hispanic or Latino. American Indian, Alaska Native or White.",
            "Ethnicity=R;Race=ST\\": "Hispanic or Latino. American Indian, Alaska Native or White.",
            "Ethnicity=R;Race=UST\\": "Hispanic or Latino. Asian, White, American Indian or Alaska Native.",
        }

        not_hispanic_ = {
            "Ethnicity=W\\": "Not Hispanic or Latino. N/A.",
            "Ethnicity=W;Race=S\\": "Not Hispanic or Latino. White.",
            "Ethnicity=W;Race=T\\": "Not Hispanic or Latino. American Indian or Alaska Native.",
            "Ethnicity=W;Race=Q\\": "Not Hispanic or Latino. Black or African American.",
            "Ethnicity=W;Race=U\\": "Not Hispanic or Latino. Asian.",
            "Ethnicity=W;Race=V\\": "Not Hispanic or Latino. Native Hawaiian or Other Pacific Islander.",
            "Ethnicity=W;Race=QS\\": "Not Hispanic or Latino. Black, African American or White.",
            "Ethnicity=W;Race=US\\": "Not Hispanic or Latino. Asian or White.",
            "Ethnicity=W;Race=UV\\": "Not Hispanic or Latino. Asian, Native Hawaiian or Other Pacific Islander.",
            "Ethnicity=W;Race=TS\\": "Not Hispanic or Latino. American Indian, Alaska Native or White.",
            "Ethnicity=W;Race=ST\\": "Not Hispanic or Latino. American Indian, Alaska Native or White.",
            "Ethnicity=W;Race=UST\\": "Not Hispanic or Latino. Asian, White, American Indian or Alaska Native.",
        }

        other_ = {
            "Ethnicity=\\": "N/A. N/A.",
            "Ethnicity=R\\": "Hispanic or Latino. N/A.",
        }

        dictionaries = [hispanic_, not_hispanic_, other_]

        for dicts in dictionaries:
            for key, value in dicts.items():
                if key == target:
                    return value
    
    def gender_value(self, _str: str) -> str:
        """Gender value markdown replacement  text. Gives a clearer representation of the 
        different options students can choose from.

        :param _str: string from designated markdown text
        :type _str: str
        :return: new string based on dict values
        :rtype: str
        """
        
        if len(_str) >= 4:
            target = "".join(_str[3]).translate(str.maketrans("", "", "\\0"))
        else:
            target = ""

        gender_ = {
            'F': 'Gender=Female',
            'M': 'Gender=Male',
            '': 'Gender=N/A'
        }

        for key, value in gender_.items():
           if key == target:
               return value