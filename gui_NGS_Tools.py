# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/chief/PycharmProjects/NGS_Tools/gui_NGS_Tools.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(591, 401)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.plainTextEdit = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.plainTextEdit.setObjectName("plainTextEdit")
        self.verticalLayout_2.addWidget(self.plainTextEdit)
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setObjectName("groupBox")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.groupBox)
        self.verticalLayout.setObjectName("verticalLayout")
        self.pushButton_bcl = QtWidgets.QPushButton(self.groupBox)
        self.pushButton_bcl.setObjectName("pushButton_bcl")
        self.verticalLayout.addWidget(self.pushButton_bcl)
        self.pushButton_demultiplex = QtWidgets.QPushButton(self.groupBox)
        self.pushButton_demultiplex.setObjectName("pushButton_demultiplex")
        self.verticalLayout.addWidget(self.pushButton_demultiplex)
        self.pushButton_HDR = QtWidgets.QPushButton(self.groupBox)
        self.pushButton_HDR.setObjectName("pushButton_HDR")
        self.verticalLayout.addWidget(self.pushButton_HDR)
        self.pushButton_BE = QtWidgets.QPushButton(self.groupBox)
        self.pushButton_BE.setObjectName("pushButton_BE")
        self.verticalLayout.addWidget(self.pushButton_BE)
        self.pushButton_NHEJ = QtWidgets.QPushButton(self.groupBox)
        self.pushButton_NHEJ.setObjectName("pushButton_NHEJ")
        self.verticalLayout.addWidget(self.pushButton_NHEJ)
        self.verticalLayout_2.addWidget(self.groupBox)
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setTextFormat(QtCore.Qt.MarkdownText)
        self.label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label.setOpenExternalLinks(True)
        self.label.setTextInteractionFlags(QtCore.Qt.TextBrowserInteraction)
        self.label.setObjectName("label")
        self.verticalLayout_2.addWidget(self.label)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 591, 28))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "NGS_Tools"))
        self.plainTextEdit.setPlainText(_translate("MainWindow", "NGS工具箱：\n"
"\n"
"本工具箱提供了图形界面并缝合了一系列软件以实现以下功能：\n"
"1. 将illumina下机数据转换成fastq数据。\n"
"2. 使用CRISPResso2的部分功能进行基因编辑效果分析\n"
"3. 汇总结果\n"
"\n"
"程序源码公开于 https://github.com/Masterchiefm/NGS_Tools\n"
"\n"
"\n"
"\n"
"\n"
"\n"
"本程序由莫淇钦创建于上海科技大学马涵慧实验室\n"
"联系邮箱：moqiqin@live.com\n"
""))
        self.groupBox.setTitle(_translate("MainWindow", "请选择功能"))
        self.pushButton_bcl.setText(_translate("MainWindow", "BCL2Fastq (内存 + swap >= 32GB)"))
        self.pushButton_demultiplex.setText(_translate("MainWindow", "Fastq文件二次拆分"))
        self.pushButton_HDR.setText(_translate("MainWindow", "HDR or PE"))
        self.pushButton_BE.setText(_translate("MainWindow", "BE"))
        self.pushButton_NHEJ.setText(_translate("MainWindow", "NHEJ"))
        self.label.setText(_translate("MainWindow", "[关于本软件](https://gitee.com/MasterChiefm/NGS_Tools/blob/master/README.md)    [LICENSE](https://gitee.com/MasterChiefm/NGS_Tools/blob/master/LICENSE)"))
