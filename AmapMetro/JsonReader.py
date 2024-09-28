# -*- coding: utf-8 -*-
"""
Created on Sun Sep 22 17:40:07 2024

@author: scuzzk

"""

import os
import json

# 文件夹下文件名称列表的获取
def file_name_reader(file_name_path):
        try:
            file_name_list = os.listdir(file_name_path)
            return file_name_list
        except:
            print("")


# 读取json文件并返回原始数据
def file_reader(file_path):
        try:
            with open(file_path,"r",encoding='utf-8') as rawjson_data:
                load_json = json.load(rawjson_data)
            busline_list = load_json['data']['busline_list']
            return busline_list
        except:
            print("")