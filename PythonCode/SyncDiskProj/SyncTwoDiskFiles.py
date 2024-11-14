from Ui_SyncDiskFiles import Ui_Form
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QMessageBox
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import sys
import os
import shutil


global g_diffCopyFilesAToB
global g_diffCopyFilesBToA

def SyncTwoPathFiles(dirOneName, dirTwoName):
    
    diffCopyFilesOne = []
    diffCopyFilesTwo = []

    filePairOne = []
    filePairTwo = []

    dirOneSplitLength = len(dirOneName.split(os.sep))
    dirTwoSplitLength = len(dirTwoName.split(os.sep))

    for root, dirs, files in os.walk(dirOneName, topdown=False):
        for file in files:
            absFile = root + os.sep + file
            pathSplitc = absFile.split(os.sep)[dirOneSplitLength:]
            pairFileAndSplit = []
            pairFileAndSplit.append(absFile)
            pairFileAndSplit.append(pathSplitc)
            filePairOne.append(pairFileAndSplit)
            

    for root, dirs, files in os.walk(dirTwoName, topdown=False):
        for file in files:
            absFile = root + os.sep + file
            pathSplitc = absFile.split(os.sep)[dirTwoSplitLength:]
            pairFileAndSplit = []
            pairFileAndSplit.append(absFile)
            pairFileAndSplit.append(pathSplitc)
            filePairTwo.append(pairFileAndSplit)

    fileDealPairOne = []
    fileDealPairTwo = []

    for pairValue in filePairOne:
        if len(pairValue) != 2:
            pass
        splitPathOne = pairValue[1]
        oneLastPath = ""
        for splitOne in splitPathOne:
            oneLastPath = oneLastPath + os.sep + splitOne
        pairTempList = []
        pairTempList.append(pairValue[0])
        pairTempList.append(oneLastPath)
        fileDealPairOne.append(pairTempList)
        

    for pairValue in filePairTwo:
        if len(pairValue) != 2:
            pass
        splitPathTwo = pairValue[1]
        oneLastPath = ""
        for splitTwo in splitPathTwo:
            oneLastPath = oneLastPath + os.sep + splitTwo
        pairTempList = []
        pairTempList.append(pairValue[0])
        pairTempList.append(oneLastPath)
        fileDealPairTwo.append(pairTempList)


    copyNeedPathTwo = []
    for pairValue in fileDealPairOne:
        if len(pairValue) != 2:
            pass
        oldAbsPath = pairValue[0]
        copyPath = dirTwoName + pairValue[1]
        if not os.path.exists(copyPath):
            dirExist = os.path.dirname(copyPath)
            if not os.path.exists(dirExist):
                os.makedirs(dirExist)
            copyTempList = []
            copyTempList.append(oldAbsPath)
            copyTempList.append(copyPath)
            diffCopyFilesOne.append(copyTempList)

    copyNeedPathOne = []
    for pairValue in fileDealPairTwo:
        if len(pairValue) != 2:
            pass
        oldAbsPath = pairValue[0]
        copyPath = dirOneName +  pairValue[1]
        if not os.path.exists(copyPath):
            dirExist = os.path.dirname(copyPath)
            if not os.path.exists(dirExist):
                os.makedirs(dirExist)
            copyTempList = []
            copyTempList.append(oldAbsPath)
            copyTempList.append(copyPath)
            diffCopyFilesTwo.append(copyTempList)

    return (diffCopyFilesOne, diffCopyFilesTwo)  


global g_fileNameA
global g_fileNameB


@pyqtSlot()
def btnFileA():
    global g_fileNameA
    g_fileNameA = QtWidgets.QFileDialog.getExistingDirectory()
    ui.edtFileA.setText(g_fileNameA)
    ui.edtFileA.setAlignment(Qt.AlignCenter)
    ui.btnFileB.setEnabled(True)

