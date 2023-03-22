import os
import re
import time

from PyQt5 import QtCore
from PyQt5.QtWidgets import QMainWindow, QApplication, QTableWidgetItem, QFileDialog, QMessageBox
import pandas as pd
from gui_BE import Ui_CRISPResso
import subprocess
import requests
import webbrowser

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
        else:
            self.label_version.setText("未安装")


    # 功能区
    def start(self):
        self.label.setText(""" ε٩(๑> ₃ <)۶з  正在运行，界面会卡住很久，请少安毋躁♥""")
        self.setSavePath()
        output_path = self.lineEdit_FqDir.text()
        path = self.plainTextEdit_readIllumina.toPlainText()
        if path == "":
            return
        self.exportSheet(tem_save=True)
        ref = pd.read_excel(".tmp.xlsx",index_col=0)
        newRef = pd.DataFrame(columns=ref.columns)
        newRef.to_excel('.tmp2.xlsx')
        for i in ref.index:
            try:
                sample = ref.loc[i, "样品名"]
                base_from =  ref.loc[i, "原始碱基"].upper()
                base_to = ref.loc[i, "修改后碱基"].upper()
                edit_site = str(ref.loc[i, "最想看的位置"])
                if str(edit_site) == "nan":
                    edit_site = 0
                output_name = sample + "_" + edit_site + "-"  + base_from + "-" + base_to

                newRef.loc[output_name] = ref.loc[i]
            except:
                continue



        lyric = getLyric()
        self.label.setText(lyric)
        parameter = "  " + self.plainTextEdit_parameters.toPlainText().replace("\n","  ")

        # 生成批处理文件

        bashData = ["#!/bin/bash\n source ~/miniconda3/bin/activate base \n date > timeCounter \n"]  # bash文件头
        authorInfo = """# This Script is generated automatically. Do not modify anything unless you know what you are doing.
                # Script Author:\tMo Qiqin
                # Contact:\tmoqq@shanghaitech.edu.cn\n
                """
        bashData.append(authorInfo)
        thread = 12
        counter = 0

        log = ''
        cmdList = []
        fileList = os.listdir(path)
        seq_pairs = {}
        for i in newRef.index:
            sample = str(newRef.loc[i]["样品名"]).strip()
            output_name = str(i).strip()
            sg = newRef.loc[i]["sg"]
            # sg2 = ref.loc[i]["sgRNA2"]
            seqPair = []

            # 测序文件一一匹配
            for f in fileList:
                seq_name = f.split("_")[0]
                if seq_name == sample:
                    seqPair.append(path + "/" + f)

            seq_pairs[sample] = (seqPair)

            if seqPair:
                r1 = seqPair[0]
                r2 = seqPair[1]
                newRef.loc[i,"测序文件1"] = r1
                newRef.loc[i,"测序文件2"] = r2

                if len(seqPair) != 2:
                    print(sample)
                    print(seqPair)
            else:
                print(sample + " not found")
                log = log + (sample + " not found")
                continue

            # 比对的目标序列
            amplicon = newRef.loc[i]["原始序列"]
            baseFrom = newRef.loc[i]["原始碱基"].upper()
            baseTo = newRef.loc[i]["修改后碱基"].upper()


            # 判断是否为被编辑的链
            if sg.upper().strip() in reverseDNA(amplicon.upper()):
                amplicon = reverseDNA(amplicon)
                print("non edit strand provided, I'll reverse it.")

            # qualitification windown size and center
            center = str(int(len(sg) / 2))
            win = str(int((int(len(sg) / 2)) + len(sg)%2))

            cmd = "CRISPResso  --base_editor_output  " + (" -r1 %s -r2 %s  -a %s -g %s  --conversion_nuc_from %s --conversion_nuc_to %s " % (
            r1, r2, amplicon, sg, baseFrom, baseTo)) + \
                  parameter + " --quantification_window_center -" + center + " -w " + win + " --plot_window_size " + win + \
                  " -o %s/%s" % (output_path, output_name)
            cmdList.append(cmd)
            # cmdFrame.loc[sample, "cmd"] = cmd

            CMD = "{\n" + cmd + "\n}&\n" + "\n clear \n"
            bashData.append(CMD)
            counter = counter + 1
            if counter == thread:
                bashData.append("\nwait\n")
                counter = 0

        bashData.append("\n wait \n date >> timeCounter\n")
        a = "".join(bashData)
        with open(".run.sh", "w") as f:
            f.write(a)


        # 正式开始分析
        time0 = str(time.ctime())
        info = os.system("bash ./.run.sh")


        # 汇总结果
        fileList = os.listdir()
        summaryFiles = ''
        sampleIndex = {}
        errorResults = []
        result = pd.DataFrame(columns=["样品名", "描述",
                                       "原始碱基",
                                       "修改后碱基",
                                       "最想看的位置",
                                       "最想看的位置的效率",
                                       "测序深度",
                                       "各位点的特异性编辑效率",
                                       '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15',
                                       '16', '17', '18', '19', '20',
                                       '21', '22', '23', '24', '25', '26', '27', '28', '29', '30', '31', '32', '33',
                                       '34', '35', '36', '37', '38', '39', '40',
                                       "各位点的非特异编辑效率",
                                       'u1', 'u2', 'u3', 'u4', 'u5', 'u6', 'u7', 'u8', 'u9', 'u10', 'u11', 'u12', 'u13',
                                       'u14', 'u15', 'u16', 'u17', 'u18', 'u19', 'u20',
                                       'u21', 'u22', 'u23', 'u24', 'u25', 'u26', 'u27', 'u28', 'u29', 'u30', 'u31',
                                       'u32', 'u33', 'u34', 'u35', 'u36', 'u37', 'u38', 'u39', 'u40'
                                       ])

        n = 0
        for i in newRef.index:
            name = str(i)
            real_name = str(newRef.loc[i, "样品名"]).strip()
            # ex_time = str(ref.loc[i,"时间"]).strip()
            resultDir = output_path + "/" + name


            desire_position = str(newRef.loc[i,"最想看的位置"])
            result.loc[name, "最想看的位置"] = desire_position

            try:
                for f in os.listdir(resultDir):
                    if "html" in f:
                        pass
                    elif "ipynb" in f:
                        pass
                    else:
                        folder = f
                        logFile = resultDir + "/" + folder + "/CRISPResso_RUNNING_LOG.txt"
                        infoFile = resultDir + "/" + folder + "/CRISPResso2_info.json"
                        subsitutionFile = resultDir + "/" + folder + "/Quantification_window_substitution_frequency_table.txt"


            except Exception as e:
                print(e)
                input()
                continue

            with open(logFile) as log:
                o = log.read()
                if "ERROR" in o:
                    errorResults.append(name)
                    result.loc[name, "原始碱基"] = "No enough reads"
                    print(name + " error")
                else:

                    # result.loc[name,"Indel占总体比例"] = "%.2f%%" % (float(0)*100)
                    with open(infoFile) as info:
                        info = info.read()
                        baseFromPattern = re.compile('"conversion_nuc_from": "(.)"')
                        baseToPattern = re.compile('"conversion_nuc_to": "(.)"')
                        baseFrom = baseFromPattern.findall(info)[0].upper()
                        baseTo = baseToPattern.findall(info)[0].upper()
                        sgPattern = re.compile('Selected_nucleotide_frequency_table_around_sgRNA_.*?\.txt?')
                        sgFile = sgPattern.search(info).group()

                        result.loc[name, "原始碱基"] = baseFrom.upper()
                        result.loc[name, "修改后碱基"] = baseTo.upper()
                        result.loc[name, "样品名"] = real_name
                        result.loc[name, "描述"] = str(newRef.loc[i, "描述"]).strip()
                        # result.loc[name,"时间"] = ex_time

                    editTable = pd.read_csv(resultDir + "/" + folder + "/" + sgFile, sep="\t")

                    for location in editTable.columns:
                        if "Unn" in location:
                            # print("Fuck " + location)
                            pass
                        else:
                            editLocation = str(location[1:])
                            # print(editTable)
                            # print(editLocation)
                            # input()
                            baseReads = {}
                            baseReads["A"] = int(editTable.loc[0, location])
                            baseReads["C"] = int(editTable.loc[1, location])
                            baseReads["G"] = int(editTable.loc[2, location])
                            baseReads["T"] = int(editTable.loc[3, location])
                            baseReads["N"] = int(editTable.loc[4, location])
                            baseReads["-"] = int(editTable.loc[5, location])
                            allReads = sum(baseReads.values())

                            editReads = "%.2f%%" % (float(baseReads[baseTo] / allReads) * 100)
                            # unspecificEditReads = "%.2f%%" % (float((allReads - baseReads[baseFrom] - baseReads[baseTo]) /allReads)*100)
                            # uneditReads = "%.2f%%" % (( baseReads[baseFrom] /allReads)*100)

                            result.loc[name, str(editLocation)] = editReads
                            # print(editReads)
                            result.loc[name, "测序深度"] = allReads

                            if str(int(editLocation)) == desire_position:
                                result.loc[name, "最想看的位置的效率"] = editReads

                            # result.loc[name,"n" + editLocation] = unspecificEditReads

                    subTable = pd.read_csv(subsitutionFile, sep="\t")

                    # print(allReads)
                    n = 0
                    for base in subTable.columns:

                        baseReads = {}
                        # print(subTable.iloc[0,n])
                        try:
                            baseReads["A"] = subTable.iloc[0, n + 1]
                            baseReads["C"] = subTable.iloc[1, n + 1]
                            baseReads["G"] = subTable.iloc[2, n + 1]
                            baseReads["T"] = subTable.iloc[3, n + 1]
                            baseReads["N"] = subTable.iloc[4, n + 1]
                            allSubReads = sum(baseReads.values())
                            # print(name , allReads)
                            # print(name, baseReads[baseFrom],baseReads[baseTo])
                            unspecificEditReads = "%.2f%%" % (
                                        float((allSubReads - baseReads[baseFrom] - baseReads[baseTo]) / allReads) * 100)
                            # unspecificEditReads =  (float((allReads - baseReads[baseFrom] - baseReads[baseTo]) /allReads)*100)
                            result.loc[name, "u" + str(n + 1)] = unspecificEditReads
                            n = n + 1
                        except:
                            n = n + 1
                            pass

        time1 = str(time.ctime())
        result.to_excel(output_path + "/结果汇总.xlsx")
        newRef.to_excel(output_path + "/原始信息表格.xlsx")
        QMessageBox.about(self, "Done", "已完成！\n开始时间：" + time0 + "\n结束时间：" + time1)

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
            webbrowser.open("file://" + self.lineEdit_FqDir.text())
            # os.popen("nautilus " + self.lineEdit_FqDir.text())
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