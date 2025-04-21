import binascii
from fileinput import close
import struct
import base64
import json
import os,sys, ctypes
import re, time
import threading
import random
from datetime import datetime

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QMessageBox, QButtonGroup
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import shutil
from Ui_ReadJapanese_free import Ui_MainWindow
from PyTTSInterface import PyTTSInterface
from ReadSentence import combined_dict

#pyinstaller -F -w -i kent.ico  SyncTwoDiskFiles.py	

deleteArray = []
global btnChineMode
dictCont = {}

# 使用 pyttsx3
# import pyttsx3
import asyncio
import edge_tts

class JapaneseTTS:
    def __init__(self):
        self.voice = "ja-JP-NanamiNeural"
        self.rate = "+0%"
        self.volume = "+0%"
        
    async def _play_audio(self, text):
        try:
            communicate = edge_tts.Communicate(text, self.voice, rate=self.rate, volume=self.volume)
            await communicate.save("temp.mp3")
            
            import pygame
            pygame.mixer.init()
            if os.path.exists("temp.mp3"):
                pygame.mixer.music.load("temp.mp3")
                pygame.mixer.music.play()
                while pygame.mixer.music.get_busy():
                    pygame.time.Clock().tick(10)
                pygame.mixer.music.unload()
                # 清理临时文件
                os.remove("temp.mp3")
        except Exception as e:
            print(f"TTS Error: {str(e)}")
            
    def playAudioCont(self, text):
        # 使用事件循环运行异步函数
        asyncio.get_event_loop().run_until_complete(self._play_audio(text))

jpTTS = JapaneseTTS()

def ReadFunc(file):
    with open(file, "r", encoding='utf-8') as fp:
        contentLines = fp.readlines()
        lineLen = len(contentLines)
        index = 0
        while index < lineLen - 1:  # 修改循环逻辑
            contentPre = contentLines[index].strip()
            contentNext = contentLines[index + 1].strip()
            if len(contentPre) > 1 and len(contentNext) > 1:
                dictCont[contentPre] = contentNext
            index += 2  # 每次跳过两行
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
global keepList
global pkeepIndex

def getRandomNum():
    global selectNum 
    global selectId
    global pageSize
    global keyArray
    global contArray
    global keepList
    global pkeepIndex

    nums = list(range(0, pageSize))
    randomNums = random.sample(nums, 6)
    selectId = random.randint(0, 5)
    selectNum = randomNums[selectId]
    return randomNums, selectNum

def getValidRandomNum():
    global selectNum 
    global selectId
    global pageSize
    global keepList
    global pkeepIndex

    while True:
        # 生成随机数组和 selectNum
        nums = list(range(0, pageSize))
        randomNums = random.sample(nums, 6)
        selectId = random.randint(0, 5)
        selectNum = randomNums[selectId]

        # 检查 selectNum 是否在最近的 keepList 中
        if selectNum not in keepList:
            # 更新 keepList，确保只保留最近的 10 个值
            if len(keepList) < 20:
                keepList.append(selectNum)
            else:
                keepList[pkeepIndex % 20] = selectNum
                pkeepIndex += 1
            return randomNums, selectNum
    
@pyqtSlot()
def Reflesh(ui):
    global pageSize
    global selectNum 
    global selectId
    global keyArray
    global contArray
    global keepList
    global pkeepIndex

    # nums = list(range(0, pageSize))
    # randomNums = random.sample(nums, 6)
    # selectId = random.randint(0, 5)
    # selectNum = randomNums[selectId]
    # if pkeepIndex < 10:
    #     keepList.append(selectNum)
    #     pkeepIndex += 1
    # else:
    #     index = pkeepIndex % 10
    #     keepList[index] = selectNum
    #     pkeepIndex += 1
    
    # for value in keepList:
    #     if value == selectNum:
    #         nums = list(range(0, pageSize))
    #         randomNums = random.sample(nums, 6)
    #         selectId = random.randint(0, 5)
    #         selectNum = randomNums[selectId]
    #         break
    randomNums, selectNum = getValidRandomNum()

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
    
    selectId += 1
    
    if btnChineMode:
        ttsText = ""
        if "|" in showTextArray[selectNum]:
            ttsText = showTextArray[selectNum].split("|")[1]
        else: 
            ttsText = showTextArray[selectNum]
        replaceList = ["③", "◎", "①", "②", "④"]
        for trRp in replaceList:
            ttsText = ttsText.replace(trRp,"")
        ttsText = preprocessJapaneseText(ttsText)
        try:
            jpTTS.playAudioCont(ttsText)
        except Exception as e:
            print(f"Error playing audio: {str(e)}")

global buttonGroup
global tmPrevious
@pyqtSlot()
def PyQtBtnClicked(button):
    global buttonGroup
    global selectId 

    btnId = buttonGroup.id(button)
    styleRed = "background-color: red; font-size: 15px;text-align: center; padding-top: 50px; padding-bottom: 50px;"
    styleCor = "background-color: green; font-size: 15px;text-align: center; padding-top: 50px; padding-bottom: 50px;"
    
    if btnId == selectId:
        global selectNum 
        global keyArray
        global contArray
        showBtnArray = []
        showTextArray = []
        if not btnChineMode:
            showBtnArray = keyArray
            showTextArray = contArray
        else:
            showBtnArray = contArray
            showTextArray = keyArray
        print(showTextArray[selectNum])
        Reflesh(ui)
        pass
    else:
        pass
   
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
    else:
        btnChineMode = False