@pyqtSlot()
def btnFileB():
    global g_fileNameA
    global g_fileNameB
    global g_diffCopyFilesAToB
    global g_diffCopyFilesBToA
    g_fileNameB = QtWidgets.QFileDialog.getExistingDirectory()
    ui.edtFileB.setText(g_fileNameB)
    ui.edtFileB.setAlignment(Qt.AlignCenter)
    g_diffCopyFilesAToB, g_diffCopyFilesBToA = SyncTwoPathFiles(g_fileNameA, g_fileNameB)
    isAtoBEnable = False
    isBtoAEnable = False
    if len(g_diffCopyFilesAToB) != 0:
        ui.btnSyncAToB.setEnabled(True)
        isAtoBEnable = True
        ui.pdtInfo.appendPlainText("A Have Differ Files To B........................")
        countDiffA = 0
        for diff in g_diffCopyFilesAToB:
            countDiffA = countDiffA + 1
            if countDiffA > 10:
                ui.pdtInfo.appendPlainText("and so on ......")
                break
            fileStr = diff[0] + "      " + diff[1]
            ui.pdtInfo.appendPlainText(fileStr)
        ui.pdtInfo.appendPlainText("\n\n")
    if len(g_diffCopyFilesBToA) != 0:
        ui.btnSyncBToA.setEnabled(True)
        isBtoAEnable = True
        countDiffB = 0
        ui.pdtInfo.appendPlainText("B Have Differ Files To A.......................")
        for diff in g_diffCopyFilesBToA:
            countDiffB = countDiffB + 1
            if countDiffB > 10:
                ui.pdtInfo.appendPlainText("and so on ......")
                break
            fileStr = diff[0] + "     " + diff[1]
            ui.pdtInfo.appendPlainText(fileStr)
    if isAtoBEnable and isBtoAEnable:
        ui.btnSyncBoth.setEnabled(True)


def funcSyncAToB():
    global g_diffCopyFilesAToB
    fileToBNum = len(g_diffCopyFilesAToB) 
    perIndex = 0
    for diff in g_diffCopyFilesAToB:
        perIndex = perIndex + 1
        trTopIndex = "\n>>>>>>>>>>>>>>>>>>>>>>>>>  % " + str(perIndex / fileToBNum * 100)
        ui.pdtInfo.insertPlainText(trTopIndex)
        fileStr = diff[0] + "      " + diff[1]
        ui.pdtInfo.appendPlainText(fileStr)
        shutil.copy(diff[0], diff[1])
    ui.pdtInfo.appendPlainText("\n------------------------over A To B------------------\n")

def funcSyncBToA():
    global g_diffCopyFilesBToA
    fileToBNum = len(g_diffCopyFilesBToA) 
    perIndex = 0
    for diff in g_diffCopyFilesBToA:
        perIndex = perIndex + 1
        trTopIndex = "\n>>>>>>>>>>>>>>>>>>>>>>>>>  % " + str(perIndex / fileToBNum * 100)
        ui.pdtInfo.insertPlainText(trTopIndex)
        fileStr = diff[0] + "      " + diff[1]
        ui.pdtInfo.appendPlainText(fileStr)
        shutil.copy(diff[0], diff[1])
    ui.pdtInfo.appendPlainText("\n------------------------over B To A------------------\n")

def funcDelAOtherFiles():
    global g_diffCopyFilesAToB
    fileToBNum = len(g_diffCopyFilesAToB) 
    perIndex = 0
    for diff in g_diffCopyFilesAToB:
        perIndex = perIndex + 1
        trTopIndex = "\ndel >>>>>>>>>>>>>>>>>>>>>>  % " + str(perIndex / fileToBNum * 100)
        fileStr =  "Del>>       " +  diff[0]
        ui.pdtInfo.appendPlainText(fileStr)
        os.remove(diff[0])
    ui.pdtInfo.appendPlainText("\n------------------------End del A Files------------------\n")


