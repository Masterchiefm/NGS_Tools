import os
import zipfile
import time

from PyQt5 import QtCore
from PyQt5.QtWidgets import QMainWindow, QApplication, QTableWidgetItem, QFileDialog, QMessageBox
import pandas as pd
from gui_NGS_Tools import Ui_MainWindow


class MyMainWin(QMainWindow, Ui_MainWindow):
    def __init__(self, parent = None):
        super(MyMainWin, self).__init__(parent)

        self.setupUi(self)
        self.version = "1.2.0"
        self.setWindowTitle(self.windowTitle() + "v"+self.version)

        self.pushButton_bcl.clicked.connect(self.startBCL)


    def startBCL(self):
        from bcl2fastq import  MyMainWin as subwin
        subwin = subwin()
        subwin.show()





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
