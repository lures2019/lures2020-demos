"""
    平面上有N个矩形（编号依次位1，2，……N），每个矩形可用它的左下角和右上角顶点坐标来表示（默认该矩形的4条边分别两两平行于X轴或Y轴，
        所以确认这两个顶点之后，矩形是唯一的），现在给出一些矩形，规定它们的面积各不相同，请输出面积第三大的矩形序号及其面积。
    输入说明：第一行输入一个整数N（3 <=N <= 1000），之后N行，每行有两个二维坐标(x,y)，分别表示对应矩形的左下角和右上角的顶点坐标
    输出说明：面积第三大的矩形序号和它的面积，中间用空格隔开
    输入样例：5
        0 0 1 2
        1 2 5 5
        0 0 3 5
        1 2 5 6
        4 3 8 8
    输出样例：3 15
"""
nums = int(input())
datas = []
for i in range(nums):
    x = list(input().split(' '))
    datas.append(x)
# 记录矩形面积
rectangular_areas = []
for i in range(nums):
    # x1是左上角的横坐标，y1是左上角的纵坐标
    x1 = int(datas[i][0])
    y1 = int(datas[i][1])
    # x2是右下角的横坐标，y2是右下角的纵坐标
    x2 = int(datas[i][2])
    y2 = int(datas[i][3])
    # 现在计算矩形的面积
    area = abs(x2-x1) * abs(y2-y1)
    rectangular_areas.append(area)
rectangular_areas.sort()
value = rectangular_areas[2]
for i in range(nums):
    # x1是左上角的横坐标，y1是左上角的纵坐标
    x1 = int(datas[i][0])
    y1 = int(datas[i][1])
    # x2是右下角的横坐标，y2是右下角的纵坐标
    x2 = int(datas[i][2])
    y2 = int(datas[i][3])
    # 现在计算矩形的面积
    area = abs(x2-x1) * abs(y2-y1)
    if area == value:
        print("{} {}".format(i+1,value))