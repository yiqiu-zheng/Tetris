#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2020/10/24 10:10 PM
# @Author  : mirko
# @FileName: MainPanel.py
# @Software: PyCharm


import sys
from PyQt5 import QtWidgets,QtCore
from PyQt5.QtWidgets import QDesktopWidget, QApplication, QMainWindow, QWidget, QFrame, QHBoxLayout, QPushButton,QGridLayout
from PyQt5.QtGui import QPainter, QColor

from PyQt5.QtCore import Qt, QBasicTimer, pyqtSignal


import Panel
from Panel.CoreFrame import CoreFrame
from Panel.SideFrame import SideFrame

from Panel.LogicControl import StateMatrix
from Shape import AllTypes

class GamePanel(QMainWindow):

    def __init__(self, parent=None):
        super(GamePanel, self).__init__(parent)

        # self.setWindowTitle("Tetris")
        #
        #
        # self.timer = QBasicTimer()
        self.setFocusPolicy(Qt.StrongFocus)

        # #Handle the state matrix
        # self.state_matrix = StateMatrix(self.timer)
        #
        # #self.is_gameover = self.state_matrix.is_gameover

        #
        # self.core = CoreFrame(self, self.state_matrix)
        # self.side = SideFrame(self, self.state_matrix)
        #
        #
        # self.core.begin_loop()
        # self.start_game()
        #
        #
        # layout = QHBoxLayout()
        #
        # layout.addWidget(self.core)
        # layout.addWidget(self.side)
        #
        # self.setLayout(layout)
        # self.move_to_center()
        # self.setFixedSize(self.core.width()+self.side.width(), self.core.height())

        self.timer = QBasicTimer()

        self.setWindowTitle("test")

        self.state_matrix = StateMatrix(self.timer)
        self.is_paused = self.state_matrix.is_paused


        self.core = CoreFrame(self, self.state_matrix)
        self.side = SideFrame(self, self.state_matrix)

        self.setFixedSize((Panel.GRID_X_NUMS + 11) * Panel.GRID_PIXEL, (Panel.GRID_Y_NUMS+2) * Panel.GRID_PIXEL)


        main_grid_layout = QGridLayout()
        self.main_widget = QtWidgets.QWidget()
        self.main_widget.setLayout(main_grid_layout)


        self.core_widget = QtWidgets.QWidget()
        self.core_widget.setObjectName("core_widget")
        self.core_widget.setStyleSheet('background-color:white;border-radius:3px;')
        core_grid_layout = QGridLayout()
        self.core_widget.setLayout(core_grid_layout)
        core_grid_layout.addWidget(self.core)


        self.side_widget = QtWidgets.QWidget()
        self.side_widget.setObjectName("side_widget")
        self.side_widget.setStyleSheet('background-color:skyblue;border-radius:3px;')

        side_grid_layout = QGridLayout()
        self.side_widget.setLayout(side_grid_layout)

        self.right_close = QtWidgets.QPushButton("")  # 关闭按钮
        self.right_mini = QtWidgets.QPushButton("")  # 最小化按钮

        self.right_close.setDefault(False)
        self.right_close.setAutoDefault(False)
        self.right_mini.setDefault(False)
        self.right_mini.setAutoDefault(False)

        self.right_close.clicked.connect(self.close_click)
        self.right_mini.clicked.connect(self.mini_click)



        self.right_close.setFixedSize(15,15)
        self.right_mini.setFixedSize(15,15)

        self.right_close.setStyleSheet('''QPushButton{background:#F76675;border-radius:5px;}QPushButton:hover{background:red;}''')
        self.right_mini.setStyleSheet('''QPushButton{background:#6DDF6D;border-radius:5px;}QPushButton:hover{background:green;}''')

        side_grid_layout.addWidget(QtWidgets.QLabel(""), 0, 0)
        side_grid_layout.addWidget(self.right_mini, 0,1)
        side_grid_layout.addWidget(self.right_close, 0, 2)
        side_grid_layout.addWidget(QtWidgets.QLabel("The next tetromino:"), 1, 0)
        side_grid_layout.addWidget(self.side, 2, 0, 3, 3)

        self.display_widget = QtWidgets.QWidget();
        self.display_widget.setObjectName("display_widget")
        self.display_widget.setStyleSheet("background-color:skyblue;border-radius:3px;")

        display_grid_layout = QGridLayout()
        self.display_widget.setLayout(display_grid_layout)
        #display_grid_layout.addWidget(self.display_widget)

        self.score_label = QtWidgets.QLabel("Score:")
        self.score_value = QtWidgets.QLabel("2")
        self.speed_label = QtWidgets.QLabel("Speed:")
        self.speed_value = QtWidgets.QLabel("2")
        display_grid_layout.addWidget(self.score_label)
        display_grid_layout.addWidget(self.score_value)
        display_grid_layout.addWidget(self.speed_label)
        display_grid_layout.addWidget(self.speed_value)

        main_grid_layout.addWidget(self.core_widget,0,0, 12, 8)
        main_grid_layout.addWidget(self.side_widget, 0, 8, 4, 6)
        main_grid_layout.addWidget(self.display_widget, 4, 8, 8, 6 )


        self.setCentralWidget(self.main_widget)



        self.core.begin_loop()
        self.start_game()

        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setWindowOpacity(0.9) # 设置窗口透明度
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground) # 设置窗口背景透明


    def close_click(self):
        qApp = QApplication.instance()
        qApp.quit()

    def mini_click(self):
        self.showMinimized()

    def start_game(self):
        self.timer.start(self.state_matrix.speed, self)

    def pause_game(self):
        if not self.is_paused:
            self.timer.stop()
        else:
            self.timer.start(self.state_matrix.speed, self)

        self.is_paused = not self.is_paused


    def move_to_center(self):
        """
        Move the window to the middle of screen
        :return:
        """
        screen = QDesktopWidget().screenGeometry()

        size = self.geometry()
        self.move((screen.width() - size.width()) //2, (screen.height() - size.height()) // 2)

    def timerEvent(self, event):
        """
        Handle the timer event of main panel
        :param event:
        :return:
        """

        if event.timerId() == self.timer.timerId():

            if self.is_paused or self.state_matrix.is_gameover:
                return



            cur_tetromino = self.state_matrix.cur_tetromino
            cur_x = self.state_matrix.cur_x
            cur_y = self.state_matrix.cur_y

            if not self.state_matrix.call_idle_down():
                self.state_matrix.drop_and_generate()
            # if self.state_matrix.graceful_waiting:
            #     #Now we have a graceful waiting state, which means the program needs to produce a new tetromino
            #     self.state_matrix.graceful_waiting = not self.state_matrix.graceful_waiting
            #     self.state_matrix.generate_new_tetromino()
            # else:
            #     if not self.state_matrix.call_idle_down():
            #         self.state_matrix.drop_and_generate()


            self.refresh_all()

        else:
            super(CoreFrame, self).timerEvent(event)


    def refresh_all(self):
        self.core.refresh()
        self.side.refresh()
        self.update()



    def keyPressEvent(self, event):
        '''
        Handle the keyboard event of main panel
        :param event:
        :return:
        '''

        key = event.key()

        cur_tetromino = self.state_matrix.cur_tetromino
        cur_x = self.state_matrix.cur_x
        cur_y = self.state_matrix.cur_y

        if key == Qt.Key_R and self.state_matrix.is_gameover:
            self.state_matrix.is_gameover = not self.state_matrix.is_gameover

            self.core.initCoreFrame()
            self.core.begin_loop()
            self.refresh_all()
            self.timer.start(Panel.FPS, self)
            return


        if self.state_matrix.is_gameover:
            return


        if key == Qt.Key_P:
            self.pause_game()
            return

        if self.is_paused:
            return

        if key == Qt.Key_Left:
            print("left after go")
            self.state_matrix.call_move_left()
        elif key == Qt.Key_Right:
            self.state_matrix.call_move_right()
        elif key == Qt.Key_Down:
            self.state_matrix.call_idle_down()
        elif key == Qt.Key_Up:
            self.state_matrix.call_rotate()
        elif key == Qt.Key_Space:
            self.state_matrix.call_quick_down()
        else:
            super(CoreFrame, self).keyPressEvent(event)

        self.refresh_all()


if __name__ == '__main__':
        app = QApplication(sys.argv)
        win = GamePanel()
        win.show()
        sys.exit(app.exec_())