import json
import pandas as pd
import numpy as np
import scipy.io 
import glob
import os
from tqdm import tqdm
# SELECT MODE
from datetime import datetime 
import copy
from css_frame import *
from natsort import natsorted
def make_CSS(directory,tmp_lane_num,json_save_path,index):
    '''
    css 를 만들기 위한 함수
    
    input : directory 
    여기서 directory 는 raw data 가 있는 폴더를 의미함.
    파일 자체의 경로가 아님.
    디렉토리 구조는 아래와 같음
    - raw
        - data_name
            - data_number
                - image
                - lidar
    자세한 구조는 
    
    output : CSS.json file
    
    example : make_CSS(r"D:\Data\OP_SAMPLE\raw\multi_sensor_detection\1_1_7_20210906_010")
    '''

    
    tmp_CSS = copy.deepcopy(CSS)
    
    put_admin_KADAP(tmp_CSS, directory)
    
    put_scenery(tmp_CSS, tmp_lane_num)
    
    to_json(tmp_CSS, json_save_path,num = index)
    
    # print("make_CSS")    

def put_admin(_CSS, _directory ):
    # directory
    _CSS["directory"]['raw'] = _directory

    image_directory = _directory + r"\image"
    first_image_path = glob.glob(image_directory + r"\*.jpg")[0]
    
    # date
    _CSS["date"] = str(get_file_creation_date(first_image_path)).split(".")[0]
    
    # dataType
    _CSS["dataType"] = _directory.split("\\")[-1]

    # sameple time
    _CSS["sampleTime"] = "0.1"
    
    # travel Time 
    # sample time 이 있는 경우에만 계산 가능함.
    if _CSS["sampleTime"] == None:
        print("sampleTime is 0")
        travel_time = 0
    else:        
        file_num = len(glob.glob(image_directory + r"\*.jpg"))
        travel_time = file_num * float(_CSS["sampleTime"])
    _CSS["travelTime"] = str(travel_time)

def put_admin_KADAP(_CSS, _directory ):
    # directory
    _CSS["directory"]['raw'] = _directory

    image_directory = _directory + r"\CAM_FRONT"
    first_image_path = glob.glob(image_directory + r"\*.jpg")[0]
    
    # date
    _CSS["date"] = str(get_file_creation_date(first_image_path)).split(".")[0]
    
    # dataType
    _CSS["dataType"] = "KADAP"

    # sameple time
    _CSS["sampleTime"] = "0.2"
    
    # travel Time 
    # sample time 이 있는 경우에만 계산 가능함.
    if _CSS["sampleTime"] == None:
        print("sampleTime is 0")
        travel_time = 0
    else:        
        file_num = len(glob.glob(image_directory + r"\*.jpg"))
        travel_time = file_num * float(_CSS["sampleTime"])/3600
    _CSS["travelTime"] = str(travel_time)
    
def put_scenery(_CSS, tmp_lane_num):
    """
    scenery 에 대한 정보를 입력하는 함수
    input : CSS, directory
    output : CSS 의 scenery 부분에 정보가 입력됨.
    
    vision only 데이터의 경우 numMaxLane 정보만 채워질 수 있음.
    
    """
    
    # lane_num_csv_path = _directory + r"\registration\registration.csv"
    # lane_num_csv_path = r"J:\\KADaP_lane_data_lane.csv"

    # df = pd.read_csv(lane_num_csv_path)
    
    # _CSS["scenery"]["numOfLane"] = [str(df["lanenumber"].min()), str(df["lanenumber"].max())]
    _CSS["scenery"]["numOfLane"] = str(tmp_lane_num)
    
    
def get_file_creation_date(file_path):
    '''
    # 파일의 경로를 입력해주면 그 파일이 생성된 날짜를 반환해주는 함수
    
    # input : file_path
    # output : creation_date ex(2021-09-06 10:00:00)
    
    '''
    if os.path.exists(file_path):
        timestamp = os.path.getctime(file_path)
        creation_date = datetime.fromtimestamp(timestamp)
        return creation_date
    else:
        return None    

def to_json(_CSS, _directory = os.getcwd(),num = 0):
    '''
    save json file 
    input : CSS, directory
    directory : default = os.getcwd()
    '''
    
    with open(_directory + r"\CSS_"+str(num).zfill(5)+".json", 'w') as outfile:
        json.dump(_CSS, outfile,indent='\t')


if __name__ == "__main__":
    os.system('cls' if os.name == 'nt' else 'clear')
    
#     # test = get_file_creation_date(r"C:\Users\Administrator\OneDrive - Ajou University\바탕 화면\정영훈 전달\CN7_030323_069_Lidar.mat")
#     # print(str(test).split(".")[0])
    
#     # dir_list = [r"J:\OP_SAMPLE_2\raw\차선_횡단보도_인지_영상_수도권"]
    
    lane_result_csv = pd.read_csv(r'J:\KADaP_lane_data_lane.csv')
    root = r'J:\OP_SAMPLE_2\raw\차선_횡단보도_인지_영상_수도권'
    lane_dir_list = natsorted(os.listdir(root))
    json_save_path = r'J:\json_save_path'
    for index, row in lane_result_csv.iterrows():
        # old_tmp_path = row['filename']
        
        new_tmp_path = os.path.join(root, lane_dir_list[index])
        tmp_lane_num = row['max_lane_num']
        make_CSS(new_tmp_path,tmp_lane_num,json_save_path,index)
        
        
    
    
#     # for directory in dir_list:
        
    print("DONE")