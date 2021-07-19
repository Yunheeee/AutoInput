# encoding: utf-8
# module PyQt5.QtWidgets
# from E:\soft\Anaconda\envs\python36\lib\site-packages\PyQt5\QtWidgets.pyd
# by generator 1.147
# no doc


from PyQt5.QtWidgets import  QPushButton
from PyQt5.QtCore import pyqtSignal

class AnchorButton(QPushButton):
    '''
    使文本输入框能有行号，类种类哦！
    '''

    mousePress = pyqtSignal()
    mouseMove = pyqtSignal()
    mouseRelease = pyqtSignal()

    def __init__(self, editor):
        '''
        一些初始设置
        '''
        super().__init__()

    def mouseMoveEvent(self, *args, **kwargs):  # real signature unknown
        self.mouseMove.emit()

    def mousePressEvent(self, *args, **kwargs):  # real signature unknown
        self.mousePress.emit()

    def mouseReleaseEvent(self, *args, **kwargs):  # real signature unknown
        self.mouseRelease.emit()
