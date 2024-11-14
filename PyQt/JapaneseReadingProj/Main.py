import binascii
from fileinput import close
import struct
import base64
import json
import os,sys
import re, time
import threading
import random
from datetime import datetime

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QMessageBox, QButtonGroup
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import shutil
from ReadJapanese_ui import Ui_MainWindow
from PyTTSInterface import PyTTSInterface

#pyinstaller -F -w -i kent.ico  SyncTwoDiskFiles.py	

deleteArray = []
global btnChineMode
dictCont = {}
jpTTS = PyTTSInterface("Japanese", 100, 1.0)

def ReadFunc(file):
    with open(file, "r", encoding='utf-8') as fp:
        contentLines = fp.readlines()
        lineLen = len(contentLines)
        for index in range(lineLen):
            if index == lineLen -1:
                pass
            else:
                contentPre = contentLines[index]
                contentNext = contentLines[index+1]
                if len(contentPre) > 1 and len(contentNext) > 1:
                    dictCont[contentPre] = contentNext
        fp.close()

keyArray = []
contArray = []
pageSize = 0
def ChangeContext(file):
    global keyArray
    global contArray
    global pageSize
    ReadFunc(file)
    pageSize = len(dictCont)
  
    nums = []
    for key, val in dictCont.items():
        keyArray.append(key)
        if len(val) > 18:
            val = val[0:18]
        contArray.append(val)
    
global selectNum 
global selectId
@pyqtSlot()
def Reflesh(ui):
    global pageSize
    global selectNum 
    global selectId
    global keyArray
    global contArray
    nums = list(range(1, pageSize))
    randomNums = random.sample(nums, 18)
    selectNum = random.choice(randomNums)
    showBtnArray = []
    showTextArray = []
    if not btnChineMode:
        showBtnArray = keyArray
        showTextArray = contArray
    else:
        showBtnArray = contArray
        showTextArray = keyArray
    ui.pushButton_1.setText(showBtnArray[randomNums[0]])
    ui.pushButton_2.setText(showBtnArray[randomNums[1]])
    ui.pushButton_3.setText(showBtnArray[randomNums[2]])
    ui.pushButton_4.setText(showBtnArray[randomNums[3]])
    ui.pushButton_5.setText(showBtnArray[randomNums[4]])
    ui.pushButton_6.setText(showBtnArray[randomNums[5]])
    ui.pushButton_7.setText(showBtnArray[randomNums[6]])
    ui.pushButton_8.setText(showBtnArray[randomNums[7]])
    ui.pushButton_9.setText(showBtnArray[randomNums[8]])
    ui.pushButton_10.setText(showBtnArray[randomNums[9]])
    ui.pushButton_11.setText(showBtnArray[randomNums[10]])
    ui.pushButton_12.setText(showBtnArray[randomNums[11]])
    ui.pushButton_13.setText(showBtnArray[randomNums[12]])
    ui.pushButton_14.setText(showBtnArray[randomNums[13]])
    ui.pushButton_15.setText(showBtnArray[randomNums[14]])
    ui.pushButton_16.setText(showBtnArray[randomNums[15]])
    ui.pushButton_17.setText(showBtnArray[randomNums[16]])
    ui.pushButton_18.setText(showBtnArray[randomNums[17]])
    for index in range(18):
        if randomNums[index] == selectNum:
            selectId = index + 1
            break
        
    ui.plainTextEdit.clear()
    font = QFont("MS Gothic")
    ui.plainTextEdit.setFont(font)
    ui.plainTextEdit.setPlainText(showTextArray[selectNum])
    if btnChineMode:
        ttsText = ""
        if "|" in showTextArray[selectNum]:
            ttsText = showTextArray[selectNum].split("|")[1]
        else: 
            ttsText = showTextArray[selectNum]
        replaceList = ["③", "◎", "①", "②"]
        for trRp in replaceList:
            ttsText = ttsText.replace(trRp,"")
        jpTTS.playAudioCont(ttsText)
    styleGrey = "background-color: grey; font-size: 24px;text-align: center; padding-top: 50px; padding-bottom: 50px;"
    ui.btnNext.setStyleSheet(styleGrey)

