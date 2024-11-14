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

def CheckAdbDevices():
    try:
        result = subprocess.run(['adb', 'devices'], capture_output=True, text=True, check=True)
        output = result.stdout
        lines = output.strip().split('\n')
        if len(lines) > 1:
            for line in lines[1:]:
                if line.strip():
                    pass
                    #print(line.strip())
            return True
        else:
            pass
            
    except subprocess.CalledProcessError as e:
        print(f"Run adb Error: {e}")
    return False

def GetCurrentFolder():
    current_file_path = os.path.abspath(__file__)
    current_dir = os.path.dirname(current_file_path)
    return current_dir

class HandleKeyWordCfg():
    def __init__(self, cfg, deep = 25):
        self._configPr = configparser.ConfigParser()
        configPath = GetCurrentFolder() + os.sep + cfg
        self._configPr.read(configPath)
        self._deep = deep
        self._cfg = cfg

    def readKeyWords(self):
        keyWordList = []
        for index in range(self._deep):
            keyWd = "KEY_WORD_" + str(index + 1)
            keyWord = self._configPr["GENERAL"][keyWd]
            if len(keyWord.strip(" ")) > 0:
                keyWordList.append(keyWord)
        return keyWordList
    
    def readLogFolder(self):
        return self._configPr["GENERAL"]["LOG_PATH"]
   
    def setLogFolder(self, logFolder):
        self._configPr.set("GENERAL", "LOG_PATH", logFolder)
        cfgPath = GetCurrentFolder() + os.sep + self._cfg
        with open(cfgPath, 'w', encoding='utf-8', errors='ignore') as cfgFile:
            self._configPr.write(cfgFile)
    

# def ReadConfigs(config):
#     dictConfigs = {}
#     configPr = configparser.ConfigParser()
#     config_path = GetCurrentFolder() + os.sep + config
#     configPr.read(config_path)
#     bFilterMode = configPr["GENERAL"]["isFilterLog"]
#     bAutoSaveMode = configPr["GENERAL"]["isAutoSaving"]
#     bMonitorMode = configPr["GENERAL"]["isMonitorLog"]
#     fileSize =  configPr["GENERAL"]["FILE_SIZE"]
#     timeInterval =  configPr["GENERAL"]["TIME_INTERVAL"]
#     fillterWord = configPr["GENERAL"]["FILTER_WORD"]
#     monitorWord =  configPr["GENERAL"]["MONITOR_WORD"]

#     dictConfigs["isFilterLog"] = bFilterMode
#     dictConfigs["isAutoSaving"] = bAutoSaveMode
#     dictConfigs["isMonitorLog"] = bMonitorMode
#     dictConfigs["FILE_SIZE"] = fileSize
#     dictConfigs["TIME_INTERVAL"] = timeInterval
#     dictConfigs["FILTER_WORD"] = fillterWord
#     dictConfigs["MONITOR_WORD"] = monitorWord

#     return dictConfigs

# def InitConfigAndUI(dictConfigs, ui):
#     FilterWord = dictConfigs["FILTER_WORD"].split(",")
#     for keyWd in FilterWord:
#         ui.etdFilter.appendPlainText(keyWd)
#     MonitorWord = dictConfigs["MONITOR_WORD"].split(",")
#     for keyWd in MonitorWord:
#         ui.edtMoKeys.appendPlainText(keyWd)
#     styleRed = "background-color: red; font-size: 24px;text-align: center; padding-top: 50px; padding-bottom: 50px;"
#     styleGreen = "background-color: green; font-size: 24px;text-align: center; padding-top: 50px; padding-bottom: 50px;"
#     if check_adb_devices():
#         ui.btnSatrt.setStyleSheet(styleGreen)
#     else:
#         ui.btnSatrt.setStyleSheet(styleRed)

# ReadKeyWords("KeyWord.ini")
