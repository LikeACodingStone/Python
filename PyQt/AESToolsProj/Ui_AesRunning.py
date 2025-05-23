# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'd:\Project\PyQtGui\AESTools\AesRunning.ui'
#
# Created by: PyQt5 UI code generator 5.15.7
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from cryptography.fernet import Fernet
import os
import datetime
import shutil

class Ui_AesRun(object):
    def getStrNow(self):
        now_time = datetime.datetime.now()
        trTime = datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S')
        return trTime

    def loadKey(self):
        self.keyPath = QtWidgets.QFileDialog.getOpenFileName(None, "Sel key",  "", "All Files (*);;Text Files (*.key)")[0]
        self.edtKey.setText(self.keyPath)
        self.edtKey.setAlignment(Qt.AlignCenter)
        self.edtKey.setStyleSheet("background-color: rgb(128, 161, 166);\nfont: 12pt \"新宋体\";")
    
    def loadFile(self):
        self.filePath = QtWidgets.QFileDialog.getOpenFileName(None, "Sel File",  "", "All Files (*)")[0]
        self.edtFile.setText(self.filePath)
        self.edtFile.setAlignment(Qt.AlignCenter)
        self.edtFile.setStyleSheet("background-color: rgb(128, 161, 166);\nfont: 12pt \"新宋体\";")
        self.btnAesRun.setEnabled(True)
     
    def aesRun(self):
        curDir = os.getcwd()
        ensDir = os.path.dirname(curDir) + os.sep + "EnsOut"
        curTimeStr = self.getStrNow()
        outKey = ensDir + os.sep + "key_" + curTimeStr + ".key"
        outFile = ensDir + os.sep + "ens_" +  curTimeStr +  ".md"

        if not os.path.exists(ensDir):
            os.makedirs(ensDir)
        keyContent = open(self.keyPath, "rb").read()
        f = Fernet(keyContent)

        with open(self.filePath, "rb") as file: 
            file_data = file.read()
            encrypted_data = f.encrypt(file_data)
        
        with open(outFile, "wb") as file:
            file.write(encrypted_data)
            shutil.copy(self.keyPath, outKey)
            outFileName = curTimeStr +  ".md"
            self.lblSmile.setText("> " + outFileName)
            self.lblSmile.setStyleSheet("background-color: rgb(110, 200, 197);\nfont: 10pt \"新宋体\";")
            self.btnDelOrigin.setEnabled(True)


    def delOrigin(self):
        os.remove(self.keyPath)
        os.remove(self.filePath)
        self.lblSmile.setText("Del Success!")
        self.lblSmile.setStyleSheet("background-color: rgb(110, 200, 197);\nfont: 12pt \"新宋体\";")

    def setupUi(self, AesRun):
        AesRun.setObjectName("AesRun")
        AesRun.resize(695, 483)
        AesRun.setStyleSheet("background-color: rgb(155, 163, 214);")
        self.btnLoadKey = QtWidgets.QPushButton(AesRun)
        self.btnLoadKey.setGeometry(QtCore.QRect(70, 80, 151, 61))
        self.btnLoadKey.setStyleSheet("background-color: rgb(97, 205, 255);\n"
"font: 20pt \"新宋体\";")
        self.btnLoadKey.setObjectName("btnLoadKey")
        self.edtKey = QtWidgets.QTextEdit(AesRun)
        self.edtKey.setGeometry(QtCore.QRect(280, 80, 361, 61))
        self.edtKey.setStyleSheet("background-color: rgb(128, 161, 166);")
        self.edtKey.setObjectName("edtKey")
        self.btnLoadFile = QtWidgets.QPushButton(AesRun)
        self.btnLoadFile.setGeometry(QtCore.QRect(70, 190, 151, 61))
        self.btnLoadFile.setStyleSheet("background-color: rgb(97, 205, 255);\n"
"font: 20pt \"新宋体\";")
        self.btnLoadFile.setObjectName("btnLoadFile")
        self.edtFile = QtWidgets.QTextEdit(AesRun)
        self.edtFile.setGeometry(QtCore.QRect(280, 190, 361, 61))
        self.edtFile.setStyleSheet("background-color: rgb(128, 161, 166);")
        self.edtFile.setObjectName("edtFile")
        self.btnAesRun = QtWidgets.QPushButton(AesRun)
        self.btnAesRun.setGeometry(QtCore.QRect(70, 330, 151, 61))
        self.btnAesRun.setStyleSheet("background-color: rgb(97, 205, 255);\n"
"font: 22pt \"新宋体\";")
        self.btnAesRun.setObjectName("btnAesRun")
        self.btnDelOrigin = QtWidgets.QPushButton(AesRun)
        self.btnDelOrigin.setGeometry(QtCore.QRect(280, 330, 151, 61))
        self.btnDelOrigin.setStyleSheet("background-color: rgb(97, 205, 255);\n"
"font: 20pt \"新宋体\";")
        self.btnDelOrigin.setObjectName("btnDelOrigin")
        self.lblSmile = QtWidgets.QLabel(AesRun)
        self.lblSmile.setGeometry(QtCore.QRect(470, 330, 171, 61))
        self.lblSmile.setStyleSheet("background-color: rgb(110, 200, 197);\n"
"font: 20pt \"新宋体\";")
        self.lblSmile.setObjectName("lblSmile")

        self.btnLoadKey.clicked.connect(self.loadKey)
        self.btnLoadFile.clicked.connect(self.loadFile)
        self.btnAesRun.clicked.connect(self.aesRun)
        self.btnDelOrigin.clicked.connect(self.delOrigin)
        self.btnAesRun.setDisabled(True)
        self.btnDelOrigin.setDisabled(True)

        self.retranslateUi(AesRun)
        QtCore.QMetaObject.connectSlotsByName(AesRun)

    def retranslateUi(self, AesRun):
        _translate = QtCore.QCoreApplication.translate
        AesRun.setWindowTitle(_translate("AesRun", "Form"))
        self.btnLoadKey.setText(_translate("AesRun", "选择KEY"))
        self.btnLoadFile.setText(_translate("AesRun", "选择FILE"))
        self.btnAesRun.setText(_translate("AesRun", "封印"))
        self.btnDelOrigin.setText(_translate("AesRun", "删除原文件"))
        self.lblSmile.setText(_translate("AesRun", "<html><head/><body><p align=\"center\">Smile</p></body></html>"))
