
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
            
    def rearrange_markdown_list(self, _list: list) -> list:

        app_list = self.find_app_types(_list)
        updated_list = self.remove_markdown_items(_list)

        from pprint import pprint
        pprint(updated_list)

        _example = [
            'N1!TM!!ZZ!TXAPP',
            'RQS!AQ!ZZ!APP SUBMIT/TRANSMIT!!',
            'REF!48!',
            'REF!SY!',
            'SSE!',
            'FOS!',
            'RQS!AQ!ZZ!FORMER STUDENT!',
            'N1!HS!',
        ]

        for idx, sublist in enumerate(updated_list):
            sublist[:] = [item for item in sublist if any(str(item).startswith(add) for add in _example)]

        return updated_list

        # insert_no_matter_what = [
        #     'RQS!AQ!ZZ!FORMER STUDENT!'
        # ]

        # output = _list.copy()

        # for apps in output:
        #     for idx, item in enumerate(apps):
        #         for e_idx, e_item in enumerate(example):
        #             # if e_item not in apps and e_item in insert_no_matter_what:
        #             #     print(f'Item {item} was not found!, inserting at index {e_idx} anyways.')
        #             #     apps.insert(e_idx, e_item)
        #             if str(item).startswith(e_item):

        #                 if e_item == 'N1!HS!':
        #                     hs_name = apps.pop(idx)
        #                     hs_loc = apps.pop(idx)
        #                     apps.insert(e_idx, hs_name)
        #                     apps.insert(e_idx+1, hs_loc)

        #                 else:
        #                     # print(f'\n{item} found in example list, {e_item}')
        #                     # print(f'Popping item idx {idx} from apps list')
        #                     apps.pop(idx) # Remove from list before moving
        #                     # print(f'Inserting {item} at index {e_idx} for apps list')
        #                     apps.insert(e_idx, item) # Move removed item to correct spot in list

        # return output
