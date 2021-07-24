#!/usr/bin/env python
# -*- coding: utf-8 -*-
import math
import numpy as np


class Cell():
    code = ''  # 编号
    type = None  # 类型
    is_slam = None  # 区别是阵列 还是单节点
    rotation = None  # 旋转角度 ，以0点为0°，顺时针方向为正
    corner = None
    center = []
    index = []
    size = []  # x ,y
    load_dir = ''
    unload_dir = ''


class MapCells():
    def __init__(self, map_shape):
        self.map_shape = map_shape
        self.cells = dict()
        self.max_cell_size = [0, 0]
        pass

    def setcell(self, type, index, corner=None, center=None, size=None, load_dir=None, no_load_dir=None, cellnode=None):
        cell = Cell()
        cell.type = type
        cell.corner = np.array(corner)
        cell.index = index
        cell.size = np.array(size)
        cell.load_dir = load_dir
        cell.no_load_dir = no_load_dir
        cell.center = cell.corner + cell.size / 2
        key = str(index)
        self.cells[key] = cell

        cell.code = cellnode

    def getcell(self, index):
        return self.cells[str(list(index))]

    def get_turn_area_location(self, index):
        x = math.ceil(index[0])
        y = math.ceil(index[1])
        center1 = self.cells[str([x, y])].center
        x = int(index[0])
        y = int(index[1])
        center2 = self.cells[str([x, y])].center

        return (center1 + center2) / 2


class Map(object):
    # 地图信息
    def __init__(self, map_type):
        # 索引、大小，
        self.map_type = map_type  #
        self.map_matrix = list()
        self.locked = list()  #
        self.map_width = 0  # width
        self.map_length = 0  # length
        self.cell_width = 0  # width
        self.cell_length = 0  # length
        self.map_no_load_dir_initial = []  # 空载地图
        self.map_load_dir_initial = []  # 负载地图
        self.map_no_load_dir = []  #
        self.map_load_dir = []  #

        self.robot_map = list()


if __name__ == '__main__':
    map_cells = MapCells([1, 1])
    map_cells.setcell(1, [1, 2], corner=[123, 456], size=[2, 4])
    print(map_cells)
    print(map_cells.cells)
    print(map_cells.cells['[1, 2]'])
    print(map_cells.cells['[1, 2]'])
