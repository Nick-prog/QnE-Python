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
                 f'{target}','',
                 'Parent Information:']
    
    def prev_syntax(self, _str: str) -> list:
        """Text fully listing the question given from previous college information from
        students on ApplyTexas.

        :param _str: string from designated markdown text
        :type _str: str
        :return: list of strings to display the proper output
        :rtype: list
        """

        target = "".join(_str[-1]).translate(str.maketrans("", "", "\\0"))

        target = target.replace('N', "No").replace('Y', "Yes")

        return ['During the 12 months prior to you applying, did you register',
                'for a public college or university in Texas?',
                f'{target}']
    
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