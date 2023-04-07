# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/chief/PycharmProjects/NGS_Tools/gui_demultiplex.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_BCL2Fastq(object):
    def setupUi(self, BCL2Fastq):
        BCL2Fastq.setObjectName("BCL2Fastq")
        BCL2Fastq.resize(1046, 1274)
        self.centralwidget = QtWidgets.QWidget(BCL2Fastq)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setMaximumSize(QtCore.QSize(16777215, 150))
        self.groupBox.setObjectName("groupBox")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.groupBox)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.plainTextEdit_readIllumina = PlainTextEdit(self.groupBox)
        self.plainTextEdit_readIllumina.setMaximumSize(QtCore.QSize(16777215, 250))
        self.plainTextEdit_readIllumina.setObjectName("plainTextEdit_readIllumina")
        self.horizontalLayout_2.addWidget(self.plainTextEdit_readIllumina)
        self.pushButton_chooseFolder = QtWidgets.QPushButton(self.groupBox)
        self.pushButton_chooseFolder.setObjectName("pushButton_chooseFolder")
        self.horizontalLayout_2.addWidget(self.pushButton_chooseFolder)
        self.verticalLayout_3.addWidget(self.groupBox)
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setWordWrap(True)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_3.addWidget(self.label_4)
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setWordWrap(True)
        self.label_5.setObjectName("label_5")
        self.verticalLayout_3.addWidget(self.label_5)
        self.groupBox_2 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_2.setInputMethodHints(QtCore.Qt.ImhPreferNumbers)
        self.groupBox_2.setFlat(False)
        self.groupBox_2.setObjectName("groupBox_2")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.groupBox_2)
        self.verticalLayout.setObjectName("verticalLayout")
        self.checkBox_auto_fill_col = QtWidgets.QCheckBox(self.groupBox_2)
        self.checkBox_auto_fill_col.setObjectName("checkBox_auto_fill_col")
        self.verticalLayout.addWidget(self.checkBox_auto_fill_col)
        self.tableWidget = QtWidgets.QTableWidget(self.groupBox_2)
        self.tableWidget.setMinimumSize(QtCore.QSize(0, 300))
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(7)
        self.tableWidget.setRowCount(4)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(5, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(6, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setItem(0, 0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setItem(0, 1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setItem(0, 2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setItem(0, 3, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setItem(0, 4, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setItem(0, 5, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setItem(0, 6, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setItem(1, 0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setItem(1, 2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setItem(1, 4, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setItem(1, 6, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setItem(2, 0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setItem(2, 2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setItem(2, 4, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setItem(2, 6, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setItem(3, 0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setItem(3, 2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setItem(3, 4, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setItem(3, 6, item)
        self.verticalLayout.addWidget(self.tableWidget)
        self.frame = QtWidgets.QFrame(self.groupBox_2)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.frame)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.pushButton_add_line = QtWidgets.QPushButton(self.frame)
        self.pushButton_add_line.setObjectName("pushButton_add_line")
        self.horizontalLayout.addWidget(self.pushButton_add_line)
        self.pushButton_del_lines = QtWidgets.QPushButton(self.frame)
        self.pushButton_del_lines.setObjectName("pushButton_del_lines")
        self.horizontalLayout.addWidget(self.pushButton_del_lines)
        self.pushButton_import_from_sheet = QtWidgets.QPushButton(self.frame)
        self.pushButton_import_from_sheet.setObjectName("pushButton_import_from_sheet")
        self.horizontalLayout.addWidget(self.pushButton_import_from_sheet)
        self.pushButton_export_sheet = QtWidgets.QPushButton(self.frame)
        self.pushButton_export_sheet.setObjectName("pushButton_export_sheet")
        self.horizontalLayout.addWidget(self.pushButton_export_sheet)
        self.pushButton_clear_table = QtWidgets.QPushButton(self.frame)
        self.pushButton_clear_table.setObjectName("pushButton_clear_table")
        self.horizontalLayout.addWidget(self.pushButton_clear_table)
        self.verticalLayout.addWidget(self.frame)
        self.frame_2 = QtWidgets.QFrame(self.groupBox_2)
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.frame_2)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label_selection = QtWidgets.QLabel(self.frame_2)
        self.label_selection.setObjectName("label_selection")
        self.verticalLayout_2.addWidget(self.label_selection)
        self.verticalLayout.addWidget(self.frame_2)
        self.frame_3 = QtWidgets.QFrame(self.groupBox_2)
        self.frame_3.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_3.setObjectName("frame_3")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.frame_3)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.label_3 = QtWidgets.QLabel(self.frame_3)
        self.label_3.setObjectName("label_3")
        self.verticalLayout_4.addWidget(self.label_3)
        self.label_version = QtWidgets.QLabel(self.frame_3)
        self.label_version.setObjectName("label_version")
        self.verticalLayout_4.addWidget(self.label_version)
        self.pushButton_install_bcl2fq = QtWidgets.QPushButton(self.frame_3)
        self.pushButton_install_bcl2fq.setObjectName("pushButton_install_bcl2fq")
        self.verticalLayout_4.addWidget(self.pushButton_install_bcl2fq)
        self.verticalLayout.addWidget(self.frame_3)
        self.verticalLayout_3.addWidget(self.groupBox_2)
        self.groupBox_10 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_10.setObjectName("groupBox_10")
        self.verticalLayout_9 = QtWidgets.QVBoxLayout(self.groupBox_10)
        self.verticalLayout_9.setObjectName("verticalLayout_9")
        self.pushButton_generateFq = QtWidgets.QPushButton(self.groupBox_10)
        self.pushButton_generateFq.setObjectName("pushButton_generateFq")
        self.verticalLayout_9.addWidget(self.pushButton_generateFq)
        self.groupBox_status = QtWidgets.QGroupBox(self.groupBox_10)
        self.groupBox_status.setObjectName("groupBox_status")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.groupBox_status)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.progressBar = QtWidgets.QProgressBar(self.groupBox_status)
        self.progressBar.setProperty("value", 0)
        self.progressBar.setObjectName("progressBar")
        self.horizontalLayout_3.addWidget(self.progressBar)
        self.pushButton_stop = QtWidgets.QPushButton(self.groupBox_status)
        self.pushButton_stop.setObjectName("pushButton_stop")
        self.horizontalLayout_3.addWidget(self.pushButton_stop)
        self.verticalLayout_9.addWidget(self.groupBox_status)
        self.lineEdit_FqDir = QtWidgets.QLineEdit(self.groupBox_10)
        self.lineEdit_FqDir.setClearButtonEnabled(True)
        self.lineEdit_FqDir.setObjectName("lineEdit_FqDir")
        self.verticalLayout_9.addWidget(self.lineEdit_FqDir)
        self.pushButton_openFqDir = QtWidgets.QPushButton(self.groupBox_10)
        self.pushButton_openFqDir.setObjectName("pushButton_openFqDir")
        self.verticalLayout_9.addWidget(self.pushButton_openFqDir)
        self.verticalLayout_3.addWidget(self.groupBox_10)
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setObjectName("label")
        self.verticalLayout_3.addWidget(self.label)
        BCL2Fastq.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(BCL2Fastq)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1046, 28))
        self.menubar.setObjectName("menubar")
        BCL2Fastq.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(BCL2Fastq)
        self.statusbar.setObjectName("statusbar")
        BCL2Fastq.setStatusBar(self.statusbar)

        self.retranslateUi(BCL2Fastq)
        QtCore.QMetaObject.connectSlotsByName(BCL2Fastq)

    def retranslateUi(self, BCL2Fastq):
        _translate = QtCore.QCoreApplication.translate
        BCL2Fastq.setWindowTitle(_translate("BCL2Fastq", "Fastq数据二次拆分"))
        self.groupBox.setTitle(_translate("BCL2Fastq", "Fastq folder"))
        self.pushButton_chooseFolder.setText(_translate("BCL2Fastq", "选择文件夹"))
        self.label_4.setText(_translate("BCL2Fastq", "样品名请尽量写简洁，样品名，库名禁止出现下划线_!可以用A1,A2或者PE1,PE2,BE1这样的。禁止出现空格！文件路径也不能出现空格！"))
        self.label_5.setText(_translate("BCL2Fastq", "如果在Pool1_S39_L001_R1_001.fastq.gz和Pool1_S39_L001_R2_001.fastq.gz的样品需要二次拆分，例如sample1 使用 GAG和CAG这一对barcod, sample12使用 GAG和CCT这一对barcode，那么应当如下表填写。程序将识别fastq文件的第一个下划线_前的内容为库名，并从库中寻找匹配的索引序列，并输出为 \"sample1_on_Pool1.fastq\"等文件(索引序列仅从开头或者结尾寻找，中间忽略)\n"
"\n"
"使用前点击清空即可删除示例！！！"))
        self.groupBox_2.setTitle(_translate("BCL2Fastq", "基本信息"))
        self.checkBox_auto_fill_col.setText(_translate("BCL2Fastq", "自动向下填充"))
        item = self.tableWidget.verticalHeaderItem(0)
        item.setText(_translate("BCL2Fastq", "示例"))
        item = self.tableWidget.verticalHeaderItem(1)
        item.setText(_translate("BCL2Fastq", "示例"))
        item = self.tableWidget.verticalHeaderItem(2)
        item.setText(_translate("BCL2Fastq", "示例"))
        item = self.tableWidget.verticalHeaderItem(3)
        item.setText(_translate("BCL2Fastq", "示例"))
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("BCL2Fastq", "样品名"))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("BCL2Fastq", "描述"))
        item = self.tableWidget.horizontalHeaderItem(2)
        item.setText(_translate("BCL2Fastq", "所在样品库"))
        item = self.tableWidget.horizontalHeaderItem(3)
        item.setText(_translate("BCL2Fastq", "索引名1"))
        item = self.tableWidget.horizontalHeaderItem(4)
        item.setText(_translate("BCL2Fastq", "索引序列1"))
        item = self.tableWidget.horizontalHeaderItem(5)
        item.setText(_translate("BCL2Fastq", "索引名2"))
        item = self.tableWidget.horizontalHeaderItem(6)
        item.setText(_translate("BCL2Fastq", "索引序列2"))
        __sortingEnabled = self.tableWidget.isSortingEnabled()
        self.tableWidget.setSortingEnabled(False)
        item = self.tableWidget.item(0, 0)
        item.setText(_translate("BCL2Fastq", "sample1"))
        item = self.tableWidget.item(0, 1)
        item.setText(_translate("BCL2Fastq", "随便写，给自己看"))
        item = self.tableWidget.item(0, 2)
        item.setText(_translate("BCL2Fastq", "Pool1"))
        item = self.tableWidget.item(0, 3)
        item.setText(_translate("BCL2Fastq", "barcode1 （可以不写）"))
        item = self.tableWidget.item(0, 4)
        item.setText(_translate("BCL2Fastq", "GAG"))
        item = self.tableWidget.item(0, 5)
        item.setText(_translate("BCL2Fastq", "barcode4 （可以不写）"))
        item = self.tableWidget.item(0, 6)
        item.setText(_translate("BCL2Fastq", "CAG"))
        item = self.tableWidget.item(1, 0)
        item.setText(_translate("BCL2Fastq", "sample2"))
        item = self.tableWidget.item(1, 2)
        item.setText(_translate("BCL2Fastq", "Pool1"))
        item = self.tableWidget.item(1, 4)
        item.setText(_translate("BCL2Fastq", "GAG"))
        item = self.tableWidget.item(1, 6)
        item.setText(_translate("BCL2Fastq", "CCT"))
        item = self.tableWidget.item(2, 0)
        item.setText(_translate("BCL2Fastq", "sample3"))
        item = self.tableWidget.item(2, 2)
        item.setText(_translate("BCL2Fastq", "Pool4"))
        item = self.tableWidget.item(2, 4)
        item.setText(_translate("BCL2Fastq", "GAG"))
        item = self.tableWidget.item(2, 6)
        item.setText(_translate("BCL2Fastq", "CCT"))
        item = self.tableWidget.item(3, 0)
        item.setText(_translate("BCL2Fastq", "sample3"))
        item = self.tableWidget.item(3, 2)
        item.setText(_translate("BCL2Fastq", "Pool4"))
        item = self.tableWidget.item(3, 4)
        item.setText(_translate("BCL2Fastq", "GAG"))
        item = self.tableWidget.item(3, 6)
        item.setText(_translate("BCL2Fastq", "CCT"))
        self.tableWidget.setSortingEnabled(__sortingEnabled)
        self.pushButton_add_line.setText(_translate("BCL2Fastq", "加一行"))
        self.pushButton_del_lines.setText(_translate("BCL2Fastq", "删除选中行"))
        self.pushButton_import_from_sheet.setText(_translate("BCL2Fastq", "从表格导入"))
        self.pushButton_export_sheet.setText(_translate("BCL2Fastq", "导出当前表格"))
        self.pushButton_clear_table.setText(_translate("BCL2Fastq", "清空"))
        self.label_selection.setText(_translate("BCL2Fastq", "TextLabel"))
        self.label_3.setText(_translate("BCL2Fastq", "bcl2fastq安装信息："))
        self.label_version.setText(_translate("BCL2Fastq", "TextLabel"))
        self.pushButton_install_bcl2fq.setText(_translate("BCL2Fastq", "安装bcl2fastq"))
        self.groupBox_10.setTitle(_translate("BCL2Fastq", "操作"))
        self.pushButton_generateFq.setText(_translate("BCL2Fastq", "开始拆分"))
        self.groupBox_status.setTitle(_translate("BCL2Fastq", "进度"))
        self.progressBar.setFormat(_translate("BCL2Fastq", "%v / %m"))
        self.pushButton_stop.setText(_translate("BCL2Fastq", "停止"))
        self.pushButton_openFqDir.setText(_translate("BCL2Fastq", "打开结果文件夹"))
        self.label.setText(_translate("BCL2Fastq", "当前选定："))
from plaintextedit import PlainTextEdit
