# import subprocess as sp
# from curses import ascii



# sp.Popen(["adb", "shell", "cat", "/dev/smd10", "&"])
# sp.Popen(["adb", "shell", "echo", "-e", "AT+CMGF=1\r\n", ">", "/dev/smd10"]) 
# sp.Popen(["adb", "shell", "echo", "-e", 'AT+CMGS="+381649402195"\r\n', ">", "/dev/smd10"]) 
# sp.Popen(["adb", "shell", "echo", "-e", "Zdravo\x1a\r\n", ">", "/dev/smd10"]) 


# import serial

# ser = serial.Serial('/dev/smd10', 115200, timeout=5)
# ser.write("AT\r")
# response =  ser.readline()
# ser.write(chr(26)) 
# ser.close()

# print (response)


import subprocess
from subprocess import call
import tkinter as tk
import tkinter.filedialog
import os

# global variables
module_dir = "/etc"
outputFile = "output.txt"
desktopPath = "C:\\Users\\Milos\\Desktop"
isPrinted = True

def pushScript(filename, moduleDir, filePath):
    p = subprocess.run(["adb", "push", filename, moduleDir], cwd = filePath)
    
def pullScript(moduleDir):
    p = subprocess.run(["adb", "pull", moduleDir, desktopPath])
    
def givePermission(moduleDirApp, filePath):
    p = subprocess.run(["adb", "shell", "chmod", "777", moduleDirApp], cwd = filePath)
    
def executeScript(filename, moduleDir):
    # executeString = "./" + filename
    moduleDirApp = moduleDir + "/" + filename
    p1 = subprocess.run(["adb", "shell", moduleDirApp])
    # p2 = subprocess.run(["cd", moduleDir])
    # p3 = subprocess.run(executeString)
    
def removeScript(moduleDirApp):
    p = subprocess.run(["adb", "shell", "rm", moduleDirApp])
    
    
def printMainMenu():
    print("\n Choose the action for the script: \n")
    print("[1] Push the script")
    print("[2] Execute the script")
    print("[3] Remove the script")
    print("[4] Pull the output file")
    print("[0] Exit  \n")

while(True):
    if(isPrinted):
        printMainMenu()

        i = int(input())

        if(i == 1):
            print("Choose the path of the script: \n")

            root = tk.Tk()
            root.withdraw() # use to hide tkinter window

            currdir = os.getcwd()
            file_path = tk.filedialog.askdirectory(parent=root, initialdir=currdir, title='Please select a directory')
            print("Chosen directory: ", file_path, "\n") 
            print("Choose the file name for pushing to the module: \n")  
            file = tk.filedialog.askopenfilename()
            file_name = os.path.basename(file)
            print("Chosen file name: ", file_name, "\n")
            module_dir_app = module_dir + "/" + file_name
            
            pushScript(file_name, module_dir, file_path)
            
            givePermission(module_dir_app, file_path)
            
            if (subprocess.CompletedProcess):
                print("Permission granted")
            else:
                print("Permission denied")
            
        elif(i == 2):
            executeScript(file_name, module_dir)        
            
        elif(i == 3):
            removeScript(module_dir_app)
            if (subprocess.CompletedProcess):
                print("The script has been removed")
            else:
                print("Unsuccessful removal of the script")
                
        elif(i == 4):
            moduleDir = module_dir + "/" + outputFile
            pullScript(moduleDir)
            
        elif(i == 0):
            break
            
        else:
            print("\n Invalid case \n")



