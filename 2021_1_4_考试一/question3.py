"""
    某人第一天存款10元，第二天存款20元，第三天存款40元，每天的存款为前一天的两倍
    请用递归程序来计算第十天时应该存入多少元，10天共存了多少元？
"""
def save_each_day(i):
    if i == 1:
        money = 10
    else:
        # i天存款是i-1天的2倍
        money = 2 * save_each_day(i-1)
    return money

def save_total(i):
    count = 0
    for i in range(1,i+1):
        count += save_each_day(i)
    return count


if __name__ == '__main__':
    x = save_each_day(10)
    y = save_total(10)
    print("第10天存了{}元，共存了{}元".format(x,y))