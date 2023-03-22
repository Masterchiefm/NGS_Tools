# 用于后台运行，以提供更好的用户交互
from PyQt5.QtCore import QThread, pyqtSignal
import os
class bg_thread(QThread):
    finished = pyqtSignal(str)
    updated = pyqtSignal(str)

    def __int__(self):
        super(bg_thread,self).__int__()

    def bg_task(self):
        os.system("bash ./.run.sh")
        import time
        # time.sleep(20)
        self.finished.emit("done")

    def run(self) -> None:
        self.bg_task()