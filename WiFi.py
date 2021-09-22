import time
import subprocess
import shlex
import sys
from threading import Timer
import os
import tkinter as tk
import tkinter.filedialog


with open("wifi.txt", "w") as f:
    subprocess.run(["adb", "shell", "/etc/init.d/wlan", "start"], stdout = f, stderr = f)
    subprocess.run(["adb", "shell", "hostapd", "-dddd", "/data/misc/wifi/hostapd.conf"], stdout = f, stderr = f)
    subprocess.run(["adb", "shell", "ifconfig", "wlan0", "192.168.1.1", "netmask", "255.255.255.0", "up"], stdout = f, stderr = f)
    subprocess.Popen(["adb", "shell", "btproperty", "&"], stdout = f, stderr = f)
    subprocess.run(["adb", "shell", "btapp", ], stdout = f, stderr = f)
    subprocess.run(["adb", "shell", "gap_menu"], stdout = f, stderr = f)
    subprocess.run(["adb", "shell", "enable"], stdout = f, stderr = f)