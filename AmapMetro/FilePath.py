# -*- coding: utf-8 -*-
"""
Created on Sun Sep 22 17:31:13 2024

@author: scuzzk

"""

import os
'''
整个文件存储的嵌套关系为：
|<D:/Python/get_subway_from_AMap>: 根目录

|-</jsondata>: 原始json数据目录

|-</final_data>: 转化数据文件目录
|--</shp_data>: shapefile文件目录
|---</gaode>高德坐标系文件目录
|---</wgs84>WGS坐标系文件目录
|---</baidu>百度坐标系文件目录

|--</geojson_data>: geojson文件目录
|---</gaode>高德坐标系文件目录
|---</wgs84>WGS坐标系文件目录
|---</baidu>百度坐标系文件目录

'''


# 根目录
root = 'D:/Python/AmapMetro/'

##-----------------------以下数据谨慎变更，已经预设路径名称-----------------------##
# 原始json数据目录
json_data = root + 'RawData/' 

# 转化数据文件目录
final_data = root + 'FinalData/'

# 文件目录
shp_data = final_data + 'shp_data/'
# 高德坐标系文件目录
shp_data_gaode_line = shp_data + 'line/gaode/'
shp_data_gaode_point = shp_data + 'point/gaode/'
# WGS坐标系文件目录
shp_data_wgs84_line = shp_data + 'line/wgs84/'
shp_data_wgs84_point = shp_data + 'point/wgs84/'
# 百度坐标系文件目录
shp_data_baidu_line = shp_data + 'line/baidu/'
shp_data_baidu_point = shp_data + 'point/baidu/'

# geojson文件目录
geojson_data = final_data + 'geojson_data/'
# 高德坐标系文件目录
geojson_data_gaode_line = geojson_data + 'line/gaode/'
geojson_data_gaode_point = geojson_data + 'point/gaode/'
# WGS坐标系文件目录
geojson_data_wgs84_line = geojson_data + 'line/wgs84/'
geojson_data_wgs84_point = geojson_data + 'point/wgs84/'
# 百度坐标系文件目录
geojson_data_baidu_line = geojson_data + 'line/baidu/'
geojson_data_baidu_point = geojson_data + 'point/baidu/'


total_path = [root,json_data,final_data,
              shp_data_gaode_line, shp_data_gaode_point,
              shp_data_wgs84_line, shp_data_wgs84_point,
              shp_data_baidu_line, shp_data_baidu_point,
              geojson_data_gaode_line, geojson_data_gaode_point,
              geojson_data_wgs84_line, geojson_data_wgs84_point,
              geojson_data_baidu_line, geojson_data_baidu_point]

def pre_path():
    try:
        for path_i in range(len(total_path)):
            if not os.path.exists(total_path[path_i]):
                os.makedirs(total_path[path_i])
    except:
        print("Problems in model <pre_path>")

def path(file_type,geo_type,coor_type):
    try:
        if file_type == 'shp':
            if geo_type == 'point':
                if coor_type == 'gaode':
                    path = shp_data_gaode_point
                elif coor_type == 'wgs84':
                    path = shp_data_wgs84_point
                elif coor_type == 'baidu':
                    path = shp_data_baidu_point
                else:
                    print("确认坐标点的坐标系名称")
            elif geo_type == 'line':
                if coor_type == 'gaode':
                    path = shp_data_gaode_line
                elif coor_type == 'wgs84':
                    path = shp_data_wgs84_line
                elif coor_type == 'baidu':
                    path = shp_data_baidu_line
                else:
                    print("确认地铁线路的坐标系名称")
        elif file_type == 'geojson':
            if geo_type == 'point':
                if coor_type == 'gaode':
                    path = geojson_data_gaode_point
                elif coor_type == 'wgs84':
                    path = geojson_data_wgs84_point
                elif coor_type == 'baidu':
                    path = geojson_data_baidu_point
                else:
                    print("确认坐标点的坐标系名称")
            elif geo_type == 'line':
                if coor_type == 'gaode':
                    path = geojson_data_gaode_line
                elif coor_type == 'wgs84':
                    path = geojson_data_wgs84_line
                elif coor_type == 'baidu':
                    path = geojson_data_baidu_line
                else:
                    print("确认地铁线路的坐标系名称")
        else:
            pass
        return path

    except:
        print("Problems in model <path>")

def raw_data_path():
    return json_data

pre_path()