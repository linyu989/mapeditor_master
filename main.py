"""
 @Author       :linyu
 @File         :main.py
 @Description  :
 @Software     :PyCharm
"""
from excel_map import excel_map_show
from json_map import mapnode_show
from json_map import mapseg_show
from json_map import nodeseg_show


def show_main(path, flag=None, img_save=0):
    print(path[-5:])

    if path[-5:] == '.xlsx' or path[-4:] == '.xls':
        dict_list = excel_map_show.read_xlsx_data(path)
        excel_map_show.excel_show(dict_list, img_save)

    elif path[-5:] == '.json':
        if flag == None or flag == 0:
            dict_list = mapnode_show.read_json_mapnode_data(path)
            mapnode_show.json_mapnode_show(dict_list, img_save)

        elif flag == 1:
            jsonnode_data, jsonseg_data = mapseg_show.read_node_seg_data(path)
            mapseg_show.jsonseg_show(jsonnode_data, jsonseg_data, img_save)

        elif flag == 2:
            jsonnode_data, jsonseg_data = mapseg_show.read_node_seg_data(path)
            nodeseg_show.json_nodeseg_show(jsonnode_data, jsonseg_data, img_save)

        else:
            print("[INFO] Error Flag!!!")
    else:
        print("[INFO] Error Path!!!")


if __name__ == '__main__':
    # path = './data/1_1_20210414111721_.xlsx'
    # path = './data/1_1_20210706155008_.xlsx'
    path = './data/map_1_1625803734368.json'

    # flag=0/None,1,2 0/None表示只读node,1表示只读seg，2表示两者皆读取
    flag = 2

    img_save = 0  # 0表示不保存图片1表示保存，默认不保存

    show_main(path, flag, img_save)
