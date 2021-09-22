#!/bin/bash

echo -e "\nAdb shell\n"
adb shell

echo -e "\nExit from Adb shell\n"
exit

echo -e "RebOot\n"
adb reboot

adb wait-for-device devices

echo -e "\ncat /proc/mtd\n" 
cat /proc/mtd 

echo -e "\ncat /proc/meminfo\n" 
cat /proc/meminfo 

echo -e "\nFree space\n" 
free -m 

echo -e "\nDisk space\n" 
df -ha 

echo -e "\nProcessor activity in real time\n" 
top -n 1

echo -e "\nRunning processes\n" 
ps -A 

echo -e "\nDmesg\n" 
dmesg

