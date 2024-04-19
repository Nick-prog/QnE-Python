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
    

    def find_largest_index(self, input: list) -> int:
        """Based on the largest row found, returns the index with the row
        from a given nested list.

        :param input: nested list of varying length
        :type input: list
        :return: index of largest row
        :rtype: int
        """

        largest = self.find_largest_row(input)

        for row in range(len(input)):
            if largest == len(input[row]):
                index = row

        return index


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
        """Creation of two data list based on destinction found at index 5
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
        """NOT USED, attempt at making all data list uniform for better
        manipulations.

        :param input: nested list of rows found
        :type input: list
        :return: updated nested list of same length
        :rtype: list
        """

        template_index = self.find_largest_index(input)
        template_list = input[template_index]
        
        # Initialize an empty result list
        result_nested_list = []

        # Iterate through each sublist in the given list
        for given_sublist in input:
            # Create a set to store the prefixes of matched items in the given sublist
            matched_prefixes = set()
            result_list = []
            # Iterate through the template list for each sublist
            for template_item in template_list:
                # Extract the prefix from the template item
                template_prefix = template_item.split('!')[0]

                # Check if the template prefix has already been matched
                if template_prefix in matched_prefixes:
                    result_list.append("")  # Append a blank string if the prefix has been matched before
                else:
                    # Iterate through the given sublist to find a match
                    found = False
                    for given_item in given_sublist:
                        given_prefix = given_item.split('!')[0]
                        if given_prefix == template_prefix:
                            result_list.append(given_item)
                            matched_prefixes.add(template_prefix)  # Add the matched prefix to the set
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
        """NOT USED, attempt at making all data list uniform for better
        manipulations.

        :param input: nested list of rows found
        :type input: list
        :return: updated nested list of same length
        :rtype: list
        """
        template_idx = self.find_largest_index(input)
        template_list = input[template_idx]
        template_markdown = []
        
        for idx in template_list:
            template_markdown.append(str(idx).split('!')[0])

        data = input[0:5]

        for sublist in range(len(data)):
            insert = 0
            for idx in range(len(template_markdown)):
                val = str(data[sublist][idx+insert]).split('!')[0]
    
                if val != template_markdown[idx]:
                    print("No MATCH", val, template_markdown[idx])
                    data[sublist].insert(idx, "")
                    insert += 1
                else:
                    print("\nMATCH!", val, template_markdown[idx])

        
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
    
    def process_guar(self, _list: list) -> list:

        # example_list = ['N', 'Y', 'NONE OF THE ABOVE', 'Y2535H', 'N000000N000000', '000000NN', '0000N']

        new_list = []
        # modified = []
        _str = ''
        skip_idx = 0

        for i, item in enumerate(_list):
            if item == 'NONE':
                _str += f'{_list[i]} {_list[i+1]} {_list[i+2]} {_list[i+3]}'
                skip_idx = i+3
                new_list.append(_str)
            elif i > skip_idx or i == 0:
                new_list.append(item)

        # print(new_list)
        # given_index = 0

        # for item in example_list:
        #     if given_index < len(new_list) and len(new_list[given_index]) == len(item) or len(new_list[given_index]) == len(item)-1:
        #         modified.append(new_list[given_index])
        #         given_index += 1
        #     else:
        #         modified.append('N/A')

        return new_list