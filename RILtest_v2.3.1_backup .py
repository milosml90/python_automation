####################################################################################################################
# IMPROVEMENTS NEEDED:
# 1. Events instead of hard-coded timeout
# 2. Regex instead of hardcoded keywords as a criteria for PASS/FAIL
####################################################################################################################

import time
import subprocess
import shlex
import sys
from threading import Thread, Timer, Event
import os
import tkinter as tk
import tkinter.filedialog
import signal
import asyncio

if sys.platform == 'win32':
    import msvcrt

# escapes = ''.join([chr(char) for char in range(1, 32)])
escape = ''.join(chr(27))  # character generated in the report file which should be removed

command = [";", "ping", "8.8.8.8"]  # a string which should be concatenated to the Linux command since ping should be repeated x times
command2 = [";", "ping", "www.google.com"]  # a string which should be concatenated to the Linux command since ping should be repeated x times
res = []
isPrinted = True
timeout = 15
operator = ""
flag = False

# operator = "vipmobile"
# operator = "internet"
# phoneNumber = "381649402195"
# phoneNumber = "001010123456793"
# phoneNumber = "220052131091208"

print("Choose the path where reports will be saved to: \n")

root = tk.Tk()  # used for creation of GUI file dialog
root.withdraw()  # use to hide tkinter window

currdir = os.getcwd()
file_path = tk.filedialog.askdirectory(parent=root, initialdir=currdir, title='Please select a directory')


# concatenate ping command 100 times to ensure it will return some bytes
# until data connection is established
def repeatCommand(command, times):
    for i in range(times):
        for x in command:
            res.append(x)
    return res


def alarm_handler(signum, frame):
    raise TimeoutExpired


    def run(self, cmd):
        p = subprocess.Popen(cmd,
                             shell=False,
                             stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE)

        self.stdout, self.stderr = p.communicate()


if sys.platform == 'linux':
    def _input(msg, q):
        ra = raw_input(msg)
        if ra:
            q.put(ra)
        else:
            q.put("")
        return

    def _slp(tm, q):
        time.sleep(tm)
        q.put("Timeout")
        return

    def wait_for_input(msg="Press Enter to continue", time=10):
        q = Queue.Queue()
        th = threading.Thread(target=_input, args=(msg, q,))
        tt = threading.Thread(target=_slp, args=(time, q,))

        th.start()
        tt.start()
        ret = None
        while True:
            ret = q.get()
            if ret:
                th._Thread__stop()
                tt._Thread__stop()
                return ret
        return ret


class Error(Exception):
    """Base class for other exceptions"""
    pass


class RILFailure(Error):
    pass


class TimeoutExpired(Exception):
    pass


class myClass:
        _input = None

        def __init__(self):
            get_input_thread = Thread(target=self.get_input)
            get_input_thread.daemon = True  # Otherwise the thread won't be terminated when the main program terminates.
            get_input_thread.start()
            get_input_thread.join(timeout=20)

            if myClass._input is None:
                print("No input was given within 20 seconds")
            else:
                print("Input given was: {}".format(myClass._input))


        @classmethod
        def get_input(cls):
            cls._input = input("")
            return


if sys.platform == 'win32':
    def input_with_timeout(prompt, timeout, timer=time.monotonic):
        sys.stdout.write(prompt)
        sys.stdout.flush()
        endtime = timer() + timeout
        result = []
        while timer() < endtime:
            if msvcrt.kbhit():
                result.append(msvcrt.getwche())  # XXX can it block on multibyte characters?
                if result[-1] == '\r':
                    return ''.join(result[:-1])
            time.sleep(0.04)  # just to yield to other processes/threads
        raise TimeoutExpired


