"""
    编写一个Python程序来计算字符串中特定字符出现次数
    测试案例：
        你好呀，好不好，不好，真不好，实在太不开心了
"""
# 先让用户输入一串字符
string = input("请输入任意字符串：")
# 用户输入一个特定的字符
char = input("请输入一个特定的字符：")
# 创建变量count用来计数,初始化为0
count = 0
for i in string:
    if i == char:
        count += 1
    else:
        pass
print("{}中{}出现的次数是：{}次".format(string,char,count))