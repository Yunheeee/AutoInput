#!/usr/bin/env python3
# encoding: utf-8

from PyQt5.QtCore import QRegExp,Qt
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QFont, QColor,QSyntaxHighlighter,QTextCharFormat

class PythonHighlighter(QSyntaxHighlighter):

    Rules = []
    Formats = {}

    def __init__(self, parent=None):
        super(PythonHighlighter, self).__init__(parent)

        self.initializeFormats()

        KEYWORDS = ["mount", "umount", "ls", "du", "cat",
                "testStore", "ln", "ifconfig", "outputClose", "outputOpen", "prtHardInfo",
                "conda", "activate", "pip", "setIp", "getIp", "kill",
                "enca", "enconv", "iconv", "ulimit", "cp", "mkdir", "setDebug",
                "getDebug", "echo", "ps", "grep", "reboot", "setGateway",
                "ifconfig", "gdbcfg"]
        BUILTINS = ["-d", "-l", "-m", "-t", "-o",
                "nolock", "-x", "-L", "-f", "-e"]
        CONSTANTS = ["False", "True", "None", "NotImplemented",
                     "Ellipsis"]

        PythonHighlighter.Rules.append((QRegExp(
                "|".join([r"\b%s\b" % keyword for keyword in KEYWORDS])),
                "keyword"))
        PythonHighlighter.Rules.append((QRegExp(
                "|".join([r"\b%s\b" % builtin for builtin in BUILTINS])),
                "builtin"))
        PythonHighlighter.Rules.append((QRegExp(
                "|".join([r"\b%s\b" % constant
                for constant in CONSTANTS])), "constant"))
        PythonHighlighter.Rules.append((QRegExp(
                r"\b[+-]?[0-9]+[lL]?\b"
                r"|\b[+-]?0[xX][0-9A-Fa-f]+[lL]?\b"
                r"|\b[+-]?[0-9]+(?:\.[0-9]+)?(?:[eE][+-]?[0-9]+)?\b"),
                "number"))

        stringRe = QRegExp(r"""(?:'[^']*'|"[^"]*")""")
        stringRe.setMinimal(True)
        PythonHighlighter.Rules.append((stringRe, "string"))
        self.stringRe = QRegExp(r"""(:?"["]".*"["]"|'''.*''')""")
        self.stringRe.setMinimal(True)
        PythonHighlighter.Rules.append((self.stringRe, "string"))
        self.tripleSingleRe = QRegExp(r"""'''(?!")""")
        self.tripleDoubleRe = QRegExp(r'''"""(?!')''')


    @staticmethod
    def initializeFormats():
        baseFormat = QTextCharFormat()
        for name, color in (("normal", Qt.darkBlue),
                ("keyword", Qt.darkGreen), ("builtin", Qt.darkRed),
                ("constant", Qt.darkRed),
                ("decorator", Qt.darkBlue), ("comment", QColor("#FF00FF")),
                ("string", Qt.darkYellow), ("number", Qt.darkMagenta),
                ("error", Qt.darkRed), ("pyqt", Qt.darkCyan)):
            format = QTextCharFormat(baseFormat)
            format.setForeground(QColor(color))
            if name in ("keyword", "decorator"):
                format.setFontWeight(QFont.Bold)
            if name == "comment":
                format.setFontItalic(True)
            PythonHighlighter.Formats[name] = format


    def highlightBlock(self, text):
        textLength = len(text)
        self.setFormat(0, textLength,PythonHighlighter.Formats["normal"])

        if text.startswith("//") or text.startswith("#"):
            self.setFormat(0, textLength,PythonHighlighter.Formats["comment"])
            return

        for regex, format in PythonHighlighter.Rules:
            i = regex.indexIn(text)
            while i >= 0:
                length = regex.matchedLength()
                self.setFormat(i, length,PythonHighlighter.Formats[format])
                i = regex.indexIn(text, i + length)

    def rehighlight(self):
        QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))
        QSyntaxHighlighter.rehighlight(self)
        QApplication.restoreOverrideCursor()