def execAllRIL(cmd, file, timeout):
    # the last 3 files should not be read, those have to be executed the other way
    if len(cmd) == len(file[:-3]):
        for i in range(len(cmd)):
            try:
                with open(file[i], "w") as f:
                    if i == 2:
                        operator = input("Input the name of the operator, e.g. vipmobile: ")
                        if (operator == ""):
                            operator = "vipmobile"
                        print("Chosen operator: ", operator)
                        subprocess.run(cmd[2] + " " + operator, stdout=f, stderr=f, timeout=timeout)

                    if i == 4:
                        phoneNumber = input("Enter phone number: ")
                        if (phoneNumber == ""):
                            phoneNumber = "381649402195"
                        print("Chosen phone number: ", phoneNumber)
                        subprocess.run(cmd[4] + " " + phoneNumber, stdout=f, stderr=f, timeout=timeout)

                    subprocess.run(shlex.split(cmd[i]), stdout=f, stderr=f, timeout=timeout)
            except subprocess.TimeoutExpired:
                print(os.path.basename(file[i])[:-4], ' timeout expired')
                with open(file[i], "a+") as f:
                    f.write('\n TIMEOUT EXPIRED \n')

    else:
        raise RILFailure("Lengths of cmd and file must be the same!")


def execSingleRIL(cmd, file, timeout):
    try:
        with open(file, "w") as f:
            subprocess.run(shlex.split(cmd), stdout=f, stderr=f, timeout=timeout)
    except subprocess.TimeoutExpired:
        print(os.path.basename(file)[:-4], ' timeout expired')
        with open(file, "a+") as f:
            f.write('\n TIMEOUT EXPIRED \n')


async def pingTest(target, file):
    operator = ""
    kill = lambda process: process.kill()
    
    if target == "8.8.8.8":
        target = target + " ".join(repeatCommand(command, 60))
        
    elif target == "www.google.com":
        target = target + " ".join(repeatCommand(command2, 20))
    
    if sys.platform == 'win32':
        try:
            operator = input_with_timeout("Input the name of the operator, e.g. vipmobile: ", 10)
        except TimeoutExpired:
            print('Timeout expired')
        else:
            print("\n Operator vipmobile is chosen by default \n")

    elif sys.platform == 'linux':
        try:
            operator = wait_for_input("Input the name of the operator, e.g. vipmobile: ", 10)
        except TimeoutExpired:
            print('Timeout expired')
        else:
            print("\n Operator vipmobile is chosen by default \n")    

    if (operator == ""):
        operator = "vipmobile"
    # print("\nChosen operator: ", operator)
    with open(file_path + "/" + "request_and_test_data_connection.txt", "w") as f:
        rtdc = subprocess.Popen(["adb", "shell", "request_and_test_data_connection", "-a", operator],
                                stdout=f, stderr=f)
        time.sleep(5)
        
    with open(file, "w") as g:
        ping = subprocess.Popen(["adb", "shell", "ping", target], stdout=g, stderr=g)     
            
            
    my_timer = Timer(30, kill, [rtdc])
    my_timer2 = Timer(30, kill, [ping])

    try:
        my_timer.start()
        my_timer2.start()
        rtdc.communicate()
        ping.communicate()
  
    finally:
        my_timer.cancel()
        my_timer2.cancel()


async def main():
    await asyncio.gather(pingTest("8.8.8.8", file[6]))
    await asyncio.gather(pingTest("www.google.com", file[7]))


def checkLogs(file):
    try:
        with open(file, "r+") as f:
            a = f.read()
            if ((('E_GENERIC_FAILURE' or 'moderm no response' or 'Segmentation fault') in a
                 or 'Request completed: E_SUCCESS' not in a)
                    or os.stat(file).st_size == 0):
                # os.path.basename(file)[:-4] takes the report name from the file path and excludes .txt
                f.write("\n\n")
                f.write("____________________________________________________________________ \n")
                f.write(os.path.basename(file)[:-4])
                f.write(" FAILED \n")
                f.write("____________________________________________________________________")

            # if a read file is not from the RIL functions which are running in inf loop:
            elif (file == file[0] or file == file[1] or file == file[3] or file == file[4]):
                if (subprocess.TimeoutExpired):
                    f.write("\n\n")
                    f.write("____________________________________________________________________ \n")
                    f.write(os.path.basename(file)[:-4])
                    f.write(" FAILED \n")
                    f.write("____________________________________________________________________")

            else:
                f.write("\n\n")
                f.write("____________________________________________________________________ \n")
                f.write(os.path.basename(file)[:-4])
                f.write(" PASSED \n")
                f.write("____________________________________________________________________")

    except subprocess.TimeoutExpired:
        print("RIL function FAILED: timeout expired")


