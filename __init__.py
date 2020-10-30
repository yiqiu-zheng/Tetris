#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2020/10/24 12:35 PM
# @Author  : YIQIU ZHENG
# @FileName: __init__.py.py
# @Software: PyCharm

import random
import math

XAXIS = "X"
YAXIS = "Y"


class RegisterTetrominoType(object):

    tetromino_type = {}

    def __init__(self, type):
        self._type = type

    def __call__(self, cls, *args, **kwargs):
        self.tetromino_type[self._type] = cls

        return cls

class TetrominoFactory(object):

    __tetromino_type = RegisterTetrominoType.tetromino_type

    rotate_angle = [0, 90, 180, 270]

    @classmethod
    def build_tetromino(cls, type):
        if cls.__tetromino_type.__contains__(type):
            return cls.__tetromino_type[type]
        else:
            raise NotImplementedError()

    @classmethod
    def create_random_tetromino(cls):
        import random
        #random_tetromino = TetrominoFactory.build_tetromino("ITetromino").from_settings(None)

        random_tetromino = TetrominoFactory.build_tetromino(random.choice(list(cls.__tetromino_type.keys()))).from_settings(None)
        #Before return, we need to rotate the tetromino by a random angle
        return random_tetromino.rotate(random.choice(cls.rotate_angle))


class Tetromino(object):

    @classmethod
    def from_settings(cls, settings):
        tetromino = cls(settings)

        return tetromino


    def __init__(self, settings):
        self.rotation_matrix = list([[0 for x in range(2)] for y in range(2)])


    #handle the tetromino's color
    @property
    def color(self):
        return self.__color

    @color.setter
    def color(self, value):
        self.__color = value



    def set_matrix(self, params):

        """
        Set value in game state matrix
        :param params: a tuple like this:("Y", index, coordinate)
        :return: none
        """

        try:
            type, index, coordinate = params
        except ValueError:
            raise ValueError("A iterable object with three items is expected here.")

        axis = -1

        if isinstance(type, str) and type.strip() == "X":
            axis = 0

        elif isinstance(type, str) and type.strip() == "Y":
            axis = 1
        else:
            raise ValueError("str(X) or str(Y) is expected here.")

        self.rotation_matrix[index][axis] = coordinate


    def get_matrix(self, params):
        """
        Get value in game state matrix
        :param params: a tuple like this: ("X", index)
        :return: coordinate value
        """

        try:
            type, index = params

        except ValueError:
            raise ValueError("A iterable object with two items is expected here.")

        axis = -1

        if isinstance(type, str) and type.strip() == "X":
            axis = 0

        elif isinstance(type, str) and type.strip() == "Y":
            axis = 1
        else:
            raise ValueError("str(X) or str(Y) is expected here.")

        return self.rotation_matrix[index][axis]

    def rotate(self, angle):
        """
        Rotate tetromino
        :param angle:
        :return:
        """
        #rotation formula: xl = cos(angle)*x - sin(angle)*y, yl = cos(angle)*y + sin(angle)*x
        from copy import deepcopy
        angle = math.radians(angle)
        tmp_matrix = self.rotation_matrix.copy()

        for i in range(4):
            xl = math.cos(angle)*tmp_matrix[i][0] - math.sin(angle)*tmp_matrix[i][1]
            yl = math.cos(angle)*tmp_matrix[i][1] + math.sin(angle)*tmp_matrix[i][0]

            self.set_matrix((XAXIS, i, round(xl)))
            self.set_matrix((YAXIS, i, round(yl)))

        del tmp_matrix

        return deepcopy(self)


    def __str__(self):
        """
        Print function
        :return:
        """
        raise NotImplementedError("The tetromino must have a __str__() func to display")
