
class Process:

    def __init__(self, file_path: str=None):
        self.file_path = file_path

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
        
        for sublist in _list:
            sublist[:] = [item for item in sublist if not any(str(item).startswith(remove) for remove in _translate)]

        return _list
    
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