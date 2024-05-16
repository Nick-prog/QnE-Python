# https://www.pythonguis.com/examples/python-pdf-report-generator/
import csv

from typing import Union

class Process:

    def __init__(self, file: str = None):
        """Class created to house methods for any list processing. Mainly given
        a .csv file for reading and creating the desired data lists.

        :param file: string to .csv file path
        :type file: str, default to None
        """

        self.csv_file = file
        self.data = []

    def find_largest_row(self, input: list) -> int:
        """Finds the length of the largest row from a given nested list.

        :param input: nested list of varying length
        :type input: list
        :return: length of largest row
        :rtype: int
        """

        largest = 0

        for row in input:
            if largest < len(row):
                largest = len(row)

        return largest
    

    def find_largest_char(self, input: list) -> int:
        """Based on the largest row found, returns the char with the row
        from a given nested list.

        :param input: nested list of varying length
        :type input: list
        :return: char of largest row
        :rtype: int
        """

        largest = self.find_largest_row(input)

        for row in range(len(input)):
            if largest == len(input[row]):
                char = row

        return char


    def read_csv_file(self) -> list:
        """Opens and reads a .csv file and stores in self.data.

        :raises RuntimeError: Checks CSV file input
        :return: nested list of rows found
        :rtype: list
        """

        if self.csv_file is None:
            raise RuntimeError("Missing CSV file data.")
        
        # Open the CSV file
        with open(self.csv_file, newline='') as csvfile:
            # Create a CSV reader object
            csv_reader = csv.reader(csvfile)
            
            # Iterate over each row in the CSV file
            for row in csv_reader:
                # Append each row to the data list
                self.data.append(row)

        return self.data
    
    def create_data_list(self, input: list) -> Union[list, list]:
        """Creation of two data list based on destinction found at char 5
        for each row.

        :param input: nested list of rows found
        :type input: list
        :return: foreign and domestic list types
        :rtype: Union[list, list]
        """

        nested_list = input[2:]

        foreign = []
        domestic = []
         
        for idx, item in enumerate(nested_list):
            if str(item[5]).startswith('N4!'):
                foreign.append(nested_list[idx])
            else:
                domestic.append(nested_list[idx])

        return foreign, domestic
    
    def uniform_data_list(self, input: list) -> list:
        """NOT USED, atcurrent_strt at making all data list uniform for better
        manipulations.

        :param input: nested list of rows found
        :type input: list
        :return: updated nested list of same length
        :rtype: list
        """

        current_strlate_char = self.find_largest_char(input)
        current_strlate_list = input[current_strlate_char]
        
        # Initialize an empty result list
        result_nested_list = []

        # Iterate through each sublist in the given list
        for given_sublist in input:
            # Create a set to store the prefixes of matched items in the given sublist
            matched_prefixes = set()
            result_list = []
            # Iterate through the current_strlate list for each sublist
            for current_strlate_item in current_strlate_list:
                # Extract the prefix from the current_strlate item
                current_strlate_prefix = current_strlate_item.split('!')[0]

                # Check if the current_strlate prefix has already been matched
                if current_strlate_prefix in matched_prefixes:
                    result_list.append("")  # Append a blank string if the prefix has been matched before
                else:
                    # Iterate through the given sublist to find a match
                    found = False
                    for given_item in given_sublist:
                        given_prefix = given_item.split('!')[0]
                        if given_prefix == current_strlate_prefix:
                            result_list.append(given_item)
                            matched_prefixes.add(current_strlate_prefix)  # Add the matched prefix to the set
                            found = True
                            break
                    
                    # If no match is found, append a blank string
                    if not found:
                        result_list.append("")

            # Add the result list for the current sublist to the result nested list
            result_nested_list.append(result_list)

        return result_nested_list
    
    def discover_unique_markdown(self, input: list) -> set:
        """Set of all unique markdown text found based on the first
        separation.

        :param input: nested list of rows found
        :type input: list
        :return: set of unique values
        :rtype: set
        """

        unique_values = set()

        for sublist in input:
            for item in sublist:
                value = item.split('!')[0]
                unique_values.add(value)

        return unique_values
    
    def discover_dual_unique_markdown(self, input: list) -> set:
        """Set of all unique markdown text found based on two
        separations.

        :param input: nested list of rows found
        :type input: list
        :return: set of unqiue values
        :rtype: set
        """

        unique_values = set()
        
        for sublist in input:
            for item in sublist:
                parts = item.split('!')
                if len(parts) >= 3:  # Ensure at least two '!' separators exist
                    value = '!'.join(parts[:2])  # Join first two parts with '!'
                    unique_values.add(value)

        return unique_values

    def uniform_data_list_2(self, input: list) -> list:
        """NOT USED, atcurrent_strt at making all data list uniform for better
        manipulations.

        :param input: nested list of rows found
        :type input: list
        :return: updated nested list of same length
        :rtype: list
        """
        current_strlate_idx = self.find_largest_char(input)
        current_strlate_list = input[current_strlate_idx]
        current_strlate_markdown = []
        
        for idx in current_strlate_list:
            current_strlate_markdown.append(str(idx).split('!')[0])

        data = input[0:5]

        for sublist in range(len(data)):
            insert = 0
            for idx in range(len(current_strlate_markdown)):
                val = str(data[sublist][idx+insert]).split('!')[0]
    
                if val != current_strlate_markdown[idx]:
                    print("No MATCH", val, current_strlate_markdown[idx])
                    data[sublist].insert(idx, "")
                    insert += 1
                else:
                    print("\nMATCH!", val, current_strlate_markdown[idx])

        
        return data
    
    def process_list(self, _list: list) -> list:
        """Processing method for list that contain multiple blanks. Removes
        all blanks and leaves only a list of text found separated by commas.

        :param _list: list of text and blanks
        :type _list: list
        :return: list of remaining text
        :rtype: list
        """

        result = []
        current_item = ''

        for item in _list:
            if item:
                current_item += ' ' + item if current_item else item
            elif current_item:
                result.append(current_item)
                current_item = ''

        if current_item:
            result.append(current_item)

        return result
    
    def process_list_2(self, _list: list) -> list:

        result = []
        current_chunk = ''

        for item in _list:
            if item:  # If item is not empty
                current_chunk += item
            else:  # If item is empty, append current_chunk if it's not empty
                if current_chunk:
                    result.append(current_chunk)
                    current_chunk = ''
        # Append the last chunk if it's not empty
        if current_chunk:
            result.append(current_chunk)

        return result
    
    def process_str(self, _str: str) -> list:

        result = []

        last_idx = 1

        for idx in range(len(_str)):
            if idx == 0:
                result.append(_str[idx])
            elif _str[idx] == " " or _str[idx] == "\\":
                result.append(_str[last_idx:idx])
                last_idx = idx + 1 

        return [x for x in result if x]
    
    def process_str_2(self, _str: str) -> list:

        result = []
        formatted_list = []
        current_str = ''

        for idx in range(len(_str)):

            current_str += _str[idx]
            
            if _str[idx] == " ":
                result.append(current_str)
                current_str = ''

        for item in result:
            item = item.strip()
            if item:
                current_str += item + ' '
            else:
                if current_str:
                    formatted_list.append(current_str.strip())
                    current_str = ''

        if current_str:
            formatted_list.append(current_str.strip())

        return "-".join(formatted_list)
    
    def process_guar(self, _list: list) -> list:

        syntax = {
            'N': 'No',
            'Y': 'Yes',
            'K': 'Not provided',
            'H': 'Establish/Maintain a home',
            'W': 'Work Assignment',
            'E': 'Gainfully Employed',
            'P': 'Owns Property',
            'B': 'Owns Business',
            '0': 'Not provided',
            '000000': 'Not provided'
        }
        
        if len(_list) == 11:
            _list.insert(2, ' '.join(_list[2:7]))
            del(_list[3:8])
        elif len(_list) == 10:
            _list.insert(2, ' '.join(_list[2:6]))
            del(_list[3:7])
        elif len(_list) == 9:
            if _list[2] == 'current_strORARY':
                _list.insert(2, ' '.join(_list[2:5]))
                del(_list[3:6])
            else:
                _list.insert(2, ' '.join(_list[2:6]))
                del(_list[3:7])
        elif len(_list) == 8:
            _list.insert(2, ' '.join(_list[2:4]))
            del(_list[3:5])
        elif len(_list) == 6:
            _list.insert(2, 'K')
        elif len(_list) == 5:
            if _list[1] == 'Y' or _list[1] == 'N':
                _list.insert(2, 'K')
            else:
                _list.insert(1, 'K')
                _list.insert(2, 'K')
        elif len(_list) == 4:
            _list.insert(1, 'K')
            _list.insert(2, 'K')
            if len(_list[-1]) > 13:
                val = _list[-1]
                _list.insert(-1, val[:8])
                _list[-1] = val[8:]
        elif len(_list) == 3:
            _list.insert(1, 'K')
            _list.insert(2, 'K')
            if len(_list[3]) == 23:
                val = _list[3]
                del(_list[3])
                _list.insert(3, val[:6])
                _list.insert(4, val[6:])
            
            if len(_list[5]) == 14:
                val = _list[5]
                del(_list[5])
                _list.insert(5, val[:8])
                _list.insert(6, val[8:])
        
        if len(_list[3]) == 5:
            _list[3] += 'K'
        elif len(_list[3]) == 19:
            _list[3] += 'K'
            val = _list[3]
            del(_list[3])
            _list.insert(3, val[:6])
            _list.insert(4, val[6:])
        elif len(_list[3]) == 20:
            val = _list[3]
            del(_list[3])
            _list.insert(3, val[:6])
            _list.insert(4, val[6:])
        elif len(_list[3]) == 23:
            val = _list[3]
            del(_list[3])
            _list.insert(3, val[:6])
            _list.insert(4, val[6:])

        val = _list[3]
        del(_list[3])

        _list.insert(3, val[0])
        _list.insert(4, f'{val[3:5]} months; {val[1:3]} years')
        _list.insert(5, val[5])

        if len(_list[6]) == 17:
            val = _list[6]
            del(_list[6])
            _list.insert(6, val[0])
            _list.insert(7, val[1:3])
            _list.insert(8, val[3:])
        elif len(_list[6]) == 16:
            val = _list[6]
            del(_list[6])
            _list.insert(6, 'K')
            _list.insert(7, val[:2])
            _list.insert(8, val[2:])
        elif len(_list[6]) == 14:
            _list.insert(6, 'K')
            _list.insert(7, 'K')
        
        val = _list[8]
        del(_list[8])

        _list.insert(8, f'{val[0]} -- {val[5:7]}/{val[1:5]}')
        _list.insert(9, val[7])

        
        if len(_list[10]) == 14:
            val = _list[10]
            del(_list[10])
            _list.insert(10, val[:8])
            _list.insert(11, val[8:])

        val = _list[10]
        final = _list[11]

        if len(final) == 5:
            final = '0' + final

        del(_list[10])
        del(_list[10])

        _list.insert(10, val[-2])
        _list.insert(11, final[-1])
        _list.insert(12, val[-1])
        _list.insert(13, final[0])
        _list.insert(14, f'{final[3:5]} months; {final[1:3]} years')

        _list.insert(2, 'K')

        for idx in range(len(_list)):
            for key, value in syntax.items():
                if key == _list[idx]:
                    _list[idx] = value
                    break

        return _list
    
    def process_self(self, _list: list) -> list:

        new_list = []

        syntax = {
            'N': 'No',
            'Y': 'Yes',
            'K': 'Not provided',
            'H': 'Establish/Maintain a home',
            'W': 'Work Assignment',
            'E': 'Gainfully Employed',
            'C': 'Go to College',
            'P': 'Owns Property',
            'B': 'Owns Business',
            '0': 'Not provided',
            '000000': 'Not provided',
            '000': 'Not provided',
            ' ': 'Not provided'
        }

        if len(_list) == 8 or len(_list) == 9:
            new_list.append(' '.join(_list[1:5]))
            del(_list[1:5])
        elif len(_list[1]) == 23:
                _list.insert(2, _list[1][6:])
                _list[1] = _list[1][:6]
                new_list.append(_list[0])
        elif len(_list) == 4:
            new_list.append(_list[0])
            if len(_list[1]) == 5:
                new_list.append(_list[1][0])
                new_list.append(f"{_list[1][1:3]} Years; {_list[1][3:5]} Months")
                new_list.append('Not provided')
            elif len(_list[1]) == 6:
                new_list.append(_list[1][0])
                new_list.append(f"{_list[1][1:3]} Years; {_list[1][3:5]} Months")
                new_list.append(_list[1][5])
            elif len(_list[1]) == 23:
                new_list.append(_list[1][0])
                new_list.append(f"{_list[1][1:3]} Years; {_list[1][3:5]} Months")
                new_list.append(_list[1][5])
                new_list.append(_list[1][6])
                new_list.append(str(_list[1][7:9]))
                new_list.append(f'{_list[1][9]}--acquired: {_list[1][14:16]}, {_list[1][10:14]}')
                new_list.append(_list[1][16])
            
            if len(_list[2]) == 8:
                new_list.append(_list[2][-2])
                new_list.append(_list[2][-1])
            elif len(_list[2]) == 14:
                if _list[2][1:7] == '000000':
                    new_list.append('Not provided')
                    new_list.append('Not provided')
                    new_list.append(_list[2][0])
                    new_list.append(f'{_list[2][7]}--acquired: {_list[2][12:]}, {_list[2][8:12]}')
                elif _list[2][8:] == '000000':
                    new_list.append('Not provided')
                    new_list.append('Not provided')
                    new_list.append(f'{_list[2][0]}--acquired: {_list[2][5:7]}, {_list[2][1:5]}')
                    new_list.append(_list[2][7])
                else:
                    new_list.append('Not provided')
                    new_list.append('Not provided')
                    new_list.append(f'{_list[2][0]}--acquired: {_list[2][5:7]}, {_list[2][1:5]}')
                    new_list.append(f'{_list[2][7]}--acquired: {_list[2][12:]}, {_list[2][8:12]}')
            elif len(_list[2]) == 16:
                new_list.append('Not provided')
                new_list.append(_list[2][0:2])
                new_list.append(f"{_list[2][2]}--acquired: {_list[2][3:7]}, {_list[2][7:9]}")
                new_list.append(_list[2][9])
            elif len(_list[2]) == 17:
                new_list.append(_list[2][0])
                new_list.append(_list[2][1:3])
                new_list.append(f'{_list[2][3]}--acquired: {_list[2][8:10]}, {_list[2][4:8]}')
                new_list.append(_list[2][10])

            if len(_list[3]) == 5:
                new_list.append(_list[3][-1])
                new_list.append("Not provided")
                new_list.append(f"{_list[3][0:2]} Years; {_list[3][2:4]} Months")
            elif len(_list[3]) == 14:
                new_list.append(_list[3][6])
                new_list.append(_list[3][-1])
                new_list.append(_list[3][7])
                new_list.append(_list[3][8])
                new_list.append(f"{_list[3][9:11]} Years {_list[3][11:13]} Months")

        elif len(_list) == 5:
            new_list.append(_list[0])
            if len(_list[1]) == 5:
                new_list.append(_list[1][0])
                new_list.append(f"{_list[1][1:3]} Years; {_list[1][3:5]} Months")
                new_list.append('Not provided')
            elif len(_list[1]) == 6:
                new_list.append(_list[1][0])
                new_list.append(f"{_list[1][1:3]} Years; {_list[1][3:5]} Months")
                new_list.append(_list[1][5])

            if len(_list[2]) == 14:
                new_list.append(_list[2][-3:])
                new_list.append(_list[2][-6:-3])
                new_list.append(f'{_list[2][0]}--acquired: {_list[2][5:7]}, {_list[2][1:5]}')
                new_list.append(_list[2][7])
            elif len(_list[2]) == 16:
                new_list.append('Not provided')
                new_list.append(_list[2][0:2])
                new_list.append(f'{_list[2][2]}--acquired: {_list[2][7:9]}, {_list[2][3:7]}')
                new_list.append(_list[2][9])
            elif len(_list[2]) == 17:
                new_list.append(_list[2][0])
                new_list.append(_list[2][1:3])
                new_list.append(f'{_list[2][3]}--acquired: {_list[2][8:10]}, {_list[2][4:8]}')
                new_list.append(_list[2][10])

            if len(_list[3]) == 8:
                new_list.append(_list[3][-2])
                new_list.append(_list[4][-1])
                new_list.append(_list[3][:6])

            if len(_list[4]) == 5:
                new_list.append(_list[3][-1])
                new_list.append(f"{_list[4][:2]} Years; {_list[4][2:4]} Months")

        elif len(_list) == 6:
            new_list.append(_list[0])

            if len(_list[1]) == 5:
                new_list.append(_list[1][0])
                new_list.append(f"{_list[1][1:3]} Years; {_list[1][3:]} Months")
                new_list.append('Not provided')

            if len(_list[2]) == 1:
                new_list.append(_list[2])

            if len(_list[3]) == 14:
                new_list.append(_list[3][1:7])
                new_list.append(_list[3][0])
                new_list.append(_list[3][7])

            if len(_list[4]) == 8:
                new_list.append(_list[4][-2])
                new_list.append(_list[4][-1])
                new_list.append(_list[5][-1])

            if len(_list[5]) == 5:
                new_list.append(_list[4][:6])
                new_list.append(f"{_list[5][:2]} Years; {_list[5][2:4]} Months")

        else:
            new_list.append(_list[0])

            
        for idx in range(len(new_list)):
            for key, value in syntax.items():
                if key == new_list[idx]:
                    new_list[idx] = value

        return new_list