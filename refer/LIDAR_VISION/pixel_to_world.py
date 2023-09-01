# import cv2
# import numpy as np

# # H 행렬 정의

h11,h12,h13 = 224.655246649527,	63.6494490868106, 0.0624221433774384
h21,h22,h23 = -50.2413480763060, -7.95293261905732,	-0.00291759653581131
h31,h32,h33 = 2525.63416541402,	1089.39475263459,	1

# H = np.array([[h11, h12, h13],
#               [h21, h22, h23],
#               [h31, h32, h33]])

# # 픽셀 좌표
# pixel_x,pixel_y = 2312,   1043
 

# # 픽셀 좌표를 확장된 형태로 변환
# pixel_coords = np.array([[pixel_x],
#                          [pixel_y],
#                          [1]])

# # 월드 좌표 계산
# world_coords = np.dot(np.linalg.inv(H), pixel_coords)
# world_coords /= world_coords[2]  # 확장된 형태를 일반 형태로 변환

# # 월드 좌표 출력
# world_x = world_coords[0][0]
# world_y = world_coords[1][0]
# print("월드 좌표 (x, y):", world_x, world_y)


import cv2
import numpy as np

# H 행렬 정의
H = np.array([[h11, h12, h13],
              [h21, h22, h23],
              [h31, h32, h33]])

# 객체의 이미지 상에서의 위치
object_pixel_x = 2312
object_pixel_y = 1043

# 객체의 이미지 상에서의 크기
object_width = 50
object_height = 80

# 객체의 이미지 상에서 중심점 계산
object_center_x = object_pixel_x + object_width / 2
object_center_y = object_pixel_y + object_height / 2

# 객체의 이미지 상에서의 중심점을 확장된 형태로 변환
- = np.array([[object_center_x],
                                 [object_center_y],
                                 [1]])

# 월드 좌표로 변환
world_coords = np.dot(np.linalg.inv(H), object_center_coords)
world_coords /= world_coords[2]  # 확장된 형태를 일반 형태로 변환

# 월드 좌표 출력
world_x = world_coords[0][0]
world_y = world_coords[1][0]
print("월드 좌표 (x, y):", world_x, world_y)

# # 월드 좌표 기준 객체의 종 방향 거리 계산
# distance_along_x = world_x - reference_point_x
# print("종 방향 거리:", distance_along_x)

# # 월드 좌표 기준 객체의 횡 방향 거리 계산
# distance_along_y = world_y - reference_point_y
# print("횡 방향 거리:", distance_along_y)
