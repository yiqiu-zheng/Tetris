#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2020/10/24 6:07 PM
# @Author  : YIQIU ZHENG
# @FileName: AllTypes.py
# @Software: PyCharm

from . import RegisterTetrominoType, Tetromino


@RegisterTetrominoType("ITetromino")
class ITetromino(Tetromino):
    def __init__(self, settings):
        super(ITetromino, self).__init__(settings)
        self.rotation_matrix = list([[0, -1], [0, 0], [0, 1], [0, 2]])
        self.color = 0

    def __str__(self):
        return "ITetromino"



@RegisterTetrominoType("OTetromino")
class OTetromino(Tetromino):
    def __init__(self, settings):
        super(OTetromino, self).__init__(settings)
        self.rotation_matrix = list([[0, 0], [1, 0], [0, 1], [1, 1]])
        self.color = 1

    def rotate(self, angle):
        return self

    def __str__(self):
        return "OTetromino"


@RegisterTetrominoType("TTetromino")
class TTetromino(Tetromino):
    def __init__(self, settings):
        super(TTetromino, self).__init__(settings)
        self.rotation_matrix = list([[-1, 0], [0, 0], [1, 0], [0, 1]])
        self.color = 2

    def __str__(self):
        return "TTetromino"



@RegisterTetrominoType("STetromino")
class STetromino(Tetromino):
    def __init__(self, settings):
        super(STetromino, self).__init__(settings)
        self.rotation_matrix = list([[0, -1], [0, 0], [1, 0], [1, 1]])
        self.color = 3

    def __str__(self):
        return "STetromino"



@RegisterTetrominoType("ZTetromino")
class ZTetromino(Tetromino):
    def __init__(self, settings):
        super(ZTetromino, self).__init__(settings)
        self.rotation_matrix = list([[0, -1], [0, 0], [-1, 0], [-1, 1]])
        self.color = 4

    def __str__(self):
        return "ZTetromino"

@RegisterTetrominoType("JTetromino")
class JTetromino(Tetromino):
    def __init__(self, settings):
        super(JTetromino, self).__init__(settings)
        self.rotation_matrix = list([[1, -1], [0, -1], [0, 0], [0, 1]])
        self.color = 5

    def __str__(self):
        return "JTetromino"


@RegisterTetrominoType("LTetromino")
class LTetromino(Tetromino):
    def __init__(self, settings):
        super(LTetromino, self).__init__(settings)
        self.rotation_matrix = list([[-1, -1], [0, -1], [0, 0], [0, 1]])
        self.color = 6

    def __str__(self):
        return "LTetromino"


