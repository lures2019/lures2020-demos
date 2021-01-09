"""
    (1)测试案例：59 60 89 90 100 83 76 34 89 64
"""
# 用户一行输入10位同学的成绩，默认用空格隔开
scores = [int(i) for i in list(input("请输入10位同学的成绩：").split(" "))]
# 创建列表，用于存储及格同学的成绩
exam_pass = []
# 开始遍历scores列表
for score in scores:
    if (score >= 60):
        exam_pass.append(score)
    else:
        pass
    # 小数点后保留三位有效数字
print("及格同学们的平均分数是：{:.3f}分".format(sum(exam_pass)/len(exam_pass)))

"""
    （2）测试案例：30 70 100
"""
# 创建空列表，用于存储输入同学的分数
scores_now = []
scores_pass = []
# 持续输入分数，当分数为200时break跳出循环（？？？200是总分？）
while sum(scores_now) < 200:
    score = int(input("请输入一位同学的成绩："))
    if score >= 60:
        scores_pass.append(score)
        scores_now.append(score)
    else:
        scores_now.append(score)
    # 小数点后保留3位有效数字
print("所有及格同学的分数的平均成绩是：{:.3f}".format(sum(scores_pass)/len(scores_pass)))
