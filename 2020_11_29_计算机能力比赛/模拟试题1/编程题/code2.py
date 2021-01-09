# 对于整数区间[N,M]，已知0输入说明：两个整数N和M
"""
    输出说明：顺序输出元素位上各个数字的平方和大于元素本身的数
    输入样例：21 25
    输出样例：25
    说明：例如22的数位数字为2，2，这两个数字的平方和为8，小于22，不满足筛选条件所以不输出；25的数位数字时
        2和5，这两个数字平方和时29，大于25，满足筛选条件，所以将25输出
"""
n = input()
nums = [int(i) for i in list(n.split(' '))]
for num in nums:
    total = 0
    for i in str(num):
        total += (int(i) ** 2)
    if total > num:
        print(num)