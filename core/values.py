import core

class Values:
    """Class created to house methods for in-place replacement text of varying types of markdown text in the 
    form of a string.
    """

    def short_msg_value(self, _list: list) -> str:

        transform_dict = {
            'Y': 'Yes',
            'N': 'No',
            'Y\\': 'Yes',
            'N\\': 'No',
            ' Y\\': 'Yes',
            ' N\\': 'No',
            'NO RESIDENCY COMMENTS INCLUDED\\': None
        }

        output = transform_dict.get(_list[-1], "Other")

        if output == 'Other':

            p = core.Process()
            output = p.process_str_2(_list[-1])

        return output

    def long_med_req_value(self, _list: list) -> str:
        """Long and Med REQ value output replacers based on given text.

        :param _list: full string of Long or Med REQ
        :type _list: list
        :return: updated string value for proper display
        :rtype: str
        """

        target = _list[3]

        transform_dict = {
            'Y': 'Yes',
            'N': 'No',
            'Y\\': 'Yes',
            'N\\': 'No',
            'S\\': 'Applicant indicates address is correct as entered',
            'I\\': 'International address (not standardized)'
        }

        output = transform_dict.get(_list[-1], _list[-1])

        output = output.strip()

        med_value = {
            'DUAL CREDIT': None,
            'IB DIPLOMA': f'IB Diploma: {output}',
            'RESUME SWITCH': f'Resume: {output}',
            'CURRENT ACADEMIC SUSP': None,
            'HOME SCHOOLED': None,
            'COLLEGE WORK': None,
            'RES: DETERM': None,
            'REVERSE TRANSFER': None,
            'APPLICATION SHARING': None,
            'FORMER STUDENT': None,
            'PHI THETA KAPPA': None,
            'INT CURR RESIDE IN US': None,
            'ULTIMATE DEGREE SOUGHT': f'Ultimate degree you wish to seek in this major from this institution? ',
            'PAYMENT RECONCILIATION': "Billing Information:", 
            'GRADUATE AWARD': None, 
            'TEST1 SENT': None, 
            'TEST2 SENT': None, 
            'CUR COLLEGE CRS': f"Current college course: {output}",
            'CUR COLLEGE ATT': f"Current college attending code: {output}",
            'COLLEGE WORK IN CLASSROOM': None,
            'FAMILY OBLIGATIONS': None,
            'EMERGENCY CONTACT HAS NO PHONE': f'Does the listed emergency contact NOT have a phone? {output}',
            'NATIVE LANGUAGE': f'What languages do you speak fluently? {output}',
            'INTL EXIT US': None,
            'INT VISA STATUS CHANGE': None,
        }

        long_value = {
            'COUNSELOR OPT IN': f'Opt-In for Counselor? {output}',
            'PERM COUNTY INFO' : f'Permanent County Info--{output[3:]}  (Country code = {output[:3]})',
            'PERM COUNTRY INFO' : f'Permanent Country Info--{output}',
            'PERM ADDR STND' : f'Mailing/Permanent Address Standardized: {output}',
            'CURR COUNTY INFO' : f'Current County CODE Info--{output}',
            'CURR COUNTRY INFO' : f'Current Country Info--{output}',
            'PHYS ADDR STND' : f'Physical Address Standardized: {output}',
            'FERPA CERT SWITCH' : f'FERPA Certification box checked on: {output[:4]}-{output[4:6]}-{output[6:]}',
            'MENINGITIS CERT SWITCH' : f'MENINGITIS Certification box checked on: {output[:4]}-{output[4:6]}-{output[6:]}',
            'TRUTH CERT SWITCH' : f'TRUTH Certification box checked on: {output[:4]}-{output[4:6]}-{output[6:]}',
            'CONSERVATORSHIP SWITCHES' : None,
            'TEACHING CERTIFICATE TYPE' : f'Will you seek Teacher Certification? Yes--{_list[-1]}',
            'HS GED TYPE': None,
            'PARENT 1 ED LEVEL RELATIONSHIP': None,
            'PARENT 2 ED LEVEL RELATIONSHIP': None,
            'PARENT OR GUARDIAN INFO': None,
            'CTRY SELF': f'Country: {output}',
            'CTRY SPOUSE': f'Country Spouse: {output[:3]}-{output[3:]}',
            'CTRY CHILD': f'Country Child: {output[:3]}-{output[3:]}',
            'FAMILY': None,
            'RES: PREVIOUS ENROLLMENT': None,
            'RES: RESIDENCY CLAIM': None,
            'RES: HS DIPLOMA OR GED': None,
            'RES: BASIS OF CLAIM': None,
            'RES: SELF': None,
            'RES: GUAR': None,
            'SPOKEN LANGUAGES': None,
            'PRE-PROFESSIONAL PGMZ': f'Do you plan to pursue a preprofessional program? {output}--Others',
            'PRE-PROFESSIONAL PGMC': f'Do you plan to pursue a preprofessional program? NURSING--{output}',
            'PRE-PROFESSIONAL PGMN': f'Do you plan to pursue a preprofessional program? {output}',
            'PRE-PROFESSIONAL PGMD': f'Do you plan to pursue a preprofessional program? {output}',
            'PRE-PROFESSIONAL PGMF': f'Do you plan to pursue a preprofessional program? PHARMACY--{output}',
            'PRE-PROFESSIONAL PGMB': f'Do you plan to pursue a preprofessional program? MEDICINE--{output}',
            'PRE-PROFESSIONAL PGME': f'Do you plan to pursue a preprofessional program? PHYSICAL THERAPY--{output}',
            'PRE-PROFESSIONAL PGMA': f'Do you plan to pursue a preprofessional program? PRELAW--{output}',
            'APP TYPE INFO': f'You are applying as a/an TRANSFER. Total hours earned: {output[8:11]}',
            'AUTO TRANSFER ADM': f'Automatic Admission for Transfer Applicants Based on Texas Law: {output}',
            'OTHER FIRST NAME1': f"Other first name: {output}",
            'OTHER MIDDLE NAME1': f"Other middle name: {output}",
            'OTHER LAST NAME1': f"Other last name: {output}",
            'OTHER LAST NAME2': f"Other last name: {output}",
            'OTHER SUFFIX NAME1': f"Other suffix: {output}",
            'FAMILY OBLIGATION INCOME': None,
            'FAMILY OBLIGATION OTHER': None,
            'FAMILY OBLIGATION CARE': None,
            'ALIEN APP/INT': None,
            'VET STATUS': None,
        }

        dictionaries = [med_value, long_value]
        
        for dicts in dictionaries:
            for key, value in dicts.items():
                if key == target:
                    if target == 'ULTIMATE DEGREE SOUGHT':
                        return value + self.additional_value(_list)
            
                    return value

        return _list
    
    def req_and_or_answer_value(self, _list: list) -> str:
        """Request and or Answer value markdown replacement text. Gives a clearer representation of
        the original question asked.

        :param _list: string from designated markdown text
        :type _list: list
        :return: new string based on dict value
        :rtype: str
        """

        target = _list[3]

        req_ = {
            'ALIEN APP/INT\\': None,
            'RES: COMMENTS\\': None,
            'FAMILY OBLIGATION INCOME\\': None,
            'FAMILY OBLIGATION CARE\\': None,
            'FAMILY OBLIGATION OTHER\\': None,
            'TREX TRANSCRIPT REQUESTED\\': None,
            'FUNDS SUPPORT\\': "Do you have a source of financial suppport if your are, or will be, in F-1 or J-1 status?",
            'CONTACT AT WORK\\': None,
            'RES: BASIS OF CLAIM\\': None,
            'REVERSE TRANSFER\\': None,
            'APPLICATION SHARING\\': None,
            'FAMILY OBLIGATIONS\\': None,
            'OTHER FIRST NAME1\\': None,
            'OTHER FIRST NAME2\\': None,
            'OTHER MIDDLE NAME1\\': None,
            'OTHER MIDDLE NAME2\\': None,
            'OTHER LAST NAME1\\': None,
            'OTHER LAST NAME2\\': None,
            'OTHER SUFFIX NAME1\\': None,
            'OTHER SUFFIX NAME2\\': None,
            'GRADUATE AWARD\\': None
        }

        return req_[target]
    
    def additional_value(self, _list: list) -> str:
        """Additional value markdown replacement text. Meant for markdown text that have more than one 
        option to be or semester information.

        :param _list: string from designated markdown text
        :type _list: list
        :return: new string based on dict values
        :rtype: str
        """

        target = _list[-1]

        semester = target[-5:]
        
        additional_= {
            'Is Parent TAMUK Alumni?\\': "Is Parent TAMUK Alumni ?",
            'Concentration\\': 'Concentration ?',
            'RELLIS Campus\\': 'RELLIS Campus ?',
            'Area of Emphasis/Concentration\\': "Area of Emphasis/Concentartion",
            'Pre-Veterinary Medicine\\': "Pre-Veterinary Medicine",
            'RELLIS Academic Alliance\\': "'RELLIS Academic Alliance ?'",
            '2.2\\': 'Certificate',
            '3.1\\': 'Professional',
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
    
    def ethnicity_race_value(self, _list: list) -> str:
        """Ethnicity and Race value markdown replacement  text. Gives a clearer representation of the 
        different options students can choose from.

        :param _list: string from designated markdown text
        :type _list: list
        :return: new string based on dict values
        :rtype: str
        """

        target = _list[-1]

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
            "Ethnicity=W\\": "Not Hispanic or Latino. Ethnicity=N/A.",
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
            "Ethnicity=\\": "Gender=N/A. Ethnicity=N/A.",
            "Ethnicity=R\\": "Hispanic or Latino. Ethnicity=N/A.",
        }

        dictionaries = [hispanic_, not_hispanic_, other_]

        for dicts in dictionaries:
            for key, value in dicts.items():
                if key == target:
                    return value
                
    def address_value(self, _list: list) -> str:
        
        target = []

        for item in _list[1:]:
            if item != '':
                target.append(item)
       
        return target
    
    def gender_value(self, _list: list) -> str:
        """Gender value markdown replacement  text. Gives a clearer representation of the 
        different options students can choose from.

        :param _list: string from designated markdown text
        :type _list: list
        :return: new string based on dict values
        :rtype: str
        """
        
        if len(_list) >= 4:
            target = "".join(_list[3]).translate(str.maketrans("", "", "\\0"))
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
           
    def extra_value(self, _list: list) -> str:

        target = str(_list[-1]).replace('\\', '')

        extra_ = {
            '01': 'Spouse Contact Information:',
            '02': 'Child Information:',
            '51': 'Emergency Contact Information:'
        }

        return extra_[target]
    
    def app_value(self, _list: list) -> str:

        target = str(_list[-1]).replace('\\', '')

        app_ = {
            'FFRESHMAN APPLICATION ID': 'U.S. Freshman Admission',
            'IFOREIGN GRAD APPLICATION ID': 'Interanational Graduate Admission',
            'CREENTRY UNDERGRAD APPLICATION ID': 'U.S. Re-Entry Admission',
            'GUS GRAD APPLICATION ID': 'U.S. Graduate Admission',
            'TUS TRANSFER APPLICATION ID': 'U.S. Transfer Admission',
            'AFOREIGN TRANSFER APPLICATION ID': 'International Transfer Admission'
        }

        return f'App ID: {_list[-2]}|{app_[target]}'
    
    def ssn_value(self, _list: list) -> str:
        
        target = str(_list[-2:]).replace('\\', '')
        
        if len(target) == 47:
            return 'STUDENT DECLINED TO PROVIDE SSN OR ITIN'

        return target
    
    def grade_level_value(self, _list: list) -> str:

        target = []

        for item in _list[1:]:
            if item != '':
                target.append(item)

        if len(target[0]) >= 8:
            target[0] = f'Date: {target[0][:4]}-{target[0][4:6]}-{target[0][6:]}'
            target[1] = f'Degree Sought: {target[1]}'
        else:
            if len(target) == 2:
                target[0] = f'Date: {target[0][:4]}-{target[0][4:]}'
                target[1] = f'Degree Earned: {target[1]}'
            else:
                target[0] = f'Date: {target[0][:4]}-{target[0][4:]}'

        return target
    
    def high_school_value(self, _list: list) -> str:

        return f"High School: {_list[-3]}-{_list[-1]}"