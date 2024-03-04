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

    def applicant(self, line):
        if line.startswith('IN2!05!') and self.last == '': # Last name
            self.last = line[7:-2]
        elif line.startswith('IN2!02!') and self.first == '': # First name
            self.first = line[7:-2]
        elif line.startswith('IN2!03!') and self.middle == '': # Middle name
            self.middle = line[7:-2]
        else:
            pass