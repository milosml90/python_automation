import subprocess
from subprocess import call
import tkinter as tk
import tkinter.filedialog
import os
from fileinput import filename
import wx

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
        


class wxFrame(wx.Frame):
    """
    A Frame that says Hello World
    """

    def __init__(self, *args, **kw):
        # ensure the parent's __init__ is called
        super(wxFrame, self).__init__(*args, **kw)

        # create a panel in the frame
        pnl = wx.Panel(self)

        # put some text with a larger bold font on it
        # st = wx.StaticText(pnl, label="Hello World!")
        # font = st.GetFont()
        # font.PointSize += 10
        # font = font.Bold()
        # st.SetFont(font)

        # and create a sizer to manage the layout of child widgets
        # sizer = wx.BoxSizer(wx.VERTICAL)
        # sizer.Add(st, wx.SizerFlags().Border(wx.TOP|wx.LEFT, 25))
        # pnl.SetSizer(sizer)

        # create a menu bar
        self.makeMenuBar()

        # and a status bar
        self.CreateStatusBar()
        self.SetStatusText("Status text")


    def makeMenuBar(self):
        """
        A menu bar is composed of menus, which are composed of menu items.
        This method builds a set of menus and binds handlers to be called
        when the menu item is selected.
        """

        # Make a file menu with Hello and Exit items
        fileMenu = wx.Menu()
        # The "\t..." syntax defines an accelerator key that also triggers
        # the same event
        helloItem = fileMenu.Append(-1, "&Hello...\tCtrl-H",
                "Help string shown in status bar for this menu item")
        fileMenu.AppendSeparator()
        # When using a stock ID we don't need to specify the menu item's
        # label
        exitItem = fileMenu.Append(wx.ID_EXIT)

        # Now a help menu for the about item
        helpMenu = wx.Menu()
        aboutItem = helpMenu.Append(wx.ID_ABOUT)

        # Make the menu bar and add the two menus to it. The '&' defines
        # that the next letter is the "mnemonic" for the menu item. On the
        # platforms that support it those letters are underlined and can be
        # triggered from the keyboard.
        menuBar = wx.MenuBar()
        menuBar.Append(fileMenu, "&File")
        menuBar.Append(helpMenu, "&Help")

        # Give the menu bar to the frame
        self.SetMenuBar(menuBar)

        # Finally, associate a handler function with the EVT_MENU event for
        # each of the menu items. That means that when that menu item is
        # activated then the associated handler function will be called.
        self.Bind(wx.EVT_MENU, self.OnHello, helloItem)
        self.Bind(wx.EVT_MENU, self.OnExit,  exitItem)
        self.Bind(wx.EVT_MENU, self.OnAbout, aboutItem)
        # self.Bind(wx.EVT_MENU, self.onButton, buttonItem)


    def OnExit(self, event):
        """Close the frame, terminating the application."""
        self.Close(True)


    def OnHello(self, event):
        """Say hello to the user."""
        wx.MessageBox("Hello again from wxPython")


    def OnAbout(self, event):
        """Display an About Dialog"""
        wx.MessageBox("This is a wxPython Hello World sample",
                      "About Hello World 2",
                      wx.OK|wx.ICON_INFORMATION)
        
    def onButton(self, event):
        print ("Button pressed.")


if __name__ == '__main__':
    # When this module is run (not imported) then create the app, the
    # frame, show it, and start the event loop.
    app = wx.App()
    frm = wxFrame(None, title='Script Processing')
    frm.SetDimensions(0,0,200,70)
    panel = wx.Panel(frm, wx.ID_ANY)
    button = wx.Button(panel, wx.ID_ANY, 'Test', (10, 10))
    # button.Bind(wx.EVT_BUTTON, onButton())
    
    frm.Show()
    app.MainLoop()
    
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



