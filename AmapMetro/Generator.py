# -*- coding: utf-8 -*-
"""
Created on Tue Sep 24 21:42:24 2024

@author: zoro
"""

# 坐标转化模块
import CoorTrans
# 文件地址归集模块
import FilePath
# 文件类型转换模块
#from AmapMetro import FileTrans
# GeoJson文件保存模块
import json
# 提取数据信息模块-
import GetData
# 读取原始Json文件模块
import JsonReader
# 完成geojson文件的编辑工作
from geojson import FeatureCollection
# 用于geojson数据的处理
import geopandas
# 用于geopandas中矢量数据处理
from shapely import geometry


# 清洗得到火星坐标系的地铁线路和站点数据
def MetroGaode():
    try:
        # 获取所有城市目录，即得到广州、东莞等城市名称
        city_menu = JsonReader.file_name_reader(FilePath.raw_data_path())
        # 在每个城市下进行数据汇总
        for city_i in range(len(city_menu)):
            try:
                # 获取城市所有线路目录，得到地铁线路清单
                line_path = FilePath.raw_data_path() + city_menu[city_i]
                line_menu = JsonReader.file_name_reader(line_path)
                
                #存储geojson文件的临时容器,换城市自动清空
                tem_line_features=[]
                tem_line_features_collect = []
                tem_point_features=[]
                tem_point_features_collect= []
                
                # 如果城市文件夹下面没有数据则不再执行程序
                if len(line_menu)>0:
                    for line_i in range(len(line_menu)):
                        '''
                        获取原始json数据地址：
                        json数据根目录+城市名称+线路文件保存名称
                        实际地址组成如下，注意添加中间的分割和文件后缀：
                        json_root + city_menu[city_i] + line_menu[line_i]
                        '''
                        # 获取线路json数据地址
                        city_json_path = FilePath.raw_data_path()  + city_menu[city_i] + '/' + line_menu[line_i]
                        # 读取原始json数据
                        raw_data = JsonReader.file_reader(city_json_path)
                        
                        # 清洗geojson数据
                        GetData.geojson_line(raw_data, tem_line_features)
                        GetData.geojson_point(raw_data, tem_point_features)
                       
                # 保存线路信息         
                GeojsonLine = FilePath.path('geojson', 'line', 'gaode') + city_menu[city_i] +'.geojson'
                tem_line_features_collect =  FeatureCollection(tem_line_features)
                with open(GeojsonLine, 'w') as f1:
                    json.dump(tem_line_features_collect, f1)                
                
                # 保存站点信息
                GeojsonPoint = FilePath.path('geojson', 'point', 'gaode') + city_menu[city_i] +'.geojson'
                tem_point_features_collect =  FeatureCollection(tem_point_features)
                with open(GeojsonPoint, 'w') as f2:
                    json.dump(tem_point_features_collect, f2)                
            except:
                pass        
    except:
        print('问题出在MetroGaode函数')

# 清洗得到目标坐标系的地铁站点数据
def MetroTransPoint(reproject):
    try:
        city_point_menu = JsonReader.file_name_reader(FilePath.path('geojson','point','gaode'))
        #print(city_point_menu)
        for city_i in range(len(city_point_menu)):
            DataPath = FilePath.path('geojson','point','gaode') + city_point_menu[city_i]
            tem_data = geopandas.read_file(DataPath)
            tem_data_geometry = tem_data.geometry
            #print(tem_data_geometry)
            #创建用于存放GeoSeries中坐标点的空列表
            geometry_list = []
            record_list=[]
            
            #依次把各个站点的坐标点进行转换
            #属性信息直接继承之前数据的
            for point_i in range(len(tem_data_geometry)):
                if reproject == 'wgs84':
                    point_cor = CoorTrans.gcj02_to_wgs84(tem_data_geometry[point_i].x, 
                                                         tem_data_geometry[point_i].y)
                    geometry_list.append(geometry.Point(point_cor[0],point_cor[1]))
                elif reproject == 'baidu':
                    point_cor = CoorTrans.gcj02_to_wgs84(tem_data_geometry[point_i].x, 
                                                         tem_data_geometry[point_i].y)
                    geometry_list.append(geometry.Point(point_cor[0],point_cor[1]))
                else:
                    print('确认MetroTransPoint坐标系名称是否正确')
                
                # 直接沿用原来数据的属性信息
                station_num = tem_data.station_num[point_i]
                line_name = tem_data.line_name[point_i]
                station_name= tem_data.station_name[point_i]
                status = tem_data.status[point_i]
                
                # 集合形成属性列表
                tem_list = (station_num,line_name,station_name,status)
                record_list.append(tem_list)
            
            geojson_file = geopandas.GeoDataFrame(data=record_list,
                                                  geometry=geometry_list,
                                                  columns=['station_num','line_name',
                                                               'station_name','status'])
            if reproject == 'wgs84':
                tem_point_path = FilePath.path('geojson', 'point', 'wgs84') + city_point_menu[city_i]
            elif reproject == 'baidu':
                tem_point_path = FilePath.path('geojson', 'point', 'baidu') + city_point_menu[city_i]
            else:
                print('确认坐标系名称是否正确')
                  
            geojson_file.to_file(tem_point_path, driver='GeoJSON', encoding = 'utf8')  
    except:
        print('问题出在MetroTransPoint函数')

