# coding = utf-8

"""
这是一个纯文本带行号和高亮的输入框例子！
文章链接：http://www.xdbcb8.com/archives/644.html
文章链接：http://www.xdbcb8.com/archives/655.html
文章链接：http://www.xdbcb8.com/archives/664.html
"""

import sys
from PyQt5.QtCore import Qt, QRect
from PyQt5.QtWidgets import QWidget, QTextEdit, QPlainTextEdit, QApplication
from PyQt5.QtGui import QColor, QPainter, QFont, QTextFormat
from PyQt5.QtCore import pyqtSignal

class QCodeEditor(QPlainTextEdit):
    '''
    带行号和高亮的文本输入
    '''

    class NumberBar(QWidget):

        '''
        使文本输入框能有行号，类种类哦！
        '''
        double_clicked = pyqtSignal(str)

        def __init__(self, editor):
            '''
            一些初始设置
            '''
            QWidget.__init__(self, editor)
            # NumberBar是类中类，故我们在初始化的时候也要把外部类的对象带进来

            self.editor = editor
            self.editor.blockCountChanged.connect(self.updateWidth)
            # 每当块数（段落）发生变化时都会发出该信号并调用updateWidth()函数

            self.editor.updateRequest.connect(self.updateContents)
            # 当文本文档需要更新指定的矩形时，会发出此信号

            self.font = QFont()
            self.numberBarColor = QColor("#e8e8e8")

        def paintEvent(self, event):
            '''
            重写小部件的绘图事件
            '''
            painter = QPainter(self)
            painter.fillRect(event.rect(), self.numberBarColor)
            # 构建一个绘画设备，并用指定的颜色填充给定的矩形。

            block = self.editor.firstVisibleBlock()
            # 返回第一个可见块，也就是文本块。

            while block.isValid():
                blockNumber = block.blockNumber()
                # 在文本块有效的情况下进入循环，返回此文本块的编号（行号），如果块无效，则返回-1。

                block_top = self.editor.blockBoundingGeometry(block).translated(self.editor.contentOffset()).top()
                # 同时我们使用blockBoundingGeometry()函数以内容坐标返回文本块的边界矩形，并使用contentOffset()转义得到矩形以获得视口上的视觉坐标。这里得到top。

                if blockNumber == self.editor.textCursor().blockNumber():
                    self.font.setBold(True)
                    painter.setPen(QColor("#000000"))
                else:
                    self.font.setBold(False)
                    painter.setPen(QColor("#1E90FF"))
                # 当鼠标移动到某一行的时候，其对应的行号会相应的变黑加粗

                paint_rect = QRect(0, block_top, self.width(), self.editor.fontMetrics().height())
                # 行号绘画的区域是paint_rect，这里使用QRect对象实现的；

                painter.drawText(paint_rect, Qt.AlignCenter, str(blockNumber + 1))
                # 居中对齐，具体的内容是str(blockNumber+1)，不加1就是0开始了。

                block = block.next()

        def getWidth(self):
            '''
            返回显示行号的小部件宽度
            '''
            count = self.editor.blockCount()
            # 保存文档中文本块的数量

            if 0 <= count < 99999:
                width = self.fontMetrics().width('99999')
            else:
                width = self.fontMetrics().width(str(count))
            return width
            # 如果行数小于99999行，那么返回小部件当前字体的字体的宽度，这个宽度是内容’99999’的字体宽度。否则就返回实际宽度。

        def updateWidth(self):
            '''
            显示行号位置的实际宽度
            '''
            width = self.getWidth()
            self.editor.setViewportMargins(width, 0, 0, 0)
            # 通过setViewportMargins设置编辑器显示行号位置的实际宽度

        def updateContents(self, rect, dy):
            '''
            重新绘制小部件区域
            '''
            if dy:
                self.scroll(0, dy)
            # 如果存在垂直滚动，且像素dy > 0，那么将小部件向下滚动。滚动后，小部件将接收需要重新绘制区域的绘画事件。
            else:
                self.update(0, rect.y(), self.width(), rect.height())
            # 否则更新小部件内的矩形（x，y，w，h）。

            if rect.contains(self.editor.viewport().rect()):
                # 判断编辑器视口的矩形是否在rect这个矩形内。
                fontSize = self.editor.currentCharFormat().font().pointSize()
                self.font.setPointSize(fontSize)
                self.font.setStyle(QFont.StyleNormal)
                self.updateWidth()

        def find_loc_block(self, y):
            block = self.editor.firstVisibleBlock()
            # 返回第一个可见块，也就是文本块。
            while block.isValid():
                # 在文本块有效的情况下进入循环，返回此文本块的编号（行号），如果块无效，则返回-1。
                block_top = self.editor.blockBoundingGeometry(block).translated(self.editor.contentOffset()).top()
                # 同时我们使用blockBoundingGeometry()函数以内容坐标返回文本块的边界矩形，并使用contentOffset()转义得到矩形以获得视口上的视觉坐标。这里得到top。

                if (y >= block_top and y <= (block_top + self.editor.fontMetrics().height())):
                    return block.text()

                block = block.next()
            return None


        def mouseDoubleClickEvent(self, QMoveEvent):
            str = self.find_loc_block(QMoveEvent.y())
            if(str != None):
                self.double_clicked.emit(str)

    def __init__(self):

        super(QCodeEditor, self).__init__()
        #self.setWindowTitle('微信公众号：学点编程吧--带行号和颜色的文本框')

        self.setFont(QFont("Ubuntu Mono", 12))
        # 设置当前的字体和大小

        self.setLineWrapMode(QPlainTextEdit.NoWrap)
        # 类似于记事本中的自动换行

        self.number_bar = self.NumberBar(self)
        self.currentLineNumber = None
        # 实例化我们的内部类，同时将当前需要标记的行号初始值为None

        self.cursorPositionChanged.connect(self.highligtCurrentLine)
        # 只要光标位置改变，就会发出此信号

        self.setViewportMargins(40, 0, 0, 0)
        # 滚动区域周围的边距设置为左侧

        self.highligtCurrentLine()

    def resizeEvent(self, *e):
        '''
        接收在事件参数中传递的小部件大小调整事件
        '''
        cr = self.contentsRect()
        # 小部件边界内的区域

        rec = QRect(cr.left(), cr.top(), self.number_bar.getWidth(), cr.height())
        self.number_bar.setGeometry(rec)
        # 使用整数精度在平面中定义一个矩形

        QPlainTextEdit.resizeEvent(self, *e)

    def highligtCurrentLine(self):
        '''
        用来突出显示包含光标的行
        '''
        newCurrentLineNumber = self.textCursor().blockNumber()
        # 返回光标所在块的编号，如果光标无效，则返回0

        if newCurrentLineNumber != self.currentLineNumber:
            lineColor = QColor(Qt.yellow).lighter(160)
            self.currentLineNumber = newCurrentLineNumber

            hi_selection = QTextEdit.ExtraSelection()
            # QTextEdit.ExtraSelection结构提供了一种为文档中已选择指定字符格式的方法

            hi_selection.format.setBackground(lineColor)
            # 设定背景色

            hi_selection.format.setProperty(QTextFormat.FullWidthSelection, True)
            # 设定文本的整个宽度将显示为选中状态

            hi_selection.cursor = self.textCursor()
            hi_selection.cursor.clearSelection()
            # 通过将锚点设置为光标位置来清除当前选择

            self.setExtraSelections([hi_selection])
            # 允许用指定的颜色临时标记文档中的某些区域


if __name__ == '__main__':
    app = QApplication(sys.argv)
    editor = QCodeEditor()
    editor.resize(600, 450)
    editor.show()
    sys.exit(app.exec_())