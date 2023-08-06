# run app on device & collect log & support communicate pip
import select
import signal
import tempfile
import os
import shlex
import subprocess
import threading
import time
import psutil

from lldblogger.breakpoint_log_loader import *


CMD_Template = "ios-deploy -d --noinstall --bundle {0}  --custom-script {1}"
INJECT_SCRIPT_PATH = os.path.join(os.path.dirname(__file__), "inject_script.py")

class Runner:
    log_output_file_path: str
    lldb_thread: threading.Thread = None
    is_terminate: bool

    def __init__(self, log_output_path=''):
        self.is_terminate = False
        if len(log_output_path) == 0:
            self.log_output_file_path = os.path.join(tempfile.gettempdir(), 'tmp.log')
        else:
            self.log_output_file_path = log_output_path
        print("LOG: {0}".format(self.log_output_file_path))

    def run(self, app_dir, log_brk_config_file):
        # process = subprocess.Popen(args, stdout=subprocess.PIPE, stdin=subprocess.PIPE)
        self.lldb_thread = threading.Thread(target=self.lldb_process_runloop, args=(app_dir, log_brk_config_file))
        # self.lldb_thread.setDaemon(1)
        self.lldb_thread.start()

    def terminate(self):
        if self.lldb_thread:
            self.is_terminate = True
            self.lldb_thread.join()
            self.lldb_thread = None

    def lldb_process_runloop(self, app_dir, log_brk_config_file):
        cmd = CMD_Template.format(app_dir, INJECT_SCRIPT_PATH)

        os.environ['LLDB_LOGGER_CONFIG'] = log_brk_config_file
        os.environ['LLDB_LOGGER_OUTPUT'] = self.log_output_file_path

        print("export LLDB_LOGGER_CONFIG=" + log_brk_config_file)
        print("export LLDB_LOGGER_OUTPUT=" + self.log_output_file_path)
        print(cmd)
        args = shlex.split(cmd)
        process = subprocess.Popen(args, stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, shell=False)
        while True:
            if self.is_terminate:
                current_process = psutil.Process()
                children = current_process.children(recursive=True)
                for child in children:
                    print("kill: " + str(child.pid))
                    child.kill()
                process.kill()
                print("kill: " + str(process.pid))
                break

