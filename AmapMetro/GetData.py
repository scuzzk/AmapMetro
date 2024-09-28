# -*- coding: utf-8 -*-
"""
Created on Sun Sep 22 17:13:13 2024

@author: scuzzk

"""

from geojson import Feature,Point, LineString

def geojson_line(busline_list,line_features):
    '''
    由于busline_list当中包含了双向的地铁线路以及不同分段的地铁数据，因此需要
    1.剔除重复线路的数据，
    2.选用busline_list列表中奇数序号的元素
    3.判断buslist下的type属性是否为2或11，2即是否为地铁数据，11就是城际线路
    4.判断status是1还是3，1就是在运营，3就是在建
    '''
    try:
        if (busline_list[0]['type'] == '2' or busline_list[0]['type'] == '11'):
            # 地铁名称带终点站，例如地铁1号线（西塱-广州东站）
            linename = busline_list[0]['name'].split("(")[0]
            # 这里说整体线路编号，例如地铁1号线
            key_line_name = busline_list[0]['key_name']
            company = busline_list[0]['company']
            front_name = busline_list[0]['front_name']
            terminal_name = busline_list[0]['terminal_name']
            end_time = busline_list[0]['end_time']
            start_time = busline_list[0]['start_time']
            # 这里需要组合经纬度坐标
            lons = busline_list[0]['xs'].split(",")
            lats = busline_list[0]['ys'].split(",")
            cor = []
            for cor_i in range(len(lons)):
                tem_cor = (float(lons[cor_i]), float(lats[cor_i]))
                cor.append(tem_cor)
                ## 这里判断地铁线路运营状态
            if (busline_list[0]['status'] == '1'):
                status = "运营中"
            else:
                status = "建设中"
            line_feature = Feature(geometry=LineString(tuple(cor)), properties={
                    "key_name":key_line_name,
                    "line_name": linename,
                    "front_name": front_name,
                    "terminal_name": terminal_name,
                    "status":status,
                    "start_time":start_time,
                    "end_time":end_time,
                    "company":company})
            line_features.append(line_feature)
        else:
            print("线路可能不是地铁或城际线路")
    except:
        print("geojson_line线路获取错误")
        
def geojson_point(busline_list,subwaypointFeatures):
        '''
        由于busline_list当中包含了双向的地铁线路以及不同分段的地铁数据，因此需要
        1.剔除重复线路的数据，
        2.选用busline_list列表中奇数序号的元素
        3.剔除type不为2的元素
        4.判断status是1还是3，1就是在运营，3就是在建
        '''
        try:
            # 判断buslist下的type属性是否为2或11，2即是否为地铁数据，11就是城际线路
            if (busline_list[0]['type'] == '2' or busline_list[0]['type'] == '11'):
                line_name = busline_list[0]['name']

                # 这里循环提取站点坐标
                for station_id in range(len(busline_list[0]['stations'])):
                    try:
                        station_name = busline_list[0]['stations'][station_id]['name']
                        station_num = busline_list[0]['stations'][station_id]['station_num']
                        station_cor_raw = busline_list[0]['stations'][station_id]['xy_coords'].split(
                            ";")
                        station_lon = float(station_cor_raw[0])
                        station_lat = float(station_cor_raw[1])
                        station_cor = (station_lon, station_lat)
                        ## 这里判断地铁线路运营状态
                        if (busline_list[0]['status'] == '1'):
                            status = '运营中'
                        else:
                            status = '建设中'
                        station_feature = Feature(geometry=Point(tuple(station_cor)), properties={
                            "station_num": station_num,
                            "line_name": line_name,
                            "station_name": station_name,
                            "status":status
                        })

                        subwaypointFeatures.append(station_feature)
                    except:
                        print("站点提取出错")
            else:
                print("线路可能不是地铁或城际线路")
        except:
            print("geojson_point站点获取错误")