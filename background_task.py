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
                        
                        uid=$1
                       
                        """

        bashData = [header,authorInfo]
        # bashData0 = list(bashData)
        max_thread = int(os.cpu_count()) * 2
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


class bgCRISPResso2(QThread):
    finished = pyqtSignal(str)
    updated = pyqtSignal(int)
    uid = ""

    def __init__(self, uid="sdf", cmdList=[]):
        self.uid = uid
        self.cmd_list = cmdList
        self.waitting = self.cmd_list.copy()
        self.running = []
        self.finished_tasks =[]

        super(bgCRISPResso2, self).__init__()


    def update(self,i):
        self.running.remove(i)
        self.waitting.remove(i)
        self.finished_tasks.append(i)
        self.updated.emit(1)


    def terminate(self) -> None:
        self.waitting = []
        self.running = []
        self.cmd_list = []
        for i in self.tasks:
            i.terminate()
        super(bgCRISPResso2, self).terminate()

    def freeMem(self):
        try:
            with open('/proc/meminfo') as fd:

                for line in fd:

                    if line.startswith('MemTotal'):
                        total = line.split()[1]

                        continue

                    if line.startswith('MemFree'):
                        free = line.split()[1]

                        break

            FreeMem = int(free) / 1024.0

            TotalMem = int(total) / 1024.0

            # print("FreeMem:" + "%.2f" % FreeMem + 'M')
            #
            # print("TotalMem:" + "%.2f" % TotalMem + 'M')
            #
            # print("FreeMem/TotalMem:" + "%.2f" % ((FreeMem / TotalMem) * 100) + '%')
            free = (FreeMem / TotalMem)
        except:
            print("无法获取内存使用信息!")
            free = 0.8
        return free


    def bgTask(self):
        # bashData0 = list(bashData)
        max_thread = int(os.cpu_count() * 1.5)
        # max_thread = 80
        self.tasks = []

        while True:
            # 判断队列是否满了
            if len(self.running) <= max_thread:
                for i in self.cmd_list:
                    # 判断任务是否已经运行过了
                    if i in self.running:
                        pass
                    elif i in self.finished_tasks:
                        pass
                    else: # 任务未运行过

                        #判断内存没爆炸
                        free_memory = self.freeMem()
                        if free_memory < 0.15:
                            print("内存将满，暂停添加任务")
                            time.sleep(5)
                        else:
                            # print("剩余内存/总内存 = " + "%.2f" % (free_memory * 100) + '%')
                            if len(self.running) <= max_thread:
                                locals()["task_"+str(i)] = bgRun(i)
                                self.running.append(i)
                                locals()["task_" + str(i)].start()
                                locals()["task_" + str(i)].finished.connect(self.update)
                                self.tasks.append(locals()["task_"+str(i)])
                                time.sleep(1)



            if len(self.waitting) == 0:
                self.finished.emit('')
                return




    def run(self) -> None:
        self.bgTask()

class bgRun(QThread):
    started = pyqtSignal(str)
    finished = pyqtSignal(str)

    def __init__(self,cmd="sdf"):
        self.cmd = cmd

        super(bgRun, self).__init__()

    def run(self) -> None:
        # self.started.emit(self.cmd)
        os.system("~/miniconda3/bin/conda run " + self.cmd)
        self.finished.emit(self.cmd)

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



