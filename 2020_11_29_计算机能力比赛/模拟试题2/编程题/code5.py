"""
    某机械公司生产两种产品。A的单件利润是100元，B的单件利润是150元。每种产品由三种材料构成，现给出
        每种材料的库存（库存小于100000），求利润最大的生产方案
    输入说明：第一行给出生产每件A产品所需要的三种材料数量
            第二行给出生产每件B产品所需要的三种材料数量
            第三行给出三种材料的库存数量
    输出说明：输出利润最大生产方案多对应的每种产品的生产数量（按照产品A、产品B的顺序）和利润最大值，每个数值间用空格隔开
    输入样例：3 1 2
            5 2 2
            30 4 6
    输出样例： 2 1 350
"""
M_A = [int(i) for i in list(input().split(' '))]
M_B = [int(i) for i in list(input().split(' '))]
M = [int(i) for i in list(input().split(' '))]
"""
    实际是求出A和B生产的件数x和y，总利润位total = 100x + 150y
    其中x和y满足下面的关系式：
        M_A[0]*x + M_B[0]*y < M[0]
        M_A[1]*x + M_B[1]*y < M[1]
        M_A[2]*x + M_B[2]*y < M[2]
    在满足上面关系式所对应的x和y构成的解决方案使得total最大，进行输出
    其中x和y是有取值范围的：
        x = min(M[0] // M_A[0],M[1] // M_A[1],M[2] // M_A[2])
        y = min(M[0] // M_B[0],M[1] // M_B[1],M[2] // M_B[2])
    默认是不为0，为0时，因为考虑情况多，太复杂了
"""
totals = []
for x in range(0,min(M[0] // M_A[0],M[1] // M_A[1],M[2] // M_A[2])):
    for y in range(0,min(M[0] // M_B[0],M[1] // M_B[1],M[2] // M_B[2])):
        total = 100*x + 150*y
        totals.append(total)
value = max(totals)
# 如果存在多种可能，默认输出第一种情况
for x in range(0,min(M[0] // M_A[0],M[1] // M_A[1],M[2] // M_A[2])):
    for y in range(0,min(M[0] // M_B[0],M[1] // M_B[1],M[2] // M_B[2])):
        total = 100*x + 150*y
        if total == value:
            print("{} {} {}".format(x,y,total))
            break

