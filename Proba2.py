import re
import pandas as pd
from Format2 import FormattingAndExcelCreating
import subprocess

import os

# global variables
input_file          = "input.txt"
module_dir          = "/etc"
module_dir_app      = "/etc/atinout"
module_dir_out      = "/etc/output.txt"
module_dir_in       = "/etc/input.txt"
app_name            = "atinout"
port_name           = "/dev/smd10"

# subprocesses run from the CMD
process1 = subprocess.run(["adb", "push", app_name, module_dir], stdout=subprocess.PIPE)
process2 = subprocess.run(["adb", "shell", "chmod", "+x", module_dir_app], stdout=subprocess.PIPE)
process3 = subprocess.run(["adb", "push", input_file, module_dir], stdout=subprocess.PIPE)
process4 = subprocess.run(["adb", "shell", module_dir_app, module_dir_in, port_name, module_dir_out], stdout=subprocess.PIPE)
process5 = subprocess.run(["adb", "pull", module_dir_out], stdout=subprocess.PIPE)
process6 = subprocess.run(["adb", "shell", "rm", module_dir_in], stdout=subprocess.PIPE)
process7 = subprocess.run(["adb", "shell", "rm", module_dir_out], stdout=subprocess.PIPE)
process8 = subprocess.run(["adb", "shell", "rm", module_dir_app], stdout=subprocess.PIPE)

## Removing files which are created with last script run, if files are not created then notification appears
if os.path.exists("Output.xlsx"):
    os.remove("Output.xlsx")
else:
  print("The file - Output.xlsx - does not exist")

ExcelName = "Output.xlsx"
sheet = "Log" 
filename_expected = "expected.txt"
filename_output = "output.txt" 
filename_input = "input.txt"

f_expected = open(filename_expected, "r")
f_output = open(filename_output, "r")
f_input = open(filename_input, "r")


expected = re.split("\nat|\nAT", f_expected.read())
output = re.split("\nat|\nAT", f_output.read())
inp = re.split("\nat|\nAT", f_input.read())

# If ATE0 is the first command and ATE1 the second then the both commands will be
# parsed as only one member in the list, so it needs to be divided into two list members
if output[0] == "ATE0\nOK\n\nOK":
    expected = ["ATE0\nOK", "\nOK"] + expected[1:]
    output = ["ATE0\nOK", "\nOK"] + output[1:]
elif output[0] == "\nOK\n\nOK":
    expected = ["\nOK", "\nOK"] + expected[1:]
    output = ["\nOK", "\nOK"] + output[1:]
else:
    print("ATE0 doesn't return good feedback, please exclude ATE0 from the input.txt!")

print('OUTPUT:      ', len(output))
print('EXPECTED:    ', len(expected))
print('INPUT:       ', len(inp))


result=[]
for i, j in zip(expected, output):
    if ": Regex" in i:
        result.append("PASS" if bool(re.search(i.strip(": Regex"),j))==True else "FAIL")
    else:
        result.append("PASS" if i==j else "FAIL")

# After report, print the percentage of successful cases
pass_nr = str(result.count("PASS"))
fail_nr = str(result.count("FAIL"))
percentage = str(round(result.count("PASS")/len(result) * 100, 2))

## Creating DataFrame with four columns
df = pd.DataFrame()

# Add columns to data frame
df["Input"] = inp
df["Expected results"] = expected
df["Response"] = output
df["Result"] = result

# Remove "AT" from the first row for each column to equivavelent with other rows
df.loc[0] = df.loc[0].str.strip("AT")

# Add "AT" to each row of "Input" column
df["Input"] = "AT" + df["Input"]

# Add "AT" to each row of "Expected results" column
df["Expected results"] = "AT" + df["Expected results"]

# Add "AT" to each row of "Response" column
df["Response"] = "AT" + df["Response"]

# Remove "AT" from the first row for the columns "Response" and "Expected result"
df.loc[1, "Response"] = df.loc[1, "Response"].strip("AT")
df.loc[1, "Expected results"] = df.loc[1, "Expected results"].strip("AT")

# If echo is turned off before script starts, then it is neccessary to present ATE0 in
# the "Response" and "Expected result" columns without "AT"
if output[0] == "\nOK":
    df.loc[0, "Expected results"] = "\nOK"
    df.loc[0, "Response"] = "\nOK"

# Formatting and excel creating
writer = pd.ExcelWriter(ExcelName, engine="xlsxwriter")
# Write to excel table
df.to_excel(writer, sheet, index=False)

## Formatting of DataFrame (Excel)
FormattingAndExcelCreating(df, sheet, writer, pass_nr, fail_nr, percentage)

print('Output.xlsx created!')
