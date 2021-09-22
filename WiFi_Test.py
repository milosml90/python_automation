import subprocess
import sys
original = sys.stdout

with open("wifi_output.txt", "w") as f:
            p1 = subprocess.Popen(["adb", "shell", "/etc/init.d/wlan start"], stdin=subprocess.PIPE, stdout = f, stderr = f)
            _stdout = p1.communicate(input = b"------------------WLAN start test------------------\n\n")[0]
            p2 = subprocess.Popen(["adb", "shell", "hostapd -dddd /data/misc/wifi/hostapd.conf"], stdin=subprocess.PIPE, stdout = f, stderr = f)
            _stdout = p2.communicate(input = b"\n------------------hostapd test------------------\n\n")[0]
            p3 = subprocess.Popen(["adb", "shell", "ifconfig wlan0 192.168.1.1 netmask 255.255.255.0 up"], stdin=subprocess.PIPE, stdout = f, stderr = f)
            _stdout = p3.communicate(input = b"\n------------------ifconfig AP mode test------------------\n\n")[0]
            p4 = subprocess.Popen(["adb", "shell", "ifconfig wlan0 192.165.100.123 up"], stdin=subprocess.PIPE, stdout = f, stderr = f)
            _stdout = p4.communicate(input = b"\n------------------ifconfig station mode test------------------\n\n")[0]
            p5 = subprocess.Popen(["adb", "shell", "wpa_supplicant Dnl80211 iwlan0 c /data/misc/wifi wpa_supplicant.conf"], stdin=subprocess.PIPE, stdout = f, stderr = f)
            _stdout = p5.communicate(input = b"\n------------------wpa supplicant test------------------\n\n")[0]