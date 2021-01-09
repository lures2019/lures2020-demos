"""
    对于给出的长度为N的整数数组，对连续3个元素求平方和，输出平方和的最大值
    输入说明：第一行，数组中元素个数N(N < 1000)，第二行是这个数组中的N个元素，中间用空格隔开，每个元素小于100000
    输出说明：输出连续三个元素平方和的最大值
    输入样例：8
            1 1 -1 2 -3 3 -4 2
    输出样例：34
"""
length = int(input())
nums = [int(i) for i in list(input().split(' '))]
values = []
for i in range(len(nums) - 2):
    # 8个元素的话，因为是连续3个元素，所以i的遍历范围是0~5，即range(6)
    value = (nums[i] ** 2) + (nums[i+1] ** 2) + (nums[i+2] ** 2)
    values.append(value)
print(max(values))
