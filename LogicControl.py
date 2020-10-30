#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2020/10/26 10:58
# @Author  : YIQIU ZHENG
# @FileName: LogicControl.py
# @Software: PyCharm

import Panel
from Shape import TetrominoFactory


class StateMatrix(object):

    def __init__(self, timer):

        self.t_matrix = [[None] * Panel.GRID_Y_NUMS for i in range(Panel.GRID_X_NUMS)]

        self.cur_x = 0
        self.cur_y = 0

        self.cur_tetromino = None
        self.next_tetromino = TetrominoFactory.create_random_tetromino()

        self.lines_removed = 0

        self.score = 0
        self.speed = Panel.FPS

        #when we need a new tetromino, let the gui be softer
        self.graceful_waiting = False

        self.is_paused = False
        self.is_gameover = False

        self.timer = timer

    def set_state_matrix(self, x_index, y_index, tetromino):

        self.t_matrix[x_index][y_index] = tetromino

    def get_state_matrix(self, x_index, y_index):

        return self.t_matrix[x_index][y_index]

    def generate_new_tetromino(self):

        self.cur_tetromino = self.next_tetromino
        self.next_tetromino = TetrominoFactory.create_random_tetromino()

        self.cur_x = Panel.GRID_X_NUMS // 2 + 1
        self.cur_y = Panel.GRID_Y_NUMS - 2
                    #+ self.curPiece.minY()

        self.judge_is_gameover()

        # if not self.tryMove(self.curPiece, self.curX, self.curY):
        #     self.curPiece.setShape(Tetrominoe.NoShape)
        #     self.timer.stop()
        #     self.isStarted = False
        #     self.msg2Statusbar.emit("Game over")


    def judge_is_gameover(self):

        if self.__collision_detection(self.cur_tetromino, self.cur_x, self.cur_y):
            print("game over")
            self.is_gameover = True
            self.cur_tetromino = None
            self.timer.stop()



    def clear_state_matrix(self):
        for i in range(Panel.GRID_X_NUMS):
            for j in range(Panel.GRID_Y_NUMS):
                self.t_matrix[i][j] = None


    def detect_and_move(self, tetromino, new_x, new_y):
        if not self.__collision_detection(tetromino, new_x, new_y):
            self.__move_tetromino(tetromino, new_x, new_y)
            return True

        return False



    def __collision_detection(self, tetromino, new_x, new_y):
        """
        Check if a tetromino is dropped
        :param tetromino:
        :param newX:
        :param newY:
        :return: true:collision false:nothing happened
        """
        for i in range(4):

            x = new_x + tetromino.get_matrix(("X", i))
            y = new_y - tetromino.get_matrix(("Y", i))

            #beyond boundary
            if x < 0 or x >= Panel.GRID_X_NUMS or y < 0 or y >= Panel.GRID_Y_NUMS:
                return True

            #overlapping
            if not self.get_state_matrix(x, y) is None:
                return True


        return False

    def __move_tetromino(self, tetromino, new_x, new_y):

        self.cur_tetromino = tetromino
        self.cur_x = new_x
        self.cur_y = new_y


    def call_move_left(self):
        self.detect_and_move(self.cur_tetromino, self.cur_x-1, self.cur_y)


    def call_move_right(self):
        self.detect_and_move(self.cur_tetromino, self.cur_x+1, self.cur_y)

    def call_rotate(self):
        if not self.detect_and_move(self.cur_tetromino.rotate(90), self.cur_x, self.cur_y):
            self.cur_tetromino.rotate(-90)

    def call_idle_down(self):
        return True if self.detect_and_move(self.cur_tetromino, self.cur_x, self.cur_y - 1) else False



    def call_quick_down(self):
        new_y = self.cur_y

        while new_y > 0:
            if not self.detect_and_move(self.cur_tetromino, self.cur_x, new_y - 1):
                break
            new_y -= 1

        self.drop_and_generate()


    def drop_and_generate(self):

        for i in range(4):
            x = self.cur_x + self.cur_tetromino.get_matrix(("X", i))
            y = self.cur_y - self.cur_tetromino.get_matrix(("Y", i))

            self.set_state_matrix(x, y, self.cur_tetromino.color)

        self.remove_full_lines()

        # if not self.graceful_waiting:
        self.generate_new_tetromino()
            #self.judge_is_gameover()

    def remove_full_lines(self):
        num_full_lines = 0
        rows_to_remove = []

        for i in range(Panel.GRID_Y_NUMS):

            n = 0
            for j in range(Panel.GRID_X_NUMS):
                if not self.get_state_matrix(j, i) is None:
                    n = n + 1

            if n == Panel.GRID_X_NUMS:
                rows_to_remove.append(i)

        rows_to_remove.reverse()

        for m in rows_to_remove:

            for k in range(m, Panel.GRID_Y_NUMS - 1):
                for l in range(Panel.GRID_X_NUMS):
                    self.set_state_matrix(l, k, self.get_state_matrix(l, k + 1))

        num_full_ines = num_full_lines + len(rows_to_remove)


        if num_full_ines > 0:
            self.lines_removed = self.lines_removed + num_full_ines
            self.cur_tetromino = None
