import core

class Syntax:

    def __init__(self, target: list):
        self.target = target

        self._syntax = {
            'Y': 'Yes',
            'N': 'No',
            'I': 'International address (not standardized)',
            'S': 'Applicant indicates address is correct as entered',
            'K': 'Not provided'
        }

    def PRE_PROFESSIONAL(self) -> list:
        
        _list = core.Process().process_str_with_blank(self.target[3])
        
        _syntax = {
            'PGMZ': 'Others',
            'PGMN': 'None',
            'PGMD': 'VETERINARY',
            'PGMC': 'NURSING',
            'PGMF': 'PHARMACY',
            'PGMB': 'MEDICINE',
            'PGME': 'PHYSICAL THERAPY',
            'PGMA': 'PRELAW'
        }

        return ['Do you plan to pursue a preprofessional program?', f'{_syntax.get(_list[1], _list[1])}', '']

    def CERT_SWITCH(self) -> list:

        _syntax = {
            'FERPA CERT SWITCH': 'FERPA certification box checked on', 
            'MENINGITIS CERT SWITCH': 'MENINGITIS certification box checked on', 
            'TRUTH CERT SWITCH': 'TRUTH certification box checked on',
            'RESUME CERT SWITCH': 'Resume:'
            }

        if self.target[3] not in _syntax.keys():
            return
        
        _type = _syntax.get(self.target[3], self.target[3])

        output = [f'{_type} {self.target[-1][4:6]}/{self.target[-1][6:8]}/{self.target[-1][:4]}']

        if self.target[3] == 'TRUTH CERT SWITCH':
            output.append('')
        elif self.target[3] == 'FERPA CERT SWITCH':
            output.insert(0, '')

        return output

    def CONSERVATORSHIP_SWITCHES(self) -> list:

        if self.target[3] != 'CONSERVATORSHIP SWITCHES':
            return
        
        first = str(self.target[-2]).replace('\\', '')
        second = str(self.target[-1]).replace('\\', '')

        first = self._syntax.get(first, first)
        second = self._syntax.get(second, second)


        return ['17. Texas Conservatorship:',
                'At anytime in your life were you placed in foster care or adopted from foster care in Texas?', 
                f'{first}', '',
                'If admitted, would your like to receive student foster care info and benefits?',
                f'{second}', '']
    
    def HS_GED_TYPE(self) -> list:

        if self.target[3] != 'HS GED TYPE':
            return

        target = self._syntax.get(self.target[4], self.target[4])
        final = str(self.target[-1]).replace('\\', '')


        return ['', '3. If you did not graduate from high school, do you have a DEG or have you completed',
                'another high school equivalency program?',
                 f'{target}-{final}', '']
    
    def COLLEGE_WORK(self) -> list:

        if self.target[3] != 'COLLEGE WORK':
            return

        if len(self.target) == 5:
            return ['Will you have college credit hours by high school graduation date, if so how many?',
                    f'{self._syntax.get(self.target[-1], self.target[-1])}', '']

        return ['Will you have college credit hours by high school graduation date, if so how many?',
                f'{self._syntax.get(self.target[-1], self.target[-1])}','',
                'Are your college credit hours earned (or being earned) through dual credit, concurrent',
                'enrollment, or an early college high school?',
                f'{self.target[-1]}', '']

    def RES_PREVIOUS_ENROLLMENT(self) -> list:

        if self.target[3] != 'RES: PREVIOUS ENROLLMENT':
            return
        
        _str = str(self.target[-1][1:]).replace('\\', '')

        _list = core.Process().process_str_with_num(_str)
        _list[-1] = core.Process().create_uniform_item(_list[-1], 12)

        _syntax = {
            'K': 'Not provided',
            'U': 'Not provided',
            'R': 'Resident (In-State)',
            'N': "Didn't pay in-state tution",
            '2': 'Spring',
            '9': 'Fall'
        }

        if not str(_list[-1]).startswith('0'):
            term = _list[-1][:-2]

            start = _syntax.get(term[4], term[4])
            end = _syntax.get(term[9], term[9])

            third = f'{start} {term[:4]} - {end} {term[5:9]}'
            

            return ['Residency Information', '', '1. Residency Information', '',
                    'During the 12 months prior to you applying, did you register',
                    'for a public college or university in Texas?', f'{self._syntax.get(self.target[-1][0], self.target[-1][0])}', '',
                    'What Texas public college or university did you last attend?',
                    f'{_list[0]}', '',
                    'In which terms were you last enrolled?', f'{third}', '',
                    'During you last semester at a Texas public institution, did you pay resident (in-state)',
                    'or nonresident (out-of-state) tution?', f'{_syntax.get(_list[-1][-2], _list[-1][-2])}', '',
                    'If you paid in-state tution at your last institution, was it because you were classified',
                    'as a resdient or because you were non-resident who received a wavier?', f'{_syntax.get(_list[-1][-1], _list[-1][-1])}', '']
        
        return ['Residency Information', '', '1. Residency Information', '',
                'During the 12 months prior to you applying, did you register',
                'for a public college or university in Texas?', f'{self._syntax.get(self.target[-1][0], self.target[-1][0])}', '']
    
    def RES_BASIS_OF_CLAIM(self) -> list:

        if self.target[3] != 'RES: BASIS OF CLAIM':
            return
        
        _syntax = {
            'S': 'Self',
            'P': 'Parent of Legal Guardian'
        }
        
        if len(self.target) == 4:
            return ['Do you file your own federal income tax as an independent tax payer?', 'Not provided', '',
                'Are you claimed as a dependent or are you eligible to be claimed as a dependent',
                'by a parent or court-appointed legal guardian?', 'Not provided', '']
        elif len(self.target[-1]) == 3:
            return ['Do you file your own federal income tax as an independent tax payer?', f'{self._syntax.get(self.target[-1][0], self.target[-1][0])}', '',
                'Are you claimed as a dependent or are you eligible to be claimed as a dependent',
                'by a parent or court-appointed legal guardian?', f'{self._syntax.get(self.target[-1][1], self.target[-1][1])}', '',
                'Who provides the majority of your support?', f'{_syntax.get(self.target[-1][-1], self.target[-1][-1])}', '']

        return ['Do you file your own federal income tax as an independent tax payer?', f'{self._syntax.get(self.target[-1][0], self.target[-1][0])}', '',
                'Are you claimed as a dependent or are you eligible to be claimed as a dependent',
                'by a parent or court-appointed legal guardian?', f'{self._syntax.get(self.target[-1][1], self.target[-1][1])}', '']
    
    def RES_DETERM(self) -> list:

        if self.target[3] != 'RES: DETERM':
            return
        
        _syntax = {
            'Y' : 'Y - Texas Resident',
            'N' : 'N - Non-Texas Resident',
            'A' : 'Needs Affidavit'
        }

        return ['To assist colleges or universities in residency determinations, the ApplyTexas System asks',
                'applicants a series of core questions. Based on answers to these questions, the System estimates',
                'the residency of each applicant. College or university administrators should make final residency',
                'determinations based on rules set out in the Texas Administrative Code Title 19, Part 1, Chapter 21,',
                'Subchapter B. The residency determinations are Texas resident (T), Non-Texas resident (N), or Unable',
                'to Determine (U).', '',
                'Exception codes are provided for applicants with Unable to Determine status, and may be',
                'provided for applicants with Texas resident status, if the applicant needs to provide more',
                'information or verification of status. It is recommended that institutions verify this information.', '',
                'Note: The residency determination is not visible to the applicant.', '',
                f'Applytexas Residency Determination: {_syntax.get(self.target[-1], "U - Unable to determine")}', ''] 

    def RES_HS_DIPLOMA_OR_GED(self) -> list:

        if self.target[3] != 'RES: HS DIPLOMA OR GED':
            return

        return [f'Previous High School Name: {self.target[-1][:-2]}',
                'Did you live or will you have lived in Texas the 36 months leading up',
                'to high school graduation or completion of the GED?', f'{self._syntax.get(self.target[-1][-2:][0], self.target[-1][-2:][0])}', '',
                'When you begin the semester for which you are applying, will you have lived',
                'in Texas for the previous 12 months?', f'{self._syntax.get(self.target[-1][-2:][1], self.target[-1][-2:][1])}', '']

    def RES_RESIDENCY_CLAIM(self) -> list:

        if self.target[3] != 'RES: RESIDENCY CLAIM':
            return
        

        return ['', 'Of what state or country are you a resident?',
                f'{self.target[-2]}--{self.target[-1]}', '']

    def RES_SELF(self) -> list:

        if self.target[3] != 'RES: SELF':
            return

        _str = str(self.target[-1]).strip()
        
        _list = list(_str)
        
        if len(_list) != 38:
            extra = len(_list) - 38
            start = ''.join(_list[:extra])
            _list = _list[extra:]
        else:
            start = 'Not provided'

        if _list[0] == ' ' or _list[0] == '0':
            return
        
        _syntax = {
            'H': 'Establish/Maintain a home',
            'W': 'Work Assignment',
            'E': 'Gainfully Employed',
            'C': 'Go to College',
            'P': 'Owns Property',
            'B': 'Owns Business',
            'Y': 'Yes',
            'N': 'No',
            ' ': 'Not provided',
        }

        return ['Residency Information - continued:', '',
                '4. If you are not a U.S. Citizen or U.S. Permanent Resident, are you a foreign national',
                'here with a visa eligible to domicile in the United States or are you a Refugee, Asylee,',
                'Parolee or here under Temporary Protective Status? If so, indicate which:', 
                f'{start}', '',
                '5. Do you currently live in Texas?',
                _syntax.get(_list[0], _list[0]), '',
                '6. If you currently live in Texas:',
                '(a) How long have you been living here?', 
                f'{_list[1]}{_list[2]} Years {_list[3]}{_list[4]} Months', '',
                '(b) What is your main purpose for being in the state?', 
                _syntax.get(_list[5], _list[5]), '',
                '7. If you are a member of the U.S. military:',
                '(a) Is Texas your Home of Record?', 
                _syntax.get(_list[6], _list[6]), '',
                '(b) What state is listed as your military legal residence for tax purposes on your Leave', 
                'and Earnings Statment', 
                f'{_list[7]}{_list[8]}', '',
                '8. Do any of the following apply to you?', 
                '(a) Do you hold the title (Warranty Deed, Deed of Trust, or other similar instrument that', 
                'is effective to hold title) to residential real property in Texas?', 
                f'{_syntax.get(_list[9], _list[9])} - acquired: {_list[14]}{_list[15]}/{_list[10]}{_list[11]}{_list[12]}{_list[13]}', '',
                '(b) Do you have ownership interest and customarily manage a business in Texas without the',
                'intention of liquidation in the foreseeable future?', 
                _syntax.get(_list[16], _list[16]), '',
                '9. For the past 12 months', 
                '(a) Have you been gainfully employed in Texas?', 
                _syntax.get(_list[31], _list[31]), '',
                '(b) Have you recieved primary support from a social service agency?', 
                _syntax.get(_list[37], _list[37]), '',
                '10. Are you married to a person who could claim YES to any part of question 8 or 9?', 
                _syntax.get(_list[30], _list[30]), '',
                '(a) If yes, indicate which question could be answered YES by your spouse:', 
                _syntax.get(_list[32], _list[32]), '',
                '(b) How long have you been married to the Texas Resident?', 
                f'{_list[33]}{_list[34]} Years {_list[35]}{_list[36]} Months', '']

    def RES_GUAR(self) -> list:

        if self.target[3] != 'RES: GUAR':
            return

        _str = str(self.target[-1]).strip()
        _list = list(_str)
        
        if len(_list) == 36:
            return
        
        _syntax = {
            'H': 'Establish/Maintain a home',
            'W': 'Work Assignment',
            'E': 'Gainfully Employed',
            'C': 'Go to College',
            'P': 'Owns Property',
            'B': 'Owns Business',
            'Y': 'Yes',
            'N': 'No',
            ' ': 'Not provided',
            '0': ' '
        }

        return ['Residency Information - continued:', '',
                '1. Is the parent or legal guardian upon whom you base your claim of residency a U.S.',
                'Citizen?', _syntax.get(_list[0], _list[0]), '',
                '2. If no, does the parent or legal guardian upopn whom you base your claim residency',
                'hold Permanent Residence Status (valid I-551) for the U.S.?', _syntax.get(_list[1], _list[1]), '',
                '3. Is this parent or legal guardian a foreign national whose application for Permanent',
                'Resident Status has been preliminarily reviewed?', _syntax.get(_list[2], _list[2]), '',
                '4. is this parent or legal guardian a foreign national here with a visa eligible to',
                'domicile in the United States or are you a Refugee, Asylee, Parolee or here under',
                'Temporary Protective Status? If so, indicate which:', _syntax.get(_list[3], _list[3]), '',
                '5. Does this parent or legal guardian currently live in Texas?', _syntax.get(_list[36], _list[36]), '',
                '6. If your parent or legal guardian currently live in Texas:', '',
                '(a) How long has he or she been living here?', f'{_list[39]}{_list[40]} Months; {_list[37]}{_list[38]} Years', '',
                "(b) What is your parent's or legal guardian's main purpose for being in the state?", _syntax.get(_list[41], _list[41]), '',
                '7. If your parent or legal guardian is a member of the U.S. military:', '',
                '(a) Is Texas his or her Home of Record?', f'{_syntax.get(_list[42], _list[42])}', '',
                '(b) What state is listed as his or her military legal residence for tax purposes on his or',
                'her Leave and Earnings Statement?', f'{_list[43]}{_list[44]}', '',
                '8. Do any of the following apply ot your parent or legal guardian?', '',
                '(a) Does your parent or legal guardian hold the title (Warranty Deed, Deed of Trust, or',
                'other similar instrument that is effective to hold title) to residential real property in',
                'Texas?', f'{_syntax.get(_list[45], _list[45])} - {_list[50]}{_list[51]}/{_list[46]}{_list[47]}{_list[48]}{_list[49]}', '',
                '(b) Does your parent or legal guardian have ownership interest and customarily manage a',
                'business in Texas without the intention of liquidation in the foreseeable future?', _syntax.get(_list[52], _list[52]), '',
                '9. For the past 12 months', '',
                '(a) Has your parent or legal guardian been gainfully employed in Texas?', _syntax.get(_list[66], _list[66]), '',
                '(b) Has your parent or legal guardian received primary support from a social service',
                'agency?', _syntax.get(_list[-1], _list[-1]), '',
                '10. Is your parent or legal guardian married to a person who could claim "yes" to any part',
                'of question (8) or (9)?', _syntax.get(_list[67], _list[67]), '',
                '(a) If yes, indicate which question could be answered "yes" by your parent or legal',
                "guardian's spouse:", _syntax.get(_list[68], _list[68]), '',
                '(b) How long has your parent or legal guardian been married to the Texas Resident?', f'{_list[71]}{_list[72]} Months; {_list[69]}{_list[70]} Years', '']

    def FORMER_STUDENT(self) -> list:

        if self.target[3] != 'FORMER STUDENT':
            return
        
        return ['Are you a former student of this institution?', 
                f'{self._syntax.get(self.target[-1][-2], self.target[-1][-2])}', '',
                'Have you previously applied?',
                f'{self._syntax.get(self.target[-1][-1], self.target[-1][-1])}', '']
    
    def ULTIMATE_DEGREE_SOUGHT(self) -> list:

        if self.target[3] != 'ULTIMATE DEGREE SOUGHT':
            return
        
        _syntax = {
            '4.2': 'Masters (M.)',
            '4.4': 'Doctoral (PhD)'
        }

        return ['Ultimate Degree Sought:', f'{_syntax.get(self.target[-1], self.target[-1])}', '']

    def CTRY_SELF(self) -> list:

        if self.target[3] != 'CTRY SELF':
            return
        
        _list = core.Process().process_str_with_blank(self.target[-1])
        
        if _list[0] == '':
            return ['Of what country are you a citizen?', _list[-1], '',
                    f'Country of legal Permanent Residence: {_list[-1]}', ''] 

        return ['Of what country are you a citizen?', _list[0], '',
                f'Country of legal Permanent Residence: {_list[1]}', '']

    def PAYMENT_RECONCILIATION(self) -> list:

        if self.target[3] != 'PAYMENT RECONCILIATION':
            return

        target = self.target[-1]

        return ["Application Fee Information:",
                f"Transcation Time: {target[0:4]}-{target[4:6]}-{target[6:8]} {target[8:10]}:{target[10:12]}:{target[12:14]}",
                f"Payment Status: {target[15:19]}",
                f"Payment Amount: ${target[22:24]}",
                f"Transcation Trace: {target[24:36]}",
                f"Customer Reference: {target[36:48]}",
                f"Card Type: {target[48]}",
                f"Last 4 digit card number: {target[49:53]}",
                f"Card Expiration Date: {target[53:55]}/{target[55:57]}", '']
    
    def VET_STATUS(self) -> list:

        if self.target[3] != 'VET STATUS':
            return
        
        _list = []

        _syntax = {
            '1': 'Veteran',
            '2': 'Current US Miliary Service Member',
            '3': 'Spouse or Dependen of Veteran or Current Service Member',
            '4': 'Spouce or dependent of, or a veteran or current U.S. military servicemember with injury or illness', 
            '4+': 'resulting from military service (service-connected injury/illness)',
            '5': 'Spouse or dependent of deceased US servicemember'
        }

        status = self.target[-1]

        for item in status:
            _list.append(_syntax.get(item, item))
            if item == '4':
                _list.append(_syntax.get('4+', '4+'))

        return _list.append('')
    
    def OTHER_NAME(self) -> list:
        
        if len(self.target) != 6:
            return

        for idx, char in enumerate(self.target[3]):
            if char == 'N':
                stop = idx
                break

        return [f'{self.target[3][:stop]}: {self.target[-1]}']