import os
from PyQt5 import QtCore
from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox
import json
import requests
import webbrowser
from gui_NGS_Tools import Ui_MainWindow
import HDR_PE
import bcl2fastq
import BE
import NHEJ


class MyMainWin(QMainWindow, Ui_MainWindow):
    def __init__(self, parent = None):
        super(MyMainWin, self).__init__(parent)
        self.setupUi(self)
        self.version = "1.2.2"
        self.setWindowTitle(self.windowTitle() + " v"+self.version)
        self.checkUpdate()

        self.pushButton_bcl.clicked.connect(self.startBCL)
        self.pushButton_BE.clicked.connect(self.startBE)
        self.pushButton_HDR.clicked.connect(self.startHDR)
        self.pushButton_NHEJ.clicked.connect(self.startNHEJ)

    def checkUpdate(self):
        """使用requests模块和GitHub api获取最新版本"""

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'}
        latestInfo = requests.get("https://gitee.com/api/v5/repos/MasterChiefm/NGS_Tools/releases/latest", timeout=2,
                                  headers=headers)
        # print(latestInfo)
        try:
            info = latestInfo.text
            info = json.loads(info)
            # print(info)
            latestVersion = info["tag_name"]
            releaseInfo = info["body"]
            # print(latestVersion)

            if latestVersion == self.version:
                # QMessageBox.about(self, "更新", "已经是最新")
                return
            else:
                msg = latestVersion + "\n" + releaseInfo
                # QMessageBox.about(self,"更新",msg)
                answer = QMessageBox.question(self, "有新版本啦\t  ε٩(๑> ₃ <)۶з", msg + "\n\n Update now?")
                if answer == QMessageBox.Yes:
                    webbrowser.open("https://gitee.com/MasterChiefm/NGS_Tools/releases/latest")
                else:
                    return
        except Exception as e:
            # QMessageBox.about(self,"网络错误","无法连接到GitHub服务器")
            print(e)


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
