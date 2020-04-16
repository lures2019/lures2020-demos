import math
r = float(input("请输入圆的半径："))
perimeter = 2 * math.pi * r
area = math.pi * (r**2)
print("圆的周长是%f，圆的面积是%f"%(perimeter,area))