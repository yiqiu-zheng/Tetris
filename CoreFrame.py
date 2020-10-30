#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2020/10/25 7:18 PM
# @Author  : YIQIU ZHENG
# @FileName: CoreFrame2.py
# @Software: PyCharm

from PyQt5 import QtWidgets

from PyQt5.QtWidgets import QMainWindow, QFrame, QDesktopWidget, QApplication
from PyQt5.QtCore import Qt, QBasicTimer, pyqtSignal
from PyQt5.QtGui import QPainter, QColor

from Shape import TetrominoFactory

from Panel.Utils import draw_tetromino

import Panel
import random

class CoreFrame(QtWidgets.QFrame):


    def __init__(self, parent, state_matrix):
        super(CoreFrame, self).__init__(parent)
        #self.setFixedSize(width, height)
        self.setFixedSize(Panel.CORE_PANEL_WIDTH, Panel.CORE_PANEL_HEIGHT)

        # self.setFrameShape(QFrame.Box)
        self.state_matrix = state_matrix
        self.setStyleSheet("background-color:skyblue;")
        self.x_pixel = self.contentsRect().width() // Panel.GRID_X_NUMS
        self.y_pixel = self.contentsRect().height() // Panel.GRID_Y_NUMS

        self.initCoreFrame()


    def initCoreFrame(self):

        #self.t_matrix = [[None] * Panel.GRID_Y_NUMS for i in range(Panel.GRID_X_NUMS)]
        #self.isWaitingAfterLine = False

        # self.curX = self.state_matrix.curX
        # self.curY = self.state_matrix.curY
        # self.self.lines_removed = self.state_matrix.lines_removed


        # self.isStarted = False
        # self.isPaused = False

        #self.clearCorePanel()
        self.state_matrix.clear_state_matrix()

    def begin_loop(self):

        self.state_matrix.generate_new_tetromino()
        # self.timer.start(Panel.FPS, self)

    # def timerEvent(self, event):
    #
    #     if event.timerId() == self.timer.timerId():
    #
    #         cur_tetromino = self.state_matrix.cur_tetromino
    #         cur_x = self.state_matrix.cur_x
    #         cur_y = self.state_matrix.cur_y
    #
    #         # if self.isWaitingAfterLine:
    #         #     self.isWaitingAfterLine = False
    #         #     self.generateNewTetromino()
    #         # else:
    #         #     #self.oneLineDown()
    #
    #         if not self.state_matrix.detect_and_move(cur_tetromino, cur_x, cur_y - 1):
    #             self.state_matrix.drop_and_generate()
    #
    #
    #     else:
    #         super(CoreFrame, self).timerEvent(event)

    def paintEvent(self, event):
        """

        Rendering logic, include background, tetromino
        :param event:
        :return:
        """

        painter = QPainter(self)
        rect = self.contentsRect()

        boardTop = rect.bottom() - self.y_pixel*Panel.GRID_Y_NUMS

        # painter.begin(self)
        #Rendering the background
        for i in range(Panel.GRID_X_NUMS):
            for j in range(Panel.GRID_Y_NUMS):
             #color = self.getCorePanel(i, j)
             color_index = self.state_matrix.get_state_matrix(i, j)

             if not color_index is None:
                 draw_tetromino(painter, rect.left() + i*self.x_pixel,
                                boardTop + (Panel.GRID_Y_NUMS - j - 1) * self.y_pixel, color_index, self.x_pixel, self.y_pixel)


        cur_tetromino = self.state_matrix.cur_tetromino

        #Rendering the falling tetromino
        if cur_tetromino:
            for i in range(4):
                x = self.state_matrix.cur_x + cur_tetromino.get_matrix(("X", i))
                y = self.state_matrix.cur_y - cur_tetromino.get_matrix(("Y", i))

                draw_tetromino(painter, rect.left() + x * self.x_pixel,
                                boardTop + (Panel.GRID_Y_NUMS - y - 1) * self.y_pixel, cur_tetromino.color, self.x_pixel, self.y_pixel)



        # Rendering a border
        # painter.setPen(QColor(0x777777))
        # painter.drawLine(self.width()-1, 0, self.width()-1, self.height())
        #
        # painter.setPen(QColor(0xCCCCCC))
        # painter.drawLine(self.width(), 0, self.width(), self.height())

        # painter.end()



    def refresh(self):
        self.update()
