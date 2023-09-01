import numpy as np
import math
import os
from natsort import natsorted
import matplotlib.pyplot as plt
from tqdm import tqdm




def txt2array(txt_path):
    '''
    텍스트 파일의 경로를 입력해주면 텍스트 파일을 읽어와서 array로 반환해주는 함수
    '''
    
    with open(txt_path, 'r', encoding='utf-8') as f:  #텍스트 파일을 읽어옴
        lines = f.readlines() #텍스트 파일을 한 줄씩 읽어와서
        lines = [line.strip() for line in lines] #줄마다 strip()을 해줌
        lines = [line.split() for line in lines] #줄마다 split()을 해줌
        lines = np.array(lines).astype(np.float32) #numpy array로 변환, float32 타입으로 변환
    
    return lines

def get_specific_type_file_list(directory,filetype = ".jpg"):
    '''
    - 선정한 파일 타입의 파일들만 리스트로 반환해주는 함수
    - 이름순으로 정렬해줌
    - 파일타입을 입력하지 않는경우 jpg 파일을 반환해줌
    '''
    
    files = []
    for filename in os.listdir(directory):
        if filename.endswith(filetype):
            files.append(filename)
    files = natsorted(files)
            
    return files

def read_text_file(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()  # 파일의 모든 줄 읽기
        data = [line.strip().split(',') for line in lines]  # 각 줄을 구분자(,)로 분리하여 배열 생성
        data = np.array(data).astype(np.int32) #numpy array로 변환, int32 타입으로 변환
    return data

def get_P_BLB(tmp_lane,calib_cam,calib_cam2Lidar):
    '''
    P_BLP를 구해주는 함수
    
    tmp_lane = [x,y] pixel 좌표
    calib_cam = 카메라 캘리브레이션 행렬
    calib_cam2Lidar = 카메라에서 리더까지의 변환 행렬
    
    이 부분만 잘 튜닝하면 될듯 함..
    '''
    
    K = calib_cam
    R = calib_cam2Lidar[:][:,0:3]
    t = calib_cam2Lidar[:][:,3]
    t = [[t[0]],[t[1]],[t[2]]]
    ### intrinsics(fixel) ###
    fx = K[0][0]; fy = K[1][1]
    u0 = K[0][2]; v0 = K[1][2]
    
    Pc_lane = np.array([[1, -(tmp_lane[0] - u0)/fx, -(tmp_lane[1] - v0)/fy]]).reshape(3,1)

    Pw_lane = R.T@(Pc_lane - t)

    Cc = np.array([0,0,0]).reshape(3,1)
    Cw = R.T@(Cc - t)

    k_BLB = -Cw[2]/(Pw_lane[2]-Cw[2])

    P_BLB = (Cw+k_BLB*(Pw_lane-Cw)).T
    
    return P_BLB

def get_wline(tmp_txt_files, wline):
    for txt_file in tmp_txt_files:
        line = read_text_file(os.path.join(image_result_path, txt_file))
        
        for tmp_line in line :
            P_PLB = get_P_BLB(tmp_line,calib_cam,calib_cam2Lidar)
            # wline.append(P_PLB[0][:2])
            wline = np.vstack((wline,P_PLB[0][:2])) if (len(wline)==0)==False else P_PLB[0][:2]                            
            # wline = np.vstack((wline,P_PLB[0][:2])) if wline != [] else P_PLB[0][:2]                            
    return wline

if __name__ == "__main__":
    os.system('cls')
    '''
    파일 경로 잡아주는 부분
    이 부분만 잘 잡아주면됨
    자기 경로에서 raw 디렉토리로 잡아주면알아서 다 잡아줌
    '''
    total_path = r"I:\KADaP\MultiSensor_Prediction\2.Validation\raw"
    
    first_folder_list = os.listdir(total_path)
    first_tqdm = tqdm(first_folder_list,
                    total=len(first_folder_list),
                    desc="2D to 3D 변환 중",
                    ncols = 100,
                    ascii = ' #',
                    leave = True,
                    )
    
    
    for tmp_path_1 in first_tqdm:
        first_tqdm.set_description('현재 폴더 %s' % tmp_path_1)        
        
        tmp_full_path_1 = os.path.join(total_path, tmp_path_1)
        
        second_folder_list = os.listdir(tmp_full_path_1)
        second_tqdm = tqdm(second_folder_list,
                            total=len(second_folder_list),
                            desc="2D to 3D 변환 중",
                            ncols = 100,
                            ascii = ' =',
                            leave = False,
                            )
        
        
        for tmp_path_2 in second_tqdm:
            second_tqdm.set_description('현재 폴더 %s' % tmp_path_2)                
            path = os.path.join(tmp_full_path_1, tmp_path_2)
            '''
            캘리브레이션 텍스트 파일을 읽어와서 행렬로 변환하여 변수에 저장해주는 부분
            '''
            calib_cam_path = path + r"\calib_Camera0.txt"
            calib_cam2Lidar_path = path + r"\calib_CameraToLidar0.txt"
            
            '''
            K = calib_cam
            Rt = calib_cam2Lidar
            '''
            calib_cam = txt2array(calib_cam_path)    
            calib_cam2Lidar = txt2array(calib_cam2Lidar_path)        

            '''
            image result 파일 경로를 읽어와서 경로 내의 모든 텍스트 파일을 시각화 해주는 부분
            '''
            image_result_path = path + r"\image_result"
            
            img_files = get_specific_type_file_list(image_result_path, ".jpg")
            txt_files = get_specific_type_file_list(image_result_path, ".txt")
            
            # grouping text file
            new_txt_files = []
            
            for img_file in img_files:
                img_name = img_file.split(".")[0]
                txt_file_prefix = img_name +"_"
                new_txt_files.append([txt_file for txt_file in txt_files if txt_file.startswith(txt_file_prefix)])
            
            
            img_path = os.path.join(os.getcwd() +r"\world_line", path.split('\\')[-2] ,path.split('\\')[-1], img_files[0])
            os.makedirs(os.path.dirname(img_path), exist_ok=True)

            
            third_tqdm = tqdm(new_txt_files,
                            total=len(new_txt_files),
                            desc="현재 파일",
                            ncols = 100,
                            ascii = ' *',
                            leave = False,
                            )

            
            for tmp_txt_files in third_tqdm:
                # third_tqdm.set_description('현재 파일 %s' % tmp_txt_files[0][:-6])    
                '''
                check tmp_txt_files is empty
                '''
                if len(tmp_txt_files) == 0:
                    continue
                
                wline = []
                plt.clf()            
                wline = get_wline(tmp_txt_files, wline)
                plt.plot(wline[:,0],wline[:,1],'.',color='red',markersize=1)
                plt.xlabel('x')
                plt.ylabel('y')
                plt.xlim(-5,5)
                plt.ylim(-10,10)
                plt.title('{}'.format(tmp_txt_files[0][:-6]))
                plt.grid(True)
                tmp_img_path = os.path.join(os.path.dirname(img_path), tmp_txt_files[0][:-6] + ".jpg")
                plt.savefig(tmp_img_path)
                
