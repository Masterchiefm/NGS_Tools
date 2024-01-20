from PyQt5 import QtCore
from PyQt5.QtWidgets import QMainWindow, QApplication, QTableWidgetItem, QFileDialog, QMessageBox
from gui_demultiplex import Ui_BCL2Fastq
import subprocess
import requests
import webbrowser
import pandas as pd
import os
import time
from background_task import bgThread
import background_task
# DNA序列工具
def reverseDNA(dna):
    #a = list(dna)
    result = ''
    dna=dna.upper().strip()
    b = ''.join(reversed(dna))
    for i in b:
        if i == "A":
            j = "T"
        elif i == "T":
            j = "A"
        elif i == "C":
            j = "G"
        elif i == "G":
            j = "C"
        else:
            j = "N"

        result = result + j
    return result


def getLyric():
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


def extractSample(index1='', index2='',r1 = "",r2="",output_name=""):
    """根据index序列提取部分测序内容"""
    script = """#!/bin/bash
#the input $1 is R1-index
#the input $2 is R2-index
#the input $3 is R1 file
#the input $4 is R2 file
#the input $5 is R1 output
#the input $6 is R2 output


index1=$1
index2=$2
r1=$3
r2=$4
o1=$5
o2=$6

session=$(cat /proc/sys/kernel/random/uuid)

varR1=${index1}
zcat $r1| grep -E "^.{0,5}${varR1}" -i -B1| grep @ | awk '{print$1}' > ${varR1}.${session}.tmp.id.txt
varR2=${index2}

zcat ${r2}| grep -A1 -F -f ${varR1}.${session}.tmp.id.txt |\
grep -E "^.{0,5}${varR2}" -i -B1| grep @| awk '{print$1}' >${varR1}.${varR2}.${session}.id.txt

echo  $r1 split.
rm ${varR1}.${session}.tmp.id.txt
#gunzip ${r1}
#gunzip ${r2}
    
echo stage1 done.
zcat ${r1} | grep -A3 -F -f ${varR1}.${varR2}.${session}.id.txt |grep -v "\-\-" > ${o1}
zcat ${r1} | grep -A3 -F -f ${varR1}.${varR2}.${session}.id.txt |grep -v "\-\-" > ${o2}
echo zip $r1
gzip -f ${o1}
gzip -f ${o2}

rm ${varR1}.${varR2}.${session}.id.txt
echo $r1 reads have done."""
    with open(".extract.sh", "w") as f:
        f.write(script)
    # cmd = "bash .extract.sh " + index1 + " " + index2 + " " + r1 + " " + r2 + " " + output_name + "_R1.fastq " + output_name + "_R2,fastq"
    # print(cmd)
    # os.system(cmd)


