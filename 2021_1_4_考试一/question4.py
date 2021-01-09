"""
    写一个程序，输入班上同学（10个）参加TOEIC考试（范围0—120）所考分数，求：
        （a）全班最高分
        （b）105分以上人数
        （c）介于80——95（含95）的人数
        （d）全班总平均分（当输入140这个数字时，代表输入结束，直接跳出循环）
    输入案例：105 110 90 95 87 78 100 83 67 80 140
"""
# 根据题意知道是1位同学1位同学的录入
score = int(input("请输入1位同学的成绩："))
# 创建列表，存储各位同学的成绩
scores_all = []
# 大于105分的列表
scores_bigger = []
# 介于80-95分的列表
scores_80_95 = []
# 判断当前输入的成绩是否跳出循环
while score != 140:
    # 只有在输入不是140的时候有效
    scores_all.append(score)
    if score > 105:
        scores_bigger.append(score)
    if score > 80 and score <= 105:
        scores_80_95.append(score)
    score = int(input("请继续输入一位同学的成绩："))
# 循环结束后
print("全班最高分是：{}".format(max(scores_all)))
print("105分以上有{}人".format(len(scores_bigger)))
print("介于80-95分有{}人".format(len(scores_80_95)))
print("全班总平均分是：{}分".format(sum(scores_all) / len(scores_all)))
