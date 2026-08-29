"""环境安装对话框：在后台线程执行 checkEnv.check()，实时显示安装输出，界面不卡顿
安装完成或出错后窗口保持打开，由用户自行关闭，日志可选中复制"""
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import (QDialog, QLabel, QPlainTextEdit, QVBoxLayout,
                             QHBoxLayout, QPushButton, QApplication)

import checkEnv


class InstallWorker(QThread):
    line = pyqtSignal(str)
    finished_check = pyqtSignal(bool)

    def run(self):
        checkEnv.set_progress_callback(self.line.emit)
        try:
            ok = checkEnv.check()
        except Exception as e:
            self.line.emit("安装出错: {}".format(e))
            ok = False
        finally:
            checkEnv.set_progress_callback(None)
        self.finished_check.emit(bool(ok))


class InstallDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("环境安装")
        self.resize(680, 480)

        self.status = QLabel("正在安装分析环境，以下为实时输出：", self)
        self.text = QPlainTextEdit(self)
        self.text.setReadOnly(True)
        self.text.document().setMaximumBlockCount(2000)

        self.copyButton = QPushButton("复制全部日志", self)
        self.copyButton.clicked.connect(self.copyLog)

        layout = QVBoxLayout(self)
        layout.addWidget(self.status)
        layout.addWidget(self.text)
        buttons = QHBoxLayout()
        buttons.addStretch()
        buttons.addWidget(self.copyButton)
        layout.addLayout(buttons)

    def copyLog(self):
        QApplication.clipboard().setText(self.text.toPlainText())

    def onFinished(self, ok):
        if ok:
            self.status.setText("安装流程已结束，可自行关闭本窗口。")
        else:
            self.status.setText("安装未完成或出错，详情见上方日志，可关闭窗口后重试。")


def run_install(parent=None, on_finished=None):
    """弹出安装对话框，实时显示输出；on_finished(bool) 在安装结束时回调（不自动关闭窗口）"""
    dialog = InstallDialog(parent)
    worker = InstallWorker(dialog)
    worker.line.connect(dialog.text.appendPlainText)
    worker.finished_check.connect(dialog.onFinished)
    if on_finished:
        worker.finished_check.connect(on_finished)
    worker.start()
    dialog.exec_()
