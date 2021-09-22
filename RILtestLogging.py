# Run the next line in cmd before running this script: 
# python E:\AutomationScripts\RILtest\RILtest.py &> E:\AutomationScripts\RILtest\request_get_sim_status_report.txt
# or python E:\AutomationScripts\RILtest\RILtest.py &> E:\AutomationScripts\RILtest\RIL_Test_Report.docx

import subprocess
import os
import sys
from threading import Timer
import logging
import threading

original_stdout = sys.stdout

class LogPipe(threading.Thread):
    
    def __init__(self, level):
        """Setup the object with a logger and a loglevel
        and start the thread
        """
        threading.Thread.__init__(self)
        self.daemon = False
        self.level = level
        self.fdRead, self.fdWrite = os.pipe()
        self.pipeReader = os.fdopen(self.fdRead)
        self.start()

    def fileno(self):
        """Return the write file descriptor of the pipe
        """
        return self.fdWrite

    def run(self):
        """Run the thread, logging everything.
        """
        for line in iter(self.pipeReader.readline, ''):
            logging.log(self.level, line.strip('\n'))

        self.pipeReader.close()

    def close(self):
        """Close the write end of the pipe.
        """
        os.close(self.fdWrite)

class RIL:

    # def __init__(self, f):
    #     self.f = f
    
    def request_operator(self):
        return subprocess.run(["adb", "shell", "request_operator"])

    def request_get_sim_status(self):
        return subprocess.run(["adb", "shell", "request_get_sim_status"])
    
    def request_setup_data_call(self):
        return subprocess.run(["adb", "shell", "request_setup_data_call", "-a", "vipmobile"])
    
    def request_and_test_data_connection(self):
        return subprocess.run(["adb", "shell", "request_and_test_data_connection", "-a", "vipmobile"])
    
    def request_radio_power(self):
        return subprocess.run(["adb", "shell", "request_radio_power"])
    
    def request_send_sms(self):
        return subprocess.run(["adb", "shell", "request_send_sms", "18110417673"])

pid = os.getpid()
# print("PID: ", pid)
obj = RIL()

# f =  open("request_get_sim_status_report.txt", "w")
# sys.stdout = f
# subprocess.run(["python", "E:\\AutomationScripts\\RILtest\\RILtest.py", ">", "E:\\AutomationScripts\\RILtest\\request_get_sim_status_report.txt"])
f = open("request_get_sim_status_report.txt", "w")

logpipe = LogPipe(logging.INFO)
with subprocess.Popen(["adb", "shell", "request_operator"], stdout=logpipe, stderr=logpipe) as s:
    logpipe.close()
print(logpipe)
sys.exit()
    
# ro = obj.request_operator()
# if(ro.returncode == 0):
#     print("\n\n ** request_operator report done **\n\n")
# else:
#     print("\n\n !! request_operator report error !! \n\n")
    
    
# rgss = obj.request_get_sim_status()  
# if(rgss.returncode == 0):  
#     print("\n\n ** request_get_sim_status report done **\n\n")
# else:
#     print("\n\n !! request_get_sim_status report error !! \n\n")

# rsdc = obj.request_setup_data_call()
# if(rsdc.returncode == 0):
#     print("\n\n ** request_setup_data_call report done **\n\n")
# else:
#     print("\n\n !! request_setup_data_call report error !! \n\n")
    
# rtdc = obj.request_and_test_data_connection()    
# if(rtdc.returncode == 0):
#     print("\n\n ** request_and_test_data_connection report done **\n\n")
# else:
#     print("\n\n !! request_and_test_data_connection report error !! \n\n")
    
# rrp = obj.request_radio_power()
# if(rrp.returncode == 0):
#     print("\n\n ** request_radio_power report done **\n\n")
# else:
#     print("\n\n !! request_radio_power report error !! \n\n")
    
# rss = obj.request_send_sms()
# if(rrp.returncode == 0):
#     print("\n\n ** request_send_sms report done **\n\n")
# else:
#     print("\n\n !! request_send_sms report error !! \n\n")
    
if(not(os.getpid())):
    f.close()

sys.stdout = original_stdout