"""
    （1）可以看出是 第i天存款是1+3+……+（4i+1)元，那么i天总共存款便可以计算出来了！
"""
# 计算每天存款多少元
def save_every_day(i):
    # 用于计数
    count = 0
    # 步长设置为2，将奇数保存下来
    for m in range(1,4*i+2,2):
        count += m
    return count
print("第10天存%s元"%save_every_day(10))
# 计算目标天数内存了多少元
def save_total(i):
    # 用于计数
    count = 0
    for m in range(1,i+1):
        count += save_every_day(m)
    return count
print("10天共存{}元".format(save_total(10)))