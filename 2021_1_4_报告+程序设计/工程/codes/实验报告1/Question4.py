"""
    假设s是包含多个小数的字符串，由逗号隔开，如s= '1.23，2.4，3.123'。编写一个程序，输出s中所有数值的和。
"""
# 1、用户输入多个小数，中间用,进行隔开
nums = input("请输入用逗号隔开的多个小数：")
# 2、存放到列表中，并将字符串类型转换为float类型
nums_now = [float(i) for i in list(nums.split(","))]
# 3、计算nums_now数值和
count = sum(nums_now)
print("s中所有数值的和是：{}".format(count))