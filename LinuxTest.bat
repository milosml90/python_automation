echo off
echo ### adb shell and exit ###
echo.
adb shell exit
echo.
echo ### adb reboot ###
echo.
adb reboot
echo.
echo ### adb wait-for-device devices ###
echo.
adb wait-for-device devices
echo.
echo ### The list of Linux partitions and their sizes ###
echo.
adb shell cat /proc/mtd
echo.
echo ### Memory information ###
echo.
adb shell cat /proc/meminfo
echo.
echo ### Freeing memory ###
echo.
adb shell free -m
echo.
echo ### Free disk space ###
echo.
adb shell df -ha
echo.
echo ### Processor activity in real time ###
echo.
adb shell top -n 1
echo.
echo ### Running processes ###
echo.
adb shell ps -A
echo.
echo ### Diagnostic messages ###
echo.
adb shell dmesg
echo.
echo ### Rebooting into bootloader ###
echo.
adb reboot bootloader
echo.
echo ### Flashing partitions ###
echo.
fastboot flash sbl %1\update\sbl1.mbn
fastboot flash tz %1\update\tz.mbn
fastboot flash rpm %1\update\rpm.mbn
fastboot flash aboot %1\appsboot.mbn
fastboot flash boot %1\mdm9607-boot.img
fastboot flash modem %1\NON-HLOS.ubi
fastboot flash system %1\mdm9607-sysfs.ubi
echo.
echo ### Rebooting into fastboot ###
echo.
fastboot reboot
pause >nul

