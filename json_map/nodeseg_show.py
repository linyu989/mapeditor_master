"""
 @Author       :linyu
 @File         :nodeseg_show.py
 @Description  :node与segment的展示
 @Software     :PyCharm
"""
import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
import random

from simulation import map_show
from json_map import mapnode_show
from json_map import mapseg_show

plt.rcParams['figure.dpi'] = 500  # 分辨率


# 对已经生成的mapnode图像加线段
def seg_node_map(seg_code_centers_dict, img):
    max_cell_size = img.shape[:2]
    seg_code_celltype = seg_code_centers_dict['seg_code_celltype']
    seg_code_centers = seg_code_centers_dict['seg_code_centers']

    # 线条宽度
    line_width = 10
    # 坐标缩放
    scale = 10

    for index, seg_code_center in enumerate(seg_code_centers):

        center1 = [int(seg_code_center[0][0] / scale), int(seg_code_center[0][1] / scale)]
        center2 = [int(seg_code_center[1][0] / scale), int(seg_code_center[1][1] / scale)]

        min_centerx = min(center1[0], center2[0])
        max_centerx = max(center1[0], center2[0])
        min_centery = min(center1[1], center2[1])
        max_centery = max(center1[1], center2[1])
        distance_x = max_centerx - min_centerx
        distance_y = max_centery - min_centery

        if distance_x == 0:
            img[min_centerx - line_width:min_centerx + line_width, min_centery:max_centery] = [135, 167, 237]
        elif distance_y == 0:
            img[min_centerx:max_centerx, min_centery - line_width:min_centery + line_width] = [135, 167, 237]
        else:
            img[min_centerx:max_centerx + line_width, min_centery:max_centery + line_width] = [135, 167, 237]

    return img


def nodeseg_img(dict_list, seg_code_centers_dict, img_save):
    img = map_show.img_get(dict_list)

    '''segment画线'''
    img = seg_node_map(seg_code_centers_dict, img)

    # 处理图像，先y=x对称再y=c对称
    img = map_show.img_symmtry_rotation(img)
    print("imgreal================================")
    print(img.shape, img.dtype)

    plt.imshow(img)
    # plt.axis('off')

    # 保存图片
    if img_save == 1:
        plt.savefig(f'./output/nodeseg_show_{str(random.randint(0, 9999))}.png', dpi=500)

    plt.show()


def json_nodeseg_show(jsonnode_data, jsonseg_data, img_save=0):
    '''jsonnode转字典'''
    jsonnode_dict_list = mapnode_show.jsonnode2dict_list(jsonnode_data)
    jsonnode_dict_list = mapnode_show.standard_format(jsonnode_dict_list)
    '''jsonseg数据转字典格式'''
    jsonseg_dict_list = mapseg_show.jsonseg2dict_list(jsonseg_data)
    seg_code_centers_dict, max_cell_size = mapseg_show.code_local(jsonnode_dict_list, jsonseg_dict_list)

    nodeseg_img(jsonnode_dict_list, seg_code_centers_dict, img_save)


if __name__ == '__main__':
    '''数据集'''

    path = '../data/map_1_1625803734368.json'

    '''读取json_node_seg数据'''
    jsonnode_data, jsonseg_data = mapseg_show.read_node_seg_data(path)

    json_nodeseg_show(jsonnode_data, jsonseg_data)
