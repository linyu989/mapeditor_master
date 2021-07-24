"""
 @Author       :linyu
 @File         :excel_map_show.py
 @Description  :excel数据展示
 @Software     :PyCharm
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
import random

from simulation import map_show

plt.rcParams['figure.dpi'] = 500  # 分辨率


def read_xlsx_data(path):
    df = pd.read_excel(path)
    dict_list = df.to_dict('list')
    # print(dict_list)

    return dict_list


def excel_show(dict_list, img_save=0):
    img = map_show.img_get(dict_list)
    # 处理图像，先y=x对称再y=c对称
    img = map_show.img_symmtry_rotation(img)
    print("imgreal================================")
    print(img.shape, img.dtype)

    plt.imshow(img)
    # plt.axis('off')

    # 保存图片
    if img_save == 1:
        plt.savefig(f'./output/excel_map_show_{str(random.randint(0, 9999))}.png', dpi=700)
    plt.show()


if __name__ == '__main__':
    path = '../data/1_1_20210414111721_.xlsx'
    dict_list = read_xlsx_data(path)
    excel_show(dict_list)
