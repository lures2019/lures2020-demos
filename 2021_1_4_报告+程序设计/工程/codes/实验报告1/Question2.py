"""
    编写一个程序，要求用户输入10个整数，然后输出其中最大的奇数。如果用户没有输入奇数，则输出一个信息进行说明。
    测试用例：
        10 20 30 40 50 2 4 6 8 0        无奇数
        1 10 20 30 40 50 2 4 6 8        1奇数
        1 3 5 7 10 20 30 40 50 2        多奇数
"""
# 和Question1思路大致一样
# 1、input()得到用户输入的含有10个整数的字符串，输入两数之间空格隔开
nums = input("请输入10个整数：")
# 2、根据split(" ")将字符串进行切割,最后list转换为列表
nums_now = [int(i) for i in list(nums.split(" "))]
# 3、创建一个空列表，用于存储奇数
odds = []
# 4、确定状态status = False,表无奇数情况
status = False
# 5、开始遍历整个列表
for num in nums_now:
    # num % 2 == 1则表示奇数，否则是偶数
    if (num % 2 == 1):
        status = True
        odds.append(num)
    else:
        # pass表占位
        pass
# 6、根据状态结果输出对应信息
if status == False:
    print("您输入的10个数中无奇数！")
else:
    print("您输入的10个数中最大奇数是：{}".format(max(odds)))
