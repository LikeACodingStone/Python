import os,sys
import re, time
import threading
import configparser
from datetime import datetime
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QMessageBox, QButtonGroup
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from Ui_PlayerWeight import Ui_FreePlayer
from PyQt5.QtCore import pyqtSignal, QObject
import pygame
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from BaseModules import ConfigParseHandle, GetCurrentFolder, MainWindow
from AudioPlayer import AudioPlayer, Communicator

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
def SlotBtnPop():
    global g_config_parse
    GenerateTypeFiles(g_config_parse.style_popular)

@pyqtSlot()
def SlotBtnBlues():
    global g_config_parse
    GenerateTypeFiles(g_config_parse.style_blues)

@pyqtSlot()
def SlotBtnCountry():
    global g_config_parse
    GenerateTypeFiles(g_config_parse.style_country)

@pyqtSlot()
def SlotBtnMetal():
    global g_config_parse
    GenerateTypeFiles(g_config_parse.style_metal)

@pyqtSlot()
def SlotBtnPunk():
    global g_config_parse
    GenerateTypeFiles(g_config_parse.style_punk)

@pyqtSlot()
def SlotBtnHardRock():
    global g_config_parse
    GenerateTypeFiles(g_config_parse.style_hardRock)

@pyqtSlot()
def SlotBtnSolo():
    global g_config_parse
    GenerateTypeFiles(g_config_parse.style_solo)

@pyqtSlot()
def SlotBtnJapanese():
    global g_config_parse
    GenerateTypeFiles(g_config_parse.style_japan)

@pyqtSlot()
def SlotNextSong():
    global g_audio_player
    global g_playList
    g_audio_player.current_index += 1
    g_audio_player.play_audio()
    
@pyqtSlot()
def SlotPreSong():
    global g_audio_player
    global g_playList
    g_audio_player.current_index -= 1
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

def GenerateTypeFiles(type):
    type_file = type + ".txt"
    global g_audio_player
    global g_playList
    fileNameContent = g_playList[g_audio_player.current_index]
    global g_config_parse
    g_config_parse.AddStyleList(type_file, fileNameContent)


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
    for root, dirs, files in os.walk(g_config_parse._media_folder_val):
        for file in files:
            if not file.endswith(".wma"):
                play_file = root + os.sep + file
                playList.append(play_file)
    return playList, g_config_parse._media_folder_val, int(g_config_parse._media_index_val)

if __name__ == '__main__':
    CONFIG = "config.ini"
    g_config_parse = ConfigParseHandle(CONFIG)
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = MainWindow(388,85)
    ui = Ui_FreePlayer()
    ui.setupUi(MainWindow)
    ui.btnPlay.clicked.connect(SlotPlay)
    ui.btnPause.clicked.connect(SlotPause)
    ui.btnDel.clicked.connect(SlotDelete)
    ui.btnBlues.clicked.connect(SlotBtnBlues)
    ui.btnCountry.clicked.connect(SlotBtnCountry)
    ui.btnMetal.clicked.connect(SlotBtnMetal)
    ui.btnHard.clicked.connect(SlotBtnHardRock)
    ui.btnPunk.clicked.connect(SlotBtnPunk)
    ui.btnPop.clicked.connect(SlotBtnPop)
    ui.btnSolo.clicked.connect(SlotBtnSolo)
    ui.btnJapan.clicked.connect(SlotBtnJapanese)
    ui.btnNext.clicked.connect(SlotNextSong)
    ui.btnPre.clicked.connect(SlotPreSong)
    ui.btnExit.clicked.connect(SlotBtnExit)
    g_playList = []
    g_mediaIndex = -1
    g_folderIndex = -1
    g_playList, g_folderIndex, g_mediaIndex = GetIniList()
    communicator = Communicator()
    if g_mediaIndex >= len(g_playList):
        g_mediaIndex = 0
    g_audio_player = AudioPlayer(g_playList, g_mediaIndex, communicator)
    ui.lineEdit.setText(GetMediaByIndex(g_playList, g_mediaIndex))
    communicator.update_signal.connect(SlotHandleNext)
    MainWindow.show()
    sys.exit(app.exec_())