# -*- coding: utf-8 -*-
"""
Created on Mon Sep 23 00:44:09 2024

@author: scuzzk
@page:
"""

# 坐标转化模块
from AmapMetro import Generator


if __name__ == '__main__':
    
    # 默认必须生成高德坐标系下的geojson文件，包括线路和站点
    # 文件格式仅可以填写'geojson'\'shp'
    # 要素类型仅可以填写'point'\'line'
    # 坐标系类型仅可以填写'gaode'\'baidu'\'wgs84'
    Generator.MetroData('geojson', 'line', 'baidu')
    Generator.MetroData('geojson', 'point', 'baidu')
    Generator.MetroData('geojson', 'line', 'wgs84')
    Generator.MetroData('geojson', 'point', 'wgs84')
    
    Generator.MetroData('shp', 'line', 'baidu')
    Generator.MetroData('shp', 'point', 'baidu')
    Generator.MetroData('shp', 'line', 'wgs84')
    Generator.MetroData('shp', 'point', 'wgs84')
    Generator.MetroData('shp', 'line', 'gaode')
    Generator.MetroData('shp', 'point', 'gaode')
    
