# 用于后台运行，以提供更好的用户交互
import subprocess
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


class bgThread2(QThread):
    finished = pyqtSignal(str)
    updated = pyqtSignal(int)
    uid = ""
    running_pool = []
    finished_pool = []

    def __init__(self, task_list = []):
        self.task_list = task_list
        super(bgThread2, self).__init__()

    def runTask(self,  task, thread = 12):
        # task = bgThread()

        # 判断线程是否满了
        if len(self.running_pool) >= thread:
            status = "wait"
            print("thread is full!")
        else:
            status = "added"
            task.start()
            self.running_pool.append(task)

        # 检查线程池中是否有完成的，若有，踢出到完成列表中。
        tasks_to_be_pop = []
        id = 0
        for task in self.running_pool:
            is_finished = task.isFinished()
            print("finished=" + str(is_finished))
            if is_finished:
                tasks_to_be_pop.append(id)

            id = id + 1

        for id in tasks_to_be_pop:
            self.finished_pool.append(self.running_pool.pop(id))
            print("pop out " + str(id))
        print(len(self.running_pool))
        return status


    def run(self) -> None:
        task_list = self.task_list
        for task in task_list:
            status = self.runTask(task)
            print(status)
            while status == "wait":
                print(status)
                time.sleep(1)
                status = self.runTask(task)

                print("exit + " + status)

        print("add completed")




class sleepTask(QThread):
    finished = pyqtSignal(str)


    def __init__(self, id = ""):
        self.id = str(id)
        super(sleepTask, self).__init__()

    def run(self) -> None:
        print("start sleep " + self.id)
        # time.sleep(1)
        print("sleep compleat " + self.id)
        os.system("touch /home/chief/2")


class bcl2fastqThread(QThread):
    finished = pyqtSignal(str)

    def __init__(self):
        super(bcl2fastqThread,self).__init__()

    def bcl2fastq(self):
        log_path = "/tmp/bcl2fastq_" + str(time.time())
        os.system("bash ./.run.sh 2>" +log_path)
        # info = subprocess.Popen(["bash ./.run.sh"], shell=True, stderr=subprocess.PIPE)
        # info = str(info.stderr.read())

        # print(info)
        try:
            with open(log_path, "r") as f:
                log = f.read()
        except Exception as e:
            print(e)

        log_last = log.split("]")[-1]
        return log_last

    def run(self) -> None:
        print("demux...")
        log_last = self.bcl2fastq()
        time.sleep(3)
        self.finished.emit(log_last)
        print("demux donme")



if __name__ == "__main__":
    task_list = []
    for i in range(40):
        locals()[i] = sleepTask(str(i))
        task_list.append(locals()[i])
        locals()[i].start()