def checkPingLogs(file):
    try:
        with open(file, "r+") as f:
            if (file == (file_path + "/" + "ping_test.txt") or file == (file_path + "/" + "ping_test_google_com.txt")):
                a = f.read()
                if (('PING' and 'bytes from' and 'icmp_seq=1') in a):
                    f.write("\n\n")
                    f.write("____________________________________________________________________ \n")
                    f.write(os.path.basename(file)[:-4])
                    f.write(" PASSED")
                    f.write("\n____________________________________________________________________")

                else:
                    f.write("\n\n")
                    f.write("____________________________________________________________________ \n")
                    f.write(os.path.basename(file)[:-4])
                    f.write(" FAILED \n")
                    f.write("____________________________________________________________________")

            elif (file == file_path + "/" + "request_and_test_data_connection.txt"):
                a = f.read()
                if (("Request completed: E_SUCCESS" and "addresses:" and "dnses:" and "gateways:") in a):
                    f.write("\n\n")
                    f.write("____________________________________________________________________ \n")
                    f.write(os.path.basename(file)[:-4])
                    f.write(" PASSED")
                    f.write("\n____________________________________________________________________")

                else:
                    f.write("\n\n")
                    f.write("____________________________________________________________________ \n")
                    f.write(os.path.basename(file)[:-4])
                    f.write(" FAILED \n")
                    f.write("____________________________________________________________________")

    except subprocess.TimeoutExpired:
        print("RIL function FAILED: timeout expired")


def checkAllLogs(files):
    try:
        for file in files:
            print(file, " ")
            with open(file, "r+") as f:
                # different criterias for analysis are used for those 3 tests so they are excluded in the main if
                if (file != (
                        file_path + "/" + "request_and_test_data_connection.txt" and file_path + "/" + "ping_test.txt")):
                    a = f.read()
                    # os.stat(file).st_size == 0 means that the report file is empty
                    if ((('E_GENERIC_FAILURE' or 'moderm no response' or 'Segmentation fault') in a
                         or 'Request completed: E_SUCCESS' not in a)
                            or os.stat(file).st_size == 0):
                        # os.path.basename(file)[:-4] takes the report name from the file path and excludes .txt                    
                        f.write("\n\n")
                        f.write("____________________________________________________________________ \n")
                        f.write(os.path.basename(file)[:-4])
                        f.write(" FAILED \n")
                        f.write("____________________________________________________________________")
                        continue

                    # if a read file is not from the RIL functions which are running in inf loop:
                    elif (file == file[0] or file == file[1] or file == file[3] or file == file[4]):
                        # non-inf-loop RIL functions can be stuck in inf loop if there is no SIM card for example
                        # so test should be failed
                        if (subprocess.TimeoutExpired):
                            f.write("\n\n")
                            f.write("____________________________________________________________________ \n")
                            f.write(os.path.basename(file)[:-4])
                            f.write(" FAILED \n")
                            f.write("____________________________________________________________________")
                            continue

                    else:
                        f.write("\n\n")
                        f.write("____________________________________________________________________ \n")
                        f.write(os.path.basename(file)[:-4])
                        f.write(" PASSED \n")
                        f.write("____________________________________________________________________")
                        continue

                elif (file == (file_path + "/" + "ping_test.txt")):
                    a = f.read()
                    if (('PING' and 'bytes from' and 'icmp_seq=1') in a):
                        f.write("\n\n")
                        f.write("____________________________________________________________________ \n")
                        f.write(os.path.basename(file)[:-4])
                        f.write(" PASSED")
                        f.write("\n____________________________________________________________________")
                        continue

                    else:
                        f.write("\n\n")
                        f.write("____________________________________________________________________ \n")
                        f.write(os.path.basename(file)[:-4])
                        f.write(" FAILED \n")
                        f.write("____________________________________________________________________")
                        continue

                elif (file == file_path + "/" + "request_and_test_data_connection.txt"):
                    a = f.read()
                    if (("Request completed: E_SUCCESS" and "addresses:" and "dnses:" and "gateways:") in a):
                        f.write("\n\n")
                        f.write("____________________________________________________________________ \n")
                        f.write(os.path.basename(file)[:-4])
                        f.write(" PASSED")
                        f.write("\n____________________________________________________________________")
                        continue

                    else:
                        f.write("\n\n")
                        f.write("____________________________________________________________________ \n")
                        f.write(os.path.basename(file)[:-4])
                        f.write(" FAILED \n")
                        f.write("____________________________________________________________________")
                        continue

    except subprocess.TimeoutExpired:
        print("RIL function FAILED: timeout expired")


