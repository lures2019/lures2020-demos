"""
    某冶金厂生产两类合金产品，分别为M1和M2.生产M1和M2时需要三种原材料（含某种原材料的需求量为0的情形）。现有一批这样的原材料即将过期，希望尽快用这些原材料
    生产M1和M2（每种原材料的数量均小于10000），请给出浪费原材料总量最少（即三种剩余原材料的数量和最小）的生产方案。如过方案不止一种，请输出
    M1生产量最少时所对应的方案。
    输入说明：第一行给出生产M1所需的三种原材料数量，为整型数据
            第二行给出生产M2所需的三种原材料数量，为整型数据
            第三行给出原材料库存数，为整型数据
    输出说明：输出满足条件时，M1和M2各自的生产数量（整数解）
    输入样例：4 2 2
            6 3 2
            20 10 10
    输出样例：2 2
"""
def text(x_min,y_min,M1,M2,M):
    x_min,y_min,M1,M2,M = x_min,y_min,M1,M2,M
    # x的范围是(0,min(M[i]//M1[i]))，依次类推
    total1 = sum(M)
    totals = []
    for x in range(0, x_min):
        for y in range(0, y_min):
            if ((M1[0] * x + M2[0] * y <= M[0]) and (M1[1] * x + M2[1] * y <= M[1]) and (
                    M1[2] * x + M2[2] * y <= M[2])):
                total = total1 - (sum(M1) * x + sum(M2) * y)
                totals.append(total)
    total_value = min(totals)
    x_values = []
    y_values = []
    for x in range(0, min(M[0] // M1[0], M[1] // M1[1], M[2] // M1[2])):
        for y in range(0, min(M[0] // M2[0], M[1] // M2[1], M[2] // M2[2])):
            if ((M1[0] * x + M2[0] * y <= M[0]) and (M1[1] * x + M2[1] * y <= M[1]) and (
                    M1[2] * x + M2[2] * y <= M[2])):
                total = total1 - (sum(M1) * x + sum(M2) * y)
                if total == total_value:
                    x_values.append(x)
                    y_values.append(y)
    if len(x_values) == 1:
        print(x_values[0], y_values[0])
    else:
        x_end = min(x_values)
        for i in range(len(x_values)):
            if x_values[i] == x_end:
                print(x_end, y_values[i])
                break

if __name__ == '__main__':
    # 下面的测试在M1和M2各项数据不为0时有效，有0存在时报错，需重新处理
    M1 = [int(i) for i in list(input().split(' '))]
    M2 = [int(i) for i in list(input().split(' '))]
    M = [int(i) for i in list(input().split(' '))]
    # 假设剩余材料：足够生产M1和M2各：x和y件
    """
        满足下列公式：
            M1[0]x + M2[0]y <= M[0]
            M1[1]x + M2[1]y <= M[1]
            M1[2]x + M2[2]y <= M[2]
        total1 = sum(M)
        total = total1 - (sum(M1)x + sum(M2)y)
        使得total最小时的x和y解，如果total最小时有多个x和y匹配，找到最小的x输出
    """
    if 0 not in M1 and 0 not in M2:
        x_min = min(M[0] // M1[0], M[1] // M1[1], M[2] // M1[2])
        y_min = min(M[0] // M2[0], M[1] // M2[1], M[2] // M2[2])
        text(x_min, y_min, M1, M2, M)
    # M1和M2中出现0的情况
