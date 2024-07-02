import core

class Structure:

    def __init__(self, _list: list, idx: int):
        """Structure Class handles all methods related to initially translating markdown text into a readable
        format. Several class list are initialized for the purpose of holding final (self.output) and current
        (self.markdown) translations, as well as, tracking line by line inputs (self.target). Class variables
        hold a check flag for later return separations and student name capturing. 

        :param _list: list of lines captured from the selected .spe file
        :type _list: list
        :param idx: current nested list's idx
        :type idx: int
        """
        self._list = _list
        self.idx = idx

        self.target = []
        self.output = []
        self.markdown = []

        self.student_idx = 0
        self.semester_check = 0

        self.current_idx = 0
        self.post_check = 0
        self.tst_check = 0
        self.crs_check = 0
        self.xtra_check = {
            'NZZ': 0,
            'OZZ': 0,
            'RZZ': 0,
            'QZZ': 0
        }
        self.cur_college_crs_check = 0
        self.res_comments_check = 0

    def error_handler(self, markdown: str, text: str) -> None:
        """Class error handler for missing translations found at any given
        method.

        :param markdown: Method's designated markdown translation
        :type markdown: str
        :param text: flag indicator to invoke ReferenceError
        :type text: str
        :raises ReferenceError: Returns the method along with the inputted line and student name where error occurrd.
        """
        
        if text == 'Other':
            r = core.Report([self.output])
            r.capture_student_name()
            raise ReferenceError(f'{markdown} translation missing in structure: {self.target}, {self.idx}, {r.student_name}')

    def translate(self) -> list:
        """Main method created to handle translation distrubtion amongst the rest of the created
        methods.

        :return: final list of translated values
        :rtype: list
        """

        for idx, item in enumerate(self._list):
            self.target = str(item).split('!')
            self.current_idx = idx

            self.target[-1] = str(self.target[-1]).replace('\\', '')

            _translate = {
                'ATV': self.translate_ATV(),
                'BGN': "********** START OF APPLICATION **********",
                'COM': self.translate_COM(),
                'CRS': self.translate_CRS(),
                'DEG': self.translate_DEG(),
                'DMG': self.translate_DMG(),
                'DTP': self.translate_DTP(),
                'FOS': self.translate_FOS(),
                'IN1': self.translate_IN1(idx),
                'IN2': self.translate_IN2(),
                'IND': self.translate_IND(),
                'MSG': self.translate_MSG(),
                'N1': self.translate_N1(),
                'N3': self.translate_N3_N4(),
                'N4': self.translate_N3_N4(),
                'NTE': self.translate_NTE(),
                'PCL': self.translate_PCL(),
                'REF': self.translate_REF(),
                'RQS': self.translate_RQS(),
                'MSG': self.translate_MSG(),
                'SE': "********** END OF APPLICATION **********",
                'SES': self.translate_SES(),
                'SSE': self.translate_SSE(),
                'SST': self.translate_SST(),
                'SUM': self.translate_SUM(),
                'TST': self.translate_TST(),
                'LUI': None,
                'GE': None,
                'IEA': None,
                'ISA': None,
                'GS': None,
                'SBT': None,
                'SRE': None,
                }
            
            result = _translate.get(self.target[0], 'Other')
            self.error_handler('Translate', result)
            self.output.append(result)
            self.markdown.append(self.target[0])

        return self.output

    def translate_ATV(self) -> list:
        """Method for ATV markdown text: EXtra Curricular, Community, Employment, and Honor information.

        :return: translated list
        :rtype: list
        """
        
        if self.target[0] != 'ATV':
            return
        
        _list = []

        _translate = {
            'NZZ': 'Extra Curricular Activite(s):',
            'OZZ': 'Community or Volunteer Service:',
            'RZZ': 'Employment/Internships/Summer Activities:',
            'QZZ': 'Honor/Award/Achievement(s):'
        }

        translate = _translate.get(self.target[2], 'Other')
        self.error_handler('ATV', translate)

        if self.xtra_check[self.target[2]] == 0:
            self.xtra_check[self.target[2]] = 1
            _list.append('')
            _list.append(translate)

        _list.append(f'\t{self.target[3:4]} {self.target[-1]}')

        return _list
    
    def translate_COM(self) -> str:
        """Method for COM markdown text: Email and Phone information.

        :return: translated string
        :rtype: str
        """

        if self.target[0] != 'COM':
            return
        
        sep = self.target[1]

        _translate = {
            'EM': 'Email Address',
            'TE': 'Telephone',
            'AP': 'Preferred'
        }

        trans_prefix = _translate.get(sep, "Other")
        self.error_handler('COM', trans_prefix)
        sep = str(self.target[-1]).split(' ')

        while ("" in sep):
            sep.remove("")

        if len(sep) < 1:
            return

        _translate = {
            'CP': 'Cell Phone',
            'HP': 'Home Phone',
            'WP': 'Work Phone',
            'P': 'Preferred'
        }

        trans_suffix = _translate.get(sep[-1], sep[-1])
        self.error_handler('COM', trans_suffix)

        if len(sep) >= 2:
            return f'{trans_prefix}: {sep[:-1]} {trans_suffix}'
        elif sep[0] == 'P' or sep[0] == '':
            return
    
        return f'{trans_prefix}: {sep}'
        
    def translate_CRS(self) -> str:
        """Method for CRS markdown text: Course information.

        :return: translated string
        :rtype: str
        """

        if self.target[0] != 'CRS':
            return

        _list = []

        if self.target[2] == 'U':
            if self.crs_check == 0:
                self.crs_check = 1
                _list = ['', '4. Please list exact titles of courses to be completed your senior year and the number of',
                         'credits you will earn for each. Include college coursework you will complete your senior',
                         'year.', '', 
                         'AP|Sem(s) or                               Dual Cred/',
                         'IB|Tri(s)                                  Concurrrent',
                         '  1|2   Senior Courses                     Enrollment',
                         self.target[-1]]
            else:
                _list.append(self.target[-1])
        else:
            if self.crs_check == 0:
                self.crs_check = 1
                _list = ['', '4. Please list the college or university courses you are currently enrolled in and courses',
                         'you anticipate completing before you transfer.', '',
                         ' '.join(self.target[3:])]
            else:
                _list.append(' '.join(self.target[3:]))
        
        return _list
    
    def translate_DEG(self) -> str:
        """Method for DEG markdown text: Previous Degree and Major information.

        :return: translated string
        :rtype: str
        """

        if self.target[0] != 'DEG':
            return
        
        _translate = {
            '2.2': 'Certificate:',
            '2.3': 'Compeleted:',
            '2.4': 'Major:',
            '3.1': 'Degree: Professional',
            '4.1': 'No Degree',
            '4.2': 'Degree: Masters (M.)',
            '4.4': 'Degree: Doctoral (PhD)',
        }

        if len(self.target) == 2:
            translate = _translate.get(self.target[-1], "Other")
            self.error_handler('DEG', translate)
            return f'{translate}'
        else:
            translate = _translate.get(self.target[1], 'Other')
            self.error_handler('DEG', translate)
            return f'{translate} {self.target[-1]}'
        
    def translate_DMG(self) -> str:
        """Method for DMG markdown text: Date of Birth and Gender information.

        :return: translated string
        :rtype: str
        """

        if self.target[0] != 'DMG':
            return
        
        dob = f'{self.target[2][4:6]}-{self.target[2][6:8]}-{self.target[2][:4]}'

        _translate = {
            'M': 'Male',
            'F': 'Female',
            'U': 'Prefer not to say'
        }

        if len(self.target) > 3:
            gender = _translate.get(self.target[3], "Other")
            self.error_handler('DMG', gender)
        else:
            gender = 'N\A'

        return f'Date of Birth: {dob} Gender={gender}'
    
    def translate_DTP(self) -> str:
        """Method for DTP markdown text: Date and Time information.

        :return: translated string
        :rtype: str
        """

        if self.target[0] != 'DTP':
            return
        
        date = str(self.target[-1]).replace('\\', '')
        
        _translate = {
            '196': 'Start',
            '197': 'End',
            '102': 'Issued',
            '036': 'If an expiration date is indicated on you form I-94, please enter it'
        }

        sep = _translate.get(self.target[1], 'Other')
        self.error_handler('DTP', sep)

        if sep == 'Issued':
            return f'{sep}: {date[4:6]}-{date[6:8]}-{date[:4]}'
        else:
            return f'{sep}: {date[4:6]}-{date[:4]}'
        
    def translate_FOS(self) -> str:
        """Method for FOS markdown text: Application Major and Interest information.

        :return: translated string [moves Major up for clearer presentation]
        :rtype: str
        """

        if self.target[0] != 'FOS':
            return

        _translate = {
            'M': 'Major',
            'C': 'Interest'
        }

        sep = _translate.get(self.target[1], "Other")
        self.error_handler('FOS', sep)
        
        if sep == 'Major':
            return self.output.insert(self.student_idx+2, f'{sep}: [{self.target[3]}] {self.target[-1]}')
        else:
            return f'{sep}: {self.target[-1]}'
        
    def translate_IN1(self, idx: int) -> list:
        """Method for IN1 markdown text: Student and Emergency Contact information.

        :param idx:: current idx [for later student name capturing]
        :param type: int
        :return: translated list
        :rtype: list
        """

        if self.target[0] != 'IN1':
            return
        
        _translate = {
            '02': 'Student Contact:',
            '04': 'Emergency Contact:'
        }

        contact = _translate.get(self.target[2], "Other")
        self.error_handler('IN1', contact)

        if contact == 'Student Contact:':
            self.student_idx = idx

        _translate = {
            'PG1': 'Parent Guardian 1',
            'PG2': 'Parent Guardian 2',
            '': ''
        }

        contact_type = _translate.get(self.target[3], "Other")
        self.error_handler('IN1', contact_type)

        if contact_type == '':
            if int(self.target[-1]) < 30 and contact != 'Student Contact:':
                return ['', f'{contact} Child {int(self.target[-1])}']
            return ['', f'{contact}']
        else:
            return ['', f'{contact} {contact_type}']
        
    def translate_IN2(self) -> str:
        """Method for IN2 markdown text: Name information.

        :return: translated string
        :rtype: str
        """

        if self.target[0] != 'IN2':
            return
        
        _translate = {
            '02': 'First',
            '03': 'Middle',
            '05': 'Last',
            '07': 'Initial',
            '09': 'Suffix',
            '18': 'Nickname',
            '01': 'Marital Status',
            '16': "Representative Name",
        }

        sep = _translate.get(self.target[1], "Other")
        self.error_handler('IN2', sep)

        if len(self.target) != 2:
            if sep == 'Suffix':
                return f'{sep}: {self.target[-1].upper()}'
            return f'{sep}: {self.target[-1]}'
        return
    
    def translate_IND(self) -> str:
        """Method for IND markdown text: Place of Birth and Country/City information.

        :return: translated string
        :rtype: str
        """

        if self.target[0] != 'IND':
            return

        pob = self.target[1:]
        
        while ("" in pob):
            pob.remove("")

        pob = ' '.join(pob)

        return f'Place of Birth: {pob[:2]}, Country/City: {pob[2:]}'
        
    def translate_N1(self) -> str:
        """Method for N1 markdown text: Header or Subject Text information.

        :return: translated string
        :rtype: str
        """

        if self.target[0] != 'N1':
            return
        
        _translate = {
            'TM': 'ApplyTexas Appication',
            'AT': 'Date',
            'HS': 'High School Info:'
        }

        sep = _translate.get(self.target[1], "Other")
        self.error_handler('N1', sep)

        last = str(self.target[-1]).replace('\\', '')

        if sep == 'High School Info:':
            return f'{sep}: {self.target[2]} {last}'
        elif sep == 'Date':
            return f'{sep}: {last}'
        else:
            return f'{sep}'
        
    def translate_N3_N4(self) -> str:
        """Method for N3 and N4 markdown text: Address information.

        :return: translated string
        :rtype: str
        """

        if self.target[0] != 'N3' and self.target[0] != 'N4':
            return

        while ("" in self.target):
            self.target.remove("")

        _translate = {
            'L': 'Local',
            'P': 'Personal',
        }

        self.target[-1] = _translate.get(self.target[-1], self.target[-1])

        address = ', '.join(self.target[1:])

        if address == '':
            return

        if self.target[0] == 'N4':
            return f'Primary Address: {address}'
        else:
            return f'Secondary Address: {address}'
        
    def translate_NTE(self) -> list:
        """Method for NTE markdown text: Ethnicity and Race information.

        :return: translated list
        :rtype: list
        """

        if self.target[0] != 'NTE':
            return
        
        split = str(self.target[-1]).split(';')
        
        ethnicity = str(split[0]).split('=')

        _translate = {
            '': 'N\A',
            'W': 'Not Hispanic or Latino',
            'R': 'Hispanic or Latino',
            'S': 'White',
            'T': 'American Indian or White',
            'Q': 'Black or African American',
            'U': 'Asian',
            'V': 'Native Hawaiian or Other Pacific Islander'
        }

        ethnicity[-1] = _translate.get(ethnicity[-1], ethnicity)

        if len(split) == 1:
            return [f'{ethnicity[0]}={ethnicity[-1]}.']

        else:
            race_str = ''

            race = str(split[-1]).split('=')

            _translate = {
                'S': 'White',
                'T': 'American Indian or White',
                'Q': 'Black or African American',
                'U': 'Asian',
                'V': 'Native Hawaiian or Other Pacific Islander'
            }

            for item in race[-1]:
                if len(race[-1]) > 1:
                    race_str += f'{_translate.get(item, "Other")}, '
                else: 
                    race_str += _translate.get(item, 'Other')

            race[-1] = race_str

            return [f'{ethnicity[0]}={ethnicity[-1]}.', f'{race[0]}={race[-1]}']
        
    def translate_PCL(self) -> list:
        """Method for PCL markdown text: College information.

        :return: translated list
        :rtype: list
        """

        if self.target[0] != 'PCL':
            return 

        institution = str(self.target[-1]).replace('\\', '')
        code = self.target[2]
        dates = f'{self.target[4][:4]}/{self.target[4][4:6]}{self.target[4][6]}{self.target[4][7:11]}/{self.target[4][11:]}'

        if self.post_check == 0:
            self.post_check = 1
            return ['', '4. Please list ALL post-secondary colleges or universities you have previously attended or',
                    'are presently attending, including for extension, correspondence, and distance learning',
                    'credit, starting with the most recent. Failure to list all institutions will be considered',
                    'an intentional omission an may lead to forced withdrawal.', '',
                    f'Name of Insitition: {institution}', 
                    f'Code: {code}', 
                    f'Dates Attended: {dates}']
        
        return ['', f'Name of Insitition: {institution}', 
                f'Code: {code}', 
                f'Dates Attended: {dates}']
    
    def translate_REF(self) -> str:
        """Method for REF markdown text: Important Person/App Specific information.

        :return: translated string
        :rtype: str
        """

        if self.target[0] != 'REF':
            return

        _translate = {
            '48': 'App ID',
            'SY': 'SSN Info',
            'V2': 'F-1 status',
            'PSM': 'Previous App',
            'ZZ': 'Premanent Residence status'
        }

        ref = _translate.get(self.target[1], "Other")
        self.error_handler('REF', ref)


        _tranlsate = {
            'FFRESHMAN APPLICATION ID': 'U.S. Freshman Admission',
            'IFOREIGN GRAD APPLICATION ID': 'Interanational Graduate Admission',
            'CREENTRY UNDERGRAD APPLICATION ID': 'U.S. Re-Entry Admission',
            'GUS GRAD APPLICATION ID': 'U.S. Graduate Admission',
            'TUS TRANSFER APPLICATION ID': 'U.S. Transfer Admission',
            'AFOREIGN TRANSFER APPLICATION ID': 'International Transfer Admission',
            'BFOREIGN FRESHMAN APPLICATION ID': 'International Freshman Admission',
            'SUS TRANSIENT APPLICATION ID': 'Transient Admission',
        }

        final = str(self.target[-1]).replace('\\', '')
        app = _tranlsate.get(final, final)

        return f'{ref}: {self.target[2]}| {app}'
    
    def translate_RQS(self) -> list:
        """Method for RQS markdown text: Sevearl Unique Reqeust/Answer type information.

        :return: translated list
        :rtype: list
        """

        if self.target[0] != 'RQS':
            return
        
        s = core.Syntax(self.target)

        if str(self.target[3]).startswith('$ '):
            return self.target[-1]
        elif str(self.target[3]).startswith('PRE-PROFESSIONAL'):
            return s.PRE_PROFESSIONAL()
        elif str(self.target[3]).startswith('OTHER'):
            return s.OTHER_NAME()
        
        if self.target[3] == 'APP SUBMIT/TRANSMIT':
            return self.output.insert(2, ['', self.target[-1], ''])
        
        if self.target[3] == 'CUR COLLEGE CRS':
            if self.cur_college_crs_check == 0:
                self.cur_college_crs_check = 1
                return ['6. List courses to be completed during the present semester (if applicable). If you will',
                         'complete an additional term before enrolling at Texas A&M University-Kingsville (TAMKI),',
                         'list those courses also. If you need to list more than 10 courses, please send a list',
                         'directly to the graduate admissions office at Texas A&M University-Kingsville (TAMKI). Be',
                         'sure to include your full name, application ID number and date of birth on any documents',
                         'you send to the admissions office.', 
                         self.target[-1], '']
            return [self.target[-1], '']
        
        if self.target[3] == 'RES: COMMENTS':
            if self.target[-1] == 'RES: COMMENTS':
                self.res_comments_check = 1
                return ['General Comments:',
                        'Is there any additional information that you believe your college should know in',
                        'evaluating your eligibility to be classified as a resident? If so, please provide it',
                        'below.']
            if self.res_comments_check == 0:
                self.res_comments_check = 1
                return ['General Comments:',
                        'Is there any additional information that you believe your college should know in',
                        'evaluating your eligibility to be classified as a resident? If so, please provide it',
                        'below.',
                         self.target[-1]]
            return [self.target[-1]]
        
        basic_output = s._syntax.get(self.target[-1], self.target[-1])
        
        _translate = {
            'APP SUBMIT/TRANSMIT': None,
            'PERM COUNTRY INFO': [f'Permanent Country Info--{self.target[-1]}'],
            'PERM COUNTY INFO': ['', f'Permanent County Info--{self.target[-1][3:]} (Country code = {self.target[-1][:3]})'],
            'PERM ADDR STND': [f'Mailing/Permanent Address Standardized: {basic_output}'],
            'CURR COUNTY INFO': [f'Current County Info-{self.target[-1]}'],
            'CURR COUNTRY INFO': [f'Current Country Info: {self.target[-1]}'],
            'PHYS ADDR STND': [f'Physical Address Standardized: {basic_output}'],
            'FERPA CERT SWITCH': s.CERT_SWITCH(),
            'MENINGITIS CERT SWITCH': s.CERT_SWITCH(),
            'TRUTH CERT SWITCH': s.CERT_SWITCH(),
            'RESUME CERT SWITCH': s.CERT_SWITCH(),
            'CONSERVATORSHIP SWITCHES': s.CONSERVATORSHIP_SWITCHES(),
            'HS GED TYPE': s.HS_GED_TYPE(),
            'PARENT OR GUARDIAN INFO': None,
            'PARENT 1 ED LEVEL RELATIONSHIP': None,
            'PARENT 2 ED LEVEL RELATIONSHIP': None,
            'CURRENT ACADEMIC SUSP': ['5. Are you currently on academic suspension from the last college or univeristy attended?',
                                      f'{basic_output}', ''],
            'RES: PREVIOUS ENROLLMENT': s.RES_PREVIOUS_ENROLLMENT(),
            'RES: BASIS OF CLAIM': s.RES_BASIS_OF_CLAIM(),
            'RES: DETERM': s.RES_DETERM(),
            'RES: RESIDENCY CLAIM': s.RES_RESIDENCY_CLAIM(),
            'RES: HS DIPLOMA OR GED': s.RES_HS_DIPLOMA_OR_GED(),
            'RES: COMMENTS': None,
            'RES: SELF': s.RES_SELF(),
            'RES: GUAR': s.RES_GUAR(),
            'TEST1 SENT': None,
            'TEST2 SENT': None,
            'FAMILY': None,
            'CONTACT AT WORK': None,
            'REVERSE TRANSFER': None,
            'APPLICATION SHARING': [f'Application sharing on denied admission {basic_output}'],
            'TREX TRANSCRIPT REQUESTED': [f'Transcript sharing consent {basic_output}'],
            'COLLEGE WORK': s.COLLEGE_WORK(),
            'FORMER STUDENT': s.FORMER_STUDENT(),
            'ALIEN APP/INT': None,
            'PHI THETA KAPPA': ['Are you a Phi Theta Kappa?', 
                                basic_output, ''],
            'ULTIMATE DEGREE SOUGHT': s.ULTIMATE_DEGREE_SOUGHT(),
            'COLLEGE WORK IN CLASSROOM': None,
            'CTRY SELF': s.CTRY_SELF(),
            'HOME SCHOOLED': ['Home Schooled?', 
                              basic_output, ''],
            'IB DIPLOMA': ['', 'IB Diploma?', 
                           basic_output],
            'RESUME SWITCH': ['Resume?', 
                              basic_output],
            'COUNSELOR OPT IN': ['Opt-In for Counsler?',
                                 basic_output, ''],
            'FAMILY OBLIGATION INCOME': None,
            'FAMILY OBLIGATION CARE': None,
            'FAMILY OBLIGATION OTHER': None,
            'FAMILY OBLIGATIONS': ['Do you have family obligations that keep you from participating in extracurricular activities?', 
                                   basic_output, ''],
            'DUAL CREDIT': ['', 'Are you applyting to take college courses to be completed while you are still', 
                            'a high school student (Dual Credit or Concurrent Enrollment)?',
                            basic_output, ''],
            'GRADUATE AWARD': None,
            'FUNDS SUPPORT': ["Do you have a source of financial suppport if your are, or will be, in F-1 or J-1 status?"],
            'SPOKEN LANGUAGES': None,
            'NATIVE LANGUAGE': None,
            'TEACHING CERTIFICATE TYPE': [f'Will you seek Teacher Certification? Yes--{self.target[-1]}', ''],
            'APP TYPE INFO': [f'You are applying as a/an TRANSFER. Total hours earned: {self.target[-1][8:11]}', ''],
            'PAYMENT RECONCILIATION': s.PAYMENT_RECONCILIATION(),
            'AUTO TRANSFER ADM': [f'Automatic Admission for Transfer Applicants Based on Texas Law: {basic_output}'],
            'INT CURR RESIDE IN US': ['Are you currently residing in the U.S.?',
                                      basic_output, ''],
            'VET STATUS': s.VET_STATUS(),
            'CTRY SPOUSE': None, # [f"Spouse's Country (Code): ({self.target[-1][:3]}) {self.target[-1][3:]}"],
            'CTRY CHILD': None, # [f"Child's Country (Code): ({self.target[-1][:3]}) {self.target[-1][3:]}"],
            'CUR COLLEGE ATT': ['5. Name of Institution Presently Attending:', 
                                self.target[-1], ''],
            'CUR COLLEGE CRS': None,
            'INTL EXIT US': ['If you are already in the U.S., do you plan to leave the U.S. before enrolling at the',
                             'university to which you are applying?', 
                             basic_output, ''],
            'EMERGENCY CONTACT HAS NO PHONE': ['Applicant has indicated this emergency contact does not have a phone.'],
            'INT VISA STATUS CHANGE': [f'Will you require a change in your visa stauts?', 
                                       basic_output, ''],
            'OPTIONAL MODULES': None
        }

        output = _translate.get(self.target[3], 'Other')

        self.error_handler('RQS', output)

        return output
    
    def translate_MSG(self) -> list:
        """Method for MSG markdown text: Several Short Message information.

        :return: translated list
        :rtype: list
        """

        if self.target[0] != 'MSG':
            return

        _list = []

        if self.target[-1] in ['AT', 'DS']:
            for idx, items in enumerate(self.target):
                if idx != 0 and idx != len(self.target)-1:
                    _list.append(items)

                    if self.target[-1] == 'DS':
                        _list.append('')
        elif len(self.target) == 2 and len(self.target[1]) <= 31:
            if (self.target[-1]  != 'NO RESIDENCY COMMENTS INCLUDED'):
                s = core.Syntax(None)
                _list.append(s._syntax.get(self.target[-1] , self.target[-1] ))
                _list.append('')
        else:
            temp = ''
            prev_char = [0, 0]

            for idx, char in enumerate(self.target[-1] ):
                temp += char
                prev_char[idx%2] = char

                if str(prev_char[0]).isspace() and str(prev_char[1]).isspace():
                    if not str(temp[0]).isspace():
                        _list.append(str(temp).strip())
                    temp = ''

            if temp:
                return [self.target[-1], '']

            _list.insert(0, '9. Mailing/Permanent Address:')
            _list.append('')

        return _list
    
    def translate_SES(self) -> str:
        """Method for SES markdown text: Specific Date Formatting or Degree information.

        :return: translated string
        :rtype: str
        """

        if self.target[0] != 'SES':
            return

        if len(self.target[1]) == 6:
            date = f'{self.target[1][4:]}/{self.target[1][:4]}'
        else:
            date = f'{self.target[1][4:6]}/{self.target[1][6:]}/{self.target[1][:4]}'
        
        if len(self.target) == 2:
            return f'Date: {date}'
        elif len(self.target) == 6:
            return f'Date: {date}, {self.target[-1]}'
        else:
            return f'Date: {date}, Degree: {self.target[-1]}'
        
    def translate_SSE(self) -> str:
        """Method for SSE markdown text: Semester and Date information.

        :return: translated string [moved Semester info up for better structure]
        :rtype: str
        """

        if self.target[0] != 'SSE':
            return

        _translate = {
            '0901': 'Fall',
            '0601': 'Spring',
            '0101': 'Spring'
        }

        if len(self.target) == 2:
            sep = _translate.get(self.target[-1][4:], self.target[-1][4:])
            if self.semester_check == 0:
                self.semester_check = 1
                self.output.insert(self.student_idx, f'{sep} {self.target[-1][:4]}')
                return self.output.insert(self.student_idx, '')
            return f'{sep} {self.target[-1][:4]}'
        elif self.target[-1] == 'ZZZ':
            return f'(Attendance dates: {self.target[1][4:6]}/{self.target[1][:4]} - {self.target[2][4:6]}/{self.target[2][:4]})'
        
    def translate_SST(self) -> list:
        """Method for SST markdown text: Graduation Date information.

        :return: translated list
        :rtype: lisr
        """

        if self.target[0] != 'SST':
            return
        
        if self.target[1] == 'ZZZ':
            return

        return ['Expected Graduation Date:', f'{self.target[-1][4:]}/{self.target[-1][:4]}', '']
    
    def translate_SUM(self) -> str:
        """Method for SUM markdown text: Hours Earned information.

        :return: translated string
        :rtype: str
        """

        if self.target[0] != 'SUM':
            return
        
        return f'Hours Earned {self.target[-1]}'
    
    def translate_TST(self) -> list:
        """Method for TST markdown text: Test (ACT/SAT) information.

        :return: translated list
        :rtype: list
        """

        if self.target[0] != 'TST':
            return
        
        _list = []
        
        if self.tst_check == 0:
            self.tst_check = 1
            _list.append('1. Admissions Tests')
        _list.append(f'{self.target[2]}:')
        _list.append(f'Checked -- Date taken/plan to take: {self.target[-1][4:]}/{self.target[-1][:4]}')

        return _list.append('')
    