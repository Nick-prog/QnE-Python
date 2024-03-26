import core

import csv
import os

class CSVGen(object):

    def __init__(self, input, csv_file):
        self.input = input
        self.csv_file = csv_file

    def spe_to_csv(self):
        max_lines = 250  # Initialize max_lines to keep track of the maximum number of lines
        new_page = 0

        with open(self.csv_file, 'w', newline='') as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow([f"line_{i+1}" for i in range(max_lines)])

        with open(self.input, 'r') as infile, open(self.csv_file, 'a', newline='') as outfile:
            csv_writer = csv.writer(outfile)
            current_row = []
            for line in infile:
                line = line.strip()
                if line.startswith('ST!189!'):
                    new_page += 1
                    # Write the current row to CSV
                    csv_writer.writerow(current_row)
                    # Start a new row
                    current_row = []
                else:
                    # Append the line to the current row
                    current_row.append(line)
            # Write the last row to CSV
            csv_writer.writerow(current_row)

    def txt_folder_to_csv(self):
        max_lines = 250  # Initialize max_lines to keep track of the maximum number of lines
        # Check if the CSV file already exists
        if not os.path.exists(self.csv_file):
            # If it doesn't exist, create it and write headers
            with open(self.csv_file, 'w', newline='') as csvfile:
                csv_writer = csv.writer(csvfile)
                csv_writer.writerow([f"line_{i+1}" for i in range(max_lines)])
        
        # Append lines from each text file to the CSV
        with open(self.csv_file, 'a', newline='') as csvfile:
            csv_writer = csv.writer(csvfile)
            for filename in os.listdir(self.input):
                if filename.endswith(".txt"):
                    with open(os.path.join(self.input, filename), 'r') as txtfile:
                        txt_reader = txtfile.readlines()
                        max_lines = max(max_lines, len(txt_reader))  # Update max_lines
                        row = [filename] + [line.strip() for line in txt_reader]
                        csv_writer.writerow(row)

    def list_to_csv(self):
        with open(self.csv_file, 'w', newline='') as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerows(self.input)