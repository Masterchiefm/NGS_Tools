# 用于后台运行，以提供更好的用户交互
import subprocess
import time
import uuid
from PyQt5.QtCore import QThread, pyqtSignal
import os
import requests

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


class bgCRISPResso(QThread):
    finished = pyqtSignal(str)
    updated = pyqtSignal(int)
    uid = ""
    def __init__(self,uid = "sdf",cmdList = []):
        self.uid = uid
        self.cmd_list = cmdList
        super(bgCRISPResso,self).__init__()

    def bgTask(self):
        header = "#!/bin/bash\n source ~/miniconda3/bin/activate base  \n" # bash文件头
        authorInfo = """# This Script is generated automatically. Do not modify anything unless you know what you are doing.
                        # Script Author:\tMo Qiqin
                        # Contact:\tmoqq@shanghaitech.edu.cn\n
                        echo a >> log
                        uid=$1
                       
                        """

        bashData = [header,authorInfo]
        # bashData0 = list(bashData)
        max_thread = int(os.cpu_count())
        counter = 0
        # i=0
        for task in self.cmd_list:
            # i=i+1
            CMD = "{\n" + task + " \n}&\n" + "\n clear \n"
            bashData.append(CMD)
            counter = counter + 1
            if counter == max_thread:
                bashData.append("\nwait\n")
                counter = 0

                a = "".join(bashData)
                with open(".run.sh", "w") as f:
                    f.write(a)
                os.system("bash ./.run.sh" )


                # 运行结束删除内容
                bashData = [header,authorInfo]
                os.system('rm -rf ./.run.sh')

                self.updated.emit(max_thread)

        # for 循环结束但是没有完成最后的剩余任务：

        bashData.append("\nwait\n")
        a = "".join(bashData)
        with open(".run.sh", "w") as f:
            f.write(a)
        os.system("bash ./.run.sh" )
        os.system("rm -rf ./.run.sh")
        self.finished.emit("done")

    def run(self) -> None:
        self.bgTask()



class lyricThread(QThread):
    updated = pyqtSignal(str)


    def __init__(self):
        super(lyricThread,self).__init__()

    def getLyric(self):
        try:
            url2 = 'https://v1.jinrishici.com/all'
            lyric = requests.get(url2, timeout=1).json()
            content = lyric['content']
            try:
                origin = lyric['origin']
            except:
                origin = "Unknown"
            try:
                author = lyric['author']
            except:
                author = "Unknown"

            output = content + "\n\t\t\t" + "——《" + origin + "》\t" + author
            return output
        except Exception as e:
            print(e)
            output = "扩增子测序分析" + "\n\t\t\t" + "——Written by M.Q. at ShanghaiTech University"
            return output

    def run(self) -> None:
        while True:
            time.sleep(600)
            lyric = self.getLyric()
            self.updated.emit(lyric)



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
        print("开始拆分")
        log_last = self.bcl2fastq()
        time.sleep(3)
        self.finished.emit(log_last)
        print("拆分完成")



if __name__ == "__main__":
    task_list = []
    for i in range(40):
        locals()[i] = sleepTask(str(i))
        task_list.append(locals()[i])
        locals()[i].start()



