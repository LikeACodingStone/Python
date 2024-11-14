import os
import sys
import time
import pyperclip

strPathCopy = ""
strPathCopy = pyperclip.paste()     #从剪切板粘贴数据
if ":" and "\\" not in strPathCopy:
    print("Error, no path input")
    time.sleep(1)
    sys.exit()
    
strPathTitle = input("Enter Link Title >> ")
listPath = strPathCopy.split(":")
driverName = listPath[0][0].lower() + ":"
listSubPath = listPath[1:][0].split("\\")
for path in listSubPath[1:]:
    driverName = driverName + "/" + path

pastePath = "[" + strPathTitle + "]" + "(" + driverName + ")"
pyperclip.copy(pastePath)      #将数据复制到剪切板
print(pastePath)
time.sleep(1)