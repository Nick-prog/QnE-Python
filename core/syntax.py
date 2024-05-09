import core
import re

class Syntax:

    def __init__(self):
        """Class created to house methods for in-place replacement text of varying types of markdown text in the
        form of a list.
        """

        self.p = core.Process()

    def payment_syntax(self, _list: list) -> list:
        """Text fully listing the question given for payment information from students
        on ApplyTexas.

        :param _list: list of designated markdown text
        :type _list: list
        :return: list of strings to display the proper output
        :rtype: list
        """

        if _list[3] != 'PAYMENT RECONCILIATION':
            return

        target = _list[-1]

        return [f"Transcation Time: {target[0:4]}-{target[4:6]}-{target[6:8]} {target[8:10]}:{target[10:12]}:{target[12:14]}",
                f"Payment Status: {target[15:19]}",
                f"Payment Amount: ${target[22:24]}",
                f"Transcation Trace: {target[24:36]}",
                f"Customer Reference: {target[36:48]}",
                f"Card Type: {target[48]}",
                f"Last 4 digit card number: {target[49:53]}",
                f"Card Expiration Date: {target[53:55]}/{target[55:57]}", '']
    
    def hs_diploma_syntax(self, _list: list) -> list:
        """Text fully listing the question given for HS Diploma information including
        some Residency information from students on ApplyTexas.

        :param _list: list of designated markdown text
        :type _list: list
        :return: list of strings to display the proper output
        :rtype: list
        """

        if _list[3] != 'RES: HS DIPLOMA OR GED':
            return
        
        diploma = {
            'N': 'No',
            'Y': 'Yes',
            'K': 'Not provided'
        }

        target = "".join(_list[-1]).translate(str.maketrans("", "", "\\0"))
        target = str(target).split(" ")
        
        output = self.p.process_list(target)

        if len(output) == 2:
            output.append('KK')

        while len(output[-1]) != 2:
            output[-1] += 'K'

        val = output[-1]
        del(output[-1])
        output.append(val[0])
        output.append(val[1])

        for idx in range(len(output)):
            for key, value in diploma.items():
                if key == output[idx]:
                    output[idx] = value

        return [f'Previous High School Name: {output[0]}',
                f'Location: {output[1]}','',
                'Did you live or will you have lived in Texas the 36 months leading up',
                'to high school graduation or completion of the GED?', f'{output[2]}', '',
                'When you begin the semester for which you are applying, will you have lived',
                'in Texas for the previous 12 months?', f'{output[3]}']
    
    def hs_ged_syntax(self, _list: list) -> list:
        """Text fully listing the question given for HS GED information from students 
        on ApplyTexas.

        :param _list: list of designated markdown text
        :type _list: list
        :return: list of strings to display the proper output
        :rtype: list
        """

        if _list[3] != 'HS GED TYPE':
            return

        target = "".join(_list[4]).translate(str.maketrans("", "", "\\0"))

        target = target.replace('N', "No").replace('Y', "Yes")

        extra = str(_list[-1]).replace('\\', '')


        return ['3. If you did not graduate from high school, do you have a DEG or have you completed',
                'another high school equivalency program?',
                 f'{target}-{extra}', '']
    
    def prev_syntax(self, _list: list) -> list:
        """Text fully listing the question given from previous college information from
        students on ApplyTexas.

        :param _list: list of designated markdown text
        :type _list: list
        :return: list of strings to display the proper output
        :rtype: list
        """

        if _list[3] != 'RES: PREVIOUS ENROLLMENT':
            return
        
        end = 0

        output = self.p.process_str(_list[-1])

        if output[0] != 'N':

            if not str(output[-1][0]).isdigit():
                output[-1] = output[-1][1:]

            for idx in range(len(output)):
                for char in output[idx]:
                    if str(char).isdigit():
                        end_point = idx

            months_q = str(output[0]).replace('Y', 'Yes') 
            attend_q = " ".join(output[1:end_point])

            for i, char in enumerate(output[-1]):
                if '0' <= char <= '9':
                    end = i

            if end > 5:
                sem_start = str(output[-1][4]).replace('2', 'Spring').replace('9', 'Fall')
                sem_end = str(output[-1][9]).replace('2', 'Spring').replace('9', 'Fall')
                enrolled_q = f'{sem_start} {output[-1][:4]} - {sem_end} {output[-1][5:9]}'
            else:
                sem_start = str(output[-1][4]).replace('2', 'Spring').replace('9', 'Fall')
                sem_end = ''
                enrolled_q = f'{sem_start} {output[-1][:4]} - {sem_end}'

            resident_q_1 = str(output[-1][-2]).replace('R', 'Resident (In-state)').replace('U', 'Not provided')
            resident_q_2 = str(output[-1][-1]).replace('R', 'Resident (In-state)').replace('U', 'Not provided').replace('N', "Didn't pay in-state tution.")

            return ['Residency Information', '', '1. Residency Information', '',
                    'During the 12 months prior to you applying, did you register',
                    'for a public college or university in Texas?', f'{months_q}', '',
                    'What Texas public college or university did you last attend?',
                    f'{attend_q}', '',
                    'In which terms were you last enrolled?', f'{enrolled_q}', '',
                    'During you last seemster at a Texas public institution, did you pay resident (in-state)',
                    'or nonresident (out-of-state) tution?', f'{resident_q_1}', '',
                    'If you paid in-state tution at your last institution, was it because you were classified',
                    'as a resdient or because you were non-resident who received a wavier?', f'{resident_q_2}']

        return ['Residency Information', '', '1. Residency Information', '',
                'During the 12 months prior to you applying, did you register',
                'for a public college or university in Texas?', 'No']
    
    def basis_syntax(self, _list: list) -> list:
        """Text fully listing the question given from basis of claim information from
        students on ApplyTexas.

        :param _list: list of designated markdown text
        :type _list: list
        :return: list of strings to display the proper output
        :rtype: list
        """

        if _list[3] != 'RES: BASIS OF CLAIM':
            return


        if len(_list) > 4:
            target = "".join(_list[-1]).translate(str.maketrans("", "", "\\0"))
        else:
            target = "N\A"

        syntax = {
            'N': 'No',
            'Y': 'Yes',
            'P': 'Parent or Legal Guardian',
            'O': 'Other',
        }

        target = re.findall('[A-Z][^A-Z]*', target)
        
        for idx in range(len(target)):
            for key, value in syntax.items():
                if key == target[idx]:
                    target[idx] = value
        
        while len(target) < 3:
            target.append('N\A')

        target[2] = ", ".join(target[2:])

        return ['Do you file your own federal income tax as an independent tax payer?', f'{target[0]}', '',
                'Are you claimed as a dependent or are you eligible to be claimed as a dependent',
                'by a parent or court-appointed legal guardian?', f'{target[1]}', '',
                'Who provides the majority of your suppport?', f'{target[2]}']
    
    def comment_syntax(self) -> list:
        """Text fully listing the question given from resident comments information from
        students on ApplyTexas.

        :return: list of strings to display the proper output
        :rtype: list
        """

        return ['General Comments:',
                'Is there any additional information that you believe your college should know in', 
                'evaluating your eligibility to be classified as a resident? If so, please provide.']
    
    def dual_syntax(self, _list: list) -> list:
        """Text fully listing the question given from dual credit information from students
        on ApplyTexas.

        :param _list: list of designated markdown text
        :type _list: list
        :return: list of strings to display the proper output
        :rtype: list
        """

        if _list[3] != 'DUAL CREDIT':
            return

        target = "".join(_list[-1]).translate(str.maketrans("", "", "\\0"))
        
        target = target.replace('N', "No").replace('Y', "Yes")

        return ['Are you applyting to take college courses to be completed while you are still', 
                'a high school student (Dual Credit or Concurrent Enrollment)?',
                f'{target}']
    
    def conservator_syntax(self, _list: list) -> list:
        """Text fully listing the question given from conservator information from students
        on ApplyTexas.

        :param _list: list of designated markdown text
        :type _list: list
        :return: list of strings to display the proper output
        :rtype: list
        """

        if _list[3] != 'CONSERVATORSHIP SWITCHES':
            return

        target = self.p.process_str(_list[-1])

        syntax = {
            'N': 'No',
            'Y': 'Yes',
            'K': 'N\A'
        }

        if len(target) != 2:
            target.append('K')

        for idx in range(len(target)):
            for key, value in syntax.items():
                if key == target[idx]:
                    target[idx] = value

        return ['17. Texas Conservatorship:',
                'At anytime in your life were you placed in foster care or adopted from foster care in Texas?', 
                f'{target[0]}', '',
                'If admitted, would your like to receive student foster care info and benefits?',
                f'{target[1]}']
    
    def country_syntax(self, _list: list) -> list:
        """Text fully listing the question given from country application information from
        students on ApplyTexas.

        :param _list: list of designated markdown text
        :type _list: list
        :return: list of strings to display the proper output
        :rtype: list
        """

        if _list[3] != 'CTRY SELF':
            return

        return ['Of what country are you a citizen?               Country of legal Permanent Residence:']

    def former_syntax(self, _list: list) -> list:
        """Text fully listing the question given from former student information from
        students on ApplyTexas.

        :param _list: list of designated markdown text
        :type _list: list
        :return: list of strings to display the proper output
        :rtype: list
        """

        if _list[3] != 'FORMER STUDENT':
            return
        
        syntax = {
            'Y': 'Yes',
            'N': 'No',
            'K': 'Not provided'
        }

        target = "".join(_list[-1]).translate(str.maketrans("", "", "\\0"))

        if len(target) != 2:
            target.append('K')

        output = []

        for idx in range(len(target)):
            val = syntax.get(target[idx], target[idx])
            output.append(val)


        return ['Are you a former student of this institution?', 
                f'{output[0]}', '',
                'Have you previously applied?',
                f'{output[1]}']
    
    def post_coll_univ_syntax(self, _list: list, found: int) -> list:

        if _list[0] != 'PCL':
            return
        
        institution = str(_list[-1]).replace('\\', '')
        
        if found == 0:
            return ['','1. Please list ALL post-secondary colleges or universities you have previously attended or',
                    'are presently attending, including for extension, correspondence, and distance learning',
                    'credit, starting with the most recent. Failure to list all institutions will be considered',
                    'an intentional omission an may lead to forced withdrawal.', '',
                    f'Name of Insitition: {institution}', 
                    f'Code: {_list[1]}/{_list[2]}', 
                    f'Dates Attended: {_list[4][:4]}/{_list[4][4:6]}{_list[4][6]}{_list[4][7:11]}/{_list[4][11:14]}']
        
        return ["",f'Name of Insitition: {institution}', 
                f'Code: {_list[1]}/{_list[2]}', 
                f'Dates Attended: {_list[4][:4]}/{_list[4][4:6]}{_list[4][6]}{_list[4][7:11]}/{_list[4][11:14]}']
    
    def senior_year_syntax(self, _list: list, found: int) -> list:

        if _list[0] != 'CRS':
            return
        
        target = str(_list[-1]).replace('\\', '')
        
        if found == 0:
            return ['', '4. Please list exact titles of courses to be completed your senior year and the number of',
                    'credits you will earn for each. Include college coursework you will complete your senior year.', '',
                    f'{target}', '']
        
        return [f'{target}', '']
    
    def current_course_syntax(self, _list: list, found: int) -> list:

        if _list[0] != 'CRS':
            return
        
        target = str(_list[-1]).replace('\\', '')
        course = str(_list[-2]).strip()
        
        if found == 0:
            return ['', '4. Please list the college or university courses you are currently enrolled in and courses',
                    'you anticipate completing before you transfer', '',
                    f'{_list[4]} {course}/{target}', '']
        
        return [ f'{_list[4]} {course}/{target}', '']
    
    def family_obj_income_syntax(self, _list: list) -> list:
        """Text fully listing the question given from family obligation income information from
        students on ApplyTexas.

        :param _list: list of designated markdown text
        :type _list: list
        :return: list of strings to display the proper output
        :rtype: list
        """

        target = "".join(_list[-1]).translate(str.maketrans("", "", "\\0"))

        return ["(a) I have to work to supplment family income", "Please Explain:",
                f'{target}']
        
    
    def family_income_syntax(self, _list: list) -> list:
        """Text fully listing the question given from family income information from
        students on ApplyTexas.

        :param _list: list of designated markdown text
        :type _list: list
        :return: list of strings to display the proper output
        :rtype: list
        """

        target = "".join(_list[-1]).translate(str.maketrans("", "", "\\0"))

        return ["Please indicate, for the most recent tax year, your family's gross income.", 
                "Include both untaxed and taxed income:", 
                f"{target}"]
    
    def family_care_syntax(self, _list: list) -> list:
        """Text fully listing the question given from family care information from
        students on ApplyTexas.

        :param _list: list of designated markdown text
        :type _list: list
        :return: list of strings to display the proper output
        :rtype: list
        """

        target = "".join(_list[-1]).translate(str.maketrans("", "", "\\0"))

        return ['How many people, including yourself, live in your household?',
                '(include brothers and sisiters attending college):',
                 f'{target}']
    
    def family_obj_extra_syntax(self, _list: list) -> list:

        if _list[3] != 'FAMILY OBLIGATION OTHER' and _list[3] != 'FAMILY OBLIGATION CARE':
            return
        
        syntax = {
            'N': 'No',
            'Y': 'Yes'
        }

        target = syntax.get(_list[-2], _list[-2])
        last = str(_list[-1]).replace('\\', '')

        if target != 'No':
            return ['Do you have family obligations that keep you from participating in extracurricular',
                    'activities?', f'{target}',
                    'Please Explain:',f'{last}','']
        
        return ['Do you have family obligations that keep you from participating in extracurricular',
                'activities?', f'{target}', '']
    
    def currently_reside_syntax(self, _list: list) -> list:

        if _list[3] != 'INT CURR RESIDE IN US':
            return

        target = str(_list[-1]).replace('\\', '')

        syntax = {
            'N': 'No',
            'Y': 'Yes'
        }
        
        target = syntax.get(target, target)

        return ['Are you currently residing in the U.S.?',
                f'{target}', '']
    
    def vet_syntax(self, _list: list) -> list:

        if _list[3] != 'VET STATUS':
            return

        syntax = {
            '1': 'Veteran',
            '2': 'Current US Miliary Service Member',
            '3': 'Spouse or Dependen of Veteran or Current Service Member',
            '4': 'Spouce or dependent of, or a veteran or current U.S. military servicemember with injury or illness',
            '4+': 'resulting from military service (service-connected injury/illness)',
            '5': 'Spouse or dependent of deceased US servicemember'
        }

        output = [str(val) for val in str(_list[-1]).replace("\\", "")]
        output.insert(0, 'U.S. Military-Veteran Status?')
        output.append(" ")

        for idx in range(len(output)):
            if output[idx] == '4':
                output.insert(idx+1, '4+')

        for idx in range(len(output)):
            for key, value in syntax.items():
                if key == output[idx]:
                    output[idx] = value
 
        return output
        
    def home_syntax(self, _list: list) -> list:

        if _list[3] != 'HOME SCHOOLED':
            return
        
        syntax = {
            'N': 'No',
            'Y': 'Yes'
        }

        target = str(_list[-1]).replace("\\", "")

        for key, value in syntax.items():
            if key == target:
                target = value

        return ['Home Schooled?',
                f'{target}']
    
    def suspension_syntax(self, _list: list) -> list:

        if _list[3] != 'CURRENT ACADEMIC SUSP':
            return
        
        syntax = {
            'N': 'No',
            'Y': 'Yes'
        }

        target = str(_list[-1]).replace("\\", "")

        for key, value in syntax.items():
            if key == target:
                target = value
        
        return ['5. Are you currently on academic suspension from the last college or univeristy attended?',
                f'{target}', '']
    
    def college_work_syntax(self, _list: list) -> list:

        if _list[3] != 'COLLEGE WORK':
            return
        
        target = _list[-2:]

        syntax = {
            'N\\': 'No',
            'Y\\': 'Yes',
            'Y': 'Yes, some or all of my college credit hours have been earned through classwork',
            'N': 'No'
        }

        for idx in range(len(target)):
            for key, value in syntax.items():
                if key == target[idx]:
                    target[idx] = value

        temp = str(target[1]).replace('\\', '')

        if temp == 'No':
            return ['Will you have college credit hours by high school graduation date, if so how many?',
                    f'{temp}',]
        else:
            return ['Will you have college credit hours by high school graduation date, if so how many?',
                    f'{temp}','',
                    'Are your college credit hours earned (or being earned) through dual credit, concurrent',
                    'enrollment, or an early college high school?',
                    f'{target[0]}']
        
    def int_visa_status_syntax(self, _list: list) -> list:

        if _list[3] != 'INT VISA STATUS CHANGE':
            return
        
        syntax = {
            'N\\': 'No',
            'Y\\': 'Yes',
        }

        target = syntax.get(_list[-1], _list[-1])

        return ['Will you require a change in your visa status?',
                f'{target}']
    
    def family_obj_syntax(self, _list: list) -> list:

        if _list[3] != 'FAMILY OBLIGATIONS':
            return
        
        target = str(_list[-1]).replace("\\", "")
        
        syntax = {
            'N': 'No',
            'Y': 'Yes'
        }

        for key, value in syntax.items():
            if key == target:
                target = value

        return ['Do you have family obligations that keep you from participating in extracurricular activities?',
                f'{target}', '']
    
    def app_share_syntax(self, _list: list) -> list:

        if _list[3] != 'APPLICATION SHARING':
            return
        
        target = str(_list[-1]).replace("\\", "")
        
        syntax = {
            'N': 'No',
            'Y': 'Yes'
        }

        for key, value in syntax.items():
            if key == target:
                target = value
        
        return ['Application sharing on denied admission?',
                f'{target}', '']
    
    def phi_theta_kappa_syntax(self, _list: list) -> list:

        if _list[3] != 'PHI THETA KAPPA':
            return
        
        syntax = {
            'N\\': 'No',
            'Y\\': 'Yes'
        }

        output = syntax.get(_list[-1], _list[-1])

        return ['Are you a Phi Theta Kappa?', 
                f'{output}', '']
    
    def exit_us_syntax(self, _list: list) -> list:

        if _list[3] != 'INTL EXIT US':
            return
        
        syntax = {
            'N\\': 'No',
        }
        
        target = syntax.get(_list[-1], "Yes")
        
        if target != "Yes":
            return ['If you are already in the U.S., do you plan to leave the U.S. before enrolling at the',
                    'university to which you are applying? If yes, estimate the date of travel.',
                    f'{target}', '']
        else:
            target = str(_list[-1]).replace('\\', '')
            return ['If you are already in the U.S., do you plan to leave the U.S. before enrolling at the',
                    'university to which you are applying? If yes, estimate the date of travel.',
                    f'{target[:4]}-{target[4:]}', '']
    
    def residency_determ_syntax(self, _list: list) -> list:

        if _list[3] != 'RES: DETERM':
            return
        
        target = str(_list[-1]).replace("\\", "")

        syntax = {
            'Y' : 'Y - Texas Resident',
            'N' : 'N - Non-Texas Resident',
            'A' : 'Needs Affidavit'
        }

        target = syntax.get(target, target)


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
                f'Applytexas Residency Determination: {target}', '']
    
    def residency_claim_syntax(self, _list: list) -> list:

        if _list[3] != 'RES: RESIDENCY CLAIM':
            return
        
        target = str(_list[-1]).replace("\\", "")
        target = target.strip()

        return ['Of what state or country are you a resident?',
                f'{target[:3]}--{target[3:]}']
    
    def residency_self_syntax(self, _list: list) -> list:

        if _list[3] != 'RES: SELF':
            return

        output = self.p.process_str(_list[-1])

        if output[-1] == '0000':
            return
        
        ans = self.p.process_self(output)

        return ['Residency Information - continued:', '',
                '4. If you are not a U.S. Citizen or U.S. Permanent Resident, are youa foreign national',
                'here with a visa eligible to domicile in the United States or are you a Refugee, Asylee,',
                'Parolee or here under Temporary Protective Status? If so, indicate which:', f'{ans[0]}', '',
                '5. Do you currently live in Texas?', f'{ans[1]}', '',
                '6. If you currently live in Texas:',
                '(a) How long have you been living here?', f'{ans[2]}', '',
                '(b) What is your main purpose for being in the state?', f'{ans[3]}', '',
                '7. If you are a member of the U.S. military:',
                '(a) Is Texas your Home of Record?', f'{ans[4]}', '',
                '(b) What state is listed as your military legal residence for tax purposes on your Leave', 
                'and Earnings Statment', f'{ans[5]}', '',
                '8. Do any of the followign apply to you?', 
                '(a) Do you hold the title (Warranty Deed, Deed of Trust, or other similar instrument that', 
                'is effective to hold title) to residential real property in Texas?', f'{ans[6]}', '',
                '(b) Do you have ownership interest and customarily manage a business in Texas without the',
                'intention of liquidation in the foreseeable future?', f'{ans[7]}', '',
                '9. For the past 12 months', 
                '(a) Have you been gainfully employed in Texas?', f'{ans[8]}', '',
                '(b) Have you recieved primary support from a social service agency?', f'{ans[9]}', '',
                '10. Are you married to a person who could claim YES to any part of question 8 or 9?', f'{ans[10]}', '',
                '(a) If yes, indicate which question could be answered YES by your spouse:', f'{ans[11]}', '',
                '(b) How long have you been married to the Texas Resident?', f'{ans[12]}']
    
    def residency_guar_syntax(self, _list: list) -> list:

        if _list[3] != 'RES: GUAR':
            return

        output = self.p.process_str(_list[-1])

        if output[-1] == '0000':
            return

        ans = self.p.process_guar(output)
        
        return ['Residency Information - continued:', '',
                '1. Is the parent or legal guardian upon whom you base your claim of residency a U.S.',
                'Citizen?', f'{ans[0]}', '',
                '2. If no, does the parent or legal guardian upopn whom you base your claim residency',
                'hold Permanent Residence Status (valid I-551) for the U.S.?', f'{ans[1]}', '',
                '3. Is this parent or legal guardian a foreign national whose application for Permanent',
                'Resident Status has been preliminarily reviewed?', f'{ans[2]}', '',
                '4. is this parent or legal guardian a foreign national here with a visa eligible to',
                'domicile in the United States or are you a Refugee, Asylee, Parolee or here under',
                'Temporary Protective Status? If so, indicate which:', f'{ans[3]}', '',
                '5. Does this parent or legal guardian currently live in Texas?', f'{ans[4]}', '',
                '6. If your parent or legal guardian currently live in Texas:', '',
                '(a) How long has he or she been living here?', f'{ans[5]}', '',
                "(b) What is your parent's or legal guardian's main purpose for being in the state?", f'{ans[6]}', '',
                '7. If your parent or legal guardian is a member of the U.S. military:', '',
                '(a) Is Texas his or her Home of Record?', f'{ans[7]}', '',
                '(b) What state is listed as his or her military legal residence for tax purposes on his or',
                'her Leave and Earnings Statement?', f'{ans[8]}', '',
                '8. Do any of the following apply ot your parent or legal guardian?', '',
                '(a) Does your parent or legal guardian hold the title (Warranty Deed, Deed of Trust, or',
                'other similar instrument that is effective to hold title) to residential real property in',
                'Texas?', f'{ans[9]}', '',
                '(b) Does your parent or legal guardian have ownership interest and customarily manage a',
                'business in Texas without the intention of liquidation in the foreseeable future?', f'{ans[10]}', '',
                '9. For the past 12 months', '',
                '(a) Has your parent or legal guardian been gainfully employed in Texas?', f'{ans[11]}', '',
                '(b) Has your parent or legal guardian received primary support from a social service',
                'agency?', f'{ans[12]}', '',
                '10. Is your parent or legal guardian married to a person who could claim "yes" to any part',
                'of question (8) or (9)?', f'{ans[13]}', '',
                '(a) If yes, indicate which question could be answered "yes" by your parent or legal',
                "guardian's spouse:", f'{ans[14]}', '',
                '(b) How long has your parent or legal guardian been married to the Texas Resident?', f'{ans[15]}',
                ]

