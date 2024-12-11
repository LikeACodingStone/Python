import os
import configparser
import pygame
import time
import threading
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QMessageBox, QButtonGroup
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from Ui_PlayerWeight import Ui_FreePlayer
from PyQt5.QtCore import pyqtSignal, QObject

def GetCurrentFolder():
    current_file_path = os.path.abspath(__file__)
    current_dir = os.path.dirname(current_file_path)
    return current_dir

CONFIG = "config_A.ini"
class ConfigParseHandle:
    def __init__(self, config):
        self._config = config
        self._delete = "Delete.txt"
        self.key_config = "GENERAL"
        self.key_folder_index = "FOLDER_INDEX"
        self.key_config_folder = "CONFIG_FOLDER"
        self.key_backup_folder = "BACKUP_FOLDER"
        self.key_media_root = "MEDIA_ROOT"
        self.key_folder = "FOLDER_"

        self.style_blues = "BluesJazz"
        self.style_hardRock = "HardRock"
        self.style_metal = "Metal"
        self.style_popular = "Popular"
        self.style_punk = "Punk"
        self.style_country = "Country"
        self.style_solo = "Solo"

        self.key_style_name = "STYLE_NAME"
        self.key_media_index = "MEDIA_INDEX"

        self.key_srand_mode = "srand_mode"
        self.key_clear_mode = "clear_mode"
     
        self._configPr = configparser.ConfigParser()
        self._config_path = GetCurrentFolder() + os.sep + config
        self._configPr.read(self._config_path)

        self._media_root_val = self._configPr[self.key_config][self.key_media_root]
        self._folder_section = self.key_folder + self._configPr[self.key_config][self.key_folder_index]
        self._media_folder_val = self._media_root_val + os.sep + self._configPr[self._folder_section][self.key_style_name]
        self._media_index_val = self._configPr[self._folder_section][self.key_media_index]

        # self._srand_mode = self._configPr[self._folder_section][self.key_srand_mode]
        # self._clear_mode = self._configPr[self._folder_section][self.key_clear_mode]

        self._abs_config_folder = GetCurrentFolder() + os.sep + self._configPr[self.key_config][self.key_config_folder] 
        if not os.path.exists(self._abs_config_folder):
            os.mkdir(self._abs_config_folder)
        

    def getStyleFolder(self, style):
        if style == "blues":
            return self._media_root_val + os.sep + self._configPr["FOLDER_2"][self.key_style_name]
        if style == "hard":
            return self._media_root_val + os.sep + self._configPr["FOLDER_6"][self.key_style_name]
        if style == "metal":
            return self._media_root_val + os.sep + self._configPr["FOLDER_7"][self.key_style_name]
        if style == "pop":
            return self._media_root_val + os.sep + self._configPr["FOLDER_4"][self.key_style_name]
        if style == "punk":
            return self._media_root_val + os.sep + self._configPr["FOLDER_11"][self.key_style_name]
        if style == "country":
            return self._media_root_val + os.sep + self._configPr["FOLDER_5"][self.key_style_name]
        if style == "solo":
            return self._media_root_val + os.sep + self._configPr["FOLDER_12"][self.key_style_name]
        
    def setMediaIndex(self, index):
        self._configPr.set(self._folder_section, self.key_media_index, str(index))
        with open(self._config_path, 'w', encoding='utf-8', errors='ignore') as configfile:
            self._configPr.write(configfile)
    
    
    def AddStyleList(self, styleFile, content):
        abs_style_file = self._abs_config_folder + os.sep + styleFile
        with open(abs_style_file, "a+", encoding='utf-8', errors='ignore') as fp:
            fp.write(content)
            fp.write("\n")
            fp.close()
        
    def AddDeleteFileList(self, content):
        del_file = self._abs_config_folder + os.sep + self._delete
        bPassDelete = False
        if os.path.exists(del_file):
            readLines = open(del_file, encoding='utf-8', errors='ignore').readlines()
            for linesCont in readLines:
                linesCont = linesCont.strip("\n").split("\\")
                if len(linesCont) > 2:
                    sprName = content.strip("\n").split("\\")
                    if linesCont[len(linesCont) -2] == sprName[len(sprName) -2] and \
                        sprName[len(sprName) -1] == linesCont[len(linesCont) -1]:
                        bPassDelete = True

        if not os.path.exists(del_file) or not bPassDelete:
            with open(del_file, 'a', encoding='utf-8', errors = 'ignore') as file:
                file.write(content)
                file.write("\n")
                file.close()

class ConfigModuleHandle:
    def __init__(self, config):
        self._config = config
        self.key_config = "GENERAL"
        self.key_random = "random_list_mode"
        self.key_play_only = "play_only"
        self._configPr = configparser.ConfigParser()
        self._config_path = GetCurrentFolder() + os.sep + config
        self._configPr.read(self._config_path)
        self._random_mode = int(self._configPr[self.key_config][self.key_random])
        self._play_only_mode = int(self._configPr[self.key_config][self.key_play_only])
    def getRandomMode(self):
        return self._random_mode
    def getPlayOnlyMode(self):
        return self._play_only_mode
    
class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, widthVal, heightVal):
        super().__init__()
        self.setWindowFlags(Qt.Window | Qt.FramelessWindowHint)
        self.setFixedSize(int(widthVal), int(heightVal))
        self.setStyleSheet("background-color: rgb(125, 168, 232)")
        
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.oldPos = event.globalPos()
        
    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            delta = event.globalPos() - self.oldPos
            self.move(self.pos() + delta)
            self.oldPos = event.globalPos()
    

        