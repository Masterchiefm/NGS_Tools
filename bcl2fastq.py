import os
import json
import time

from PyQt5 import QtCore
from PyQt5.QtWidgets import QMainWindow, QApplication, QTableWidgetItem, QFileDialog, QMessageBox
import pandas as pd
from gui_bcl2fq import Ui_BCL2Fastq
import subprocess
import requests

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


class MyMainWin(QMainWindow, Ui_BCL2Fastq):
    def __init__(self, parent = None):
        super(MyMainWin, self).__init__(parent)

        self.setupUi(self)
        self.version = "1.2.0"
        self.setWindowTitle(self.windowTitle() + "v"+self.version)
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

        # 按键区域
        self.pushButton_install_bcl2fq.clicked.connect(self.installDependence)
        self.pushButton_generateFq.clicked.connect(self.writeSampleSheet)
        self.pushButton_chooseFolder.clicked.connect(self.chooseFolder)

        bclInfo = subprocess.Popen(['~/miniconda3/bin/conda run bcl2fastq -v'], shell=True, stderr=subprocess.PIPE)
        verion = str(bclInfo.stderr.read().decode("utf-8"))
        print(verion)
        if "Illumina" in verion:
            print("### bcl2fastq ready ###")
            self.label_version.setText(verion)
        else:
            self.label_version.setText("未安装")









    # 功能区
    def writeSampleSheet(self):
        header = """[Header],,,,,,,
IEMFileVersion,5,,,,,,
Date,2023/1/1,,,,,,
Workflow,GenerateFASTQ,,,,,,
Application,HiSeq FASTQ Only,,,,,,
Instrument Type,MiniSeq,,,,,,
Assay,Ampliseq,,,,,,
Index Adapters,Illumina Universal Adapters,,,,,,
Chemistry,DNA,,,,,,
,,,,,,,
[Reads],,,,,,,
,,,,,,,
,,,,,,,
,,,,,,,
[Data],,,,,,,"""
        sheet = pd.DataFrame(columns=["Sample_ID","Index_Plate_Well","I5_Index_ID",'index2','I7_Index_ID','index','Sample_Project','Description'])
        table = self.tableWidget

        for row in range(table.rowCount()):
            try:
                ID = table.item(row,0).text()
                I5_ID = table.item(row,1).text()
                I5_seq = table.item(row, 2).text()
                I7_ID = table.item(row, 3).text()
                I7_seq = table.item(row, 4).text()
                description = table.item(row, 5).text()

                if self.checkBox_reI5.isChecked():
                    I5_seq = reverseDNA(I5_seq)
                if self.checkBox_reI7.isChecked():
                    I7_seq = reverseDNA(I7_seq)


                sheet.loc[row, "Sample_ID"] = ID
                sheet.loc[row, "I5_Index_ID"] = I5_ID
                sheet.loc[row, "index2"] = I5_seq
                sheet.loc[row, "I7_Index_ID"] = I7_ID
                sheet.loc[row, "index"] = I7_seq
                sheet.loc[row, "Description"] =description

            except:
                continue



        if self.plainTextEdit_readIllumina.toPlainText() == "":
            QMessageBox.about(self,"错误","下机文件夹未填写")
            return
        sheet.to_csv(self.plainTextEdit_readIllumina.toPlainText() + "/SampleSheet0.csv",index=False)
        with open(self.plainTextEdit_readIllumina.toPlainText() + "/SampleSheet0.csv","r") as f:
            sheet_text = f.read()
        with open(self.plainTextEdit_readIllumina.toPlainText() + "/SampleSheet.csv", "w") as f:
            content = header+"\n" + sheet_text
            f.write(content)


        self.setSavePath()
        output_path = self.lineEdit_FqDir.text()
        "bcl2fastq  -R  /home/chief/220926_MN00855_0018_A000H3NJMC  -o  /home/chief/out  --sample-sheet  /home/chief/220926_MN00855_0018_A000H3NJMC/SampleSheet.csv   --barcode-mismatches   0 "
        bcl2fq = "bcl2fastq "
        log = "/tmp/bcl2fastq_" + str(time.time())
        cmd = bcl2fq + " -R " + self.plainTextEdit_readIllumina.toPlainText().strip()  + " -o " + self.lineEdit_FqDir.text() + \
              " " +self.lineEdit_parameter.text() + " " + \
              " --sample-sheet " + self.plainTextEdit_readIllumina.toPlainText().strip() +"/SampleSheet.csv  "
        with open(".run.sh","w") as f:
            content = """#!/bin/bash
            source ~/miniconda3/bin/activate base
            echo 开始分析\n
            """ + cmd
            f.write(content)

        info = subprocess.Popen(["bash ./.run.sh"],shell=True,stderr=subprocess.PIPE)
        info = str(info.stderr.read())
        # print(info)
        try:
            with open(log,"w") as f:
                f.write(info)
        except Exception as e:
            print(e)

        log_last = log_last = info.split("]")
        QMessageBox.about(self,"运行结果",log_last[-1] + "\n\n以上为本次运行结果的最后一行输出。\n\n若有错请在终端重新运行，并根据输出修改错误。刚刚运行的指令为\n\n" +cmd)

        # os.system("gedit " + log)
        lyric = getLyric()
        self.label.setText(lyric)







    def chooseFolder(self):
        path = QFileDialog.getExistingDirectory(self,"选择下机数据文件夹")
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
            file_path = self.lineEdit_path.text() + "/临时存储.xlsx"
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