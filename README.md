# 地图生成器

## 功能

    读取xlsx/xls/json格式的地图数据文件生成图片展示和保存

## 运行方式

    1.安装requirements.txt里面所有包
    2.运行main.py文件(可根据参数说明修改对应参数)

## 项目结构

    mapeditor_master
    │  main.py      //主函数
    │  README.md
    │          
    ├─data      //资源文件夹
    │      
    ├─excel_map
    │      excel_map_show.py    //excel地图数据文件解析
    │      
    ├─json_map                  //json文件解析
    │      mapnode_show.py      //只解析mapnode节点
    │      mapseg_show.py       //只解析mapsegment节点
    │      nodeseg_show.py      //mapnode与mapsegment合并解析
    │      
    ├─output                    //图片输出文件夹
    │      
    └─simulation
            map.py               //map类对象
            map_show.py          //对解析的数据转换并生成图片

   

## 参数说明

    # 文件路径,读取xlsx/xls/json三种格式文件
    # path = './data/1_1_20210414111721_.xlsx'
    path = './data/map_1_1625803734368.json'
    
    # json文件参数
    flag = 2 # flag=0/None,1,2 0/None表示只读node,1表示只读seg，2表示两者皆读取,默认为2
    
    #是否保存图片
    img_save = 0  # 0表示不保存图片1表示保存，默认不保存

## 文件数据格式

    excel数据格式:
        dict_list={'cell_code':[] 
               'location_x':[15560,] 单位毫米，整数    
               'location_y':[20550,] 单位毫米，整数
               'cell_type':[]  字符列表
               'width':[1.15] 单位米，两位小数
               'length':[1.35] 单位米，两位小数，坐标单位转换直接相减可得  
    
    json数据格式： 
        dict_list={'cell_code':[] 
               'location_x':[15.559,] 单位米，三位小数
               'location_y':[20.548] 单位米，三位小数
               'cell_type':[]  字符列表
               'width':[1.15,] 单位米，两位小数
               'length':[1.35,] 单位米，两位小数，由坐标相减往上近似两位，或由坐标近似后计算
               
    计算所用格式: 
        dict_list={'cell_code':[] 
               'location_x':[15560,] 单位毫米，整数    
               'location_y':[20550,] 单位毫米，整数
               'cell_type':[]  字符列表
               'width':[1150,] 单位毫米,整数
               'length':[1350,] 单位毫米,整数，坐标直接相减可得  
