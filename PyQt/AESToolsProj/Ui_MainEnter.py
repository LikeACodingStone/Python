# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'd:\Project\PyQtGui\AESTools\MainEnter.ui'
#
# Created by: PyQt5 UI code generator 5.15.7
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
from Ui_Aes import Ui_AesForm
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton

class Ui_MAIN(object):
        

    def btnMainSure(self):
        edtPasswd = self.edtPasswd.toPlainText()
        if edtPasswd != "0306":
            self.edtPasswd.setText("Incorrect")
        else:
            self.mainForm.close()
            uiSelForm = Ui_AesForm()
            DialogWin = QtWidgets.QDialog()
            uiSelForm.setupUi(DialogWin)
            DialogWin.show()
            DialogWin.exec_()

    def setupUi(self, MAIN):
        MAIN.setObjectName("MAIN")
        MAIN.resize(556, 371)
        self.mainForm = MAIN
        MAIN.setStyleSheet("background-color: rgb(147, 180, 255);")
        self.btnSure = QtWidgets.QPushButton(MAIN)
        self.btnSure.setGeometry(QtCore.QRect(160, 240, 211, 71))
        self.btnSure.setStyleSheet("font: 57 22pt \"Quicksand Medium\";\n"
"color: rgb(24, 100, 255);")
        self.btnSure.setObjectName("btnSure")
        self.edtPasswd = QtWidgets.QTextEdit(MAIN)
        self.edtPasswd.setGeometry(QtCore.QRect(160, 130, 211, 71))
        self.edtPasswd.setStyleSheet("background-color: rgb(38, 161, 255);\n"
"font: 30pt \"Yellowtail\";")
        self.edtPasswd.setObjectName("edtPasswd")
        self.lblLogo = QtWidgets.QLabel(MAIN)
        self.lblLogo.setGeometry(QtCore.QRect(80, 30, 371, 61))
        self.lblLogo.setStyleSheet("background-color: rgb(124, 152, 255);\n"
"font: 30pt \"Yellowtail\";")
        self.lblLogo.setObjectName("lblLogo")
        self.btnSure.clicked.connect(self.btnMainSure)
        self.retranslateUi(MAIN)
        QtCore.QMetaObject.connectSlotsByName(MAIN)

    def retranslateUi(self, MAIN):
        _translate = QtCore.QCoreApplication.translate
        MAIN.setWindowTitle(_translate("MAIN", "Form"))
        self.btnSure.setText(_translate("MAIN", "确定"))
        self.edtPasswd.setHtml(_translate("MAIN", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Yellowtail\'; font-size:30pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:\'SimSun\'; font-size:9pt;\"><br /></p></body></html>"))
        self.lblLogo.setText(_translate("MAIN", "<html><head/><body><p align=\"center\"><span style=\" font-size:20pt;\">全自动装B管理系统</span></p></body></html>"))
