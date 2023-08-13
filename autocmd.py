# -*- encoding: utf-8 -*-

import sys
import os
import win32api
import win32con
import win32gui

'''
v1.0.1:20191016 及时关闭文件，尝试修复文件内容全部丢失问题
v1.0.2:20191022 支持中文读取与写入，文件内容丢失问题实际是写入错误
v1.0.3:20191212 支持动态选择窗口 遗留bug：cmd窗口不会高亮，chrome高亮不会消失，显示类名非应用名，拖动框
v2.0.0:20200414 使用pyQT5实现，解决:wq
行号bug，遗留问题：目标窗口关闭后，工具异常闪退
'''

TITLE_TEXT = u"Auto Input    v2.0.0"

from PyQt5 import QtCore, QtGui, QtWidgets
from untitled import Ui_MainWindow
from Qhighlighter import PythonHighlighter
from QCmdEditer import QCodeEditor
from PyQt5.QtWidgets import *
from PyQt5.QtGui import  QIcon
from split_text import Cmd_spliter
import win32api
import win32con
import win32gui


def SendKeyToWnd(hCmdWin, keyValue):
    win32api.SendMessage(hCmdWin, win32con.WM_CHAR, keyValue, 1)  # chr(65) rd('l')


def SendStringToWnd(hCmdWin, cmdString):
    if len(cmdString) == 0 or None == hCmdWin:
        return
    for key in cmdString:
        SendKeyToWnd(hCmdWin, ord(key))
    SendKeyToWnd(hCmdWin, 10)  # SendKeyToWnd(hWnd, 13)

def SendCmdToAnchor(cmd_win, cmdString):
    SendStringToWnd(cmd_win, cmdString)

