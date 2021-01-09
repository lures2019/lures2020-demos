"""
    2、写一程序，输入身高和体重，打印出BMI
"""
height = input("请输入身高/m：")
weight = input("请输入体重/kg：")
# 计算BMI指数
BMI = float(float(weight)/(float(height)**2))
print("计算得出的BMI数值是：{:.3f}".format(BMI))