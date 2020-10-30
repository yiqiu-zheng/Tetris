#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2020/10/26 8:47
# @Author  : YIQIU ZHENG
# @FileName: Utils.py
# @Software: PyCharm


from PyQt5.QtGui import QPainter, QColor
import random
import Panel


def draw_tetromino(qt_painter, abs_x, abs_y, color_index, x_pixel, y_pixel):
        """
        Use the absolute position to draw a colorful square
        :param qt_painter:
        :param abs_x:
        :param abs_y:
        :param color_index:
        :return:
        """
        color = QColor(Panel.COLORLIST[color_index])
        qt_painter.fillRect(abs_x + 1, abs_y + 1, x_pixel - 2,
                         y_pixel - 2, color)

        qt_painter.setPen(color.lighter())
        qt_painter.drawLine(abs_x, abs_y + y_pixel - 1, abs_x, abs_y)
        qt_painter.drawLine(abs_x, abs_y, abs_x + x_pixel - 1, abs_y)

        qt_painter.setPen(color.darker())
        qt_painter.drawLine(abs_x + 1, abs_y + y_pixel - 1,
                            abs_x + x_pixel - 1, abs_y + y_pixel - 1)
        qt_painter.drawLine(abs_x + x_pixel - 1,
                            abs_y + y_pixel - 1, abs_x + x_pixel - 1, abs_y + 1)
