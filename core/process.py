
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

    def filter_markdown_text(self, _list: list) -> list:

        output = []

        for apps in _list:
            current = []
            for items in apps:
                markdown = str(items).split('!')
                current.append("!".join(markdown[:-1]))
            output.append(current)

        return output
            
    def rearrange_markdown_list(self, _list: list) -> list:

        example = [
            'BGN!00!',
            'N1!TM!!ZZ!TXAPP',
            'RQS!AQ!ZZ!APP SUBMIT/TRANSMIT!!',
            'REF!48!',
            'REF!SY!',
            'SSE!',
            'FOS!',
            'RQS!AQ!ZZ!FORMER STUDENT!',
            'N1!HS!', 'HIGH SCHOOL LOCATION SKIP',
            

        ]

        insert_no_matter_what = [
            'RQS!AQ!ZZ!FORMER STUDENT!'
        ]

        output = _list.copy()

        for apps in output:
            for idx, item in enumerate(apps):
                for e_idx, e_item in enumerate(example):
                    # if e_item not in apps and e_item in insert_no_matter_what:
                    #     print(f'Item {item} was not found!, inserting at index {e_idx} anyways.')
                    #     apps.insert(e_idx, e_item)
                    if str(item).startswith(e_item):

                        if e_item == 'N1!HS!':
                            hs_name = apps.pop(idx)
                            hs_loc = apps.pop(idx)
                            apps.insert(e_idx, hs_name)
                            apps.insert(e_idx+1, hs_loc)

                        else:
                            # print(f'\n{item} found in example list, {e_item}')
                            # print(f'Popping item idx {idx} from apps list')
                            apps.pop(idx) # Remove from list before moving
                            # print(f'Inserting {item} at index {e_idx} for apps list')
                            apps.insert(e_idx, item) # Move removed item to correct spot in list

        return output
