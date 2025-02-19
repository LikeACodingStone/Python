# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'd:\Project\PyQtGui\AESTools\Aes.ui'
#
# Created by: PyQt5 UI code generator 5.15.7
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.

import os
from PyQt5 import QtCore, QtGui, QtWidgets
from Ui_AesRunning import Ui_AesRun
from Ui_DesRunning import Ui_DesRun
from cryptography.fernet import Fernet

class Ui_AesForm(object):
    def btnNewKey(self):
        newKey = Fernet.generate_key()
        curDir = os.getcwd()
        keyDir = os.path.dirname(curDir) + os.sep + "GenKey"
        if not os.path.exists(keyDir):
            os.makedirs(keyDir)
        existKeyCount = 1
        for key in os.listdir(keyDir):
            if not key.endswith(".key"):
                continue
            existKeyCount = existKeyCount + 1
        trKeyName = keyDir + os.sep + "key" + str(existKeyCount) + ".key"
        with open(trKeyName, "wb") as key_file:
            key_file.write(newKey)
        
        self.edtKey.setText("succeed see \ndir \"GenKey\"!")
    
    def btnAesRunning(self):
        self.mForm.close()
        uiAesRun = Ui_AesRun()
        DialogWin = QtWidgets.QDialog()
        uiAesRun.setupUi(DialogWin)
        DialogWin.show()
        DialogWin.exec_()

        pass
    def btnDesRunning(self):
        self.mForm.close()
        uiDesRun = Ui_DesRun()
        DialogWin = QtWidgets.QDialog()
        uiDesRun.setupUi(DialogWin)
        DialogWin.show()
        DialogWin.exec_()

        pass
    def setupUi(self, AesForm):
        self.mForm = AesForm
        AesForm.setObjectName("AesForm")
        AesForm.resize(767, 489)
        AesForm.setStyleSheet("background-color: rgb(200, 51, 99);")
        self.btnAes = QtWidgets.QPushButton(AesForm)
        self.btnAes.setGeometry(QtCore.QRect(50, 200, 221, 111))
        self.btnAes.setStyleSheet("background-color: rgb(17, 172, 255);\n"
"font: 24pt \"微软雅黑\";")
        self.btnAes.setObjectName("btnAes")
        self.btnKey = QtWidgets.QPushButton(AesForm)
        self.btnKey.setGeometry(QtCore.QRect(270, 100, 221, 101))
        self.btnKey.setStyleSheet("background-color: rgb(17, 172, 255);\n"
"font: 26pt \"微软雅黑\";")
        self.btnKey.setObjectName("btnKey")
        self.btnDes = QtWidgets.QPushButton(AesForm)
        self.btnDes.setGeometry(QtCore.QRect(490, 200, 221, 111))
        self.btnDes.setStyleSheet("background-color: rgb(17, 172, 255);\n"
"font: 24pt \"微软雅黑\";")
        self.btnDes.setObjectName("btnDes")
        self.dial = QtWidgets.QDial(AesForm)
        self.dial.setGeometry(QtCore.QRect(300, 190, 161, 131))
        self.dial.setObjectName("dial")
        self.edtKey = QtWidgets.QTextEdit(AesForm)
        self.edtKey.setGeometry(QtCore.QRect(270, 310, 221, 91))
        self.edtKey.setStyleSheet("background-color: rgb(123, 244, 255);\n"
"font: 22pt \"微软雅黑\";")
        self.edtKey.setObjectName("edtKey")

        self.btnKey.clicked.connect(self.btnNewKey)
        self.btnAes.clicked.connect(self.btnAesRunning)
        self.btnDes.clicked.connect(self.btnDesRunning)

        self.retranslateUi(AesForm)
        QtCore.QMetaObject.connectSlotsByName(AesForm)

    def retranslateUi(self, AesForm):
        _translate = QtCore.QCoreApplication.translate
        AesForm.setWindowTitle(_translate("AesForm", "Form"))
        self.btnAes.setText(_translate("AesForm", "加密"))
        self.btnKey.setWhatsThis(_translate("AesForm", "<html><head/><body><p align=\"center\"><span style=\" font-size:14pt;\">生成KEY</span></p></body></html>"))
        self.btnKey.setText(_translate("AesForm", "生成KEY"))
        self.btnDes.setText(_translate("AesForm", "解密"))