def printMenu():
    print("\n Choose the action for the script: \n")
    print("[1] Run request_operator test")
    print("[2] Run request_get_sim_status test")
    print("[3] Run request_setup_data_call test")
    print("[4] Run request_radio_power test")
    print("[5] Run request_send_sms test")
    print("[6] Run request_and_test_data_connection + ping test")
    print("[7] Run all the tests at once")
    print("[0] Exit  \n")


cmd = [
    "adb shell request_operator",
    "adb shell request_get_sim_status",
    "adb shell request_setup_data_call -a ",
    "adb shell request_radio_power",
    "adb shell request_send_sms "
]
# the last 3 files should remain on those positions for successful execution
file = [
    file_path + "/" + "request_operator.txt",
    file_path + "/" + "request_get_sim_status.txt",
    file_path + "/" + "request_setup_data_call.txt",
    file_path + "/" + "request_radio_power.txt",
    file_path + "/" + "request_send_sms.txt",
    file_path + "/" + "request_and_test_data_connection.txt",
    file_path + "/" + "ping_test.txt",
    file_path + "/" + "ping_test_google_com.txt",
]


while (True):
    if (isPrinted):
        printMenu()

        i = int(input())

        if (i == 1):
            execSingleRIL(cmd[0], file[0], 60)
            checkLogs(file[0])

        elif (i == 2):
            execSingleRIL(cmd[1], file[1], 60)
            checkLogs(file[1])

        elif (i == 3):
            if sys.platform == 'win32':
                try:
                    operator = input_with_timeout("Input the name of the operator, e.g. vipmobile: ", 10)
                except TimeoutExpired:
                    print('Timeout expired')
                else:
                    print("Operator vipmobile is chosen by default")
          
            elif sys.platform == 'linux':
                try:
                    operator = wait_for_input("Input the name of the operator, e.g. vipmobile: ", 10)
                except TimeoutExpired:
                    print('Timeout expired')
                else:
                    print("\n Operator vipmobile is chosen by default \n")
          
            if operator == "":
                operator = "vipmobile"
            cmd[2] = cmd[2] + operator
            execSingleRIL(cmd[2], file[2], 60)
            checkLogs(file[2])

        elif (i == 4):
            execSingleRIL(cmd[3], file[3], 60)
            checkLogs(file[3])

        elif (i == 5):
            if sys.platform == 'win32':
                try:
                    phoneNumber = input_with_timeout("Enter phone number: ", 10)
                except TimeoutExpired:
                    print('Timeout expired')
                else:
                    print("\n Phone number 381649402195 is chosen by default \n")
               
            if sys.platform == 'linux':        
                try:
                    operator = wait_for_input("Enter phone number: ", 10)
                except TimeoutExpired:
                    print('Timeout expired')
                else:
                    print("\n Phone number 381649402195 is chosen by default \n")        
                    
            # phoneNumber = input("Enter phone number (without + sign): ")
            if phoneNumber == "":
                phoneNumber = "381649402195"
            cmd[4] = cmd[4] + phoneNumber
            execSingleRIL(cmd[4], file[4], 60)
            checkLogs(file[4])

        elif (i == 6):
            # t1 = Thread(target = pingTest, args = ("8.8.8.8", file[6]))
            # t2 = Thread(target = pingTest, args = ("www.google.com", file[7]))
            # t1.start()
            # t1.join()
            # t2.start()
            # t2.join()
            asyncio.run(main())
            checkPingLogs(file[5])
            checkPingLogs(file[6])
            checkPingLogs(file[7])

        elif (i == 7):
            asyncio.run(main())
            
            execAllRIL(cmd, file, 60)
            checkAllLogs(file)

        elif (i == 0):
            break

        else:
            print("\n Invalid case \n")