@pyqtSlot()
def TimerLabelSlot():
    curTime = datetime.now()
    tmString = curTime.strftime("%Y-%m-%d %H:%M:%S")

@pyqtSlot()
def DeleteText():
    curTime = datetime.now()
    tmString = curTime.strftime("%Y_%m_%d_%H_%M")
    if len(deleteArray) == 0:
        return
    japaneseFile = "C:\\worksrc\\VSCODE_PROJ\\PythonCode\\JapaneseReadingProj\\backFiles\\Japanese.txt"
    japanBackFile = "C:\\worksrc\\VSCODE_PROJ\\PythonCode\\JapaneseReadingProj\\backFiles\\backList.txt"
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

# 在播放前对文本进行预处理
def preprocessJapaneseText(text):
    # 添加适当的停顿
    text = text.replace('、', '、 ')
    text = text.replace('。', '。 ')
    # 确保片假名和汉字之间有适当的间隔
    text = re.sub(r'([ァ-ン])([\u4e00-\u9fff])', r'\1 \2', text)
    return text

if __name__ == '__main__':
    if sys.platform == "win32":
        ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)
    japaneseFile = "C:\\worksrc\\VSCODE_PROJ\\PythonCode\\JapaneseReadingProj\\backFiles\\Japanese.txt"
    ChangeContext(japaneseFile)
 
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    
    MainWindow.setWindowFlags(Qt.Window | Qt.FramelessWindowHint)
    MainWindow.setAttribute(Qt.WA_TranslucentBackground)
    
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)

    # 添加关闭按钮
    closeButton = QPushButton("×", MainWindow)
    closeButton.setGeometry(MainWindow.width() - 30, 0, 30, 30)
    closeButton.clicked.connect(MainWindow.close)
    closeButton.setStyleSheet("""
        QPushButton {
            background-color: transparent;
            color: black;
            font-size: 16px;
            border: none;
        }
        QPushButton:hover {
            background-color: red;
            color: white;
        }
    """)

    # 添加播放按钮，调整位置和样式
    def replayAudio():
        global selectNum, keyArray, contArray, btnChineMode
        if btnChineMode:
            showTextArray = keyArray
            ttsText = ""
            if "|" in showTextArray[selectNum]:
                ttsText = showTextArray[selectNum].split("|")[0]
            else: 
                ttsText = showTextArray[selectNum]
            # replaceList = ["③", "◎", "①", "②", "④"]
            # for trRp in replaceList:
            #     ttsText = ttsText.replace(trRp,"")
            try:
                ttsText = ttsText.strip()
                ttsSentence = combined_dict[ttsText]
                print(ttsText, ttsSentence)
                jpTTS.playAudioCont(ttsSentence)
            except Exception as e:
                print(f"Error playing audio sentence: {str(e)}")

    playButton = QPushButton("▶", MainWindow)
    playButton.setGeometry(0, 0, 30, 30)
    playButton.setStyleSheet("""
        QPushButton {
            background-color: transparent;
            color: black;
            font-size: 20px;
            border: none;
            padding-left: 2px;
            padding-top: 0px;
        }
        QPushButton:hover {
            background-color: #4CAF50;
            color: white;
        }
    """)
    
    playButton.clicked.connect(replayAudio)

    # 添加窗口拖动功能
    class MainWindowDraggable(QtWidgets.QMainWindow):
        def mousePressEvent(self, event):
            if event.button() == Qt.LeftButton:
                self.dragPosition = event.globalPos() - self.frameGeometry().topLeft()
                event.accept()

        def mouseMoveEvent(self, event):
            if event.buttons() == Qt.LeftButton:
                self.move(event.globalPos() - self.dragPosition)
                event.accept()

    # 应用拖动功能
    MainWindow.__class__ = MainWindowDraggable

    keepList = []
    pkeepIndex = 0
    btnChineMode = True
    font = QFont("SimHei")
    ui.pushButton_1.setFont(font)
    ui.pushButton_2.setFont(font)
    ui.pushButton_3.setFont(font)
    ui.pushButton_4.setFont(font)
    ui.pushButton_5.setFont(font)
    ui.pushButton_6.setFont(font)

    style = "color: rgb(0,0,139); font-size: 15px;text-align: left; padding-top: 50px; padding-bottom: 50px;"
    ui.pushButton_1.setStyleSheet(style)
    ui.pushButton_2.setStyleSheet(style) 
    ui.pushButton_3.setStyleSheet(style) 
    ui.pushButton_4.setStyleSheet(style) 
    ui.pushButton_5.setStyleSheet(style) 
    ui.pushButton_6.setStyleSheet(style) 

    buttonGroup = QButtonGroup()
    buttonGroup.addButton(ui.pushButton_1, 1)
    buttonGroup.addButton(ui.pushButton_2, 2)
    buttonGroup.addButton(ui.pushButton_3, 3)
    buttonGroup.addButton(ui.pushButton_4, 4)
    buttonGroup.addButton(ui.pushButton_5, 5)
    buttonGroup.addButton(ui.pushButton_6, 6)
    buttonGroup.buttonClicked.connect(PyQtBtnClicked)
    buttonGroup.buttonReleased.connect(PyQtBtnReleased)
    buttonGroup.buttonPressed.connect(PyQtBtnPressed)
    timer = QTimer()
    timer.timeout.connect(TimerLabelSlot)
    timer.start(100)
    Reflesh(ui)
    MainWindow.show()
    sys.exit(app.exec_())

