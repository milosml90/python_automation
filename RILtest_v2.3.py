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
import msvcrt


# escapes = ''.join([chr(char) for char in range(1, 32)])
escape = ''.join(chr(27)) # character generated in the report file which should be removed

command = [";", "ping", "8.8.8.8"] # a string which should be concatenated to the Linux command since ping should be repeated x times
command2 = [";", "ping", "www.google.com"] # a string which should be concatenated to the Linux command since ping should be repeated x times
res = []
isPrinted = True
timeout = 15
operator = ""

# operator = "vipmobile"
# operator = "internet"
# phoneNumber = "381649402195"
# phoneNumber = "001010123456793"
# phoneNumber = "220052131091208"

print("Choose the path where reports will be saved to: \n") 

root = tk.Tk() # used for creation of GUI file dialog
root.withdraw() # use to hide tkinter window

currdir = os.getcwd()
file_path = tk.filedialog.askdirectory(parent=root, initialdir=currdir, title='Please select a directory')

# concatenate ping command 100 times to ensure it will return some bytes
# until data connection is established
def repeatCommand(command):
    for i in range(70):
        for x in command:
            res.append(x)
    return res

class Error(Exception):
    """Base class for other exceptions"""
    pass

class RILFailure(Error):
    pass


class TimeoutExpired(Exception):
    pass


def input_with_timeout(prompt, timeout, timer=time.monotonic):
    sys.stdout.write(prompt)
    sys.stdout.flush()
    endtime = timer() + timeout
    result = []
    while timer() < endtime:
        if msvcrt.kbhit():
            result.append(msvcrt.getwche()) #XXX can it block on multibyte characters?
            if result[-1] == '\r':
                return ''.join(result[:-1])
        time.sleep(0.04) # just to yield to other processes/threads
    raise TimeoutExpired
        

def execAllRIL(cmd, file, timeout):
    # the last 3 files should not be read, those have to be executed the other way
    if(len(cmd) == len(file[:-3])): 
        for i in range(len(cmd)):
            try:
                with open(file[i], "w") as f:
                    if(i == 2):
                        operator = input("Input the name of the operator, e.g. vipmobile: ")
                        if(operator == ""):
                            operator = "vipmobile"
                        print("Chosen operator: ", operator)
                        subprocess.run(cmd[2] + " " + operator, stdout = f, stderr = f, timeout = timeout)
                        
                    if(i == 4):
                        phoneNumber = input("Enter phone number: ")
                        if(phoneNumber == ""):
                            phoneNumber = "381649402195"
                        print("Chosen phone number: ", phoneNumber)  
                        subprocess.run(cmd[4] + " " + phoneNumber, stdout = f, stderr = f, timeout = timeout)  
                        
                    subprocess.run(shlex.split(cmd[i]), stdout = f, stderr = f, timeout = timeout)
            except subprocess.TimeoutExpired:
                print(os.path.basename(file[i])[:-4], ' timeout expired')  
                with open(file[i], "a+") as f:
                    f.write('\n TIMEOUT EXPIRED \n')                          
                               
    else:
        raise RILFailure("Lengths of cmd and file must be the same!")
    

def execSingleRIL(cmd, file, timeout):               
    try:
        with open(file, "w") as f:
            subprocess.run(shlex.split(cmd), stdout = f, stderr = f, timeout = timeout)
    except subprocess.TimeoutExpired:
        print(os.path.basename(file)[:-4], ' timeout expired')  
        with open(file, "a+") as f:
            f.write('\n TIMEOUT EXPIRED \n')   
            