# 清洗得到目标坐标系的地铁线路数据
def MetroTransLine(reproject):
    try:
        city_line_menu = JsonReader.file_name_reader(FilePath.path('geojson','line','gaode'))
        #print(city_line_menu)
        for city_i in range(len(city_line_menu)):
            try:
                DataPath = FilePath.path('geojson','line','gaode') + city_line_menu[city_i]
                #print(DataPath)
                tem_data = geopandas.read_file(DataPath)
                tem_data_geometry = tem_data.geometry
                
                # 创建用于存放GeoSeries中坐标点的空列表
                geometry_list = []
                record_list =[]
                
                # 依次把各条线路各个的坐标点进行转换
                # 属性信息直接继承之前数据的
                for line_i in range(len(tem_data_geometry)):
                    #用于临时存储线路关键点坐标的列表
                    line_list = []
                    #此处获取了每条线路的各个关键点坐标数据，格式为[(lng1,lon1),(lng2,lon2),(lng3,lon3),...]
                    tem_cor_list = list(tem_data_geometry[line_i].coords)
                    
                    #这里开始循环变换每个坐标点数据
                    for line_point_i in range(len(tem_cor_list)):
                        if reproject == 'wgs84':
                            line_point  = CoorTrans.gcj02_to_wgs84(tem_cor_list[line_point_i][0],
                                                                   tem_cor_list[line_point_i][1])
                            line_list.append(line_point)
                        elif reproject == 'baidu':
                            line_point  = CoorTrans.gcj02_to_bd09(tem_cor_list[line_point_i][0],
                                                                   tem_cor_list[line_point_i][1])
                            line_list.append(line_point)
                        else:
                            print('确认MetroTransLine循环坐标点是否正确')
                            
                    geometry_list.append(geometry.LineString(line_list))
                    
                    #沿用属性信息
                    key_name = tem_data.key_name[line_i]
                    line_name = tem_data.line_name[line_i]
                    front_name = tem_data.front_name[line_i]
                    terminal_name = tem_data.terminal_name[line_i]
                    status = tem_data.status[line_i]
                    start_time = tem_data.start_time[line_i]
                    end_time = tem_data.end_time[line_i]
                    company = tem_data.company[line_i]
                    
                    tem_list= (key_name,line_name,front_name,terminal_name,status,start_time,end_time,company)
                    record_list.append(tem_list)
                    
                geojson_file = geopandas.GeoDataFrame(data = record_list,
                                                      geometry=geometry_list,
                                                      columns = ['keyname', 'line_name',
                                                              'front_name','terminal_name',
                                                              'status','start_time','end_time','company'])
                # print(geojson_file)
                if reproject == 'wgs84':
                    tem_line_path = FilePath.path('geojson', 'line', 'wgs84') + city_line_menu[city_i]
                    # print(tem_line_path)
                    
                elif reproject == 'baidu':
                    tem_line_path = FilePath.path('geojson', 'line', 'baidu') + city_line_menu[city_i]
                else:
                    print('确认MetroTransLine坐标系名称是否正确')
                geojson_file.to_file(tem_line_path, driver='GeoJSON', encoding='utf8')
            except:
                pass
    except:
        print('问题出在MetroTransLine函数')

# 根据文件类型和坐标类型需求转换数据
def TransFile(cor_type,file_type,geo_type):
    try:
        city_menu = JsonReader.file_name_reader(FilePath.path('geojson',geo_type,cor_type))
        # print(city_menu)
        for city_i in range(len(city_menu)):
            raw_path = FilePath.path('geojson',geo_type,cor_type) + city_menu[city_i]
            # print(raw_path)
            tem_data = geopandas.read_file(raw_path)
            # print(tem_data)
            data_path = FilePath.path(file_type,geo_type,cor_type) + city_menu[city_i].split('.')[0]
            #print(data_path)
            if file_type == 'shp':                
                tem_data.to_file(data_path, driver='ESRI Shapefile',encoding='utf-8')
            
            else:
                print('确认TransFile坐标系')
    except:
        print('文件转化失败')

# 整合汇总数据清洗参数
def MetroData(file_type,geo_type,reproject):
    try:
        MetroGaode()
        if file_type == 'geojson':
            if reproject == 'gaode':
                pass
            elif reproject == 'baidu':
                MetroTransPoint('baidu')
                MetroTransLine('baidu')
            else:
                MetroTransPoint('wgs84')
                MetroTransLine('wgs84')            
        else:
            TransFile(reproject, file_type, geo_type)
    except:
        pass