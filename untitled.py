# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'untitled.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QObject, pyqtSignal
from QAnchorButton import AnchorButton
from QCmdEditer import QCodeEditor

class Ui_MainWindow(object):

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.newButton = QtWidgets.QPushButton(self.centralwidget)
        self.newButton.setObjectName("newButton")
        self.horizontalLayout.addWidget(self.newButton)
        self.openButton = QtWidgets.QPushButton(self.centralwidget)
        self.openButton.setObjectName("openButton")
        self.horizontalLayout.addWidget(self.openButton)
        self.saveButton = QtWidgets.QPushButton(self.centralwidget)
        self.saveButton.setObjectName("saveButton")
        self.horizontalLayout.addWidget(self.saveButton)
        self.saveasButton = QtWidgets.QPushButton(self.centralwidget)
        self.saveasButton.setObjectName("saveasButton")
        self.horizontalLayout.addWidget(self.saveasButton)
        self.redirectButton = AnchorButton(self.centralwidget)
        self.redirectButton.setObjectName("redirectButton")
        self.horizontalLayout.addWidget(self.redirectButton)
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.verticalLayout.addLayout(self.horizontalLayout)

        #文本框管理列表
        self.textEditList = []
        #页签管理器
        self.tabWidget = QTabWidget()
        self.verticalLayout.addWidget(self.tabWidget)

        #创建新文本框 加入管理列表 加入页签
        self.textEditList.append(QCodeEditor()) #FIXME:open真正命令文件时 这里可能存在泄漏 待确认
        self.tabWidget.addTab(self.textEditList[0], "未定义")

        #当前文本框
        self.currTextEdit = self.textEditList[0]

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 23))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        #页签栏 标题编辑框
        self.lineEdit = QLineEdit(self.tabWidget)
        self.lineEdit.hide()

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.newButton.setText(_translate("MainWindow", "新建"))
        self.openButton.setText(_translate("MainWindow", "打开"))
        self.saveButton.setText(_translate("MainWindow", "保存"))
        self.saveasButton.setText(_translate("MainWindow", "另存"))
        #self.pushButton_5.setText(_translate("MainWindow", "撤销"))
        #self.pushButton_6.setText(_translate("MainWindow", "重做"))
        self.redirectButton.setText(_translate("MainWindow", "定向"))
        self.label.setText(_translate("MainWindow", ""))

