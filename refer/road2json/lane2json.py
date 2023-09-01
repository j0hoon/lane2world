# '''
# 2023 8월 29일 오픈플랫폼 데이터 전달용코드로 생성중임
# 아주대 CN7 데이터에 기존에 생성되어 있는 json 파일을 읽어서 numInitLane 과 numMaxLane 을 채워주는 코드임
# '''

# import importlib

# def install_pip_module(module_name = ""):
#     '''
#     python 모듈을 설치하는 함수 입니다. \n\n
#     새로운 환경에서 python 코드를 실행하더라도 환경설정이 자동으로 되도록 하기 위해 사용합니다.  
#     일반적으로 코드 실행 시 import 되는 모듈을 선언하기 전에 실행하는것이 좋습니다.  
    
#     다른 코드에서 실행하고 싶은 경우   
#     "from install_pip_module import install_pip_module" 을 선언한 후 사용하시기 바랍니다.   
    
#     [input]/[output]  
#     [input] : module_name(str)  
#     [output] : 입력에 있는 모듈이 설치되어 있지 않으면 설치하고, 설치되어 있으면 이미 설치되어 있다는 메시지를 출력합니다.  
    
#     [example]  
#     [example 1] : install_pip_module("numpy")  
#     [output 1] : numpy 모듈이 이미 설치되어 있습니다.  
    
#     [example 2] : install_pip_module("pymongo")   
#     [output 2] : pymongo 모듈이 설치되어 있지 않습니다. 설치를 진행합니다...    
    
#     [주의사항]   
#     주의할 사항으로는 입력하는 모듈의 이름은 pip에서 사용하는 이름과 동일해야 합니다.    
#     또한 모듈 이름만 입력해야 합니다.    
    
#     예를 들어, pymongo를 설치하고 싶으면 pymongo를 입력해야 합니다.     
    
#     pip 모듈의 경우 실제로 설치되는 모듈의 이름과 다르게 사용되는 경우가 있습니다.    
#     이런 부분을 주의하여 설치하시기 바랍니다.    
    
#     [version]    
#     v0.0.1 2023.05.10 JYH    
#     코드 생성 및 주석 추가    
#     '''
#     try:
#         importlib.import_module(module_name)
#         print(f"{module_name} 모듈이 이미 설치되어 있습니다.")
#     except ImportError:
#         print(f"{module_name} 모듈이 설치되어 있지 않습니다. 설치를 진행합니다...")
#         try:
#             import pip
#             pip.main(['install', module_name])
#             print(f"{module_name} 모듈이 설치되었습니다.")
#         except Exception as e:
#             print(f"{module_name} 모듈 설치 중 오류가 발생했습니다:", str(e))

# # modules = ["numpy", "pandas", "matplotlib", "seaborn","pymongo","os","matplotlib","datetime","bson","dataframe-image"]
# # # 모듈 설치
# # for module in modules:
# #     install_pip_module(module)

import numpy as np
import pandas as pd
import json
import os

def load_json(path):
    
    return json.load(open(path, 'r', encoding='utf-8'))

def filtered_json(origin_json):
    
    filtered_json = []
    
    
    
    return filtered_json

# def to_json(CSS, directory = os.getcwd()):
#     '''
#     save json file 
#     input : CSS, directory
#     directory : default = os.getcwd()
    
#     example : to_json(CSS, r"C:\Users\Administrator\OneDrive - Ajou University\바탕 화면\정영훈 전달\CN7_030323_069_Lidar.mat")
    
#     '''
    
#     with open(directory + r"\CSS.json", 'w') as outfile:
#         json.dump(CSS, outfile,indent='\t')

def main():
    origin_json = load_json(r'D:\OneDrive - Ajou University\1_CODE\5_COMMON_SCENARIO_SCHEMA\1_FOT\1_CN7\1_road2json\test.json')
    new_json = []
    for idx, tmp_css in enumerate(origin_json):
        tnj = {
            "directory": {
                "raw": ""
            },
            "date":"",
            "dataType": "",
            "travelTime": 0,
            "travelDistance": 0,
            "fileSize": 0,
            "georeference": {
                "type": "Point",
                "coordinates": [
                    0,
                    0
                ]
            },
            "sampleTime": "0.05",
            "scenery": {
                "roadName": "",
                "event": [
                ],
                "laneWidthMax": "",
                "laneWidthMin": "",
                "curvatureMax": "",
                "curvatureMin": "",
                "numInitLane": "",
                "numMaxLane": ""
            },
            "environment": {
                "illumination": "",
                "weather": ""
            },
            "dynamic":{
                "init":[],
                "story":[]
            }
            } # tmp new json
        tnj['directory']['raw'] = tmp_css['directory']['raw']
        tnj['date'] = tmp_css['date']
        tnj['dataType'] = tmp_css['dataType']
        tnj['travelTime'] = tmp_css['travelTime']
        tnj['travelDistance'] = tmp_css['travelDistance']
        tnj['fileSize'] = tmp_css['fileSize']
        tnj['georeference']['type'] = tmp_css['georeference']['type']
        tnj['georeference']['coordinates'] = tmp_css['georeference']['coordinates']
        tnj['sampleTime'] = tmp_css['sampleTime']
        tnj['scenery']['roadName'] = tmp_css['scenery']['roadName']
        tnj['scenery']['event'] = tmp_css['scenery']['event']
        tnj['scenery']['laneWidthMax'] = tmp_css['scenery']['laneWidthMax']
        tnj['scenery']['laneWidthMin'] = tmp_css['scenery']['laneWidthMin']
        tnj['scenery']['curvatureMax'] = tmp_css['scenery']['curvatureMax']
        tnj['scenery']['curvatureMin'] = tmp_css['scenery']['curvatureMin']
        tnj['scenery']['numInitLane'] = tmp_css['scenery']['numInitLane']
        tnj['scenery']['numMaxLane'] = tmp_css['scenery']['numMaxLane']
        tnj['environment']['illumination'] = tmp_css['environment']['illumination']
        tnj['environment']['weather'] = tmp_css['environment']['weather']
        tnj['dynamic']['init'] = tmp_css['dynamic']['init']
        tnj['dynamic']['story'] = tmp_css['dynamic']['story']
        new_json.append(tnj)

    with open(os.getcwd() + r"\result_CSS.json", 'w') as outfile:
        json.dump(new_json, outfile,indent='\t')
    
    # for tmp_css in origin_json:
        
    #     numMaxLane = tmp_css['scnery']['numMaxLane']

    
    # to_json(CSS = origin_json)
    print("HIA")




if __name__ == '__main__':
    os.system('cls' if os.name == 'nt' else 'clear')
    
    main()