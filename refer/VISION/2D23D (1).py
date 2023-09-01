import numpy as np
import math

########## changing params ##########
datasetname = "strasbourg_000001_018872"

### intrinsics(fixel) ###
fx = 2256.47; fy = 2219.6024040684233
u0 = 1049.19; v0 = 515.25

### extrinscs ###
p = 0.05; r = 0.0; yaw = 0.007 # rad
x = 1.7; y = -0.1; z = 1.18 # m
#####################################
lane=np.array([,])

R = np.array([[,,],[,,],[,,]]).T 
print(R)

t = np.array([,,]).T; 
t = -R@t
t = t.reshape(3,1)
print(t)

Pc_lane = np.array([[1, -(lane[0] - u0)/fx, -(lane[1] - v0)/fy]]).reshape(3,1)

Pw_lane = R.T@(Pc_lane - t)

Cc = np.array([0,0,0]).reshape(3,1)
Cw = R.T@(Cc - t)

k_BLB = -Cw[2]/(Pw_lane[2]-Cw[2])

P_BLB = (Cw+k_BLB*(Pw_lane-Cw)).T

print("\nP of",datasetname,"is")
print("P_BLB =",P_BLB)


print("\nGT of",datasetname,"is")
# print("      x(m)     y(m)     z(m) \nBLB : 31.64     4.85    -0.19    \nBRB : 32.41     3.31    -0.16   \nFRB : 36.26     5.22    -0.20   \nFLB : 35.49     6.76    -0.23") # aachen_000000_000019_object1