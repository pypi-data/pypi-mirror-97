FILE_NAME = __file__.split("/")[-1].split('.')[0]

import os
import json


# test command
# breakpoint set --file 'AppDelegate.m' --line 66
# add-dsym dsym-path


LLDB_LOGGER_OUTPUT = os.environ['LLDB_LOGGER_OUTPUT']
LLDB_LOGGER_CONFIG = os.environ['LLDB_LOGGER_CONFIG']
print(">>> " + LLDB_LOGGER_OUTPUT)
print(">>> " + LLDB_LOGGER_CONFIG)

LOG_FILE = open(LLDB_LOGGER_OUTPUT, 'w+')
g_target = None
g_process = None
g_brk_logmap = {}

class BreakPointLog:
    file: str
    line: int
    log: str
    symbol: str

    def __init__(self, json_info):
        self.line = -1
        if 'file' in json_info:
            self.file = json_info['file']
            self.line = json_info['line']
        elif 'symbol' in json_info:
            self.symbol = json_info['symbol']
        self.log = json_info['log']


def breakpoint_hit(frame, bp_loc, dict):
    global g_brk_logmap
    log = g_brk_logmap[bp_loc.GetBreakpoint().GetID()]
    global g_target
    import re
    var_names = re.findall("@([^@]+)@", log)
    var_vals = {}
    final_log = log
    for name in var_names:
        # print(name)
        ret_val = frame.EvaluateExpression(name)
        # print(lldb.frame.locals)
        var_val = ""
        if ret_val.type.is_pointer:
            var_val = ret_val.GetSummary()
            # print(">>>>>>>>>>> is_pointer")
        else:
            var_val = ret_val.value
            # print(ret_val.value)

        final_log = final_log.replace("@{0}@".format(name), str(var_val))
    LOG_FILE.write(final_log + '\n')
    LOG_FILE.flush()


def add_breakpoint(target, brk: BreakPointLog):
    global g_brk_logmap
    if brk.line >= 0:
        breakpoint = target.BreakpointCreateByLocation(brk.file, brk.line)
    else:
        breakpoint = target.BreakpointCreateByName(brk.symbol)
    breakpoint.SetAutoContinue(True)
    breakpoint.SetScriptCallbackFunction("{0}.breakpoint_hit".format(FILE_NAME))
    g_brk_logmap[breakpoint.GetID()] = brk.log

def load_breakpoint_logs() -> [BreakPointLog]:
    brks = []
    if not os.path.exists(LLDB_LOGGER_CONFIG):
        return brks
    with open(LLDB_LOGGER_CONFIG) as file:
        all_str = file.read()
        brk_list_json = json.loads(all_str)
        for brk_info in brk_list_json:
            brks.append(BreakPointLog(brk_info))
    return brks


def __lldb_init_module(debugger, internal_dict):
    global g_target
    global g_process
    # debugger.HandleCommand('breakpoint set --file XMGResourceDispatcher.m --line 200')
    g_target = debugger.GetTargetAtIndex(0)
    g_process = g_target.GetProcess()
    brks = load_breakpoint_logs()
    for brk in brks:
        add_breakpoint(g_target, brk)
