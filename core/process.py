# https://www.pythonguis.com/examples/python-pdf-report-generator/
import csv
from pprint import pprint


class Process(object):

    def __init__(self, file):
         self.csv_file = file
         self.data = []
        
    def find_largest_row(self, data):

        largest = 0

        for row in data:
            if largest < len(row):
                largest = len(row)

        return largest
    

    def find_largest_index(self, data):

        largest = self.find_largest_row(data)

        for row in range(len(data)):
            if largest == len(data[row]):
                index = row

        return index


    def read_csv_file(self):
            '''
            Opens and reads a .CSV file and stores in self.data, a list containing all of its information.
            Returns List.
            '''

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
    
    def create_data_list(self, data):

        nested_list = data[2:]

        foreign = []
        domestic = []
         
        for idx, item in enumerate(nested_list):
            if str(item[5]).startswith('N4!'):
                foreign.append(nested_list[idx])
            else:
                domestic.append(nested_list[idx])

        return foreign, domestic
    
    def uniform_data_list(self, data):

        template_index = self.find_largest_index(data)
        template_list = data[template_index]
        
        # Initialize an empty result list
        result_nested_list = []

        # Iterate through each sublist in the given list
        for given_sublist in data:
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
    
    def discover_unique_markdown(self, data):

        unique_values = set()

        for sublist in data:
            for item in sublist:
                value = item.split('!')[0]
                unique_values.add(value)

        return unique_values
    
    def discover_dual_unique_markdown(self, data):

        unique_values = set()
        
        for sublist in data:
            for item in sublist:
                parts = item.split('!')
                if len(parts) >= 3:  # Ensure at least two '!' separators exist
                    value = '!'.join(parts[:2])  # Join first two parts with '!'
                    unique_values.add(value)

        return unique_values

    def uniform_data_list_2(self, data):
        template_idx = self.find_largest_index(data)
        template_list = data[template_idx]
        template_markdown = []
        
        for idx in template_list:
            template_markdown.append(str(idx).split('!')[0])

        data = data[0:5]

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
