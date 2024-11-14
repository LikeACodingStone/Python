from ast import Pass
from Ui_MainEnter import Ui_MAIN
from Ui_Aes import Ui_AesForm
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QMessageBox
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import sys
import os
import shutil




if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()

    ui = Ui_MAIN()
    ui.setupUi(MainWindow)

    MainWindow.show()
    sys.exit(app.exec_())