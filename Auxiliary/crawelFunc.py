# -*- coding:utf-8 -*-
# author:Changing Xu
# file:WuhanCoronavirusDataCrawel-crawelFunc
# datetime:2020/1/27 17:17
# software: PyCharm
# 爬虫辅助func

import os
import csv
import json
import codecs
import pandas as pd
import time
import datetime
import random


# 判断网络连接状况
def judgeNetwork():
    try:
        os.popen("ping www.baidu.com -n 1").read()
        return True
    except(Exception):
        print('网络连接失败')
        return False


# pandas 读取csv
def loadCSV(path, header=0):
    return pd.read_csv(path, header=header, sep=',', encoding='gbk')


# 生成日期列表
def createAssistDate(datestart=None, dateend=None):
    # 创建日期辅助表
    if datestart is None:
        datestart = '20200101'
    if dateend is None:
        dateend = datetime.datetime.now().strftime('%Y%m%d')
    # 转为日期格式
    datestart = datetime.datetime.strptime(datestart, '%Y%m%d')
    dateend = datetime.datetime.strptime(dateend, '%Y%m%d')
    date_list = []
    date_list.append(datestart.strftime('%Y%m%d'))
    while datestart < dateend:
        # 日期叠加一天
        datestart += datetime.timedelta(days=+1)
        # 日期转字符串存入列表
        date_list.append(datestart.strftime('%Y%m%d'))
    return date_list


# 随机生成指定位数
def getRandomNum(Length):
    return '1'+''.join(str(random.sample(range(0,9),1)[0]) for _ in range(Length-1))


# 时间戳转换
def timestampToLocaltime(timestamp):
    time_local = time.localtime(int(str(timestamp)[:10]))
    return time.strftime("%Y-%m-%d %H:%M:%S", time_local)


def save_info(results, csvPath, judge):
    try:
        dataframe = pd.DataFrame(results, index=[judge])
        if (judge):
            dataframe.to_csv(csvPath, sep=',', encoding="utf_8_sig", mode='w', index=0, columns=list(results.keys()))
        else:
            dataframe.to_csv(csvPath, sep=',', encoding="utf_8_sig", mode='a', header=0, index=0, columns=list(results.keys()))

    except Exception as e:
        print(e)


def infoTemplate():
    infoTitle = ['adoptType', 'createTime', 'dataInfoOperator', 'dataInfoState', 'dataInfoTime', 'entryWay', 'id', 'infoSource', 'infoType', 'modifyTime',
                 'provinceId', 'provinceName', 'pubDate', 'pubDateStr', 'sourceUrl', 'summary', 'title']
    return dict(zip(infoTitle, ['' for _ in infoTitle]))


def jsonToCsv(path):
    filePath, fileName = os.path.split(path)
    csvPath = os.path.join(os.path.dirname(filePath), 'csv', os.path.splitext(fileName)[0] + '.csv')
    flag = True
    infoTitle = ['adoptType', 'createTime', 'dataInfoOperator', 'dataInfoState', 'dataInfoTime', 'entryWay', 'id', 'infoSource', 'infoType', 'modifyTime',
                 'provinceId', 'provinceName', 'pubDate', 'pubDateStr', 'sourceUrl', 'summary', 'title']
    with open(path, 'r', encoding='utf-8') as jsonData_f:
        jsonData = json.load(jsonData_f)
        for info in jsonData['data']:
            dictKeys = list(info.keys())
            infoTitle_tmp = infoTitle.copy()
            for titleName in infoTitle:
                if titleName in dictKeys:
                    infoTitle_tmp.remove(titleName)
                    dictKeys.remove(titleName)
            for titleName in infoTitle_tmp: info[titleName] = 'null'
            for titleName in dictKeys: del info[titleName]
            if info['createTime']: info['createLocalTime'] = timestampToLocaltime(info['createTime'])
            if info['dataInfoTime']: info['dataInfocLocalTime'] = timestampToLocaltime(info['dataInfoTime'])
            save_info(info, csvPath, flag)
            if flag: flag = False
        jsonData_f.close()
    print(f'{path} >>> {csvPath} convert complete')

