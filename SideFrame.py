#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2020/10/26 8:30
# @Author  : YIQIU ZHENG
# @FileName: SideFrame.py
# @Software: PyCharm

from PyQt5 import QtWidgets
from PyQt5.QtGui import QPainter, QColor
from Panel.Utils import draw_tetromino

import Panel

class SideFrame(QtWidgets.QFrame):

    def __init__(self, parent, state_matrix):
        super(SideFrame, self).__init__(parent)

        self.setFixedSize(Panel.GRID_PIXEL * 6, Panel.GRID_PIXEL * 6)
        self.setStyleSheet("background-color:white;")
        #self.move(Panel.GRID_PIXEL*Panel.GRID_X_NUMS, 0)


        self.x_pixel = self.contentsRect().width() // 6
        self.y_pixel = self.contentsRect().height() // 6

        self.state_matrix = state_matrix

    def refresh(self):
        self.update()


    def paintEvent(self, event):

        painter = QPainter()
        rect = self.contentsRect()

        boardTop = rect.bottom() - Panel.GRID_PIXEL*Panel.GRID_Y_NUMS

        cur_tetromino = self.state_matrix.next_tetromino
        cur_x = 0
        cur_y = 0

        dy = 3 * Panel.GRID_PIXEL
        dx = (self.width() - Panel.GRID_PIXEL) // 2
        painter.begin(self)



        if not self.state_matrix.next_tetromino is None:

            for i in range(4):
                x = cur_x + cur_tetromino.get_matrix(("X", i))
                y = cur_y + cur_tetromino.get_matrix(("Y", i))

                draw_tetromino(painter, x*self.x_pixel + dx, y*self.y_pixel + dy, cur_tetromino.color, self.x_pixel, self.y_pixel)
                #draw_tetromino(painter, x * Panel.GRID_PIXEL+self.width()//2, boardTop + (Panel.GRID_Y_NUMS - y - 1) * Panel.GRID_PIXEL, cur_tetromino.color)

        # if self.nextTetromino:
        #     for i in range(4):
        #         x = self.curX + self.curTetromino.get_matrix(("X", i))
        #         y = self.curY - self.curTetromino.get_matrix(("Y", i))
        #         self.draw(painter, rect.left() + Panel.GRID_PIXEL*Panel.GRID_X_NUMS + x * Panel.GRID_PIXEL,
        #                         boardTop + (Panel.GRID_Y_NUMS - y - 1) * Panel.GRID_PIXEL)

        painter.end()
