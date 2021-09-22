import subprocess
from subprocess import call
import tkinter as tk
import tkinter.filedialog
import os

# global variables
module_dir = "/etc"
isPrinted = True
file_name = ""
file_path = ""

def readScript():
    print("Choose the path of the example: \n")
    root = tk.Tk()
    root.withdraw() # use to hide tkinter window
    currdir = os.getcwd()
    file_path = tk.filedialog.askdirectory(parent=root, initialdir=currdir, title='Please select a directory')
    print("Chosen directory: ", file_path, "\n") 
    print("Choose the file name for pushing to the module: \n")  
    file = tk.filedialog.askopenfilename()
    file_name = os.path.basename(file)
    print("Chosen file name: ", file_name, "\n")

def pushScript(filename, moduleDir, filePath):
    p = subprocess.run(["adb", "push", filename, moduleDir], cwd = filePath)
    
def givePermission(moduleDirApp, filePath):
    p = subprocess.run(["adb", "shell", "chmod", "777", moduleDirApp], cwd = filePath)
    
def executeScript(filename, moduleDir):
    # executeString = "./" + filename
    moduleDirApp = moduleDir + "/" + filename
    p1 = subprocess.run(["adb", "shell", moduleDirApp])
    # p2 = subprocess.run(["cd", moduleDir])
    # p3 = subprocess.run(executeString)
    
def removeScript(moduleDir, filename):
    moduleDirApp = moduleDir + "/" + filename
    p = subprocess.run(["adb", "shell", "rm", moduleDirApp])
    print(p)
    
def printMainMenu():
    print("\n Choose the action for the script: \n")
    print("[1] Read the script")
    print("[2] Push the script")
    print("[3] Give permission to the script")
    print("[4] Execute the script")
    print("[5] Remove the script")
    print("[0] Exit  \n")
    

module_dir_app = module_dir + "/" + file_name

while(True):
    if(isPrinted):
        printMainMenu()

        i = int(input())

        if(i == 1):
            readScript()

        elif(i == 2):           
            pushScript(file_name, module_dir, file_path)
            
        elif(i == 3):
            givePermission(module_dir_app, file_path)
            if (subprocess.CompletedProcess):
                print("Permission granted")
            else:
                print("Permission denied")
            
        elif(i == 4):
            executeScript(file_name, module_dir)        
            
        elif(i == 5):
            removeScript(module_dir_app, file_name)
            if (subprocess.CompletedProcess):
                print("The script has been removed")
            else:
                print("Unsuccessful removal of the script")
            
        elif(i == 0):
            break
            
        else:
            print("\n Invalid case \n")



