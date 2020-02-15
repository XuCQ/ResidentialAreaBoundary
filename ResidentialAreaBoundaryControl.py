# -*- coding:utf-8 -*-
# author:Changing Xu
# file:ResidentialAreaBoundary-ResidentialAreaBoundaryControl
# datetime:2020/2/15 12:16
# software: PyCharm
import os
from random import choice
from Auxiliary.crawelFunc import loadCSV, save_info
from ResidentialAreaBoundaryFunc import *

bd_ak = ['your keys']


def crawel_residential_area_boundary(orgin_csv_path, output_path):
    judge = True
    orgin_df = loadCSV(orgin_csv_path)
    output_path=os.path.join(output_path,f"{os.path.basename(orgin_csv_path).split('.')[0]}_boundary.csv")
    for index, residential_info in orgin_df.iterrows():
        residential_name = residential_info[0]
        residential_region = f'江苏省常州市{residential_info[1]}'
        residential_uid = get_residential_uid(residential_name, residential_region, choice(bd_ak))
        if residential_uid != None:
            coord_bd09mc_list = get_boundary_by_uid(residential_uid)
            if coord_bd09mc_list != None:
                coord_bd09_list = transform_coordinate_batch(coord_bd09mc_list, choice(bd_ak))
                if coord_bd09_list != None:
                    for idx, coord in enumerate(coord_bd09_list.split(';')):
                        save_info({'residential_name': residential_name,
                                   'residential_region': residential_region,
                                   'coord_x': coord.split(',')[0],
                                   'coord_y': coord.split(',')[1],
                                   'point_id': idx
                                   }, output_path, judge)
                        if judge:
                            judge = False
                    print(f'{residential_name}  Area Boundary Save Success\t {index}/{orgin_df.shape[0]}')


if __name__ == '__main__':
    crawel_residential_area_boundary('data/czfjsj.csv','data')
