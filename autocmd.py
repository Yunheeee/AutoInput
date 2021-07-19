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
v2.0.0:20200414 使用pyQT5实现，解决行号bug，遗留问题：目标窗口关闭后，工具异常闪退
'''

TITLE_TEXT = u"Auto Input    v2.0.0"

from untitled import Ui_MainWindow
from Qhighlighter import PythonHighlighter
from PyQt5.QtWidgets import  QWidget, QMainWindow, QApplication, QFileDialog
from PyQt5.QtGui import  QIcon
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

        self.highlighter = PythonHighlighter(self.ui.textEdit.document())

        self.hwin = None
        self.prev_hwin = None
        self.file_name = None

        self.ui.pushButton.setIcon(QIcon("new.png"))

        self.ui.pushButton_7.mousePress.connect(self.mousePressCB)
        self.ui.pushButton_7.mouseMove.connect(self.mouseMoveCB)
        self.ui.pushButton_7.mouseRelease.connect(self.mouseReleaseCB)

        self.ui.pushButton.clicked.connect(self.new_file)
        self.ui.pushButton_2.clicked.connect(self.open_file)
        self.ui.pushButton_3.clicked.connect(self.save_file)
        self.ui.pushButton_4.clicked.connect(self.save_as)

        self.ui.textEdit.number_bar.double_clicked.connect(self.send_cmd_event)

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
            self.file_name = input_file
            with open(input_file, 'r') as _file:
                content = _file.read()
                self.ui.textEdit.setPlainText(content)

            self.setWindowTitle("%s   %s" % (TITLE_TEXT, input_file))
        else:
            pass

    def _write_to_file(self, file_name):
        try:
            content = self.ui.textEdit.toPlainText()

            with open(file_name, 'w') as the_file:
                the_file.write(content)
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


if __name__ == "__main__":
    app = QApplication(sys.argv)
    qb = AppWindow()
    qb.show()
    sys.exit(app.exec_())
