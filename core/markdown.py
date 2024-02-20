import core

class Markdown(object):
    '''
    Class in charge with all markdown text found during processing in the SPE class.
    
    CURRENTLY UNUSED!!!
    '''

    def __init__(self):
        self.first = ''
        self.last = ''
        self.middle = ''

    def process_line(self, line):
        if line.startswith('BGN!'):
            return True
        else:
            self.applicant_name(line)

    def applicant_name(self, line):
        if line.startswith('IN2!05!'):
            self.last = self.line[6:-1]
        elif line.startswith('IN2!02!'):
            self.first = self.line[6:-1]
        elif line.startswith('IN2!03!'):
            self.middle = self.line[6:-1]