import subprocess
from subprocess import call
import tkinter as tk
import tkinter.filedialog
import os
from fileinput import filename

# global variables
moduleDir = "/etc"
fileName = ""
filePath = ""

class ScriptProcessing:
    
    def __init__(self, fileName, moduleDir, filePath):
        self.fileName = fileName
        self.moduleDir = moduleDir
        self.filePath = filePath
        
    def browseDir(self):
        print("Choose the path of the example: \n")

        root = tk.Tk()
        root.withdraw() # use to hide tkinter window

        currdir = os.getcwd()
        self.filePath = tk.filedialog.askdirectory(parent=root, initialdir=currdir, title='Please select a directory')
        print("Chosen directory: ", self.filePath, "\n") 
        print("Choose the file name for pushing to the module: \n")
        return self.filePath
        
    def browseFile(self):
        self.browseDir()
        file = tk.filedialog.askopenfilename()
        self.fileName = os.path.basename(file)
        print("Chosen file name: ", self.fileName, "\n")
        
        return self.fileName
        
    def pushScript(self):
        p = subprocess.run(["adb", "push", self.fileName, self.moduleDir], cwd = self.filePath)
        self.moduleDirApp = self.moduleDir + "/" + self.fileName
        return subprocess.run(["adb", "shell", "chmod", "777", self.moduleDirApp], cwd = self.filePath)
        
    def executeScript(self):
        self.moduleDirApp = self.moduleDir + "/" + self.fileName
        input_ = input("Enter the script arguments: ")
        args = input_.split(' ')
        subArgs = ["adb", "shell", self.moduleDirApp] + args
        subprocess.run(subArgs)
        
    def removeScript(self):
        scriptList = input("Enter the list of scripts for removal, separated by space: ")
        scriptList = filter(lambda s: s.strip() != '', scriptList.split(' '))
        for script in scriptList:
            self.moduleDirApp = self.moduleDir + "/" + script
            p = subprocess.run(["adb", "shell", "rm", self.moduleDirApp])
        return p
            
    def printMainMenu(self):
        print("\n Choose the action for the script: \n")
        print("[1] Choose the script")
        print("[2] Push the script")
        print("[3] Execute the script")
        print("[4] Remove the script")
        print("[0] Exit  \n")
        
# moduleDirApp = moduleDir + "/" + fileName
        
if __name__ == "__main__":
    
    obj = ScriptProcessing(fileName, moduleDir, filePath)
    
    while(True):
    
        obj.printMainMenu()

        i = int(input())
        
        if(i == 1):
            obj.browseFile()

        elif(i == 2):
            
            p = obj.pushScript()
            
            if (p.returncode == 0):
                print("Permission granted")
            else:
                print("Permission denied")
            
        elif(i == 3):
            obj.executeScript()        
            
        elif(i == 4):
            obj.removeScript()
            # ScriptProcessing.removeScript(obj)
            if (p.returncode == 0):
                print("The script has been removed")
            else:
                print("Unsuccessful removal of the script")
            
        elif(i == 0):
            break
            
        else:
            print("\n Invalid case \n")



