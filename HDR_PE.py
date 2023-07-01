import os
import zipfile
import time

from PyQt5 import QtCore
from PyQt5.QtWidgets import QMainWindow, QApplication, QTableWidgetItem, QFileDialog, QMessageBox
import pandas as pd
from gui_PE import Ui_CRISPResso
import subprocess
import requests
from background_task import lyricThread, bgCRISPResso


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
    return  result


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


class MyMainWin(QMainWindow, Ui_CRISPResso):
    def __init__(self, parent = None):
        super(MyMainWin, self).__init__(parent)

        self.setupUi(self)
        # self.version = "1.2.0"
        # self.setWindowTitle(self.windowTitle() + "v"+self.version)
        output = "使用CRISPResso2分析Fastq文件" + "\n\t\t\t" + "——Written by M.Q. at Ma lab, ShanghaiTech University"
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
        self.pushButton_stop.clicked.connect(self.stopTread)

        self.pushButton_stop.setVisible(False)
        # update lyric
        self.lyricThread = lyricThread()
        self.lyricThread.updated.connect(self.updateLyric)



        # 按键区域
        self.pushButton_install.clicked.connect(self.installDependence)
        self.pushButton_generateFq.clicked.connect(self.start)
        self.pushButton_chooseFolder.clicked.connect(self.chooseFolder)

        crisprInfo = subprocess.Popen(['~/miniconda3/bin/conda run CRISPResso --version'], shell=True, stdout=subprocess.PIPE)
        verion = str(crisprInfo.stdout.read().decode("utf-8"))
        # print(verion)
        if "[CRISPResso" in verion:
            print("### CRISPResso2 ready ###")
            self.label_version.setText(str(verion.splitlines()[-2:]))
            self.pushButton_install.setVisible(False)
        else:
            self.label_version.setText("未安装")
            self.pushButton_install.setVisible(True)

    def stopTread(self):
        self.lyricThread.terminate()
        self.thread.terminate()
        self.groupBox_status.setVisible(False)
        self.pushButton_generateFq.setEnabled(True)
        self.summarize()
        self.progressBar.setValue(0)
        QMessageBox.about(self, "停止",
                          "已停止，目前已经分析的部分样品将会被汇总。\n\n 在停止的这个瞬间，后台尚有数个样品正在分析，可能会稍微多占用几分钟电脑资源，无需理会即可。")

    def updateLyric(self,lyric):
        self.label.setText(lyric)

    # 功能区
    def start(self):
        self.lyricThread.start()
        if self.plainTextEdit_readIllumina.toPlainText() == "":
            QMessageBox.about(self, "Fastq folder not set", "ERROR:\n必须指定fastq文件所在的文件夹！")
            return 0

        if self.setSavePath():
            pass
        else:
            return 0
        self.label.setText(""" ε٩(๑> ₃ <)۶з  正在运行，界面会卡住很久，请少安毋躁♥""")
        output_path = self.lineEdit_FqDir.text()
        path = self.plainTextEdit_readIllumina.toPlainText()
        if path == "":
            return
        self.exportSheet(tem_save=True)
        ref = pd.read_excel(".tmp.xlsx",index_col=0)
        lyric = getLyric()
        self.label.setText(lyric)

        # 生成批处理文件
        bashData = ["#!/bin/bash\n  source ~/miniconda3/bin/activate base \n"]  # bash文件头
        authorInfo = """# This Script is generated automatically. Do not modify anything unless you know what you are doing.
                # Script Author:\tMo Qiqin
                # Contact:\tmoqq@shanghaitech.edu.cn\n
                uid=$1
                mkdir /tmp/${uid}
                """
        bashData.append(authorInfo)
        thread = int(os.cpu_count() *2)
        if thread < 8:
            thread = 8
        counter = 0

        log = ''
        cmdList = []
        fileList = os.listdir(path)
        CRISPResso = "CRISPResso"
        parameter = "  " + self.plainTextEdit_parameters.toPlainText().replace("\n","  ")
        # print(parameter)
        # seqPair_sheet = pd.DataFrame(columns=["样品名","描述","测序文件1","测序文件2"])

        task_sum = len(ref.index)
        task_count = 0
        for i in ref.index:
            task_count = task_count + 1
            sample = str(ref.loc[i]["样品名"])
            sg1 = ref.loc[i]["sg1"]
            sg2 = ref.loc[i]["sg2"]
            seqPair = []

            # 测序文件一一匹配
            splitor = self.lineEdit_split.text().strip()
            for f in fileList:
                if (sample + splitor) in f:
                    seqPair.append(path + "/" + f)

            if seqPair:
                try:
                    r1 = seqPair[0]
                    ref.loc[i,"测序文件2"] = os.path.basename(r1)
                except Exception as e:
                    ref.loc[i, "测序文件2"] = "无文件"
                try:
                    r2 = seqPair[1]
                    ref.loc[i, "测序文件1"] = os.path.basename(r2)
                except Exception as e:
                    ref.loc[i, "测序文件1"] = "无文件"
            else:
                print(sample + " not found")
                log = log + (sample + " not found")
                continue

            # sg序列读取
            if (str(sg2) != "nan") and ("nan" != str(sg1)):
                sg = sg1.strip() + "," + sg2.strip()
                # print(sg)
            else:
                sg = str(sg1) + str(sg2)
                sg = sg.replace("nan", "")
                # print(sg)

            # 比对的目标序列
            amplicon = ref.loc[i]["原始序列"]
            hdrRef = ref.loc[i]["修改后序列"]

            if len(seqPair) == 1:
                cmd = CRISPResso + (" -r1 %s   -a %s -g %s  -e %s " % (
                    r1, amplicon, sg, hdrRef)) + "  " + parameter + " -o %s/%s" % (output_path, sample)
            elif len(seqPair) == 2:
                cmd = CRISPResso + (" -r1 %s -r2 %s  -a %s -g %s  -e %s " % (
                r1, r2, amplicon, sg, hdrRef)) + "  " + parameter + " -o %s/%s" % (output_path , sample)
            else:
                QMessageBox.about(self, "Error",f"出错🌶\n\n 根据样品名在文件夹中找到多个文件：\n{seqPair}，\n\n请把非测序文件移出测序文件夹，或更改识别样品名模式。")
                return
            cmdList.append(cmd)
            # cmdFrame.loc[sample, "cmd"] = cmd

            CMD = "{\n" + cmd + "\n}&\n" + "\n clear \n" + " touch /tmp/${uid}/" + str(task_count) + "\n\n"
            bashData.append(CMD)
            counter = counter + 1
            if counter == thread:
                bashData.append("\nwait\n")
                counter = 0

        bashData.append("\n wait \n rm -rf /tmp/${uid} ")
        a = "".join(bashData)
        with open(".run.sh", "w") as f:
            f.write(a)


        # time0 = str(time.ctime())
        # info = os.system("bash ./.run.sh")
        self.ref = ref
        self.time0 = str(time.ctime())
        self.progressBar.setRange(0, 0)
        self.progressBar.setValue(0)
        self.groupBox_status.setVisible(True)
        self.pushButton_generateFq.setEnabled(False)
        # self.thread = bgCRISPResso(uid="", cmdList=cmdList)
        from background_task import bgCRISPResso2
        self.thread = bgCRISPResso2(cmdList=cmdList)
        self.thread.updated.connect(self.updateStatus)
        self.thread.finished.connect(self.summarize)
        self.thread.start()
        self.task_sum = task_sum

    def updateStatus(self, num):
        self.progressBar.setRange(0, self.task_sum)
        current_value = int(self.progressBar.value())
        self.progressBar.setValue(int(current_value + num))

    def summarize(self):
        # 数据汇总
        # self.monitor.terminate()
        self.progressBar.setValue(0)
        self.lyricThread.terminate()
        self.groupBox_status.setVisible(False)
        self.pushButton_generateFq.setEnabled(True)

        ref = self.ref
        output_path = self.lineEdit_FqDir.text()
        summaryFiles = ''
        sampleIndex = {}
        errorResults = []
        result = pd.DataFrame(columns=["描述", "正确编辑占总体的比例",
                                       "正确编辑占总编辑的比例",
                                       "Indel占总体比例",

                                       "NHEJ占总体体比例",
                                       "总读数",
                                       "实际使用读数",
                                       ])
        n = 0
        for i in ref.index:
            name = str(ref.loc[i, "样品名"].strip())
            result.loc[name, "描述"] = ref.loc[i, "描述"]
            resultDir = output_path + "/"+ name
            try:
                os.listdir(resultDir)
            except:
                result.loc[name, "正确编辑占总体的比例"] = "无测序文件"
                continue

            for f in os.listdir(resultDir):
                if "html" in f:
                    pass
                elif "ipynb" in f:
                    pass
                else:
                    folder = f
                    logFile = resultDir + "/" + folder + "/CRISPResso_RUNNING_LOG.txt"
                    allelesFrequencyTable = resultDir + "/" + folder + "/Alleles_frequency_table.zip"
                    resultFile = resultDir + "/" + folder + "/CRISPResso_quantification_of_editing_frequency.txt"

            # 判断有没有对这个样品进行分析
            if os.path.isfile(logFile):
                # 分析日志存在
                pass
            else:
                # 分析日志不存在
                result.loc[name, "正确编辑占总体的比例"] = "No enough reads"
                print(name + "error, 未进行CRISPResso分析")
                continue  # 跳过循环，下一个样品

            # 日志存在，继续进行分析。打开日志文件，读取信息
            try:
                with open(logFile) as log:
                    o = log.read()
                    if "ERROR" in o:  # 分析过程中出错，一般为reads数为0才出错。其次是分析窗口超出范围。
                        errorResults.append(name)
                        result.loc[name, "正确编辑占总体的比例"] = "No enough reads"
                        for line in o.splitlines():
                            if "ERROR" in line:
                                print(name + line)
                        continue
                    else:
                        # 1. 解压、读取分析结果文件
                        allelesFrequencyTableZip = zipfile.ZipFile(allelesFrequencyTable)
                        allelesData = allelesFrequencyTableZip.read('Alleles_frequency_table.txt')
                        allelesFrequencyTableZip.extractall(resultDir + "/" + folder + "/")

                        # 2. 逐条进行判断是否为ambiguous Indel
                        ambiguousIndel = 0
                        allelesFrequencyTable = pd.read_csv(resultDir + "/" + folder + "/Alleles_frequency_table.txt",
                                                            sep='\t')
                        for i in allelesFrequencyTable.index:
                            if allelesFrequencyTable.loc[i, "Reference_Name"] == "AMBIGUOUS_Reference":
                                if allelesFrequencyTable.loc[i, "n_deleted"] + allelesFrequencyTable.loc[
                                    i, "n_deleted"] > 0:
                                    reads = allelesFrequencyTable.loc[i, "#Reads"]
                                    ambiguousIndel = ambiguousIndel + reads

                        # 3. 读取非ambiguous 序列的indel数据
                        resultFrame = pd.read_csv(resultFile, sep='\t')
                        # print(ambiguousIndel)
                        HDR_unmodified = resultFrame.loc[1, 'Unmodified']
                        allHDR = resultFrame.loc[1, 'Reads_aligned']
                        HDR_modified = resultFrame.loc[1, 'Modified']
                        reads_aligned = resultFrame.loc[1, 'Reads_aligned_all_amplicons']
                        reads = resultFrame.loc[1, 'Reads_in_input']
                        NHEJreads = resultFrame.loc[0, "Modified"]
                        insertion = int(resultFrame.loc[0, "Insertions"]) + int(resultFrame.loc[1, "Insertions"])
                        deletion = int(resultFrame.loc[0, "Deletions"]) + int(resultFrame.loc[1, "Deletions"])
                        insertionAndDeletion = int(resultFrame.loc[0, "Insertions and Deletions"]) + int(
                            resultFrame.loc[1, "Insertions and Deletions"])

                        substitution = int(resultFrame.loc[0, "Substitutions"]) + int(resultFrame.loc[1, "Substitutions"])
                        HDR_insertion = resultFrame.loc[0, "Insertions"]

                        # 4. 测序深度过滤
                        if reads_aligned < 1500:
                            result.loc[name, "正确编辑占总体的比例"] = "No enough reads"
                            print(name, "reads 过少")
                            n = n + 1
                            continue

                        result.loc[name, "总读数"] = reads
                        result.loc[name, "实际使用读数"] = reads_aligned

                        try:
                            result.loc[name, "正确编辑占总体的比例"] = "%.2f%%" % (
                                        float(HDR_unmodified) / float(reads_aligned) * 100)
                        except:
                            result.loc[name, "正确编辑占总体的比例"] = "%.2f%%" % (float(0))

                        try:
                            result.loc[name, "正确编辑占总编辑的比例"] = "%.2f%%" % (
                                        float(HDR_unmodified) / float(allHDR) * 100)
                        except:
                            result.loc[name, "正确编辑占总编辑的比例"] = "%.2f%%" % (float(0) * 100)

                        try:
                            result.loc[name, "NHEJ占总体体比例"] = "%.2f%%" % (
                                        float(NHEJreads) / float(reads_aligned) * 100)
                        except:
                            result.loc[name, "NHEJ占总体体比例"] = "%.2f%%" % (float(0) * 100)

                        # try:
                        #    result.loc[name,"Indel占总体比例"] = "%.2f%%" % ((float(insertion) + float(deletion)) / float(reads_aligned)*100)
                        # except:
                        #    result.loc[name,"Indel占总体比例"] = "%.2f%%" % (float(0)*100)

                        try:
                            result.loc[name, "Indel占总体比例"] = "%.2f%%" % ((float(insertion) + float(deletion) + float(
                                ambiguousIndel) - insertionAndDeletion) / float(reads_aligned) * 100)
                        except:
                            result.loc[name, "Indel占总体比例"] = "%.2f%%" % (float(0) * 100)
            except Exception as e:
                print(e)
                continue

        time1 = str(time.ctime())
        result.loc[
            "备注", "正确编辑占总体的比例"] = "有发生insertion 或者 deletetion的，或者两者同时发生的算为一个indel。统计来源：与原始amplicon类似的reads（NHEJ），与预期序列类似的（imperfect HDR），与原始、预期都相似但无法判断的reads（AMBIGUOUS）"
        result.loc[
            "Method", "正确编辑占总体的比例"] = "Modified genome was amplified and sequenced using illumina MiniSeq®. Each amlicon-seq data was analysed wiht CRISPResso2 and summarized by a home-made script. The indel is regard as the reads with insertion or deletion, but subsitution. Data analysis was performed by Qiqin Mo, and the code is avalibele at https://github.com/Hanhui-Ma-Lab/Script_for_Amplicon-seq "
        result.to_excel(output_path + "/结果汇总.xlsx")
        ref.to_excel(output_path + "/原始信息表格.xlsx")
        QMessageBox.about(self,"Done","已完成！\n开始时间：" + self.time0 + "\n结束时间：" + time1)






    def chooseFolder(self):
        path = QFileDialog.getExistingDirectory(self,"选择fastq数据所在的文件夹")
        print(path)
        self.plainTextEdit_readIllumina.setPlainText(path)


    def installDependence(self):
        self.label.setText("正在安装，请少安毋躁")
        QMessageBox.about(self,"提示","注意，点了ok后，界面将卡住不动，不要关闭该程序！")
        lyric = getLyric()
        self.label.setText(lyric)
        import checkEnv
        checkEnv.check()

        crisprInfo = subprocess.Popen(['~/miniconda3/bin/conda run CRISPResso --version'], shell=True,
                                      stdout=subprocess.PIPE)
        verion = str(crisprInfo.stdout.read().decode("utf-8"))
        # print(verion)
        if "[CRISPResso" in verion:
            print("### CRISPResso2 ready ###")
            self.label_version.setText(str(verion.splitlines()[-2:]))
        else:
            self.label_version.setText("未安装")

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
            file_path =  ".tmp.xlsx"
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