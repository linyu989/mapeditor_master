"""
 @Author       :linyu
 @File         :mapnode_show.py
 @Description  :mapnode数据显示
 @Software     :PyCharm
"""
import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
import datetime
import random

from simulation import map_show

plt.rcParams['figure.dpi'] = 500  # 分辨率

"""
json数据： dict_list={'cell_code':[] 
               'location_x':[15.559,] 单位米，三位小数
               'location_y':[20.548] 单位米，三位小数
               'cell_type':[]  字符列表
               'width':[1.15,] 单位米，两位小数
               'length':[1.35,] 单位米，两位小数，由坐标相减往上近似两位，或由坐标近似后计算

标准数据: dict_list={'cell_code':[] 
               'location_x':[15560,] 单位毫米，整数    
               'location_y':[20550,] 单位毫米，整数
               'cell_type':[]  字符列表
               'width':[1.15] 单位米，两位小数
               'length':[1.35] 单位米，两位小数，坐标直接相减可得    
"""

'''json_mapnode数据读取'''


def read_json_mapnode_data(path):
    with open(path, 'rb') as f:
        json_data = json.load(f)

    # print(json_data)
    exportMapNodeDtoList = json_data['exportMapDto']['exportMapNodeDtoList']
    # print(exportMapNodeDtoList)
    return exportMapNodeDtoList


'''json_mapnode数据转换标准格式'''


def jsonnode2dict_list(jsonnode_data):
    dict_list_maps = {}
    dict_list_maps['cell_code'] = []
    dict_list_maps['location_x'] = []
    dict_list_maps['location_y'] = []
    dict_list_maps['cell_type'] = []
    dict_list_maps['width'] = []
    dict_list_maps['length'] = []

    for dict in jsonnode_data:
        dict_list_maps['cell_code'].append(dict['cellCode'])
        dict_list_maps['location_x'].append(dict['locationX'])
        dict_list_maps['location_y'].append(dict['locationY'])
        dict_list_maps['cell_type'].append(dict['cellType'])
        dict_list_maps['width'].append(dict['width'])
        dict_list_maps['length'].append(dict['length'])

    '''{
    'cellCode': '22751215',
    'cellType': 'STATION_CELL',
    'locationX': 107.466,
    'locationY': 44.29,
    'length': 1.35,
    'width': 1.15,
  }
  '''
    return dict_list_maps


'''坐标转换标准格式'''


def standard_format(dict_list):
    location_x = dict_list['location_x']
    location_y = dict_list['location_y']

    # 坐标位数近似
    newxlist = np.around(location_x, 2)
    newylist = np.around(location_y, 2)

    # 单位转换为毫米
    dict_list['location_x'] = [int(x * 1000) for x in newxlist]
    dict_list['location_y'] = [int(y * 1000) for y in newylist]

    return dict_list


def json_mapnode_show(dict_list,img_save=0):
    '''数据处理'''
    # 转换为标准格式
    dict_list = jsonnode2dict_list(dict_list)
    dict_list = standard_format(dict_list)
    print("json format========================")
    print(dict_list)

    img = map_show.img_get(dict_list)

    # 处理图像，先y=x对称再y=c对称
    img = map_show.img_symmtry_rotation(img)
    print("imgreal================================")
    print(img.shape, img.dtype)

    plt.imshow(img)
    # plt.axis('off')

    # 保存图片
    if img_save==1:
        plt.savefig(f'./output/mapnode_show_{str(random.randint(0,9999))}.png', dpi=700)

    plt.show()


if __name__ == '__main__':
    path = '../data/map_1_1625803734368.json'
    dict_list = read_json_mapnode_data(path)

    json_mapnode_show(dict_list)
