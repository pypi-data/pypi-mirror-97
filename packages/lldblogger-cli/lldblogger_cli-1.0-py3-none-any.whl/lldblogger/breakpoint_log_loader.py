import os
import json


class BreakPointLog:
    file: str
    line: int
    log: str
    symbol: str

    def __init__(self, json_info):
        if 'file' in json_info:
            self.file = json_info['file']
            self.line = json_info['line']
        elif 'symbol' in json_info:
            self.symbol = json_info['symbol']
        self.log = json_info['log']


class BreakPointLogLoader:
    brk_list: [BreakPointLog]

    def __init__(self):
        self.bkr_list = []

    def load_file(self, file_path):
        if not os.path.exists(file_path):
            return
        with open(file_path) as file:
            all_str = file.read()
            brk_list_json = json.loads(all_str)
            for brk_info in brk_list_json:
                self.brk_list.append(BreakPointLog(brk_info))

    def get_breakpoints_logs(self) -> [BreakPointLog]:
        return self.bkr_list

