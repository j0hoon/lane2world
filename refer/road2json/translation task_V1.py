import numpy as np
import math

# 2Dimagecoordinate.py 에서 도출되는 2D 좌표는 I좌표계 기준


             # u[px]   v[px]
BLB=np.array([693.20,533.99]) ### 픽셀좌표계, 단위
BRB=np.array([816.17,528.73])
FRB=np.array([717.05,520.36])
FLB=np.array([605.66,524.83])
BLT=np.array([689.84,417.91])
BRT=np.array([813.13,415.63])
FRT=np.array([714.17,419.78])
FLT=np.array([602.53,421.89])

### 초점 거리(픽셀 단위)
fx = 2262.52; fy = 2265.3017905988554
u0 = 1096.98; v0 = 513.137

### extrinscs
p = 0.038; r = 0.0; yaw = -0.0195 ### rad 단위.

x = 1.7; y = 0.1; z = 1.22 ### world 좌표계는 후륜 중심을 기준으로!
# baseline = 0.209313 ### 이 값은 스테레오 카메라에서 두 카메라 눈 간의 거리를 의미함, 깊이 정보의 추정에 사용됨

########## Darkpgmr ##########

R = np.array([[np.cos(yaw)*np.cos(p), np.cos(yaw)*np.sin(p)*np.sin(r)-np.sin(yaw)*np.cos(r), np.cos(yaw)*np.sin(p)*np.cos(r)+np.sin(yaw)*np.sin(r)],
              [np.sin(yaw)*np.cos(p), np.sin(yaw)*np.sin(p)*np.sin(r)+np.cos(yaw)*np.cos(r), np.sin(yaw)*np.sin(p)*np.cos(r)-np.cos(yaw)*np.sin(r)],
              [-np.sin(p), np.cos(p)*np.sin(r), np.cos(p)*np.cos(r)]]).T ### world->camera, file:///C:/Users/ACL/Downloads/csCalibration%20(1).pdf
print("R =",R)
### yaw, pitch, roll 모두 0에 가까운 작은 각도, 그러면 R은 np.array([[1,0,0],[0,1,0],[0,0,1]])의 단위행렬과 근사해진다. 
### 카메라 좌표계와 월드좌표계의 축이 다른데 이렇게 R이 나와도 되는 건지 모르겠다.
### 다시 보니 V와 C좌표계의 축은 동일하다고 함. C는 카메라 광학중심을 원점으로, V는 후륜 중심 아래 지면을 원점으로.
### darkpgmr 사이트에서는 축이 달라진다!!! 이걸 맞춰줘야 함. 

t = np.array([x,y,z]).T.reshape(3,1)
t = -R@t ### t는 카메라중심 좌표계로 본 world좌표계 원점의 위치와 같다. 
# print("t =",t)

C_pos = -np.linalg.inv(R)@t ### 카메라의 위치를 월드 좌표로 봤을 때(m). 월드는 후륜 중심 아래 지면을 기준으로 진행방향이 x방향, x방향으로 1.7m, y방향(왼쪽)으로 0.1m, 위로 1.22m에 카메라가 달려있다. 
# print("C_pos=",C_pos)
# C_pos = -R.T@t
# print("C_pos=",C_pos)
### 역행렬을 취하든 transpose하든 같게 나온다. -t가 나옴.
### C_pos=-R.t@-R@t=t이므로 결국 (x,y,z).T가 나오게 된다.

# pc = np.array([[(BLB[0] - u0)/fx, (BLB[1] - v0)/fy,1]]).reshape(3,1) ### u,v를 정규화해준다
pc_BLB = np.array([[1, -(BLB[0] - u0)/fx, -(BLB[1] - v0)/fy]]).reshape(3,1) ### C좌표계 축이 V좌표계와 같으므로 맞춰주었다.
pc_BRB = np.array([[1, -(BRB[0] - u0)/fx, -(BRB[1] - v0)/fy]]).reshape(3,1) 
pc_FRB = np.array([[1, -(FRB[0] - u0)/fx, -(FRB[1] - v0)/fy]]).reshape(3,1) 
pc_FLB = np.array([[1, -(FLB[0] - u0)/fx, -(FLB[1] - v0)/fy]]).reshape(3,1) 
# pc_BLT = np.array([[1, -(BLT[0] - u0)/fx, -(BLT[1] - v0)/fy]]).reshape(3,1)
# pc_BRT = np.array([[1, -(BRT[0] - u0)/fx, -(BRT[1] - v0)/fy]]).reshape(3,1) 
# pc_FRT = np.array([[1, -(FRT[0] - u0)/fx, -(FRT[1] - v0)/fy]]).reshape(3,1) 
# pc_FLT = np.array([[1, -(FLT[0] - u0)/fx, -(FLT[1] - v0)/fy]]).reshape(3,1) 
# print("pc_BLT =",pc_BLT)
#정규화된 값이 너무 작은데 맞나? 원래 이렇게 fx, fy가 큰 건지도 모르겠다. 
## 여기 수상쩍어
### 단위가 없는 Pc에서 m단위의 translation vector를 빼도 되나?
#### 오! 축을 맞춰주었을 때 됐다. 

