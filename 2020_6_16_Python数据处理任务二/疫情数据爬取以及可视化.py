# # 1、计算矩形面积A
# long = float(input())
# width = float(input())
# print(long*width)
#
#
#
#
# # 2、存款利息
# principal = int(input())
# years = int(input())
# rate = float(input())
# get_money = principal * ((1 + rate) ** years) - principal
# print('利息={:.2f}'.format(get_money))
#
#
#
# # 3、人生苦短，我用Python
# n = int(input())
# string = "人生苦短我用python"
# lists = []
# for i in range(int(n)):
#     lists.append(string[i])
# str_now = ', '.join(lists)
# print(str_now)
#
#
# # 4、百分制成绩转换五分制
# score = float(input())
# if (score >= 90):
#     print("A")
# elif(score >= 80):
#     print("B")
# elif(score >= 70):
#     print("C")
# elif(score >= 60):
#     print("D")
# else:
#     print("E")
#
#
# # 5、分数数列求前n项和
# num = int(input())
# x,y,z,sum = 2,1,0,0
# for i in range(1,num+1):
#     sum += x/y
#     z = x
#     x = x+y
#     y = z
# print(sum)
#
#
# # 6、累加函数
# N = int(input())
# sum = 0
# for i in range(N+1):
#     sum += i
# print(sum)
