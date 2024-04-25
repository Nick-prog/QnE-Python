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

        return [f"Transcation Time: {target[0:8]}",
                f"Payment Status: {target[15:19]}",
                f"Payment Amount: {target[19:24]}",
                f"Transcation Trace: {target[24:36]}",
                f"Customer Reference: {target[36:48]}",
                f"Card Type: {target[48]}",
                f"Last 4 digit card number: {target[49:53]}",
                f"Card Expiration Date: {target[53:57]}"]
    
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
        }

        target = "".join(_list[-1]).translate(str.maketrans("", "", "\\0"))
        target = str(target).split(" ")
        
        output = self.p.process_list(target)

        while len(output) < 4:
            output.append('Not provided')

        for idx in range(len(output)):
            for key, value in diploma.items():
                if key == output[idx]:
                    output[idx] = value

        return [f'Previous High School Name: {output[0]}',
                f'Location: {output[1]}','',
                'Did you live or will you have lived in Texas the 36 months leading up',
                'to high school graduation or completion of the GED?', f'{output[2]}', '',
                'Also, when you begin the semester for which you are applying, will you have lived',
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


        return ['If you did not graduate from high school, do you have a DEG or have you completed',
                'another high school equivalency program?',
                 f'{target}','',]
    
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
            resident_q_2 = str(output[-1][-1]).replace('R', 'Resident (In-state)').replace('U', 'Not provided')

            return ['During the 12 months prior to you applying, did you register',
                'for a public college or university in Texas?', f'{months_q}', '',
                'What Texas public college or university did you last attend?',
                f'{attend_q}', '',
                'In which terms were you last enrolled?', f'{enrolled_q}', '',
                'During you last seemster at a Texa public institution, did you pay resident (in-state)',
                'or nonresident (out-of-state) tution?', f'{resident_q_1}', '',
                'If you paid in-state tution at your last institution, was it because you were classified',
                'as a resdient or because you were non-resident who received a wavier?', f'{resident_q_2}']

        return ['During the 12 months prior to you applying, did you register',
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

        return ['Is there any additional information that you believe your college should know in', 
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

        target = "".join(_list[-1]).translate(str.maketrans("", "", "\\0"))

        target = target.replace('N', "No").replace('Y', "Yes")

        return ['At anytime in your life were you placed in foster care or adopted from foster care in Texas?',
                'If admitted, would your like to receive student foster care info and benefits?',
                f'{target}']
    
    def country_syntax(self, _list: list) -> list:
        """Text fully listing the question given from country application information from
        students on ApplyTexas.

        :param _list: lsit of designated markdown text
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

        target = "".join(_list[-1]).translate(str.maketrans("", "", "\\0"))

        target = target.replace('NN', "No, No").replace('YY', "Yes, Yes").replace('YN', 'Yes, No').replace('NY', 'No, Yes')

        return ['Are you a former student of this institution?',
                'Have you previously applied?',
                f'{target}']
    
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
    
    def vet_syntax(self, _list: list) -> list:

        if _list[3] != 'VET STATUS':
            return

        syntax = {
            '1': 'Veteran',
            '2': 'Current US Miliary Service Member',
            '3': 'Spouse or Dependen of Veteran or Current Service Member',
            '4': 'Spouce or dependent of, or a veteran or current U.S. military servicemember with injury or illness resulting from military service (service-connected injury/illness)',
            '5': 'Spouse or dependent of deceased US servicemember'
        }
        print(_list, '\n')

        target = str(_list[-1]).replace("\\", "")

        output = [str(d) for d in target]
        print(output)

        
        for idx in range(len(output)):
            for key, value in syntax.items():
                if key == output[idx]:
                    output[idx] = value

        
        if len(output) == 1:
            return ['U.S. Military-Veteran Status?', 
                    f'{output}']
        elif len(output) == 2:
            return ['U.S. Military-Veteran Status?', 
                    f'{output[0]}', f'{output[1]}']
    
    def residency_self_syntax(self, _list: list) -> list:

        if _list[3] != 'RES: SELF':
            return

        output = self.p.process_str(_list[-1])

        if output[-1] == '0000':
            return
        
        ans = self.p.process_self(output)

        return ['Residency Information:',
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
        
        return ['Residency Information:',
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

