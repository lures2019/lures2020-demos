"""
    输入案例：
        学号：[1,2,3,4,5,6,7,8,9,10]
        成绩：[90,87,100,66,80,71,68,60,54,81]
"""
scores = eval(input("输入10位同学的成绩："))
numbers = eval(input("输入对应的1-位同学的学号："))
# 排序后列表
scores_sorted = sorted(scores,reverse=True)
for i in range(len(scores_sorted)):
    for j in range(len(scores)):
        if scores[j] == scores_sorted[i]:
            print("{},{}".format(numbers[j],scores[j]))

