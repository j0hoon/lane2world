import os 
import json
import os
import numpy as np
import matplotlib.patches as patches
import cv2
import math
from tqdm import tqdm
from natsort import natsorted

# [Cv2 color 설정]
Color_dict = {'Red'   : (0, 0, 255),
              'Red2'  : (0, 0, 170),
              'Green' : (0, 255, 0),
              'White' : (255, 255, 255),
              'Black' : (0, 0, 0),
              'BBOX'  : (255, 102, 51 )}

def load_json_file(json_file):
    with open(json_file) as f:
        data = json.load(f)
    return data

def get_all_file_paths(directory):
    file_paths = []
    
    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            file_paths.append(file_path)
            
    return file_paths


def custom_get_all_file_paths(directory, file_type, option ):
    file_paths = []
    
    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            
            if option in file_path:
                if file_type in file_path:
                    file_paths.append(file_path)
            
    return file_paths


def draw_bbox_on_image(image, object):
    
    x1, y1, x2, y2 = object['bbox']
    cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
    center = (int((x1+x2)/2), int((y1+y2)/2))
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 1
    font_color = Color_dict['Red']
    font_thickness = 2
    cv2.putText(image, str(center), center, font, font_scale, font_color, font_thickness)    

def vehicle_visualize(image, label):
    
    for object in label['annotations']:
        if object['class'] == "vehicle":
            draw_bbox_on_image(image, object)
            
    


    

if __name__ == "__main__":
    
    os.system('cls' if os.name == 'nt' else 'clear') 
    path_1 = r"H:\KATECH\MultiSensor_Prediction\2.Validation\raw"
    path_2 = r"H:\KATECH\MultiSensor_Prediction\2.Validation\tmplabel"
    flist_1 = natsorted(os.listdir(path_1))
    
    original_images = custom_get_all_file_paths(path_1, ".jpg", "image0")
    original_image_labels = custom_get_all_file_paths(path_2, ".json", "image0")
    
    for i in tqdm(range(len(original_images))):
        
        image_full_path = original_images[i]
        label_full_path = original_image_labels[i]
        
        # check if the image is in the label
        image_name = os.path.basename(image_full_path)
        label_name = os.path.basename(label_full_path)
        if image_name.split('.')[0] != label_name.split('.')[0]:
            raise ValueError("image and label are not matched")
        
        # load image
        image = cv2.imread(image_full_path)
        label = load_json_file(label_full_path)

        # vehicle_visualize
        vehicle_visualize(image, label)

        # save image 
        save_path = os.path.join(os.getcwd(),r'vision_bbox',image_full_path.split('\\')[-3])
        if os.path.isdir(save_path) == False:
            os.makedirs(save_path,exist_ok=True)        
        
        tmp_file_path = os.path.join(save_path, image_name)
        cv2.imwrite(tmp_file_path,image)
        
        # print("PAUSE")
    
    
    
    