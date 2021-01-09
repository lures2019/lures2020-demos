"""
    编写一个Python程序，在给定的列表中指定位置插入元素
    测试案例：
        [1,'zls','你好',1.0,True]
"""
my_list = input("请输入一个列表：")
# 使用eval将变成了str类型的列表恢复原来的类型
my_list_now = eval(my_list)
# 在列表允许范围内,用户输入一个位置
location = input("请输入一个0到{}的整数：".format(len(my_list_now)))
# 用户输入一个元素
element = input("请随意输入一个元素：")
my_list_now.insert(int(location),element)
print("在{}位置处插入{}后列表成为{}".format(location,element,my_list_now))