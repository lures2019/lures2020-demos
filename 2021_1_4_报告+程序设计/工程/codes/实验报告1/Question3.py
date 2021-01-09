"""
    编写一个程序，要求用户输入一个整数，然后输出两个整数root和pwr，满足0<pwr<6，并且root**pwr对于用户输入的整数。
        如果不存在这样一对整数，则输出一个信息进行说明。
"""
# 使用穷举法求立方根
x = int(input('输入需要判断的数字：'))
ans = 0
while ans**3 < abs(x):
    ans = ans + 1
if ans**3 != abs(x):
    print(x,'不是立方根数')
else:
    if x < 0:
        ans =- ans
    print('输入数{}的立方根是'.format(ans))
y = int(input('输入需要判断的数字：'))
root = 0
for pwr in range(1,6):#通过for循环遍历几次方
    while root**pwr < abs(y):#使用穷举法寻找方根
        root = root + 1
    if root**pwr != abs(y):
        print("{}不是{}的次方根数".format(y,pwr))
    else:
        if y < 0:
            root =- root
        print('输入数',y,'的',pwr,'次方根是',root)
    root = 0 #每一个for结束以后都要进行root=0