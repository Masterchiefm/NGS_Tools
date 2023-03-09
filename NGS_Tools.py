import os
import zipfile
import time

from PyQt5 import QtCore
from PyQt5.QtWidgets import QMainWindow, QApplication, QTableWidgetItem, QFileDialog, QMessageBox
import pandas as pd
from gui_NGS_Tools import Ui_MainWindow
import HDR_PE
import bcl2fastq
import BE
import NHEJ


class MyMainWin(QMainWindow, Ui_MainWindow):
    def __init__(self, parent = None):
        super(MyMainWin, self).__init__(parent)

        self.setupUi(self)
        self.version = "1.2.0"
        self.setWindowTitle(self.windowTitle() + "v"+self.version)

        self.pushButton_bcl.clicked.connect(self.startBCL)
        self.pushButton_BE.clicked.connect(self.startBE)
        self.pushButton_HDR.clicked.connect(self.startHDR)
        self.pushButton_NHEJ.clicked.connect(self.startNHEJ)


    def startBCL(self):
        self.subwin = bcl2fastq.MyMainWin()
        self.subwin.show()



    def startHDR(self):
        self.subwin = HDR_PE.MyMainWin()
        self.subwin.show()

    def startBE(self):
        self.subwin = BE.MyMainWin()
        self.subwin.show()

    def startNHEJ(self):
        self.subwin = NHEJ.MyMainWin()
        self.subwin.show()





if __name__ == "__main__":
    import sys

    # trans = QtCore.QTranslator()
    # trans.load("./en")


    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
    app = QApplication(sys.argv)
    # app.installTranslator(trans)
    win = MyMainWin()
    win.show()
    sys.exit(app.exec_())
