# 依赖pycrypto库
import binascii
from fileinput import close
import struct
import base64
import json
import os,sys
import re, time
from Crypto.Cipher import AES
import threading

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QMessageBox
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import shutil
from Ui_uglyformat import Ui_Form

def dump(file_path, out_path):
    core_key = binascii.a2b_hex("687A4852416D736F356B496E62617857")
    meta_key = binascii.a2b_hex("2331346C6A6B5F215C5D2630553C2728")
    unpad = lambda s: s[0:-(s[-1] if type(s[-1]) == int else ord(s[-1]))]
    f = open(file_path, 'rb')
    header = f.read(8)
    assert binascii.b2a_hex(header) == b'4354454e4644414d'
    f.seek(2, 1)
    key_length = f.read(4)
    key_length = struct.unpack('<I', bytes(key_length))[0]
    key_data = f.read(key_length)
    key_data_array = bytearray(key_data)
    for i in range(0, len(key_data_array)): key_data_array[i] ^= 0x64
    key_data = bytes(key_data_array)
    cryptor = AES.new(core_key, AES.MODE_ECB)
    key_data = unpad(cryptor.decrypt(key_data))[17:]
    key_length = len(key_data)
    key_data = bytearray(key_data)
    key_box = bytearray(range(256))
    c = 0
    last_byte = 0
    key_offset = 0
    for i in range(256):
        swap = key_box[i]
        c = (swap + last_byte + key_data[key_offset]) & 0xff
        key_offset += 1
        if key_offset >= key_length: key_offset = 0
        key_box[i] = key_box[c]
        key_box[c] = swap
        last_byte = c
    meta_length = f.read(4)
    meta_length = struct.unpack('<I', bytes(meta_length))[0]
    meta_data = f.read(meta_length)
    meta_data_array = bytearray(meta_data)
    for i in range(0, len(meta_data_array)): meta_data_array[i] ^= 0x63
    meta_data = bytes(meta_data_array)
    meta_data = base64.b64decode(meta_data[22:])
    cryptor = AES.new(meta_key, AES.MODE_ECB)
    meta_data = unpad(cryptor.decrypt(meta_data)).decode('utf-8')[6:]
    meta_data = json.loads(meta_data)
    crc32 = f.read(4)
    crc32 = struct.unpack('<I', bytes(crc32))[0]
    f.seek(5, 1)
    image_size = f.read(4)
    image_size = struct.unpack('<I', bytes(image_size))[0]
    image_data = f.read(image_size)
    file_path_dir_list = file_path.split("/")
    file_name_filter = ""
    for file_dir_path in file_path_dir_list:
        if file_dir_path.endswith(".ncm"):
            file_name_first_list = file_dir_path.split("\\")
            for file_name_first in file_name_first_list:
                if file_name_first.endswith(".ncm"):
                    file_name_filter = file_name_first
    file_name_filter_len = len(file_name_filter)
    file_name = file_name_first[0:file_name_filter_len-4] + '.' + meta_data['format']
    file_name = re.sub(u"\\(.*?\\)|\\{.*?}|\\[.*?]", "", file_name)
    out_file = out_path + os.sep + file_name
    if os.path.exists(out_file):
        return 
    m = open(out_file, 'wb')
    chunk = bytearray()
    while True:
        chunk = bytearray(f.read(0x8000))
        chunk_length = len(chunk)
        if not chunk:
            break
        for i in range(1, chunk_length + 1):
            j = i & 0xff;
            chunk[i - 1] ^= key_box[(key_box[j] + key_box[(key_box[j] + j) & 0xff]) & 0xff]
        m.write(chunk)
    m.close()
    f.close()



global g_dirName
g_listNcm = []
global g_isQuit

@pyqtSlot()
def btnDir():
    global g_dirName
    global g_isQuit
    g_isQuit = False
    g_dirName = QtWidgets.QFileDialog.getExistingDirectory()
    ui.edtDir.setText(g_dirName)
    ui.edtDir.setAlignment(Qt.AlignCenter)
    ui.btnStart.setEnabled(True)

@pyqtSlot()
def btnStart():
    global g_dirName
    global g_listNcm
    
    ncmOutDir = os.getcwd() + os.sep + "ncmParse"

    if not os.path.exists(ncmOutDir):
        os.makedirs(ncmOutDir)
    
    ncmDirList = os.listdir(g_dirName)
    for i in range(0, len(ncmDirList)):
        path = os.path.join(g_dirName, ncmDirList[i])
        if os.path.isfile(path) and path.endswith(".ncm"):
            g_listNcm.append(path)
            ui.pdtShow.append(">>   " + ncmOutDir + os.sep + ncmDirList[i])
            my_cursor = ui.pdtShow.textCursor()
            ui.pdtShow.moveCursor(my_cursor.End)
            QtWidgets.QApplication.processEvents(QtCore.QEventLoop.AllEvents)
            if g_isQuit == True:
                break
            dump(path, ncmOutDir)
        
    ui.pdtShow.insertPlainText("convert successfully over! ")
    ui.btnDel.setEnabled(True)

@pyqtSlot()
def btnDel():
    global g_listNcm
    msgBox = QMessageBox()
    msgBox.setIcon(QMessageBox.Information)
    msgBox.setText("sure about delete old ncm files")
    msgBox.setWindowTitle("enjoy yourself")
    msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
    returnValue = msgBox.exec()
    if returnValue == QMessageBox.Ok:
        for oldNcm in g_listNcm:
            os.remove(oldNcm)
            ui.pdtShow.insertPlainText("delete->  " + oldNcm)

    ui.pdtShow.insertPlainText("delete successfully over! ")

@pyqtSlot()
def btnClear():
    ui.pdtShow.clear()
    pass

@pyqtSlot()
def btnQuit():
    g_isQuit = True
    close()
    quit()
    

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_Form()
    ui.setupUi(MainWindow)

    ui.btnDir.clicked.connect(btnDir)
    ui.btnStart.clicked.connect(btnStart)
    ui.btnDel.clicked.connect(btnDel)
    ui.btnClear.clicked.connect(btnClear)
    ui.btnQuit.clicked.connect(btnQuit)

    ui.pdtShow.document().setMaximumBlockCount(100)

    ui.btnStart.setDisabled(True)
    ui.btnDel.setDisabled(True)

    MainWindow.show()
    sys.exit(app.exec_())