Pw_BLB = R.T@(pc_BLB - t)
Pw_BRB = R.T@(pc_BRB - t)
Pw_FRB = R.T@(pc_FRB - t)
Pw_FLB = R.T@(pc_FLB - t)
# Pw_BLT = R.T@(pc_BLT - t)
# Pw_BRT = R.T@(pc_BRT - t)
# Pw_FRT = R.T@(pc_FRT - t)
# Pw_FLT = R.T@(pc_FLT - t)
# print("Pw_BLT =",Pw_BLT) ### 3*1 행렬이 나와야 한다. 점 Pc의 world 좌표계 표현.

Cc = np.array([0,0,0]).reshape(3,1)
# print("Cc =",Cc) ### 카메라 좌표계로 본 카메라 원점은 (0,0,0)

Cw = R.T@(Cc - t)
print("Cw =", Cw) ### 3*1 행렬이 나와야 한다. 카메라 원점의 world 좌표. C_pos와 같음

k_BLB = -Cw[2]/(Pw_BLB[2]-Cw[2])
k_BRB = -Cw[2]/(Pw_BRB[2]-Cw[2])
k_FRB = -Cw[2]/(Pw_FRB[2]-Cw[2])
k_FLB = -Cw[2]/(Pw_FLB[2]-Cw[2])
# k_BLT = -Cw[2]/(Pw_BLT[2]-Cw[2])
# k_BRT = -Cw[2]/(Pw_BRT[2]-Cw[2])
# k_FRT = -Cw[2]/(Pw_FRT[2]-Cw[2])
# k_FLT = -Cw[2]/(Pw_FLT[2]-Cw[2])
# print("k =",k_BLT)

P_BLB = (Cw+k_BLB*(Pw_BLB-Cw)).T
P_BRB = (Cw+k_BRB*(Pw_BRB-Cw)).T
P_FRB = (Cw+k_FRB*(Pw_FRB-Cw)).T
P_FLB = (Cw+k_FLB*(Pw_FLB-Cw)).T
# P_BLT = (Cw+k_BLT*(Pw_BLT-Cw)).T
# P_BRT = (Cw+k_BRT*(Pw_BRT-Cw)).T
# P_FRT = (Cw+k_FRT*(Pw_FRT-Cw)).T
# P_FLT = (Cw+k_FLT*(Pw_FLT-Cw)).T

print("\nP of aachen_000000_000019_object1 is")
print("P_BLB =",P_BLB)
print("P_BRB =",P_BRB)
print("P_FRB =",P_FRB)
print("P_FLB =",P_FLB)
# print("P_BLT =",P_BLT)
# print("P_BRT =",P_BRT)
# print("P_FRT =",P_FRT)
# print("P_FLT =",P_FLT)
### top point들은 z!=0이므로 이런 식으로 투영할 수 없다. 

print("\nGT of aachen_000000_000019_object1 is")
print("      x(m)     y(m)     z(m) \nBLB : 31.64     4.85    -0.19    \nBRB : 32.41     3.31    -0.16   \nFRB : 36.26     5.22    -0.20   \nFLB : 35.49     6.76    -0.23")
# Vertices in V:
#          x[m]     y[m]     z[m]
# BLB:    31.64     4.85    -0.19
# BRB:    32.41     3.31    -0.16
# FRB:    36.26     5.22    -0.20
# FLB:    35.49     6.76    -0.23
# BLT:    31.64     4.88     1.34
# BRT:    32.41     3.34     1.37
# FRT:    36.26     5.25     1.33
# FLT:    35.49     6.79     1.30

# print(np.sin(30)) # Degree
# print(np.sin(np.pi/6)) # Radian
# ### numpy 삼각함수는 radian 기준. 

# p = 0.038
# r = 0.0
# yaw = -0.0195
# print(math.radians(p))
# print(math.radians(r))
# print(math.radians(yaw))

###참고 자료
### https://velog.io/@noooooh_042/%EC%B9%B4%EB%A9%94%EB%9D%BC-%EC%BA%98%EB%A6%AC%EB%B8%8C%EB%A0%88%EC%9D%B4%EC%85%98
### https://gaussian37.github.io/vision-concept-calibration/
### https://darkpgmr.tistory.com/84
### https://darkpgmr.tistory.com/84
### https://darkpgmr.tistory.com/122
### https://darkpgmr.tistory.com/153
### https://github.com/mcordts/cityscapesScripts/blob/master/cityscapesscripts/helpers/box3dImageTransform.py
### Cityscapes Calibration_Nick Schneider, Marius Cordts_July 21, 2016
### https://github.com/mcordts/cityscapesScripts
### Cityscapes 3D: Dataset and Benchmark for 9 DoF Vehicle Detection