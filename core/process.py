from typing import Union
from pprint import pprint

class Process:

    def __init__(self, file_path: str=None):
        self.file_path = file_path

        self.cert_list = []
        self.submit_list = []
        self.conduct_list = []
        self.residency_list = []

        self.consultant_list = []
        self.new_consultant_list = []
        self.concentration_list = []
        self.faculty_list = []

    def read_spe_file(self) -> list:

        spe_list = []

        with open(self.file_path, 'r') as infile:
            metadata = []
            for line in infile:
                line = line.strip()
                if line.startswith('ST!189!'):
                    spe_list.append(metadata)
                    metadata = []
                else:
                    metadata.append(line)
        
        spe_list.append(metadata)

        return spe_list[1:]
    
    def process_str_with_num(self, _str: str) -> list:

            _list = []

            for idx, item in enumerate(_str):
                if item.isnumeric():
                    sep_idx = idx
                    break

            _list.append(str(_str[:sep_idx]).strip())
            _list.append(_str[sep_idx:])

            return _list
    
    def process_str_with_blank(self, _str: str) -> list:

        _list = []

        for idx, item in enumerate(_str):
            if item.isspace():
                sep_idx = idx
                break

        _list.append(_str[:sep_idx])
        _list.append(str(_str[sep_idx:]).strip())

        return _list
    
    def process_str_with_blanks(self, _str: str) -> list:

        sep_idx = []
        _list = []
        last = 0

        for idx, item in enumerate(_str):
            if item.isspace():
                sep_idx.append(idx)

        sep_idx.append(len(_str)-1)

        for indicies in sep_idx:
            _list.append(_str[last:indicies])
            last = indicies

        return [str(item).strip() for item in _list if item != " "]
    
    def create_uniform_list(self, _list: list, max_items: int, max_chars: int) -> list:

        for idx, item in enumerate(_list):
            if len(item) > max_chars:
                del(_list[idx])
                _list.insert(idx, item[:max_chars])
                _list.insert(idx+1, item[max_chars:])

        while len(_list) < max_items:
            if len(_list) == max_items-1:
                _list.append('0')
            else:
                _list.append('000000')

        return _list
    
    def create_uniform_item(self, _str: str, max_char: int) -> str:

        while len(_str) < max_char:
            _str = _str + '0'

        return _str
    
    def create_uniform_items(self, _list: list, max_char: list) -> list:

        for idx, item in enumerate(_list):
            if len(item) != max_char[idx]:
                _list[idx] = self.create_uniform_item(item, max_char[idx])

        return _list

    def check_for_new_markdown(self, _list: list) -> bool:

        _translate = ['ATV','BGN','COM','CRS','DEG','DMG','DTP','FOS',
                    'IN1','IN2','IND','MSG','N1','N3','N4','NTE','PCL',
                    'REF','RQS','MSG','SE','SES','SSE','SST','SUM',
                    'TST','LUI','GE','IEA','ISA','GS','SBT','SRE','LT']
        
        for apps in _list:
            for item in apps:
                check = str(item).split('!')
                if check[0] not in _translate:
                    raise ReferenceError(f'ERROR! {item} is not captured.')

        return True
    
    def remove_markdown_items(self, _list: list) -> list:

        _translate = ['ATV','BGN','SE','LUI','GE','IEA',
                      'ISA','GS','SBT','SRE']
        
        # Adding because it wasn't specified if needed
        _translate.append('CRS') # CRS work info
        _translate.append('RQS!AQ!ZZ!PARENT') # Parent education info, can't translate properly
        _translate.append('DTP!196!') # Start date for extra curriculars
        _translate.append('DTP!197!') # End date ^
        _translate.append('REF!PSM!')
        _translate.append('IN2!18!')
        _translate.append('RQS!AQ!ZZ!CTRY SPOUSE!!') # Spouse info
        _translate.append('RQS!AQ!ZZ!CTRY CHILD') # Child info
        _translate.append('RQS!AQ!ZZ!TEST1 SENT!') # GRE Test scores that aren't used
        _translate.append('RQS!AQ!ZZ!TEST2 SENT!') # ^
        _translate.append('RQS!AQ!ZZ!SPOKEN LANGUAGES!!') # Languages spoken, not translated anymore
        _translate.append('RQS!AQ!ZZ!OPTIONAL MODULES!!') # Extra course moudles info, not needed
        _translate.append('RQS!AQ!ZZ!CUR COLLEGE') # Current college course work, not needed
        _translate.append('RQS!AQ!ZZ!ALIEN APP/INT\\') # Always empty, remove
        _translate.append('RQS!AQ!ZZ!FAMILY!!') # Can't properly translate, remove
        
        for sublist in _list:
            sublist[:] = [item for item in sublist if not any(str(item).startswith(remove) for remove in _translate)]

        return _list
    
    def find_student_name(self, _list: list) -> str:

        name = ''
        
        for idx, item in enumerate(_list):
            if str(item).startswith('IN1!1!02!!!'):
                last = str(_list[idx+1]).split('!')[-1][:-1]
                first = str(_list[idx+2]).split('!')[-1][:-1]
                name = f'{last}, {first}'

        return name

    def find_app_types(self, _list: list) -> list:
        
        _apps = []

        _tranlsate = {
            'FFRESHMAN APPLICATION ID': 'U.S. Freshman Admission',
            'IFOREIGN GRAD APPLICATION ID': 'International Graduate Admission',
            'CREENTRY UNDERGRAD APPLICATION ID': 'U.S. Re-Entry Admission',
            'GUS GRAD APPLICATION ID': 'U.S. Graduate Admission',
            'TUS TRANSFER APPLICATION ID': 'U.S. Transfer Admission',
            'AFOREIGN TRANSFER APPLICATION ID': 'International Transfer Admission',
            'BFOREIGN FRESHMAN APPLICATION ID': 'International Freshman Admission',
            'SUS TRANSIENT APPLICATION ID': 'Transient Admission',
        }

        for sublist in _list:
            for item in sublist:
                if str(item).startswith('REF!48!'):
                    _apps.append(_tranlsate.get(str(item).split('!')[-1].strip('\\'), 'Other'))

        return _apps
    
    def move_list_item(self, apps: list, item: str, insert_idx: int, pop_idx: int) -> list:

        apps.pop(pop_idx)
        apps.insert(insert_idx, item)

        # print(f'Moving {item} to {insert_idx}')

        return apps
    
    def rearrange_list(self, _list: list) -> list:

        store_info = ('', 0)

        for apps in _list:
            temp = []
            for idx, item in enumerate(apps):
                if str(item).startswith('RQS!AQ!ZZ!APP SUBMIT/TRANSMIT!'):
                    self.move_list_item(apps, item, 1, idx)
                elif str(item).startswith('SSE!'):
                    self.move_list_item(apps, item, 5, idx)
                elif str(item).startswith('FOS!'):
                    self.move_list_item(apps, item, 6, idx)
                elif str(item).startswith('DMG!D8!'):
                    store_info = (item, idx)
                elif str(item).startswith('COM!TE!'):
                    if store_info[1] != 0:
                        self.move_list_item(apps, store_info[0], idx, store_info[1])
                        store_info = ('', 0)
                elif str(item).startswith('RQS!AQ!ZZ!DUAL CREDIT!'):
                    store_info = (item, idx)
                elif str(item).startswith('RQS!AQ!ZZ!FORMER STUDENT!'):
                    self.move_list_item(apps, item, store_info[1], idx)
                    store_info = (item, idx)
                elif str(item).startswith('RQS!AQ!ZZ!RES: HS'):
                    self.move_list_item(apps, item, store_info[1], idx)
                    store_info = (item, store_info[1])
                elif str(item).startswith('N1!HS!'):
                    self.move_list_item(apps, item, store_info[1], idx)
                    store_info = (item, store_info[1])
                    if str(apps[idx+1]).startswith('N4!'):
                        self.move_list_item(apps, apps[idx+1], store_info[1]+1, idx+1)
                        store_info = (item, store_info[1]+1)
                        self.move_list_item(apps, apps[idx+1], store_info[1]+1, idx+1)
                        store_info = (item, store_info[1]+2)
                # insert for college info later
                elif str(item).startswith('RQS!AQ!ZZ!FERPA CERT SWITCH!'):
                    # print(f'Current: {apps[idx]}, {idx}')
                    self.move_list_item(apps, item, len(apps), idx)
                    self.move_list_item(apps, apps[idx+1], len(apps), idx)
                    self.move_list_item(apps, apps[idx+2], len(apps), idx)
                    # print(f'After: {apps[idx]}, {idx}')

        from pprint import pprint
        pprint(_list)
        print(len(_list))
        return _list
    
    def separate_list_section(self, apps: list, start: tuple, end: str, end_lines: int, separate_list: list) -> None:

        start_idx = 0
        change_check_flag = 0

        for idx, items in enumerate(apps):
            if str(items).startswith(start) and change_check_flag == 0:
                start_idx = idx
                change_check_flag = 1
            elif str(items).startswith(end):
                if change_check_flag != 0:
                    # raise IndexError('Could not find a start point to separate.')
                    separate_list.append(apps[start_idx:idx+end_lines])
                    for remove in range((idx+end_lines)-start_idx):
                        apps.pop(start_idx)
                else:
                    separate_list.append([])

    def separate_list_question(self, apps: list, app_idx: int, start: list, end_lines: int, separate_list: list) -> None:

        change_check_flag = 0
        
        for idx, items in enumerate(apps):
            if str(items).startswith(start) or str(items).endswith(start):
                change_check_flag = 1

                while not str(apps[idx+end_lines]).startswith('MSG!'):
                    end_lines = end_lines - 1
                
                separate_list.append((apps[idx:idx+end_lines+1], app_idx))

                for remove in range((idx+end_lines+1)-idx):
                    apps.pop(idx)

        if change_check_flag == 0:
            separate_list.append([])

    def merge_list_question(self, separate_list: list) -> list:

        # Dictionary to group sublists by their ending number
        grouped_data = {}

        for sublist, group_num in separate_list:
            if group_num not in grouped_data:
                grouped_data[group_num] = []
            grouped_data[group_num].append(sublist)

        # Convert dictionary values to a list of lists
        return list(grouped_data.values())

    def new_rearrange_list(self, _list: list, app_type: str) -> list:

        new_list = []

        _types = self.find_app_types(_list)

        # Focuses on only one app_type at a time
        for idx, app in enumerate(_types):
            if app == app_type:
                new_list.append(_list[idx])

        for idx, apps in enumerate(new_list):
            self.separate_list_section(apps, 'RQS!AQ!ZZ!FERPA CERT SWITCH!', 'RQS!AQ!ZZ!TRUTH CERT SWITCH!', 1, self.cert_list)
            self.separate_list_section(apps, 'SSE!', 'RQS!AQ!ZZ!APP SUBMIT/TRANSMIT!!', 1, self.submit_list)
            self.separate_list_section(apps, ('RQS!AQ!ZZ!$  4!!', 'RQS!AQ!ZZ!$  9!!'), 'RQS!AQ!ZZ!$ 11!!', 5, self.conduct_list)
            self.separate_list_section(apps, ('RQS!AQ!ZZ!RES: PREVIOUS ENROLLMENT!!'), 'RQS!AQ!ZZ!RES: DETERM!', 1, self.residency_list)
            self.separate_list_question(apps, idx, ('Consultant Agency\\', 'Consultant/Agency\\'), 3, self.consultant_list)
            self.new_consultant_list = self.merge_list_question(self.consultant_list)
            self.separate_list_question(apps, idx, 'RQS!AQ!ZZ!$  1!!', 4, self.concentration_list)
            self.separate_list_question(apps, idx, 'Faculty Mentor\\', 4, self.faculty_list)

        pprint(self.new_consultant_list)
        print(len(self.new_consultant_list))
        # print(len(self.faculty_list))
        # print(len(self.concentration_list))
        # pprint(new_list[4])
        # print(len(new_list))

        # for apps in new_list:
        #     print(len(apps))

        # Relocate each item in the separated list into the proper index
        # for idx, apps in enumerate(new_list):
        #     for items in submit_transmit_app[idx]:
        #         apps.insert(0, items)
        #     # for items in residency_list_holder[idx]:
        #     #     apps.append(items)
        #     for items in conduct_list_holder[idx]:
        #         apps.append(items)
        #     for items in cert_list_holder[idx]:
        #         apps.append(items)

        # from pprint import pprint
        # pprint(residency_list_holder)
        # pprint(new_list[15])
        # print(len(new_list))

        return new_list