import os,sys
import re, time
import threading
import configparser
from datetime import datetime

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QMessageBox, QButtonGroup
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from Ui_MainWin import Ui_MainWindow
import configparser
import subprocess

def check_adb_devices():
    try:
        result = subprocess.run(['adb', 'devices'], capture_output=True, text=True, check=True)
        output = result.stdout
        lines = output.strip().split('\n')
        if len(lines) > 1:
            for line in lines[1:]:
                if line.strip():  # 只打印非空行
                    print(line.strip())
            return True
        else:
            print("None Devices")
            
    except subprocess.CalledProcessError as e:
        print(f"Run adb Error: {e}")
    return False


def GetCurrentFolder():
    current_file_path = os.path.abspath(__file__)
    current_dir = os.path.dirname(current_file_path)
    return current_dir

def ReadConfigs(config):
    dictConfigs = {}
    configPr = configparser.ConfigParser()
    config_path = GetCurrentFolder() + os.sep + config
    configPr.read(config_path)
    bFilterMode = configPr["GENERAL"]["isFilterLog"]
    bAutoSaveMode = configPr["GENERAL"]["isAutoSaving"]
    bMonitorMode = configPr["GENERAL"]["isMonitorLog"]
    fileSize =  configPr["GENERAL"]["FILE_SIZE"]
    timeInterval =  configPr["GENERAL"]["TIME_INTERVAL"]
    fillterWord = configPr["GENERAL"]["FILTER_WORD"]
    monitorWord =  configPr["GENERAL"]["MONITOR_WORD"]

    dictConfigs["isFilterLog"] = bFilterMode
    dictConfigs["isAutoSaving"] = bAutoSaveMode
    dictConfigs["isMonitorLog"] = bMonitorMode
    dictConfigs["FILE_SIZE"] = fileSize
    dictConfigs["TIME_INTERVAL"] = timeInterval
    dictConfigs["FILTER_WORD"] = fillterWord
    dictConfigs["MONITOR_WORD"] = monitorWord

    return dictConfigs

def InitConfigAndUI(dictConfigs, ui):
    FilterWord = dictConfigs["FILTER_WORD"].split(",")
    for keyWd in FilterWord:
        ui.etdFilter.appendPlainText(keyWd)
    MonitorWord = dictConfigs["MONITOR_WORD"].split(",")
    for keyWd in MonitorWord:
        ui.edtMoKeys.appendPlainText(keyWd)
    styleRed = "background-color: red; font-size: 24px;text-align: center; padding-top: 50px; padding-bottom: 50px;"
    styleGreen = "background-color: green; font-size: 24px;text-align: center; padding-top: 50px; padding-bottom: 50px;"
    if check_adb_devices():
        ui.btnSatrt.setStyleSheet(styleGreen)
    else:
        ui.btnSatrt.setStyleSheet(styleRed)


if __name__ == '__main__':
    CONFIG = "config.ini"
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    dictConfigs = ReadConfigs(CONFIG)
    InitConfigAndUI(dictConfigs, ui)
    # ui.btnPlay.clicked.connect(SlotPlay)
    # ui.btnPause.clicked.connect(SlotPause)
    # ui.btnDel.clicked.connect(SlotDelete)
    # ui.btnBlues.clicked.connect(SlotBtnBlues)
    # ui.btnCountry.clicked.connect(SlotBtnCountry)
    # ui.btnMetal.clicked.connect(SlotBtnMetal)
    # ui.btnHard.clicked.connect(SlotBtnHardRock)
    # ui.btnPunk.clicked.connect(SlotBtnPunk)
    # ui.btnPop.clicked.connect(SlotBtnPop)
    # ui.btnNext.clicked.connect(SlotNextSong)
    # ui.btnPre.clicked.connect(SlotPreSong)
    # g_playList = []
    # g_mediaIndex = -1
    # g_folderIndex = -1
    # g_playList, g_folderIndex, g_mediaIndex = GetIniList()
    # g_audio_player = AudioPlayer(g_playList, g_mediaIndex)
    # ui.lineEdit.setText(GetMediaByIndex(g_playList, g_mediaIndex))
    MainWindow.show()
    sys.exit(app.exec_())