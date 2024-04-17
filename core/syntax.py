import core

class Syntax:
    """Class created to house methods for in-place replacement text of varying types of markdown text in the
    form of a list.
    """

    def payment_syntax(self, _str: str) -> list:
        """Text fully listing the question given for payment information from students
        on ApplyTexas.

        :param _str: string from designated markdown text
        :type _str: str
        :return: list of strings to display the proper output
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


        return [f"Transcation Time: {transaction_time}",
                f"Payment Status: {payment_status}",
                f"Payment Amount: {payment_amount}",
                f"Transcation Trace: {transaction_trace}",
                f"Customer Reference: {customer_ref}",
                f"Card Type: {card_type}",
                f"Last 4 digit card number: {last_4}",
                f"Card Expiration Date: {card_exp}"]
    
    def hs_diploma_syntax(self, _str: str) -> list:
        """Text fully listing the question given for HS Diploma information including
        some Residency information from students on ApplyTexas.

        :param _str: string from designated markdown text
        :type _str: str
        :return: list of strings to display the proper output
        :rtype: list
        """

        target = "".join(_str[-1]).translate(str.maketrans("", "", "\\0"))
        temp = str(target).split(" ")
        
        p = core.Process()
        output = p.process_list(temp)

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

        p = core.Process()
        output = p.process_str(_str[-1])

        for idx in range(len(output)):
            if str(output[idx]).startswith('2'):
                end_point = idx

        return ['During the 12 months prior to you applying, did you register',
                'for a public college or university in Texas?', f'{output[0]}',
                'What Texas public college or university did you last attend?',
                f'{output[1:end_point]}',
                'In which terms were you last enrolled?', f'{output[-1][:-2]}',
                'During you last seemster at a Texa public institution, did you pay resident (in-state)',
                'or nonresident (out-of-state) tution?', f'{output[-1][-2]}',
                'If you paid in-state tution at your last institution, was it because you were classified',
                'as a resdient or because you were non-resident who received a wavier?', f'{output[-1][-1]}']
    
    def basis_syntax(self, _str: str) -> list:
        """Text fully listing the question given from basis of claim information from
        students on ApplyTexas.

        :param _str: string from designated markdown text
        :type _str: str
        :return: list of strings to display the proper output
        :rtype: list
        """

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

        target = "".join(_str[-1]).translate(str.maketrans("", "", "\\0"))

        target = target.replace('NN', "No, No").replace('YY', "Yes, Yes").replace('YN', 'Yes, No').replace('NY', 'No, Yes')

        return ['Are you a former student of this institution?',
                'Have you previously applied?',
                f'{target}']
    
    def residency_self_syntax(self, _str: str) -> list:

        p = core.Process()
        output = p.process_str(_str[-1])
        print(output)

        return ['No self information reported...']

        return ['Residency Information:',
                '5. Do you currently live in Texas?', f'{output[0][0]}',
                '6. If you currently live in Texas:',
                '(a) How long have you been living here?', f'{output[0][1:3]} Years, {output[0][3:5]} Months',
                '(b) What is your main purpose for being in the state?', f'{output[0][-1]}',
                '7. If you are a member of the U.S. military:',
                '(a) Is Texas your Home of Record?', f'{output[1][0]}',
                '(b) What state is listed as your military legal residence for tax purposes on your Leave', 
                'and Earnings Statment', f'{output[1][1:7]}',
                '8. Do any of the followign apply to you?', 
                '(a) Do you hold the title (Warranty Deed, Deed of Trust, or other similar instrument that', 
                'is effective to hold title) to residential real property in Texas?', f'{output[1][7]}',
                '(b) Do you have ownership interest and customarily manage a business in Texas without the',
                'intention of liquidation in the foreseeable future?', f'{output[1][8: 20]}',
                '9. For the past 12 months', '(a) Have you been gainfully employed in Texas?', f'{output[1][20]}',
                '(b) Have you recieved primary support from a social service agency?', f'{output[1][21]}',
                '10. Are you married to a person who could claim YES to any part of question 8 or 9?', f'{output[1][27]}',
                '(a) If yes, indicate which question could be answered YES by your spouse:', f'{output[1][-1]}',
                '(b) How long have you been married to the Texas Resident?', f'Years: {output[1][22:24]} Months: {output[1][24:26]}']
    
    def residency_guar_syntax(self, _str: str) -> list:

        p = core.Process()
        output = p.process_str(_str[-1])
        print(output)

        return ['No guardian information reported...']
        
        return ['Residency Information:',
                '1. Is the parent or legal guardian upon whom you base your claim of residency a U.S.',
                'Citizen?', f'{output[0]}',
                '5. Does this parent or legal guardian currently live in Texas?', f'{output[1][0]}',
                '6. If your parent or legal guardian currently live in Texas:',
                '(a) How long has he or she been living here?', f'{output[1][1:3]} years; {output[1][3:5]} months',
                "(b) What is your parent's or legal guardian's main purpose for being in the state?", f'{output[1][5]}',
                '8. Do any of the following apply ot your parent or legal guardian?',
                '(a) Does your parent or legal guardian hold the title (Warranty Deed, Deed of Trust, or',
                'other similar instrument that is effective to hold title) to residential real property in',
                'Texas?', f'{output[2][0]} - {output[2][1:7]}',
                '(b) Does your parent or legal guardian have ownership interest and customarily manage a',
                'business in Texas without the intention of liquidation in the foreseeable future?', f'{output[2][7]}',
                '9. For the past 12 months',
                '(a) Has your parent or legal guardian been gainfully employed in Texas?', f'{output[2][8]}',
                '(b) Has your parent or legal guardian received primary support from a social service',
                'agency?', "",
                '10. Is your parent or legal guardian married to a person who could claim "yes" to any part',
                'of question (8) or (9)?', f'{output[2][22]}',
                '(a) If yes, indicate which question could be answered "yes" by your parent or legal',
                "guardian's spouse:", f'{output[2][23]}',
                '(b) How long has your parent or legal guardian been married to the Texas Resident?', f'{output[2][24:26]} years; {output[2][26:28]} months',
                ]

