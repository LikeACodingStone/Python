import os,sys
import re, time
import threading
import configparser
import random
from datetime import datetime

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QMessageBox, QButtonGroup
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtCore import pyqtSignal, QObject
import pygame
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from BaseModules import ConfigParseHandle, GetCurrentFolder, MainWindow, ConfigModuleHandle
from AudioPlayer import AudioPlayer, Communicator
from Ui_RandomPlayWeight import Ui_MainWindow

def GetMediaByIndex(playList, mediaIndex):
    filePath = playList[mediaIndex]
    mediName = filePath.split("\\")[-1]
    return mediName

def player_thread(player):
    player.run()

global g_playList
global g_mediaIndex
global g_folderIndex
global g_audio_player
global g_config_parse
global g_config_mode

@pyqtSlot()
def SlotPlay():
    global g_audio_player
    if g_audio_player.is_paused:
        g_audio_player.resume_audio()  
    else:
        thread = threading.Thread(target=player_thread, args=(g_audio_player,))
        thread.start()
    
@pyqtSlot()
def SlotPause():
    global g_audio_player
    if g_audio_player.is_playing:
        g_audio_player.pause_audio()

@pyqtSlot()
def SlotDelete():
    GenerateDeletFiles()

@pyqtSlot()
def SlotNextSong():
    global g_audio_player
    global g_playList
    global g_config_mode
    if g_config_mode.getRandomMode():
        randomIndex = random.randint(1, len(g_playList))
        g_audio_player.current_index =  randomIndex 
    else:
        g_audio_player.current_index += 1
    g_audio_player.play_audio()

@pyqtSlot()
def SlotBtnExit():
    g_audio_player.is_quit = True
    QApplication.quit()
    sys.exit(0)

@pyqtSlot()
def SlotHandleNext():
    UpdateConfig()
    ui.lineEdit.setText(GetMediaByIndex(g_playList ,g_audio_player.current_index))

def GenerateDeletFiles():
    global g_audio_player
    global g_playList
    global g_config_parse
    fileNameContent = g_playList[g_audio_player.current_index]
    g_config_parse.AddDeleteFileList(fileNameContent)

def UpdateConfig():
    global g_audio_player
    global g_config_parse
    g_config_parse.setMediaIndex(g_audio_player.current_index)

def GetIniList():
    global g_config_parse
    playList = []
    for root, dirs, files in os.walk(g_config_parse._media_root_val):
        for file in files:
            if not file.endswith(".wma"):
                play_file = root + os.sep + file
                playList.append(play_file)
    return playList

if __name__ == '__main__':
    CONFIG = "config.ini"
    g_config_parse = ConfigParseHandle(CONFIG)
    CONFIG_MODE = "config_modules.ini"
    g_config_mode = ConfigModuleHandle(CONFIG_MODE)
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = MainWindow(307,95)
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    g_playList = []
    g_mediaIndex = 1
    g_playList = GetIniList()
    communicator = Communicator()
    g_audio_player = AudioPlayer(g_playList, g_mediaIndex, communicator, g_config_mode.getRandomMode())
    ui.lineEdit.setText(GetMediaByIndex(g_playList, g_mediaIndex))
    ui.btnNext.clicked.connect(SlotNextSong)
    ui.btnPlay.clicked.connect(SlotPlay)
    ui.btnPause.clicked.connect(SlotPause)
    ui.btnDel.clicked.connect(SlotDelete)
    ui.btnExit.clicked.connect(SlotBtnExit)
    communicator.update_signal.connect(SlotHandleNext)
    if g_config_mode.getPlayOnlyMode():
        ui.btnDel.hide()
    MainWindow.show()
    sys.exit(app.exec_())