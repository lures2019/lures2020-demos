"""
    编写一个程序，检查变量x,y和z，输出其中最大的奇数。如果其中没有奇数，就输出一个信息进行说明。
"""
# 1、首先，从键盘依次输入三个数，中间用空格隔开
nums = input("请依次输入三个数：")
# 2、因为这三个数据的输入是空格隔开的，加上input输入的默认是字符串，因此可以用split(" ")按照空格分割
# 从而得到三个字符串，用list将其变化为列表形式，最后用[int(i) for i in nums]形式将nums里面的数强制转化为整数
nums_now = [int(i) for i in list(nums.split(" "))]
# 3、依次遍历nums_now列表，判断有无奇数
# 判断标准：奇数 % 2 == 1 而偶数 % 2 == 0
# 4、创建一个空列表，存储奇数
odds = []
# status = False默认表示无奇数
status = False
for num in nums_now:
    if (num % 2 == 1):
        odds.append(num)
        # 若为奇数，则改变status的状态
        status = True
    else:
        pass
# 5、输出部分
if status == False:
    print("您输入的三个数中无奇数！")
else:
    print("您输入的三个数中最大的奇数是：{}".format(max(odds)))