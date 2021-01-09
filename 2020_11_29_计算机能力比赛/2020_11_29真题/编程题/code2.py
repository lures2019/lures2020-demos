nums = [int(i) for i in list(input().split(' '))]
N = nums[0]
M = nums[1]

numbers = [int(i) for i in list(input().split(' '))]
max_value =[]
count = []
# N=10,M=4时，i可以最大取值N[6]，即0~6共7个数
# 1 2 3 4 5 6 7 8 9 10
for i in range(0,N-M+1):
    # 现在依次取M个数
    total = 0
    # 4*numbers[i] + (1+2+……M-1)
    true_value = M * numbers[i]
    for j in range(i,i+M):
        total += numbers[j]
    for j in range(M):
        true_value += j
    # 如果满足下式说明就是连续的M个数
    if true_value == total:
        max_value.append(total)
        count.append(i+1)
value = max(max_value)
for i in range(len(max_value)):
    if max_value[i] == value:
        print("{} {}".format(max_value[i],count[i]))
