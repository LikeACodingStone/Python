import sys, os
import subprocess
import tkinter as tk
import threading
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton,  QFileDialog
from PyQt5.QtCore import QTimer, QObject, Qt,QThread
from PyQt5.QtCore import pyqtSlot, pyqtSignal
from Ui_QtAdbLogPlugin import Ui_QtAdbLogPlugin
from BasicFunctions import CheckAdbDevices, HandleKeyWordCfg
from datetime import datetime

class TimerThread(QThread):
    tickSignal = pyqtSignal(bool)
    def run(self):
        adbStatusRecord = False
        while True:
            adbState = CheckAdbDevices()
            if adbStatusRecord != adbState:
                if adbState:
                    self.tickSignal.emit(True)
                else:
                    self.tickSignal.emit(False)
                adbStatusRecord = adbState
            self.sleep(1)
            

class AdbLogPlugin(QObject):
    def __init__(self, minWin):
        self.ui = Ui_QtAdbLogPlugin()
        self.ui.setupUi(minWin)

        super().__init__()
        # self.timer = QTimer(self)
        # self.timer.timeout.connect(self.updateAdbStatus)
  
        self.ui.btnSelFod.clicked.connect(self.BtnSelectFolder)
        self.ui.btnStart.clicked.connect(self.BtnThreadStartLogcat)
        self._adbStatus = False
        self.setLabelStatus(False)

        self._handleKeyWordCfg = HandleKeyWordCfg("KeyWord.ini")
        self._logFolder = ""
        self.setLogFolder(self._handleKeyWordCfg.readLogFolder())

        self.ui.btnSelFod.setStyleSheet("background-color: rgb(80,185,225); font-size: 16px;text-align: center;")
        self.ui.btnKeyWord.setStyleSheet("background-color: rgb(80,185,225); font-size: 15px;text-align: center;")
        self.ui.btnExit.setStyleSheet("background-color: rgb(80,85,225); font-size: 18px;text-align: center;")
        self.ui.btnStart.setStyleSheet("background-color: rgb(80,85,225); font-size: 18px;text-align: center;")

        self.ui.btnStart.setEnabled(False)
        self._adbStarted = False

        self.tmThread = TimerThread()
        self.tmThread.start()
        self.tmThread.tickSignal.connect(self.adbDevicesUpdated)

    def adbDevicesUpdated(self, bStatus):
        if self._adbStatus != bStatus:
            self._adbStatus = bStatus
            self.setLabelStatus(bStatus)

    # def startTimer(self):
    #     self.timer.start(400)
        # tmThread = threading.Thread(target=self._startLogcat, args=(,))
        # tmThread.daemon = True 
        # tmThread.start()
    # def threadStartTimer(self):
    #     tmThread = threading.Thread(target=self.startTimer, args=()) 
    #     tmThread.start()

    def stopTimer(self):
        self.timer.stop()

    # def updateAdbStatus(self):
    #     bStatus = CheckAdbDevices()
    #     if self._adbStatus != bStatus:
    #         self._adbStatus = bStatus
    #         self.setLabelStatus(bStatus)

    def _startLogcat(self, keywordList, logFolder):
        currentTime = datetime.now()
        formattedTime = currentTime.strftime("%Y_%m_%d_%H_%M_%S")
        adbLogFile = logFolder + os.sep + str(formattedTime) + ".txt"
        fpLog = open(adbLogFile, "w", encoding='utf-8', errors='ignore') 
        process = subprocess.Popen(['adb', 'logcat'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding='utf-8', errors='ignore')
        while True:
            line = process.stdout.readline()
            if not line:
                break
            for keyword in keywordList:
                if keyword.lower() in line.lower():
                    print(line)
                    #fpLog.write(line)
          
    def setLogFolder(self, folderPath):
        style = "background-color: rgb(180,85,225); font-size: 24px;text-align: center;"
        styleErr = "background-color: red; font-size: 24px;text-align: center;"
        self.ui.ldtPath.setAlignment(Qt.AlignCenter)
        if len(folderPath.strip(" ")) > 0:
            self.ui.ldtPath.setText(folderPath)
            self.ui.ldtPath.setStyleSheet(style)
            self._handleKeyWordCfg.setLogFolder(folderPath)
            self._logFolder = folderPath
        else:
            self.ui.ldtPath.setStyleSheet(styleErr)
            self.ui.ldtPath.setText("Err:  Please Select Folder")

    def setLabelStatus(self, bStatus):
        styleRed = "background-color: red; font-size: 20px;text-align: center; padding-top: 50px; padding-bottom: 50px;"
        styleGreen = "background-color: green; font-size: 20px;text-align: center; padding-top: 50px; padding-bottom: 50px;"
        self.ui.lblStatus.setAlignment(Qt.AlignCenter)
        if bStatus:
            self.ui.lblStatus.setText("ADB ON")
            self.ui.lblStatus.setStyleSheet(styleGreen)
            self.ui.btnStart.setEnabled(True)
        else:
            self.ui.lblStatus.setText("ADB OFF")
            self.ui.lblStatus.setStyleSheet(styleRed)
            self.ui.btnStart.setEnabled(False)

    def setAdbBtnStatus(self, bStart):
        if bStart:
            self.ui.btnStart.setText("Stop")
            self._adbStarted = True
        else:
            self.ui.btnStart.setText("Start")
            self._adbStarted = False
        
    def show(self):
        self.ui.show()

    @pyqtSlot()
    def BtnSelectFolder(self):
        folderPath = QFileDialog.getExistingDirectory(self.ui.centralwidget, 'Please Select Folder')
        self.setLogFolder(folderPath)
        
    @pyqtSlot()
    def BtnThreadStartLogcat(self):
        keyWordList = self._handleKeyWordCfg.readKeyWords()
        logcatThread = threading.Thread(target=self._startLogcat, args=(keyWordList, self._logFolder))
        logcatThread.daemon = True 
        logcatThread.start()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    minWin = QtWidgets.QMainWindow()
    adbPlug = AdbLogPlugin(minWin)
    # timer_thread = TimerThread()
    # timer_thread.start()
    #adbPlug.threadStartTimer()
    minWin.show()
    sys.exit(app.exec_())