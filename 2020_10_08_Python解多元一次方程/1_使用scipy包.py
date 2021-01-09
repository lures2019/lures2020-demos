"""
    1、使用已有的第三方工具包scipy和numpy进行求解（主要思路是：矩阵和行列式的知识）
"""
from scipy import linalg
import numpy as np

# 主要存放多元一次方程未知数前面的系数
# 每个等式的系数放在一个列表中
a = np.array([[3,2,2],[9,8,4],[27,24,8]])
b = np.array([-1,-3,-5])
result = linalg.solve(a,b)
print(result)
