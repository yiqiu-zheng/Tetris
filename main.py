#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2020/10/27 14:40
# @Author  : YIQIU ZHENG
# @FileName: main.py
# @Software: PyCharm
from PyQt5.QtWidgets import QDesktopWidget, QApplication
from Panel.MainPanel import GamePanel
import sys

if __name__ == '__main__':
        app = QApplication(sys.argv)
        win = GamePanel()
        win.show()
        sys.exit(app.exec_())
