"""环境安装对话框：在后台线程执行 checkEnv.check()，实时显示安装输出，界面不卡顿"""
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import QDialog, QLabel, QPlainTextEdit, QVBoxLayout

import checkEnv


class InstallWorker(QThread):
    line = pyqtSignal(str)
    finished_check = pyqtSignal(bool)

    def run(self):
        ok = True
        checkEnv.set_progress_callback(self.line.emit)
        try:
            checkEnv.check()
        except Exception as e:
            self.line.emit("安装出错: {}".format(e))
            ok = False
        finally:
            checkEnv.set_progress_callback(None)
        self.finished_check.emit(ok)


class InstallDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("环境安装")
        self.resize(680, 480)
        self.ok = False

        self.status = QLabel("正在安装分析环境，以下为实时输出，请勿关闭窗口：", self)
        self.text = QPlainTextEdit(self)
        self.text.setReadOnly(True)
        self.text.document().setMaximumBlockCount(2000)

        layout = QVBoxLayout(self)
        layout.addWidget(self.status)
        layout.addWidget(self.text)

    def onFinished(self, ok):
        self.ok = ok
        self.status.setText("安装流程已结束，窗口将自动关闭。")
        self.accept()


def run_install(parent=None):
    """弹出安装对话框并阻塞至安装结束，返回是否成功完成"""
    dialog = InstallDialog(parent)
    worker = InstallWorker(dialog)
    worker.line.connect(dialog.text.appendPlainText)
    worker.finished_check.connect(dialog.onFinished)
    worker.start()
    dialog.exec_()
    return dialog.ok
