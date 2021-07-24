"""
 @Author       :linyu
 @File         :mapseg_show.py
 @Description  :map_segment数据展示
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

plt.rcParams['figure.dpi'] = 500  # 分辨率

'''
segment读取
'''

'''读取json_node_seg数据'''


def read_node_seg_data(path):
    with open(path, 'rb') as f:
        json_data = json.load(f)

    # print(json_data)
    exportMapNodeDtoList = json_data['exportMapDto']['exportMapNodeDtoList']
    # print(exportMapNodeDtoList)
    exportMapSegmentDtoList = json_data['exportMapDto']['exportMapSegmentDtoList']
    print("==================")
    print(exportMapSegmentDtoList)
    print("==================")
    print(type(exportMapSegmentDtoList))

    return exportMapNodeDtoList, exportMapSegmentDtoList


'''
seg,node数据分别封装为字典
'''
'''jsonseg数据转字典格式'''


def jsonnode2dict_list(jsonnode_data):
    dict_list = mapnode_show.jsonnode2dict_list(jsonnode_data)
    dict_list = mapnode_show.standard_format(dict_list)

    return dict_list


def jsonseg2dict_list(jsonseg_data):
    dict_list_maps = {}
    dict_list_maps['cell1Code'] = []
    dict_list_maps['cell2Code'] = []
    dict_list_maps['segmentType'] = []
    dict_list_maps['segmentLength'] = []
    for dict in jsonseg_data:
        dict_list_maps['cell1Code'].append(dict['cell1Code'])
        dict_list_maps['cell2Code'].append(dict['cell2Code'])
        dict_list_maps['segmentType'].append(dict['segmentType'])
        dict_list_maps['segmentLength'].append(dict['segmentLength'])

    '''{
    'cell1Code': '10551070',
    'cell2Code': '10551060',
    'segmentType': 0,
    'segmentLength': 1.35,
  }
  '''
    return dict_list_maps


# 读取jsonmap数据，code对应坐标封装
def code_local(dict_list, seg_dict_list):
    # code_locations = {}
    code_center_locations = {}
    cell_code = dict_list['cell_code']
    location_x = dict_list['location_x']
    location_y = dict_list['location_y']
    cell_type = dict_list['cell_type']
    cell_size_width = dict_list['width']
    cell_size_length = dict_list['length']
    cell1Code = seg_dict_list['cell1Code']
    cell2Code = seg_dict_list['cell2Code']
    segmentType = seg_dict_list['segmentType']
    segmentLength = seg_dict_list['segmentLength']

    minx = (min(location_x))
    miny = (min(location_y))

    edge = 100

    # # 最小坐标置零后的maxsize
    maxsizew = max(location_y) - miny
    maxsizel = max(location_x) - minx
    # maxsize得到最大坐标值，实际渲染时从该坐标起点进行色块填充
    # 故maxsize需要加上最大色块长宽，可添加一定余量
    maxsizew = maxsizew + (max(cell_size_width)) * 1000 + edge
    maxsizel = maxsizel + (max(cell_size_length)) * 1000 + edge
    max_cell_size = [int(maxsizel), int(maxsizew)]

    location_x_minzero = []
    location_y_minzero = []
    minx = (min(location_x))
    miny = (min(location_y))
    for i in range(len(location_x)):
        # 不从零开始留边
        zerox = location_x[i] - minx
        zeroy = location_y[i] - miny
        location_x_minzero.append(zerox)
        location_y_minzero.append(zeroy)

    # 每个cellde匹配坐标
    # 应该计算type其对应坐标中心坐标
    for i in range(len(cell_code)):
        code_center_locations[cell_code[i]] = [int(location_x_minzero[i] + cell_size_length[i] * 1000 / 2),
                                               int(location_y_minzero[i] + cell_size_width[i] * 1000 / 2)]
    print(code_center_locations)
    print(code_center_locations)

    seg_code_centers = []
    seg_code_celltype = []
    seg_code_centers_dict = {}

    for j in range(len(cell1Code)):
        seg_code_centers.append([code_center_locations[cell1Code[j]],
                                 code_center_locations[cell2Code[j]]])
        seg_code_celltype.append([cell1Code[j], cell2Code[j]])

    print(seg_code_centers)
    print(max_cell_size)

    seg_code_centers_dict['seg_code_celltype'] = seg_code_celltype
    seg_code_centers_dict['seg_code_centers'] = seg_code_centers

    print(seg_code_centers_dict)

    return seg_code_centers_dict, max_cell_size


'''单独segment渲染'''


# 这是单独渲染的程序
# 如果结合map_node渲染则传入(seg_code_centers_dict, img)
# def seg_render_map(seg_code_centers, max_cell_size):
def seg_render_map(seg_code_centers_dict, max_cell_size):
    seg_code_celltype = seg_code_centers_dict['seg_code_celltype']
    seg_code_centers = seg_code_centers_dict['seg_code_centers']

    edge = 100
    max_xlocal = max_cell_size[0]
    max_ylocal = max_cell_size[1]
    size = [int(max_cell_size[0] / 10), int(max_cell_size[1] / 10)]

    # mytest
    print(f'size is :{size}')
    print("=====================================")

    red = np.zeros(size, dtype=np.uint8)
    green = np.zeros(size, dtype=np.uint8)
    blue = np.zeros(size, dtype=np.uint8)
    red[:, :] = 255
    green[:, :] = 255
    blue[:, :] = 255
    img = np.dstack((red, green, blue))

    print(len(seg_code_centers))

    # 线条宽度
    line_width = 5
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


def jsonseg_show(jsonnode_data, jsonseg_data,img_save):
    jsonnode_dict_list = jsonnode2dict_list(jsonnode_data)
    jsonseg_dict_list = jsonseg2dict_list(jsonseg_data)

    seg_code_centers_dict, max_cell_size = code_local(jsonnode_dict_list, jsonseg_dict_list)

    # 渲染图片
    # img = seg_render_map(seg_code_center_list, max_cell_size)
    img = seg_render_map(seg_code_centers_dict, max_cell_size)
    # print(img)
    print("imgis================================")
    print(img.shape, img.dtype)

    # 处理图像，先y=x对称再y=c对称
    img = map_show.img_symmtry_rotation(img)
    print("imgreal================================")
    print(img.shape, img.dtype)

    plt.imshow(img)
    # plt.axis('off')

    # 保存图片
    if img_save==1:
        plt.savefig(f'./output/mapseg_show_{str(random.randint(0,9999))}.png', dpi=700)

    plt.show()


if __name__ == '__main__':
    path = '../data/map_1_1625803734368.json'
    jsonnode_data, jsonseg_data = read_node_seg_data(path)

    jsonseg_show(jsonnode_data, jsonseg_data)
