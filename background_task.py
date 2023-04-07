# 用于后台运行，以提供更好的用户交互
import time
import uuid
from PyQt5.QtCore import QThread, pyqtSignal
import os

def getUid():
    uid = uuid.uuid4()
    return uid



class bgThread(QThread):
    finished = pyqtSignal(str)
    updated = pyqtSignal(int)
    uid = ""

    def __init__(self,uid = "sdf"):
        self.uid = uid
        super(bgThread,self).__init__()

    def bgTask(self):
        os.system("bash ./.run.sh  " + str(self.uid))
        import time
        # time.sleep(20)
        self.finished.emit("done")

    def run(self) -> None:
        self.bgTask()


class monitorThread(QThread):
    finished = pyqtSignal(str)
    updated = pyqtSignal(int)
    uid = ""

    def __init__(self,uid = "sdf"):
        self.uid = uid
        super(monitorThread,self).__init__()



    def monitor(self):
        '''统计完成的文件数，从而获取进度'''
        self.task_count_path = "/tmp/" + self.uid
        path = self.task_count_path
        try:
            finnished_task = os.listdir(path)
            finnished_num = len(finnished_task)
        except:
            return 0
        return finnished_num

    def run(self) -> None:
        finnished_sum = 0
        print("sdfsdafdsaf " + self.uid)
        while True:
            current_sum = int(self.monitor())
            if finnished_sum != current_sum:
                finnished_sum = current_sum
                self.updated.emit(finnished_sum)
                print(finnished_sum)
            else:
                print("on going..." + str(current_sum))
            time.sleep(0.5)


print("asdf")