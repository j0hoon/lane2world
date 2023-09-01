import cv2
import numpy as np


def C2L(x,y):

    k11, k12, k13 = 2711.612310667572, 0.000000000000, 1429.476779406936
    k21, k22, k23 = 0.000000000000, 2775.774306203296, 1034.829470572830
    k31, k32, k33 = 0.000000000000, 0.000000000000, 1.000000000000

    r11, r12, r13 = -0.999555652583, 0.024585187648, 0.016854255756
    r21, r22, r23 = -0.015271407733, 0.063207287028, -0.997883571852 
    r31, r32, r33 = -0.025598466646, -0.997697553077, -0.062803750609 

    t1, t2, t3 = 0.232415191416,-0.577600893468,-0.868952558982

    K = np.array([[k11, k12, k13],
                [k21, k22, k23],
                [k31, k32, k33]])

    R = np.array([[r11, r12, r13],
                [r21, r22, r23],
                [r31, r32, r33]])

    t = np.array([[t1],[t2],[t3]])
    
    Rt = np.hstack((R,t))
    
    Rt44 = np.vstack((Rt,np.array([0,0,0,1])))
    
    # 픽셀 좌표 (x, y)
    pixel_coords = np.array([x, y, 1])

    # 카메라 좌표계로 변환
    camera_coords = np.linalg.inv(K) @ pixel_coords

    lidar_coords = np.linalg.inv(Rt44) @ camera_coords


    # LiDAR 좌표계로 변환
    # lidar_coords = R @ camera_coords + t
    
    # lidar_coords = R.T @ (camera_coords - t)
                
    # Rt = np.hstack((R,t))
    
    # Rt2 = np.array([[r11,r12,r13,t1],
    #                 [r21,r22,r23,t2],
    #                 [r31,r32,r33,t3]])

    # pixel_coords = np.array([x,y,1])
    
    # camera_coords = np.dot(np.linalg.inv(K), pixel_coords)
    
    # lidar_coords = np.dot(np.linalg.inv(Rt2), camera_coords)
    # print(lidar_coords[:3])
    return lidar_coords


if __name__ == "__main__":
    import os
    os.system('cls')
    x = 1000
    y = 1000
    
    lidar = C2L(x,y)
    
    print(lidar)
    
    
    





# # 객체의 이미지 상에서의 위치
# object_pixel_x = 100
# object_pixel_y = 200

# # 객체의 이미지 상에서의 크기
# object_width = 50
# object_height = 80

# # 객체의 이미지 상에서 중심점 계산
# object_center_x = object_pixel_x + object_width / 2
# object_center_y = object_pixel_y + object_height / 2

# # 객체의 이미지 상에서의 중심점을 확장된 형태로 변환
# object_center_coords = np.array([[object_center_x],
#                                  [object_center_y],
#                                  [1]])

# # 월드 좌표로 변환
# world_coords = np.dot(np.linalg.inv(H), object_center_coords)
# world_coords /= world_coords[2]  # 확장된 형태를 일반 형태로 변환

# # 월드 좌표 출력
# world_x = world_coords[0][0]
# world_y = world_coords[1][0]
# print("월드 좌표 (x, y):", world_x, world_y)

# # 월드 좌표 기준 객체의 종 방향 거리 계산
# distance_along_x = world_x - reference_point_x
# print("종 방향 거리:", distance_along_x)

# # 월드 좌표 기준 객체의 횡 방향 거리 계산
# distance_along_y = world_y - reference_point_y
# print("횡 방향 거리:", distance_along_y)





























