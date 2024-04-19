import core

class Syntax:

    def __init__(self):
        """Class created to house methods for in-place replacement text of varying types of markdown text in the
        form of a list.
        """

        self.p = core.Process()
        self.example_guar = ['Y', 'Y', 'N', 'NONE', 'OF', 'THE', 'ABOVE', 'Y2535H', 'N000000N000000', '000000NN', '0000N']

    def payment_syntax(self, _str: str) -> list:
        """Text fully listing the question given for payment information from students
        on ApplyTexas.

        :param _str: string from designated markdown text
        :type _str: str
        :return: list of strings to display the proper output
        :rtype: list
        """

        if _str[3] != 'PAYMENT RECONCILIATION':
            return

        target = _str[-1]

        return [f"Transcation Time: {target[0:8]}",
                f"Payment Status: {target[15:19]}",
                f"Payment Amount: {target[19:24]}",
                f"Transcation Trace: {target[24:36]}",
                f"Customer Reference: {target[36:48]}",
                f"Card Type: {target[48]}",
                f"Last 4 digit card number: {target[49:53]}",
                f"Card Expiration Date: {target[53:57]}"]
    
    def hs_diploma_syntax(self, _str: str) -> list:
        """Text fully listing the question given for HS Diploma information including
        some Residency information from students on ApplyTexas.

        :param _str: string from designated markdown text
        :type _str: str
        :return: list of strings to display the proper output
        :rtype: list
        """

        if _str[3] != 'RES: HS DIPLOMA OR GED':
            return

        target = "".join(_str[-1]).translate(str.maketrans("", "", "\\0"))
        temp = str(target).split(" ")
        
        output = self.p.process_list(temp)

        if len(output) > 2:
            dual = str(output[2]).replace('NN', "No, No").replace('YY', "Yes, Yes").replace('YN', 'Yes, No').replace('NY', 'No, Yes')
        else:
            dual = "N\A"

        return [f'Previous High School Name: {output[0]}',
                f'Location: {output[1]}','',
                'Did you live or will you have lived in Texas the 36 months leading up',
                'to high school graduation or completion of the GED?',
                'Also, when you begin the semester for which you are applying, will you have lived',
                'in Texas for the previous 12 months?',
                f'{dual}']
    
    def hs_ged_syntax(self, _str: str) -> list:
        """Text fully listing the question given for HS GED information from students 
        on ApplyTexas.

        :param _str: string from designated markdown text
        :type _str: str
        :return: list of strings to display the proper output
        :rtype: list
        """

        if _str[3] != 'HS GED TYPE':
            return

        target = "".join(_str[4]).translate(str.maketrans("", "", "\\0"))

        target = target.replace('N', "No").replace('Y', "Yes")


        return ['If you did not graduate from high school, do you have a DEG or have you completed',
                'another high school equivalency program?',
                 f'{target}','',]
    
    def prev_syntax(self, _str: str) -> list:
        """Text fully listing the question given from previous college information from
        students on ApplyTexas.

        :param _str: string from designated markdown text
        :type _str: str
        :return: list of strings to display the proper output
        :rtype: list
        """

        if _str[3] != 'RES: PREVIOUS ENROLLMENT':
            return

        output = self.p.process_str(_str[-1])

        for idx in range(len(output)):
            if str(output[idx]).startswith('0') or str(output[idx]).startswith('2'):
                end_point = idx

        months_q = str(output[0]).replace('N', 'No').replace('Y', 'Yes') 
        attend_q = " ".join(output[1:end_point])

        sem_start = str(output[-1][4]).replace('2', 'Spring')
        sem_end = str(output[-1][9]).replace('9', 'Fall')

        enrolled_q = f'{sem_start} {output[-1][:4]} - {sem_end} {output[-1][5:9]}'

        resident_q_1 = str(output[-1][-2]).replace('R', 'Resident (In-state)')
        resident_q_2 = str(output[-1][-1]).replace('R', 'Resident (In-state)')

        return ['During the 12 months prior to you applying, did you register',
                'for a public college or university in Texas?', f'{months_q}', '',
                'What Texas public college or university did you last attend?',
                f'{attend_q}', '',
                'In which terms were you last enrolled?', f'{enrolled_q}', '',
                'During you last seemster at a Texa public institution, did you pay resident (in-state)',
                'or nonresident (out-of-state) tution?', f'{resident_q_1}', '',
                'If you paid in-state tution at your last institution, was it because you were classified',
                'as a resdient or because you were non-resident who received a wavier?', f'{resident_q_2}']
    
    def basis_syntax(self, _str: str) -> list:
        """Text fully listing the question given from basis of claim information from
        students on ApplyTexas.

        :param _str: string from designated markdown text
        :type _str: str
        :return: list of strings to display the proper output
        :rtype: list
        """

        if _str[3] != 'RES: BASIS OF CLAIM':
            return


        if len(_str) > 4:
            target = "".join(_str[-1]).translate(str.maketrans("", "", "\\0"))
        else:
            target = "N\A"

        target = target.replace('NN', "No, No").replace('YY', "Yes, Yes").replace('YN', 'Yes, No').replace('NY', 'No, Yes')

        return ['Do you file your own federal income tax as an independent tax payer?',
                'Are you claimed as a dependent or are you eligible to be claimed as a dependent',
                'by a parent or court-appointed legal guardian?',
                f'{target}']
    
    def comment_syntax(self) -> list:
        """Text fully listing the question given from resident comments information from
        students on ApplyTexas.

        :return: list of strings to display the proper output
        :rtype: list
        """

        return ['Is there any additional information that you believe your college should know in', 
                'evaluating your eligibility to be classified as a resident? If so, please provide.']
    
    def dual_syntax(self, _str: str) -> list:
        """Text fully listing the question given from dual credit information from students
        on ApplyTexas.

        :param _str: string from designated markdown text
        :type _str: str
        :return: list of strings to display the proper output
        :rtype: list
        """

        if _str[3] != 'DUAL CREDIT':
            return

        target = "".join(_str[-1]).translate(str.maketrans("", "", "\\0"))
        
        target = target.replace('N', "No").replace('Y', "Yes")

        return ['Are you applyting to take college courses to be completed while you are still', 
                'a high school student (Dual Credit or Concurrent Enrollment)?',
                f'{target}']
    
    def conservator_syntax(self, _str: str) -> list:
        """Text fully listing the question given from conservator information from students
        on ApplyTexas.

        :param _str: string from designated markdown text
        :type _str: str
        :return: list of strings to display the proper output
        :rtype: list
        """

        if _str[3] != 'CONSERVATORSHIP SWITCHES':
            return

        target = "".join(_str[-1]).translate(str.maketrans("", "", "\\0"))

        target = target.replace('N', "No").replace('Y', "Yes")

        return ['At anytime in your life were you placed in foster care or adopted from foster care in Texas?',
                'If admitted, would your like to receive student foster care info and benefits?',
                f'{target}']
    
    def alien_syntax(self, _str: str) -> list:
        """Text fully listing the question given from alien applicaiton information from
        students on ApplyTexas.

        :param _str: string from designated markdown text 
        :type _str: str
        :return: list of strings to display the proper output
        :rtype: list
        """

        if _str[3] != 'ALIEN APP/INT\\':
            return
        
        target = "".join(_str[-1]).translate(str.maketrans("", "", "\\0"))

        return ['Is this parent or legal guardian a foreign national whose application',
                'for Permanent Resident Status has been preliminarily reviewed?',
                f'{target}']
    
    def former_syntax(self, _str: str) -> list:
        """Text fully listing the question given from former student information from
        students on ApplyTexas.

        :param _str: string from designated markdown text
        :type _str: str
        :return: list of strings to display the proper output
        :rtype: list
        """

        if _str[3] != 'FORMER STUDENT':
            return

        target = "".join(_str[-1]).translate(str.maketrans("", "", "\\0"))

        target = target.replace('NN', "No, No").replace('YY', "Yes, Yes").replace('YN', 'Yes, No').replace('NY', 'No, Yes')

        return ['Are you a former student of this institution?',
                'Have you previously applied?',
                f'{target}']
    
    def family_income_syntax(self, _str: str) -> list:

        target = "".join(_str[-1]).translate(str.maketrans("", "", "\\0"))

        return ["Please indicate, for the most recent tax year, your family's gross income.", 
                "Include both untaxed and taxed income:", 
                f"{target}"]
    
    def family_care_syntax(self, _str: str) -> list:

        target = "".join(_str[-1]).translate(str.maketrans("", "", "\\0"))

        return ['How many people, including yourself, live in your household?',
                '(include brothers and sisiters attending college):',
                 f'{target}']
    
    def residency_self_syntax(self, _str: str) -> list:

        if _str[3] != 'RES: SELF':
            return

        output = self.p.process_str(_str[-1])

        if output[-1] == '0000':
            return ['No self information reported...']
        
        print(f'SELF: {output}')

        return ['Residency Information:',
                '5. Do you currently live in Texas?', '', '',
                '6. If you currently live in Texas:',
                '(a) How long have you been living here?', '', '',
                '(b) What is your main purpose for being in the state?', '', '',
                '7. If you are a member of the U.S. military:',
                '(a) Is Texas your Home of Record?', '', '',
                '(b) What state is listed as your military legal residence for tax purposes on your Leave', 
                'and Earnings Statment', '', '',
                '8. Do any of the followign apply to you?', 
                '(a) Do you hold the title (Warranty Deed, Deed of Trust, or other similar instrument that', 
                'is effective to hold title) to residential real property in Texas?', '', '',
                '(b) Do you have ownership interest and customarily manage a business in Texas without the',
                'intention of liquidation in the foreseeable future?', '', '',
                '9. For the past 12 months', 
                '(a) Have you been gainfully employed in Texas?', '', '',
                '(b) Have you recieved primary support from a social service agency?', '', '',
                '10. Are you married to a person who could claim YES to any part of question 8 or 9?', '', '',
                '(a) If yes, indicate which question could be answered YES by your spouse:', '', '',
                '(b) How long have you been married to the Texas Resident?', '']
    
    def residency_guar_syntax(self, _str: str) -> list:

        if _str[3] != 'RES: GUAR':
            return

        _list = self.p.process_str(_str[-1])

        if _list[-1] == '0000':
            return ['No guardian information reported...']

        output = self.p.process_guar(_list)
        # print(f'GUAR: {output}', len(output))
        
        return ['Residency Information:',
                '1. Is the parent or legal guardian upon whom you base your claim of residency a U.S.',
                'Citizen?', '',
                '2. If no, does the parent or legal guardian upopn whom you base your claim residency',
                'hold Permanent Residence Status (valid I-551) for the U.S.?' '',
                '3. Is this parent or legal guardian a foreign national whose application for Permanent',
                'Resident Status has been preliminarily reviewed?', '',
                '4. is this parent or legal guardian a foreign national here with a visa eligible to',
                'domicile in the United States or are you a Refugee, Asylee, Parolee or here under',
                'Temporary Protective Status? If so, indicate which:', '',
                '5. Does this parent or legal guardian currently live in Texas?', '',
                '6. If your parent or legal guardian currently live in Texas:', '',
                '(a) How long has he or she been living here?', '',
                "(b) What is your parent's or legal guardian's main purpose for being in the state?", '',
                '7. If your parent or legal guardian is a member of the U.S. military:',
                '(a) Is Texas his or her Home of Record?', '',
                '(b) What state is listed as his or her military legal residence for tax purposes on his or',
                'her Leave and Earnings Statement?', '',
                '8. Do any of the following apply ot your parent or legal guardian?',
                '(a) Does your parent or legal guardian hold the title (Warranty Deed, Deed of Trust, or',
                'other similar instrument that is effective to hold title) to residential real property in',
                'Texas?', '',
                '(b) Does your parent or legal guardian have ownership interest and customarily manage a',
                'business in Texas without the intention of liquidation in the foreseeable future?', '',
                '9. For the past 12 months',
                '(a) Has your parent or legal guardian been gainfully employed in Texas?', '',
                '(b) Has your parent or legal guardian received primary support from a social service',
                'agency?', "",
                '10. Is your parent or legal guardian married to a person who could claim "yes" to any part',
                'of question (8) or (9)?', '',
                '(a) If yes, indicate which question could be answered "yes" by your parent or legal',
                "guardian's spouse:", '',
                '(b) How long has your parent or legal guardian been married to the Texas Resident?', '',
                ]