def pingTest():
    operator = ""
    kill = lambda process: process.kill()
  
    try:
        operator = input_with_timeout("Input the name of the operator, e.g. vipmobile: ", 10)
    except TimeoutExpired:
        print('Timeout expired')
    else:
        print("Operator vipmobile is chosen by default")
    # operator = input("Input the name of the operator, e.g. vipmobile: ")

    if(operator == ""):
        operator = "vipmobile"
    print("\nChosen operator: ", operator)
    with open(file_path + "/" + "request_and_test_data_connection.txt", "w") as f:
        with open(file_path + "/" + "ping_test.txt", "w") as g:
            with open(file_path + "/" + "ping_test_google_com.txt", "w") as h:
                rtdc = subprocess.Popen(["adb", "shell", "request_and_test_data_connection", "-a", operator], stdout = f, stderr = f)
                startTime = time.time()
                while(time.time() - startTime < 10):
                    ping = subprocess.Popen(["adb", "shell", "ping", "8.8.8.8"], stdout = g, stderr = g)
                    ping2 = subprocess.Popen(["adb", "shell", "ping", "www.google.com"], stdout = h, stderr = h)
                # ping = subprocess.Popen(["adb", "shell", "ping", "8.8.8.8", " ".join(repeatCommand(command))], stdout = g, stderr = g)
                # ping2 = subprocess.Popen(["adb", "shell", "ping", "www.google.com", " ".join(repeatCommand(command2))], stdout = h, stderr = h)

                my_timer = Timer(60, kill, [rtdc])
                my_timer2 = Timer(60, kill, [ping])
                my_timer3 = Timer(60, kill, [ping2])

                try:
                    my_timer.start()
                    my_timer2.start()
                    my_timer3.start()
                    rtdc.communicate()
                    ping.communicate()
                    ping2.communicate()
                finally:
                    my_timer.cancel()
                    my_timer2.cancel()
                    my_timer3.cancel()


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
                        if(('PING' and 'bytes from' and 'icmp_seq=1') in a):
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
                if(("Request completed: E_SUCCESS" and "addresses:" and "dnses:" and "gateways:") in a):
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
                if (file != (file_path + "/" + "request_and_test_data_connection.txt" and file_path + "/" + "ping_test.txt")):
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
                    if(('PING' and 'bytes from' and 'icmp_seq=1') in a):
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
                    if(("Request completed: E_SUCCESS" and "addresses:" and "dnses:" and "gateways:") in a):
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



while(True):
    if(isPrinted):
        printMenu()

        i = int(input())

        if(i == 1):
            execSingleRIL(cmd[0], file[0], 60)
            checkLogs(file[0])
        
        elif(i==2):
            execSingleRIL(cmd[1], file[1], 60)
            checkLogs(file[1])
        
        elif(i==3):
            try:
                operator = input_with_timeout("Input the name of the operator, e.g. vipmobile: ", 10)
            except TimeoutExpired:
                print('Timeout expired')
            else:
                print("Operator vipmobile is chosen by default")
            # operator = input("Enter the name of the operator, e.g. vipmobile: ")
            if operator == "":
                operator = "vipmobile"
            cmd[2] = cmd[2] + operator
            execSingleRIL(cmd[2], file[2], 60)
            checkLogs(file[2])
        
        elif(i==4):
            execSingleRIL(cmd[3], file[3], 60)
            checkLogs(file[3])
        
        elif(i==5):
            try:
                phoneNumber = input_with_timeout("Enter phone number: ", 10)
            except TimeoutExpired:
                print('Timeout expired')
            else:
                print("Operator vipmobile is chosen by default")
            # phoneNumber = input("Enter phone number (without + sign): ")
            if phoneNumber == "":
                phoneNumber = "381649402195"
            cmd[4] = cmd[4] + phoneNumber
            execSingleRIL(cmd[4], file[4], 60)
            checkLogs(file[4])
        
        elif(i==6):         
            pingTest()
            checkPingLogs(file[5])
            checkPingLogs(file[6])
            checkPingLogs(file[7])
        
        elif(i==7):
            pingTest()
            execAllRIL(cmd, file, 60)
            checkAllLogs(file)

        elif(i == 0):
            break
            
        else:
            print("\n Invalid case \n")
            
    
