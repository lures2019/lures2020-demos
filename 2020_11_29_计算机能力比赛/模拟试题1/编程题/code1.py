# 计算1到M（含M）之间的合数数量，输出其值
"""
    输入说明：一个正整数M（M < 10000)
    输出说明：输出合数的数量1
    输入样例：12
    输出样例：6
"""
n = int(input())
m = 0
for i in range(4,n+1):
    for j in range(2,i):
        if i % j == 0:
            m += 1
            break
print(m)