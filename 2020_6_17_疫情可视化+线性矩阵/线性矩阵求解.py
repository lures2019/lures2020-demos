"""
    title:线性方程组求解问题
    date:2020/6/18
    大致思路:使用numpy包进行求解未知参数矩阵X
            AX = B---->X = A'B
"""
import numpy as np
from scipy import linalg
import math
import matplotlib.pyplot as plt

angle = float(input("请输入角度的大小(eg:90):"))
# 得到对应的弧度
angle_now = math.radians(angle)
m1 = float(input("请输入m1的值(eg:2):"))
m2 = float(input("请输入m2的值(eg:2):"))
a = np.array([[m1*math.cos(angle_now),(-1*m1),(-1*math.sin(angle_now)),0],
             [m1*math.sin(angle_now),0,math.cos(angle_now),0],
             [0,m2,(-1*math.sin(angle_now)),0],
             [0,0,(-1*math.cos(angle_now)),1]])
g = 9.8
b = np.array([0,m1*g,0,m2*g])
x = linalg.solve(a,b)
a1,a2,N1,N2 = x
print("a1,a2,N1,N2得到的值是：%.3f %.3f %.3f %.3f"%(a1,a2,N1,N2))
plt.plot(x)
plt.show()