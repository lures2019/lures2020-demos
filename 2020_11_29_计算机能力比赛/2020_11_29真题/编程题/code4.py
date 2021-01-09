nums = int(input())
totals = []
for i in range(nums):
    numbers = [int(i) for i in list(input().split(' '))]
    totals.append(numbers)
# 现在数据已经保存到totals里面
"""
    6
    0 3 0 0 1 1
    0 6 0 1 1 1 
    9 9 9 7 5 3
    6 5 3 5 3 3
    5 6 6 6 7 6
    3 4 4 5 5 5
"""
EOF = -1
# 边界不满足
for i in range(1,len(totals)-1):
    for j in range(1,len(totals[0])-1):
        """
            假设现在是第i+1行、第j+1列
            那么现在取得数据是totals[i][j]
            那么左边的数据是totals[i][j-1]
                右边的数据是totals[i][j+1]
                上面的数据是totals[i-1][j]
                下面的数据是totals[i+1][j]
        """
        if ((totals[i][j] < totals[i][j-1]) and (totals[i][j] < totals[i][j+1]) and (totals[i][j] < totals[i-1][j]) and (totals[i][j]) < totals[i+1][j]):
            print("{} {}".format(i+1,j+1))
            EOF = 1
            break
if EOF == -1:
    print("{} {}".format(-1,-1))