class MyMainWin(QMainWindow, Ui_BCL2Fastq):
    def __init__(self, parent = None):
        super(MyMainWin, self).__init__(parent)

        self.setupUi(self)
        # self.version = "1.2.0"
        # self.setWindowTitle(self.windowTitle() + "v"+self.version)
        output = "BCL2Fastq处理" + "\n\t\t\t" + "——Written by M.Q. at ShanghaiTech University"
        self.label.setText(output)
        self.selected_rows = []

        col_count = self.tableWidget.columnCount()
        self.col_names = []
        self.col_name_locations = {}
        for i in range(col_count):
            name = self.tableWidget.horizontalHeaderItem(i).text()
            self.col_names.append(name)
            self.col_name_locations[name] = i

        print(self.col_names)

        self.plainTextEdit_readIllumina.dropped.connect(self.autoInput)
        self.tableWidget.selectColumn(0)

        self.tableWidget.itemSelectionChanged.connect(self.showSelection)
        self.pushButton_add_line.clicked.connect(self.addLine)
        self.pushButton_clear_table.clicked.connect(self.clearTable)
        self.pushButton_import_from_sheet.clicked.connect(self.importFromSheet)
        self.pushButton_export_sheet.clicked.connect(self.exportSheet)
        self.pushButton_openFqDir.clicked.connect(self.openFolder)
        self.tableWidget.clicked.connect(self.disableAutoFill)
        self.pushButton_del_lines.clicked.connect(self.delLine)
        self.groupBox_status.setVisible(False)

        self.pushButton_stop.setVisible(False)


        # 按键区域
        # self.pushButton_install_bcl2fq.clicked.connect(self.installDependence)
        self.pushButton_generateFq.clicked.connect(self.start)
        self.pushButton_chooseFolder.clicked.connect(self.chooseFolder)
        self.pushButton_stop.clicked.connect(self.stopTread)








    def stopTread(self):
        self.thread.terminate()
        self.monitor.terminate()
        self.groupBox_status.setVisible(False)
        self.pushButton_generateFq.setEnabled(True)
        QMessageBox.about(self, "停止", "已停止")


    # 功能区
    def start(self):
        if self.plainTextEdit_readIllumina.toPlainText() == "":
            QMessageBox.about(self, "Fastq folder not set", "ERROR:\n必须指定fastq文件所在的文件夹！")
            return 0

        if self.setSavePath():
            pass
        else:
            return 0
        self.label.setText(""" ε٩(๑> ₃ <)۶з  正在运行，界面会卡住很久，请少安毋躁♥""")
        self.time0 = time.ctime()
        extractSample()
        bashData = ["#!/bin/bash\n  source ~/miniconda3/bin/activate NGS \n"]  # bash文件头
        authorInfo = """# This Script is generated automatically. Do not modify anything unless you know what you are doing.
                        # Script Author:\tMo Qiqin
                        # Contact:\tmoqq@shanghaitech.edu.cn\n
                        uid=$1
                        mkdir /tmp/${uid}
                        """
        bashData.append(authorInfo)
        thread = int(os.cpu_count())
        if thread < 8:
            thread = 8
        counter = 0

        output_path = self.lineEdit_FqDir.text()
        path = self.plainTextEdit_readIllumina.toPlainText()
        if path == "":
            return
        self.exportSheet(tem_save=True)
        ref = pd.read_excel(".tmp.xlsx", index_col=0)

        log = ''
        cmdList = []
        fileList = os.listdir(path)
        seq_pairs = {}
        task_sum = len(ref.index)
        task_count = 0
        for i in ref.index:
            try:
                sample = str(ref.loc[i, "样品名"]).replace(" ","")
                pool = str(ref.loc[i, "所在样品库"]).replace(" ","")
                index1 = ref.loc[i, "索引序列1"].strip()
                index2 = ref.loc[i, "索引序列2"].strip()
            except Exception as e:
                print(e)
                continue



            seqPair = []
            # 测序文件一一匹配
            for f in fileList:
                seq_name = f.split("_")[0]
                if seq_name == pool:
                    seqPair.append(path + "/" + f)

            seq_pairs[pool] = (seqPair)

            if seqPair:
                if ("_R1" in os.path.split(seqPair[0])[1]):
                    print("in")
                    r1 = seqPair[0]
                    r2 = seqPair[1]
                else:
                    r1 = seqPair[1]
                    r2 = seqPair[0]
                # ref.loc[i, "测序文件1"] = r1
                # ref.loc[i, "测序文件2"] = r2

                if len(seqPair) != 2:
                    print(pool)
                    print(seqPair)
                else:

                    # extractSample(index1,index2,r1,r2,output_path + "/" + sample + "_on_" + pool)
                    ref.loc[i,"测序文件1"] = sample + "_on_" + pool + "_R1.fastq"
                    ref.loc[i, "测序文件2"] = sample + "_on_" + pool + "_R2.fastq"
                    task_count = task_count + 1
                    cmd = "bash .extract.sh " + index1 + " " + index2 + " " + r1 + " " + r2 + " " +  output_path + "/" +sample + "_on_" + pool + "_R1.fastq " + output_path + "/"  + sample + "_on_" + pool + "_R2.fastq"
                    CMD = "{\n" + cmd + "\n}&\n" + "\n clear \n " + " touch /tmp/${uid}/" + str(task_count) + "\n\n"
                    bashData.append(CMD)
                    counter = counter + 1
                    if counter == thread:
                        bashData.append("\nwait\n")
                        counter = 0
            else:
                print(pool + " not found")
                log = log + (pool + " not found")
                continue

        bashData.append("\n wait \n rm -rf /tmp/${uid} \n")
        a = "".join(bashData)
        with open(".run.sh", "w") as f:
            f.write(a)



        # os.system("bash ./.run.sh")
        task_id = str(background_task.getUid())
        self.thread = bgThread(task_id)
        self.thread.finished.connect(self.summarize)
        self.ref = ref
        self.output_path = output_path

        self.monitor = background_task.monitorThread(task_id)
        self.progressBar.setRange(0, task_sum)

        self.thread.start()
        self.monitor.start()
        self.monitor.updated.connect(self.updateStatus)
        self.groupBox_status.setVisible(True)
        self.pushButton_generateFq.setEnabled(False)

    def updateStatus(self, status):
        self.progressBar.setValue(int(status))


    def summarize(self):
        self.monitor.terminate()
        self.groupBox_status.setVisible(False)
        self.pushButton_generateFq.setEnabled(True)
        lyric = getLyric()
        self.label.setText(lyric)
        time1 = time.ctime()
        ref = self.ref
        output_path = self.output_path
        ref.to_excel(output_path + "/样品信息.xlsx")
        QMessageBox.about(self,"Done","已完成！\n开始时间：" + self.time0 + "\n结束时间：" + time1)







    def chooseFolder(self):
        path = QFileDialog.getExistingDirectory(self,"选择 fastq.gz 数据文件夹")
        print(path)
        self.plainTextEdit_readIllumina.setPlainText(path)


    def installDependence(self):
        self.label.setText("正在安装，请少安毋躁")
        QMessageBox.about(self,"提示","注意，点了ok后，界面将卡住不动，不要关闭该程序！")
        lyric = getLyric()
        self.label.setText(lyric)
        import checkEnv
        checkEnv.check()

        bclInfo = subprocess.Popen(['~/miniconda3/bin/conda run bcl2fastq -v'], shell=True, stderr=subprocess.PIPE)
        verion = str(bclInfo.stderr.read().decode("utf-8"))
        print(verion)
        if "Illumina" in verion:
            print("### bcl2fastq ready ###")
            self.label_version.setText(verion)
        else:
            self.label_version.setText("未安装")
            verion = "安装失败，请重试"

        QMessageBox.about(self, "done", "安装进程已经结束,下面是安装详情\n" + verion)




    def disableAutoFill(self):
        self.checkBox_auto_fill_col.setChecked(False)

    def openFolder(self):
        try:

            # webbrowser.open("file://" + self.lineEdit_FqDir.text())
            os.popen("nautilus " + self.lineEdit_FqDir.text())
        except Exception as e:
            print(e)
            QMessageBox.about(self,"啊啊啊","自己打开文件浏览器看吧\n" + str(e))


    def delLine(self):
        selection = self.selected_rows
        for i in selection:
            try:
                self.tableWidget.removeRow(selection[0])
            except Exception as e:
                print(e)


    def exportSheet(self,tem_save = False):
        lyric = getLyric()
        self.label.setText(lyric)

        if tem_save == True:
            file_path = ".tmp.xlsx"
        else:
            file_path, type = QFileDialog.getSaveFileName(self, "存", "", "excel(*.xlsx)")
            if ".xlsx" in file_path[-5:]:
                pass
            else:
                file_path = file_path + ".xlsx"


        sheet = pd.DataFrame(columns = self.col_names)
        if file_path:
            pass
        else:
            return

        table = self.tableWidget

        for row in range(table.rowCount()):
            data = []
            for col in range(len(self.col_names)):
                try:
                    text = table.item(row, col).text()
                except:
                    text = ""
                data.append(text)
            sheet.loc[row] = data

        sheet.to_excel(file_path)
        return file_path

    def importFromSheet(self):
        file_path, type = QFileDialog.getOpenFileName(self,"导入", "","excel(*.xlsx)")
        lyric = getLyric()
        self.label.setText(lyric)
        if file_path:
            pass
        else:
            return

        sheet = pd.read_excel(file_path, index_col = 0)
        # count = self.tableWidget.rowCount()
        self.tableWidget.clearContents()
        self.tableWidget.setRowCount(len(sheet.index))

        for row in range(len(sheet.index)):
            data = sheet.iloc[row]
            for col in range(len(sheet.columns)):
                text = str(sheet.iloc[row][col])
                # if col == 0:
                #     if text == "nan":
                #         return
                if text == "nan":
                    text = ""

                self.tableWidget.setItem(row,col,QTableWidgetItem(text))

    def setSavePath(self):
        save_path = QFileDialog.getExistingDirectory(self,"选路径")
        if save_path:
            pass
        else:
            return False

        self.lineEdit_FqDir.setText(save_path)

        return save_path

    def autoInput(self):
        lyric = getLyric()
        self.label.setText(lyric)
        folder = self.plainTextEdit_readIllumina.toPlainText().replace("file://","").strip().replace("%20","\ ")
        self.plainTextEdit_readIllumina.setPlainText(folder)
        print(folder)


    def addLine(self):
        current_count = self.tableWidget.rowCount()
        self.tableWidget.setRowCount(current_count + 1)
        new_row = current_count + 1
        self.tableWidget.setItem(new_row,0,QTableWidgetItem(""))
        self.tableWidget.setItem(new_row, 1, QTableWidgetItem(""))
        self.tableWidget.setItem(new_row, 2, QTableWidgetItem(""))
        self.tableWidget.setItem(new_row, 3, QTableWidgetItem(""))
        self.tableWidget.setItem(new_row, 4, QTableWidgetItem(""))
        self.tableWidget.setItem(new_row, 5, QTableWidgetItem(""))
        self.tableWidget.setItem(new_row, 6, QTableWidgetItem(""))
        self.tableWidget.setItem(new_row, 7, QTableWidgetItem(""))

    def showSelection(self):
        selection = self.tableWidget.selectedIndexes()
        # self.currentSelectedIndex = selection
        # self.tabWidget.setCurrentIndex(0)
        rows = []
        names = []

        for i in selection:
            row = i.row()
            try:
                name = self.tableWidget.item(row, 0).text()
            except:
                name = ""

            if row in rows:
                pass
            else:
                rows.append(row)
                names.append(name)
        if len(rows) > 10:
            self.label_selection.setText("选中了" + str(len(rows)) + "个")
        else:
            self.label_selection.setText(str(names))
        self.selected_rows = rows

        col = self.tableWidget.currentColumn()
        if self.checkBox_auto_fill_col.isChecked():
            try:
                first_item = self.tableWidget.item(rows[0], col)
                first_data = first_item.text()
            except:
                first_data = ""

            for i in selection:
                row = i.row()
                self.tableWidget.setItem(row, col, QTableWidgetItem(first_data))




    def clearTable(self):
        self.tableWidget.clearContents()
        self.tableWidget.setRowCount(0)
        lyric = getLyric()
        self.label.setText(lyric)



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