class AppWindow(QMainWindow):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)

        self.DeviceNum = 0
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowTitle(TITLE_TEXT)

        self.hwin = None
        self.prev_hwin = None
        self.file_name = None

        self.ui.newButton.setIcon(QIcon("new.png"))

        self.ui.redirectButton.mousePress.connect(self.mousePressCB)
        self.ui.redirectButton.mouseMove.connect(self.mouseMoveCB)
        self.ui.redirectButton.mouseRelease.connect(self.mouseReleaseCB)

        self.ui.newButton.clicked.connect(self.new_file)
        self.ui.openButton.clicked.connect(self.open_file)
        self.ui.saveButton.clicked.connect(self.save_file)
        self.ui.saveasButton.clicked.connect(self.save_as)

        self.ui.tabWidget.currentChanged.connect(self.tabChanged)
        self.ui.tabWidget.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.ui.tabWidget.customContextMenuRequested.connect(self.create_rightmenu)
        self.ui.tabWidget.tabBarDoubleClicked.connect(self.tabNameEdit)

        self.ui.lineEdit.returnPressed.connect(self.tabNameChannged)
        self.ui.lineEdit.editingFinished.connect(self.tabNameChannged)

        self.menu = QMenu(self)
        self.actionA = QAction('新建页面', self)
        self.menu.addAction(self.actionA)
        self.actionB = QAction('删除页面', self)
        self.menu.addAction(self.actionB)

        self.actionA.triggered.connect(self.tabNew)
        self.actionB.triggered.connect(self.tabDel)

        self.tabNew() #显示默认页签

        #命令分页器及管理
        #self.cmd = Cmd_spliter('')

    def tabChanged(self, idx):
        print("tabChanged current:", idx)
        if(-1 != idx):
            self.currTextEdit = self.ui.tabWidget.currentWidget()
            self.highlighter = PythonHighlighter(self.currTextEdit.document())  # 影响字符开始偏移 待确认
    #仅退出
    def tabNameLeaveEditing(self):
        self.ui.lineEdit.hide()

    #完成修改
    def tabNameChannged(self):
        self.ui.tabWidget.setTabText(self.ui.tabWidget.currentIndex(), self.ui.lineEdit.text())
        self.ui.lineEdit.hide()

    def tabNameEdit(self, idx):
        #重新定位置
        self.ui.lineEdit.setGeometry(self.ui.tabWidget.tabBar().tabRect(idx))
        #填充当前名称
        self.ui.lineEdit.setText(self.ui.tabWidget.tabText(idx))
        self.ui.lineEdit.setFocus() #设置焦点以及时触发编辑退出
        #显示
        self.ui.lineEdit.show()


    def highlightWindow(self, hwnd):
        left, top, right, bottom = win32gui.GetWindowRect(hwnd)
        windowDc = win32gui.GetWindowDC(hwnd)
        if (windowDc != 0):
            rectanglePen = win32gui.CreatePen(win32con.PS_SOLID, 3, win32api.RGB(255, 0, 0))
            prevPen = win32gui.SelectObject(windowDc, rectanglePen)
            prevBrush = win32gui.SelectObject(windowDc, win32gui.GetStockObject(win32con.HOLLOW_BRUSH))

            win32gui.Rectangle(windowDc, 0, 0, right - left, bottom - top)
            win32gui.SelectObject(windowDc, prevPen)
            win32gui.SelectObject(windowDc, prevBrush)
            win32gui.ReleaseDC(hwnd, windowDc)

    def refreshWindow(self, hwnd):
        try:
            win32gui.InvalidateRect(hwnd, None, True)
            win32gui.UpdateWindow(hwnd)
            win32gui.RedrawWindow(hwnd,
                                  None,
                                  None,
                                  win32con.RDW_FRAME |
                                  win32con.RDW_INVALIDATE |
                                  win32con.RDW_UPDATENOW |
                                  win32con.RDW_ALLCHILDREN)
        except:
            pass

    def mouseMoveCB(self, *args, **kwargs):  # real signature unknown
        point = win32api.GetCursorPos()
        self.hwin = win32gui.WindowFromPoint(point)
        if self.hwin:
            if self.prev_hwin:
                self.refreshWindow(self.prev_hwin)
            self.prev_hwin = self.hwin
            self.highlightWindow(self.hwin)
            className = win32gui.GetClassName(self.hwin)
            if(className == None):
                className = ""
            self.ui.label.setText(className)
        else:
            self.ui.label.setText("Selecting")

    def mousePressCB(self, *args, **kwargs):  # real signature unknown
        self.ui.label.setText("Press")

    def mouseReleaseCB(self, *args, **kwargs):  # real signature unknown
        if self.hwin:
            self.refreshWindow(self.hwin)
            className = win32gui.GetClassName(self.hwin)
            if(className == None):
                className = ""
            self.ui.label.setText(className)
        else:
            self.ui.label.setText("")

    def new_file(self):
        self.setWindowTitle(TITLE_TEXT)
        self.file_name = None
        self.ui.textEdit.setPlainText("")

    def open_file(self):
        input_file, fileType = QFileDialog.getOpenFileName(self, "选取文件", os.getcwd(),
             "All Files(*);;Text Files(*.txt)")


        if input_file:
            print('filename:',input_file)
            self.file_name = input_file
            with open(input_file, 'r') as _file:
                content = _file.read()

            cmd = Cmd_spliter(content)
            if(0 == cmd.count()):
                cmd.add_key("未定义",content)

            #先清空页签
            self.tabDelAll()

            for each in cmd.content():
                print(each)
                print('name:', each['name'], ' content:', each['value'])
                self.tabNew()
                self.currTextEdit.setPlainText(each['value'])
                self.ui.tabWidget.setTabText(self.ui.tabWidget.currentIndex(), each['name'])

            self.setWindowTitle("%s   %s" % (TITLE_TEXT, input_file))
        else:
            pass

    def _write_to_file(self, file_name):
        try:
            content = ''
            cmd = Cmd_spliter('')

            with open(file_name, 'w') as the_file:
                for id in range(0, self.ui.tabWidget.count()):
                    print('write_to id:',id)
                    cmd.clear()
                    cmd.add_key(self.ui.tabWidget.tabText(id), self.ui.tabWidget.widget(id).toPlainText())
                    print(cmd.to_str())
                    the_file.write(cmd.to_str())

        except IOError:
            messagebox.showwarning("保存", "保存失败！")

    def save_file(self):
        if not self.file_name:
            self.save_as()
        else:
            self._write_to_file(self.file_name)

    def save_as(self):
        input_file, ok2 = QFileDialog.getSaveFileName(None, "文件保存", "./")
        if input_file:
            self.file_name = input_file
            self._write_to_file(self.file_name)
            self.setWindowTitle("%s    %s" % (TITLE_TEXT, input_file))

    def send_cmd_event(self, str):
        print("send_cmd_event")
        if (self.hwin != None):

            try:
                #window cmd窗口输入\r\n
                className = win32gui.GetClassName(self.hwin)
                if (className == 'ConsoleWindowClass'):
                    str = str + '\r\n'
                SendCmdToAnchor(self.hwin, str)
            except :
                self.hwin = None
                self.prev_hwin = None
                #print ("excption")
                pass

    #创建右键菜单函数
    def create_rightmenu(self):
        print("create_rightmenu")
        self.menu.popup(QtGui.QCursor.pos())

    def tabNew(self):
        print('before> tabcount:', self.ui.tabWidget.count())
        newEditor = QCodeEditor()
        self.ui.tabWidget.addTab(newEditor, "未定义")

        #NOTE:保证新创建的页面均链接到命令发送
        newEditor.number_bar.double_clicked.connect(self.send_cmd_event)
        self.currTextEdit = newEditor
        print('after> tabcount:', self.ui.tabWidget.count())

        # 切换到新创建的tab页
        self.ui.tabWidget.setCurrentWidget(newEditor)

    def tabDel(self):
        delIdx = self.ui.tabWidget.currentIndex()
        print('to be delete tab idx:', delIdx)
        if(delIdx < 0):
            return

        toDelEditor = self.ui.tabWidget.currentWidget()
        self.ui.tabWidget.removeTab(delIdx)
        toDelEditor.deleteLater()

        #保留一个默认框
        print('tabWidget count:', self.ui.tabWidget.count())
        if(self.ui.tabWidget.count() == 0):
            self.tabNew()

    def tabDelAll(self):
        id = 0
        print('tabDelAll, count:', self.ui.tabWidget.count())
        #print(type(self.ui.tabWidget.currentWidget()))
        while self.ui.tabWidget.currentWidget():
            print('id:',id)
            id = id+1
            toDelEditor = self.ui.tabWidget.currentWidget()
            self.ui.tabWidget.removeTab(self.ui.tabWidget.currentIndex())
            toDelEditor.deleteLater()








if __name__ == "__main__":
    app = QApplication(sys.argv)
    qb = AppWindow()
    qb.show()
    sys.exit(app.exec_())
