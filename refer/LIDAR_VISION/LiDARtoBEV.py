import os 
import json
import os
import numpy as np
import matplotlib.patches as patches
import cv2
import math
from tqdm import tqdm
from natsort import natsorted

W2PIXEL = 10

# [Cv2 color 설정]
Color_dict = {'Red'   : (0, 0, 255),
              'Red2'  : (0, 0, 170),
              'Green' : (0, 255, 0),
              'White' : (255, 255, 255),
              'Black' : (0, 0, 0),
              'BBOX'  : (255, 102, 51 )}

def read_lidar_label_file_list(lidar_label_file_list):
    file_list = []
    for file in os.listdir(lidar_label_file_list):
        if file.endswith(".txt"):
            file_list.append(file)
    return file_list

def load_json_file(json_file):
    with open(json_file) as f:
        data = json.load(f)
    return data

def get_rectangle_point(_width = 2, _length = 4, _center = [100,100], _heading = 0):

    center_x = _center[0]
    center_y = _center[1]
    
    point1 = (center_x - _width/2 , center_y + _length/2)
    point2 = (center_x + _width/2 , center_y + _length/2)
    point3 = (center_x + _width/2 , center_y - _length/2)
    point4 = (center_x - _width/2 , center_y - _length/2)

    point1 = rotate_rectangle(_center, point1 , _heading)
    point2 = rotate_rectangle(_center, point2 , _heading)
    point3 = rotate_rectangle(_center, point3 , _heading)
    point4 = rotate_rectangle(_center, point4 , _heading)    
    
    return [point1, point2, point3, point4]

def rotate_rectangle(cpt,pt,deg):
    x = pt[0]
    y = pt[1]
    cx = cpt[0]
    cy = cpt[1]
    
    rad = deg*math.pi/180.0
    dx = (x - cx)*math.cos(rad) - (y - cy)*math.sin(rad) + cx
    dy = (x - cx)*math.sin(rad) + (y - cy)*math.cos(rad) + cy
    return [dx,dy]        


def draw_rectangle(ax, cpt, hd_angle,_edge_color = "red",_ls = 'solid',_lw = 1 ,_linewidth =0.5):
    
    _points = get_rectangle_point(_center = cpt,_heading = hd_angle)
    ax.add_patch(
        patches.Polygon(
            _points,
            fill = None,
            edgecolor = _edge_color,
            ls = _ls,
            lw = _lw,
            linewidth = _linewidth))




def main(json_dir, savepath = os.getcwd()):
    
    json_list = os.listdir(json_dir)
    
    for tmp_json_name in json_list:
        
        # draw ego vehicle in BEV
        image = 255 * np.ones((800, 300, 3), dtype=np.uint8)
        # 검은색 네모 그리기
        center = (150, 500)
        size = (19, 50)
        top_left = (center[0] - size[0]//2, center[1] - size[1]//2)
        bottom_right = (center[0] + size[0]//2, center[1] + size[1]//2)        
        cv2.rectangle(image, top_left, bottom_right, 0, thickness=-1)
        
        # load json file
        tmp_json_file = os.path.join(json_dir,tmp_json_name)
        data = load_json_file(tmp_json_file)    
        
        # cv2.imshow("temp",image)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()
        
        for tmp_object in data['annotations']:
            
            # get object information
            tmp_dimension = tmp_object['attribute']['dimension']
            tmp_location = tmp_object['attribute']['location']
            tmp_yaw = tmp_object['attribute']['yaw']
            tmp_track_id = tmp_object['attribute']['track_id']
            tmp_class = tmp_object['class']
            
            x = tmp_location[0]*W2PIXEL
            y = tmp_location[1]*W2PIXEL
            
            x = 150 - x
            y = 500 + y
            
            width = tmp_dimension[0]*W2PIXEL
            length = tmp_dimension[2]*W2PIXEL
            
            
            # draw object in BEV
            object = get_rectangle_point(_width = width, _length = length, _center = [x,y], _heading = tmp_yaw)
            object = np.array(object,np.int32)
            cv2.polylines(image, [object], True, Color_dict['BBOX'],thickness=2)
            font = cv2.FONT_HERSHEY_SIMPLEX
            font_scale = 1
            font_color = Color_dict['Red']
            font_thickness = 2
            # cv2.putText(image, str(tmp_track_id) + ":(" +str(int(x/10)) + ","+str(int(y/10))+")" , (int(x), int(y)), font, font_scale, font_color, font_thickness)
            cv2.putText(image, str(tmp_track_id), (int(x), int(y)), font, font_scale, font_color, font_thickness)
            # cv2.putText(image, str(tmp_track_id) + ":(" +str(-int(tmp_location[0])) + ","+str(-int(tmp_location[1]))+")" , (int(x), int(y)), font, font_scale, font_color, font_thickness)
            # cv2.putText(image, str(tmp_track_id), (int(tmp_location[0]), int(tmp_location[1])), font, font_scale, font_color, font_thickness)
            
        tmp_file_path = os.path.join(savepath, tmp_json_name.split('.json')[0] +".jpg")
        cv2.imwrite(tmp_file_path,image)
        # cv2.imshow('Rectangle', image)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()
        
        # print("PAUSE")
        
        
        
    
    
    # get center point
    
    
    
    # draw rectangle
    

if __name__ == "__main__":
    os.system('cls' if os.name == 'nt' else 'clear') 
    os.system("python3 LiDARtoBEV.py")   
    # test_json_path = r"F:\융합센서객체추적\label\lidar\2_005_000.json"
    
    path_1 = r'H:\KATECH\178.융합센서 다중객체 추적 및 예측 데이터\2.Validation\라벨링데이터'
    flist_1 = natsorted(os.listdir(path_1))

    
    for tmp_fname_1 in tqdm(flist_1):
        path_2 = os.path.join(path_1,tmp_fname_1)
        flist_2 = os.listdir(path_2)
        for tmp_fname_2 in flist_2:
            path_3 = os.path.join(path_2, tmp_fname_2)
            path_3 = path_3 + r"\lidar"
            save_path = os.path.join(os.getcwd(),r'lidar_bev',path_3.split('\\')[-2])
            # save_path = path_3.replace("lidar","lidar_bev")
            if os.path.isdir(save_path) == False:
                os.makedirs(save_path,exist_ok=True)
            main(path_3,savepath=save_path)            
            
    
    
    
    # test_json_path = r"H:\KATECH\178.융합센서 다중객체 추적 및 예측 데이터\2.Validation\라벨링데이터\1_도심_국도 (60 kph 이하)_val\009\lidar"
    # save_path = r"F:\tmp\001"
    # main(test_json_path,savepath=save_path)
    

    