def funcDelBOtherFiles():
    global g_diffCopyFilesBToA
    fileToBNum = len(g_diffCopyFilesBToA) 
    perIndex = 0
    for diff in g_diffCopyFilesBToA:
        perIndex = perIndex + 1
        trTopIndex = "\ndel >>>>>>>>>>>>>>>>>>>>>>  % " + str(perIndex / fileToBNum * 100)
        fileStr =  "Del>>       " +  diff[0]
        ui.pdtInfo.appendPlainText(fileStr)
        os.remove(diff[0])
    ui.pdtInfo.appendPlainText("\n------------------------End del B Files------------------\n")


@pyqtSlot()
def btnSyncBoth():
    global g_diffCopyFilesAToB
    global g_diffCopyFilesBToA
    msgBox = QMessageBox()
    msgBox.setIcon(QMessageBox.Information)
    msgBox.setText("ensure dir is correct")
    msgBox.setWindowTitle("sync both differ files")
    msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)

    returnValue = msgBox.exec()
    if returnValue == QMessageBox.Ok:
        ui.pdtInfo.clear()
        funcSyncAToB()
        funcSyncBToA()
      
        ui.pdtInfo.appendPlainText("\n**********************Sync Both End***********************\n")

        ui.btnSyncBoth.setDisabled(True)
        ui.btnSyncAToB.setDisabled(True)
        ui.btnSyncBToA.setDisabled(True)
    pass


@pyqtSlot()
def btnSyncAToB():
    msgBox = QMessageBox()
    msgBox.setIcon(QMessageBox.Information)
    msgBox.setText("syc A to B And Del B others? OK deL. No only copy. Cancel to quit")
    msgBox.setWindowTitle("sync A to B")
    msgBox.setStandardButtons(QMessageBox.Yes | QMessageBox.No |QMessageBox.Cancel) 
    returnValue = msgBox.exec()
    if returnValue == QMessageBox.Yes:
        funcSyncAToB()
        funcDelBOtherFiles()
        ui.btnSyncBoth.setDisabled(True)
        ui.btnSyncBToA.setDisabled(True)
        ui.btnSyncAToB.setDisabled(True)
        pass
    if returnValue == QMessageBox.No:
        funcSyncAToB()
        ui.btnSyncBoth.setDisabled(True)
        ui.btnSyncAToB.setDisabled(True)
        pass
    if returnValue == QMessageBox.Cancel:
        pass
    pass

   

@pyqtSlot()
def btnSyncBToA():
    msgBox = QMessageBox()
    msgBox.setIcon(QMessageBox.Information)
    msgBox.setText("syc B to A And Del A others? OK deL. No only copy. Cancel to quit")
    msgBox.setWindowTitle("sync B to A")
    msgBox.setStandardButtons(QMessageBox.Yes | QMessageBox.No |QMessageBox.Cancel) 
    returnValue = msgBox.exec()
    if returnValue == QMessageBox.Yes:
        funcSyncBToA()
        funcDelAOtherFiles()
        ui.btnSyncBoth.setDisabled(True)
        ui.btnSyncBToA.setDisabled(True)
        ui.btnSyncAToB.setDisabled(True)
        pass
    if returnValue == QMessageBox.No:
        funcSyncBToA()
        ui.btnSyncBoth.setDisabled(True)
        ui.btnSyncBToA.setDisabled(True)
        pass
    if returnValue == QMessageBox.Cancel:
        pass
    pass

@pyqtSlot()
def btnStop():
    pass


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_Form()
    ui.setupUi(MainWindow)

    ui.btnFileA.clicked.connect(btnFileA)
    ui.btnFileB.clicked.connect(btnFileB)
    ui.btnSyncBoth.clicked.connect(btnSyncBoth)
    ui.btnSyncAToB.clicked.connect(btnSyncAToB)
    ui.btnSyncBToA.clicked.connect(btnSyncBToA)
    ui.btnStop.clicked.connect(btnStop)

    ui.pdtInfo.document().setMaximumBlockCount(100)

    ui.btnFileB.setDisabled(True)
    ui.btnSyncBoth.setDisabled(True)
    ui.btnSyncAToB.setDisabled(True)
    ui.btnSyncBToA.setDisabled(True)

    MainWindow.show()
    sys.exit(app.exec_())