global buttonGroup
global tmPrevious
@pyqtSlot()
def PyQtBtnClicked(button):
    global buttonGroup
    global selectId 

    btnId = buttonGroup.id(button)
    styleRed = "background-color: red; font-size: 24px;text-align: center; padding-top: 50px; padding-bottom: 50px;"
    styleCor = "background-color: green; font-size: 24px;text-align: center; padding-top: 50px; padding-bottom: 50px;"
    
    if btnId == selectId:
        ui.btnNext.setStyleSheet(styleCor)
        Reflesh(ui)
    else:
        ui.btnNext.setStyleSheet(styleRed)
   
@pyqtSlot()
def PyQtBtnPressed(id):
    global tmPrevious
    tmPrevious = time.time()

@pyqtSlot()
def PyQtBtnReleased(button):
    global tmPrevious
    timesCur = time.time()
    if timesCur - tmPrevious > 1:
        text = button.text()
        deleteArray.append(text)
        ui.textBrowser.append(text)

@pyqtSlot()
def ShowModeChangeSlot():
    global btnChineMode
    if btnChineMode == False:
        btnChineMode = True
        ui.btnType.setText("Japanese")
    else:
        btnChineMode = False
        ui.btnType.setText("Chinese")

@pyqtSlot()
def TimerLabelSlot():
    curTime = datetime.now()
    tmString = curTime.strftime("%Y-%m-%d %H:%M:%S")
    ui.label.setText(tmString)

@pyqtSlot()
def DeleteText():
    curTime = datetime.now()
    tmString = curTime.strftime("%Y_%m_%d_%H_%M")
    if len(deleteArray) == 0:
        return
    # currentPath = os.path.dirname(os.path.abspath(__file__))
    # japanBackFile = currentPath + os.sep + "backFiles" + os.sep + "backList.txt"
    # japaneseFile = currentPath + os.sep + "backFiles" + os.sep + "Japanese.txt"
    japaneseFile = "C:\\worksrc\\PythonCode\\JapaneseReadingProj\\backFiles\\Japanese.txt"
    japanBackFile = "C:\\worksrc\\PythonCode\\JapaneseReadingProj\\backFiles\\backList.txt"
    contentLines = []
    with open(japaneseFile, "r", encoding='utf-8') as fp:
        contentLines = fp.readlines()
    contLen = len(contentLines)
    contLinesArray = []
    for detelVal in deleteArray:
        for index in range(contLen):
            if detelVal in contentLines[index]:
                if index > 0 and len(contentLines[index - 1]) > 2:
                    contLinesArray.append(index-1)
                if index != (contLen - 1) and len(contentLines[index + 1]) > 2:
                    contLinesArray.append(index)

    delContent = []
    skipLines = []
    for delLine in contLinesArray:
        delContent.append(contentLines[delLine])
        delContent.append(contentLines[delLine + 1])
        delContent.append("\n")
        skipLines.append(delLine)
        skipLines.append(delLine + 1)
        skipLines.append(delLine + 2)
        # del contentLines[delLine]
        # del contentLines[delLine + 1]
        # del contentLines[delLine + 2]

    newContent = []
    for index in range(contLen):
        bSkip = False
        for skip in skipLines:
            if index == skip:
                bSkip = True
        if bSkip == False:
            newContent.append(contentLines[index])
    
    with open(japanBackFile, "a+", encoding='utf-8') as fp:
        for back in delContent:
            fp.write(back)
        fp.close()
    with open(japaneseFile, "w", encoding='utf-8') as fp:
        for cont in newContent:
            fp.write(cont)
        fp.close()
    # with open("D:\\ZhouyouGithub\\GitLab_Jimi\\PyQt\\JapaneseReadingProj\\backLog\\" + \
    #             tmString + ".txt", "w", encoding='utf-8') as fp:
    #     for array in deleteArray:
    #         fp.write(array)
    #         fp.write("\n")
    #     fp.close()

@pyqtSlot()
def ShowAnswer():
    global dictCont
    text = ui.plainTextEdit.toPlainText()
    showText = ""
    for key,value in dictCont.items():
        if text in key:
            showText = value
            break
        if text in value:
            showText = key
            break

    msgBox = QMessageBox()
    msgBox.setText(showText)
    msgBox.setStandardButtons(QMessageBox.Ok)
    msgBox.buttonClicked.connect(QMessageBox.close)
    msgBox.exec_()

