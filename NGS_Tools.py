from PyQt5 import QtCore
from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox, QDesktopWidget
import json
import requests
import webbrowser
from gui_NGS_Tools import Ui_MainWindow
import HDR_PE
import bcl2fastq
import BE
import NHEJ
import demultiplex
import qdarktheme
import random


class MyMainWin(QMainWindow, Ui_MainWindow):
    def __init__(self, parent = None):
        super(MyMainWin, self).__init__(parent)
        self.setupUi(self)
        self.version = "1.5.0"
        self.setWindowTitle(self.windowTitle() + " v"+self.version)
        self.checkUpdate()

        self.pushButton_bcl.clicked.connect(self.startBCL)
        self.pushButton_BE.clicked.connect(self.startBE)
        self.pushButton_HDR.clicked.connect(self.startHDR)
        self.pushButton_NHEJ.clicked.connect(self.startNHEJ)
        self.pushButton_demultiplex.clicked.connect(self.startDemultiplex)

        self.centerWin()

    def checkUpdate(self):
        """使用requests模块和GitHub api获取最新版本"""

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'}

        # print(latestInfo)
        try:
            latestInfo = requests.get("https://gitee.com/api/v5/repos/MasterChiefm/NGS_Tools/releases/latest",
                                      timeout=1.5,
                                      headers=headers)
            info = latestInfo.text
            info = json.loads(info)
            # print(info)
            latestVersion = info["tag_name"]
            releaseInfo = info["body"]
            print(latestVersion)

            if latestVersion == self.version:
                # QMessageBox.about(self, "更新", "已经是最新")
                return
            else:
                msg = latestVersion + "\n" + releaseInfo
                # QMessageBox.about(self,"更新",msg)
                box = QMessageBox()
                answer = box.question(self, "New version","----------------|有新版本啦\t  ε٩(๑> ₃ <)۶з |----------------\n\n\n" + msg + \
                                      "请下载最新版本，解压后在属性中赋予运行权限再使用\n\n 现在更新?")
                if answer == QMessageBox.Yes:
                    webbrowser.open("https://gitee.com/MasterChiefm/NGS_Tools/releases/latest")
                    self = QMessageBox.about(self,"Stopped","进程已关闭，请下载最新版本，请下载最新版本使用。\n解压最新版本后，后在属性中赋予运行权限再使用")
                    app.exec_()
                    print("up")
                else:
                    return
        except Exception as e:
            # QMessageBox.about(self,"网络错误","无法连接到GitHub服务器")
            print(e)

    def centerWin(self):
        '''让窗体居中'''
        screen = QDesktopWidget()
        screen_size = screen.screenGeometry()
        size = self.geometry()
        offset = int(random.randint(40,80)) * int(random.randint(-2,2))
        offset2 = int(random.randint(40,80)) * int(random.randint(-2,2))
        self.move(offset + int((screen_size.width()-size.width())/2), offset2 + int((screen_size.height()-size.height())/2))

    def startBCL(self):
        self.subwin_bcl = bcl2fastq.MyMainWin()
        self.subwin_bcl.show()


    def startDemultiplex(self):
        self.subwin_d = demultiplex.MyMainWin()
        self.subwin_d.show()



    def startHDR(self):
        self.subwin_hdr = HDR_PE.MyMainWin()
        self.subwin_hdr.show()

    def startBE(self):
        self.subwin_be = BE.MyMainWin()
        self.subwin_be.show()

    def startNHEJ(self):
        self.subwin_nhej = NHEJ.MyMainWin()
        self.subwin_nhej.show()





if __name__ == "__main__":
    import sys

    # trans = QtCore.QTranslator()
    # trans.load("./en")


    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
    qdarktheme.enable_hi_dpi()
    app = QApplication(sys.argv)
    qdarktheme.setup_theme("auto")
    # app.installTranslator(trans)
    win = MyMainWin()
    win.show()
    sys.exit(app.exec_())
