# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui_PE.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_CRISPResso(object):
    def setupUi(self, CRISPResso):
        CRISPResso.setObjectName("CRISPResso")
        CRISPResso.resize(1187, 1195)
        self.centralwidget = QtWidgets.QWidget(CRISPResso)
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
        self.label_4.setObjectName("label_4")
        self.verticalLayout_3.addWidget(self.label_4)
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
        self.tableWidget.setColumnCount(6)
        self.tableWidget.setRowCount(1)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(0, item)
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
        self.tableWidget.horizontalHeader().setDefaultSectionSize(170)
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
        self.pushButton_install = QtWidgets.QPushButton(self.frame_3)
        self.pushButton_install.setObjectName("pushButton_install")
        self.verticalLayout_4.addWidget(self.pushButton_install)
        self.verticalLayout.addWidget(self.frame_3)
        self.verticalLayout_3.addWidget(self.groupBox_2)
        self.groupBox_10 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_10.setObjectName("groupBox_10")
        self.verticalLayout_9 = QtWidgets.QVBoxLayout(self.groupBox_10)
        self.verticalLayout_9.setObjectName("verticalLayout_9")
        self.label_2 = QtWidgets.QLabel(self.groupBox_10)
        self.label_2.setObjectName("label_2")
        self.verticalLayout_9.addWidget(self.label_2)
        self.plainTextEdit_parameters = PlainTextEdit(self.groupBox_10)
        self.plainTextEdit_parameters.setMaximumSize(QtCore.QSize(16777215, 250))
        self.plainTextEdit_parameters.setObjectName("plainTextEdit_parameters")
        self.verticalLayout_9.addWidget(self.plainTextEdit_parameters)
        self.pushButton_generateFq = QtWidgets.QPushButton(self.groupBox_10)
        self.pushButton_generateFq.setObjectName("pushButton_generateFq")
        self.verticalLayout_9.addWidget(self.pushButton_generateFq)
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
        CRISPResso.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(CRISPResso)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1187, 20))
        self.menubar.setObjectName("menubar")
        CRISPResso.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(CRISPResso)
        self.statusbar.setObjectName("statusbar")
        CRISPResso.setStatusBar(self.statusbar)

        self.retranslateUi(CRISPResso)
        QtCore.QMetaObject.connectSlotsByName(CRISPResso)

    def retranslateUi(self, CRISPResso):
        _translate = QtCore.QCoreApplication.translate
        CRISPResso.setWindowTitle(_translate("CRISPResso", "PE/HDR分析"))
        self.groupBox.setTitle(_translate("CRISPResso", "fastq数据文件夹"))
        self.pushButton_chooseFolder.setText(_translate("CRISPResso", "选择文件夹"))
        self.label_4.setText(_translate("CRISPResso", "文件路径也不能出现空格！样品名请根据测序文件名填写。例如，测序文件名是DS2-165_R1.fq.gz和DS2-165_R2.fq.gz，那么样品名就写第一个下划线_前的内容，即DS2-165。这样程序就能自动根据样品名给你匹配fastq文件。描述请尽量写详细，这个是给你自己看的！"))
        self.groupBox_2.setTitle(_translate("CRISPResso", "基本信息"))
        self.checkBox_auto_fill_col.setText(_translate("CRISPResso", "自动向下填充"))
        item = self.tableWidget.verticalHeaderItem(0)
        item.setText(_translate("CRISPResso", "示例"))
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("CRISPResso", "样品名"))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("CRISPResso", "描述"))
        item = self.tableWidget.horizontalHeaderItem(2)
        item.setText(_translate("CRISPResso", "sg1"))
        item = self.tableWidget.horizontalHeaderItem(3)
        item.setText(_translate("CRISPResso", "sg2"))
        item = self.tableWidget.horizontalHeaderItem(4)
        item.setText(_translate("CRISPResso", "原始序列"))
        item = self.tableWidget.horizontalHeaderItem(5)
        item.setText(_translate("CRISPResso", "修改后序列"))
        __sortingEnabled = self.tableWidget.isSortingEnabled()
        self.tableWidget.setSortingEnabled(False)
        item = self.tableWidget.item(0, 0)
        item.setText(_translate("CRISPResso", "DS2-165"))
        item = self.tableWidget.item(0, 1)
        item.setText(_translate("CRISPResso", "PE-SITE3+2TtoG-Cas9"))
        item = self.tableWidget.item(0, 2)
        item.setText(_translate("CRISPResso", "aacacaccgggttaat    "))
        item = self.tableWidget.item(0, 3)
        item.setText(_translate("CRISPResso", "(可以不写)"))
        item = self.tableWidget.item(0, 4)
        item.setText(_translate("CRISPResso", "atgttttttattgttttgttttcctcctggaaaaatatgaacagtg..."))
        item = self.tableWidget.item(0, 5)
        item.setText(_translate("CRISPResso", "atgttttttattgttttgttttcctcctggaaaaatatgaacagtg..."))
        self.tableWidget.setSortingEnabled(__sortingEnabled)
        self.pushButton_add_line.setText(_translate("CRISPResso", "加一行"))
        self.pushButton_del_lines.setText(_translate("CRISPResso", "删除选中行"))
        self.pushButton_import_from_sheet.setText(_translate("CRISPResso", "从表格导入"))
        self.pushButton_export_sheet.setText(_translate("CRISPResso", "导出当前表格"))
        self.pushButton_clear_table.setText(_translate("CRISPResso", "清空"))
        self.label_selection.setText(_translate("CRISPResso", "TextLabel"))
        self.label_3.setText(_translate("CRISPResso", "CRISPResso2安装信息："))
        self.label_version.setText(_translate("CRISPResso", "TextLabel"))
        self.pushButton_install.setText(_translate("CRISPResso", "安装CRISPResso2"))
        self.groupBox_10.setTitle(_translate("CRISPResso", "操作"))
        self.label_2.setText(_translate("CRISPResso", "额外运行参数:"))
        self.plainTextEdit_parameters.setPlainText(_translate("CRISPResso", "--exclude_bp_from_left 1\n"
" --exclude_bp_from_right 1\n"
" --quantification_window_size 20 \n"
"--min_frequency_alleles_around_cut_to_plot 0.01 \n"
" --quantification_window_center -3 "))
        self.pushButton_generateFq.setText(_translate("CRISPResso", "开始"))
        self.pushButton_openFqDir.setText(_translate("CRISPResso", "打开结果文件夹"))
        self.label.setText(_translate("CRISPResso", "当前选定："))
from plaintextedit import PlainTextEdit
