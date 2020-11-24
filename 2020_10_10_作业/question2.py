def reverse_trajectory(s):
    coordinates = s
    if len(coordinates) <= 1:
        return ''
    else:
        lengths = []
        # x_axis和y_axis分别存放横坐标和纵坐标
        x_axis = []
        y_axis = []
        for coordinate in coordinates:
            x_axis.append(coordinate[0])
            y_axis.append(coordinate[1])
        for i in range(len(x_axis)-1):
            # 如果横坐标不变，只有纵坐标变换，即执行U/D
            if(x_axis[i] == x_axis[i+1]):
                # 移动长度就是后面的纵坐标减去前面的纵坐标
                length = y_axis[i+1] - y_axis[i]
                if length < 0:
                    lengths.append('D')
                    lengths.append(str(-1 * length))
                else:
                    lengths.append('U')
                    lengths.append(str(length))
            elif(y_axis[i+1] == y_axis[i]):
                # 如果纵坐标不变，只有横坐标变换，即执行L/R
                length = x_axis[i+1] - x_axis[i]
                if length < 0:
                    lengths.append('L')
                    lengths.append(str(-1 * length))
                else:
                    lengths.append('R')
                    lengths.append(str(length))
            else:
                # 如果横纵坐标都变换
                return "输入的列表有错误，不支持横纵坐标同时变换的列表"
        return ("".join(lengths))


test1 = reverse_trajectory([(0,0), (0,2), (-4,2), (-4,8), (-4,0), (8,0), (8,-3)])
# 'U2L4U6D8R12D3'
test2 = reverse_trajectory([(0, 0), (0, 1), (0, 0), (-1, 0), (0, 0)])
# 'U1D1L1R1'
test3 = reverse_trajectory([(0, 0)])
# ''
print(test1)
print(test2)
print(test3)