if __name__ == '__main__':
    # currentPath = os.getcwd() 
    # japaneseFile = currentPath + os.sep + "backFiles" + os.sep + "Japanese.txt"
    japaneseFile = "C:\\worksrc\\PythonCode\\JapaneseReadingProj\\backFiles\\Japanese.txt"
    ChangeContext(japaneseFile)

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    btnChineMode = False
    font = QFont("SimHei")
    ui.pushButton_1.setFont(font)
    ui.pushButton_2.setFont(font)
    ui.pushButton_3.setFont(font)
    ui.pushButton_4.setFont(font)
    ui.pushButton_5.setFont(font)
    ui.pushButton_6.setFont(font)
    ui.pushButton_7.setFont(font)
    ui.pushButton_8.setFont(font)
    ui.pushButton_9.setFont(font)
    ui.pushButton_10.setFont(font)
    ui.pushButton_11.setFont(font)
    ui.pushButton_12.setFont(font)
    ui.pushButton_13.setFont(font)
    ui.pushButton_14.setFont(font)
    ui.pushButton_15.setFont(font)
    ui.pushButton_16.setFont(font)
    ui.pushButton_17.setFont(font)
    ui.pushButton_18.setFont(font)
    style = "color: rgb(0,0,139); font-size: 12px;text-align: left; padding-top: 50px; padding-bottom: 50px;"
    ui.plainTextEdit.setStyleSheet("font-size: 16px;text-align: center")
    ui.textBrowser.setStyleSheet("font-size: 13px; color: rgb(0,0,139)")
    ui.btnType.setStyleSheet("font-size: 12px;text-align: center")
    ui.btnDelete.setStyleSheet("font-size: 16px;text-align: center")
    ui.btnAns.setStyleSheet("font-size: 16px;text-align: center")
    ui.pushButton_1.setStyleSheet(style)
    ui.pushButton_2.setStyleSheet(style) 
    ui.pushButton_3.setStyleSheet(style) 
    ui.pushButton_4.setStyleSheet(style) 
    ui.pushButton_5.setStyleSheet(style) 
    ui.pushButton_6.setStyleSheet(style) 
    ui.pushButton_7.setStyleSheet(style) 
    ui.pushButton_8.setStyleSheet(style) 
    ui.pushButton_9.setStyleSheet(style) 
    ui.pushButton_10.setStyleSheet(style)
    ui.pushButton_11.setStyleSheet(style)
    ui.pushButton_12.setStyleSheet(style)
    ui.pushButton_13.setStyleSheet(style)
    ui.pushButton_14.setStyleSheet(style)
    ui.pushButton_15.setStyleSheet(style)
    ui.pushButton_16.setStyleSheet(style)
    ui.pushButton_17.setStyleSheet(style)
    ui.pushButton_18.setStyleSheet(style)
    buttonGroup = QButtonGroup()
    buttonGroup.addButton(ui.pushButton_1, 1)
    buttonGroup.addButton(ui.pushButton_2, 2)
    buttonGroup.addButton(ui.pushButton_3, 3)
    buttonGroup.addButton(ui.pushButton_4, 4)
    buttonGroup.addButton(ui.pushButton_5, 5)
    buttonGroup.addButton(ui.pushButton_6, 6)
    buttonGroup.addButton(ui.pushButton_7, 7)
    buttonGroup.addButton(ui.pushButton_8, 8)
    buttonGroup.addButton(ui.pushButton_9, 9)
    buttonGroup.addButton(ui.pushButton_10, 10)
    buttonGroup.addButton(ui.pushButton_11, 11)
    buttonGroup.addButton(ui.pushButton_12, 12)
    buttonGroup.addButton(ui.pushButton_13, 13)
    buttonGroup.addButton(ui.pushButton_14, 14)
    buttonGroup.addButton(ui.pushButton_15, 15)
    buttonGroup.addButton(ui.pushButton_16, 16)
    buttonGroup.addButton(ui.pushButton_17, 17)
    buttonGroup.addButton(ui.pushButton_18, 18)
    buttonGroup.buttonClicked.connect(PyQtBtnClicked)
    buttonGroup.buttonReleased.connect(PyQtBtnReleased)
    buttonGroup.buttonPressed.connect(PyQtBtnPressed)
    ui.btnType.clicked.connect(ShowModeChangeSlot)
    ui.btnDelete.clicked.connect(DeleteText)
    ui.btnAns.clicked.connect(ShowAnswer)
    timer = QTimer()
    timer.timeout.connect(TimerLabelSlot)
    timer.start(100)
    Reflesh(ui)
    MainWindow.show()
    sys.exit(app.exec_())

