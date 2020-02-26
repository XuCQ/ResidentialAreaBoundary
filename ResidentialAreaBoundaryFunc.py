# -*- coding:utf-8 -*-
# author:Changing Xu
# file:ResidentialAreaBoundary-ResidentialAreaBoundaryFunc
# datetime:2020/2/15 14:31
# software: PyCharm
import requests
from requests.adapters import HTTPAdapter
import json


def get_residential_uid(residential_name, region, bmap_key):
    bmap_localserach_url = f'http://api.map.baidu.com/place/v2/search?query={residential_name}&region={region}&output=json&city_limit=true&ak={bmap_key}'
    s = requests.Session()
    s.mount('http://', HTTPAdapter(max_retries=3))
    s.mount('https://', HTTPAdapter(max_retries=3))

    data = s.get(bmap_localserach_url, timeout=5, headers={"Connection": "close"})  # , proxies=proxies
    data = data.text
    data = json.loads(data)
    if data['status'] == 0 and len(data['results']) > 0:
        try:
            for info in data['results']:
                if '-' not in info['name']:
                    return info['uid']
            return None
        except Exception as e:
            print(f'Error\t{bmap_localserach_url}')
            return None
    else:
        return None


def get_boundary_by_uid(uid):
    '''
    根据uid获得边界
    :param uid: 百度地图 目标uid
    :return: None:无geo信息 else geos.join(;)
    '''
    bmap_boundary_url = f'http://map.baidu.com/?reqflag=pcmap&from=webmap&qt=ext&uid={uid}&ext_ver=new&l=18'

    s = requests.Session()
    s.mount('http://', HTTPAdapter(max_retries=3))  # mount:将一个连接适配器注册到一个前缀上
    s.mount('https://', HTTPAdapter(max_retries=3))  # HTTPAdapter:通过实现传输适配器接口，为 session 和 HTTP、 HTTPS连接提供了一个通用的接口

    data = s.get(url=bmap_boundary_url, timeout=5, headers={"Connection": "close"})
    data = data.text
    data = json.loads(data)
    content = data['content']
    # print(data)
    if not 'geo' in content:
        return None
    try:
        geo = content['geo']
        i = 0
        strsss = ''
        for jj in str(geo).split('|')[2].split('-')[1].split(','):
            jj = str(jj).strip(';')
            if i % 2 == 0:
                strsss = strsss + str(jj) + ','
            else:
                strsss = strsss + str(jj) + ';'
            i = i + 1
        return strsss.strip(";")
    except Exception as e:
        print(f'Error\t{bmap_boundary_url}')
        return None


def transform_coordinate_batch(coordinates, bmap_key):
    req_url = 'http://api.map.baidu.com/geoconv/v1/?coords=' + coordinates + '&from=6&to=5&ak=' + bmap_key

    s = requests.Session()
    s.mount('http://', HTTPAdapter(max_retries=3))
    s.mount('https://', HTTPAdapter(max_retries=3))

    data = s.get(req_url, timeout=5, headers={"Connection": "close"})  # , proxies=proxies
    data = data.text
    data = json.loads(data)
    coords = ''
    if data['status'] == 0:
        try:
            result = data['result']
            if len(result) > 0:
                for res in result:
                    lng = res['x']
                    lat = res['y']
                    coords = coords + ";" + str(lng) + "," + str(lat)
            return coords.strip(";")
        except Exception as e:
            print(f'Error\t{req_url}')
            return None
    else:
        return None


if __name__ == '__main__':
    # uid = get_residential_uid('新城香溢紫郡', '常州', 'wU3ZlXOKopbk78vjeZiSkDeo')
    # print(uid)
    coord_bd09mc_list = get_boundary_by_uid('e4155a695f912ed6d72ce263')
    print(coord_bd09mc_list)
    coord_bd09_list = transform_coordinate_batch(coord_bd09mc_list, 'wU3ZlXOKopbk78vjeZiSkDeo')
    print(coord_bd09_list)
