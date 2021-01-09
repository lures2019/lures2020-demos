"""
    按月分期付款
        6期      利息0.6%
        12期     利息0.3%
        24期     利息0.1%
    求不同期限下对应的每期要偿还的金额
"""
# 应该是对应不同期限，每期在上一期基础上*利息，算出总偿还金额，然后按月付款
brand = input("手机名称：")
price = int(input("价格："))

def pay_total(i):
    if i == 6:
        count = price * ((1 + 0.006) ** i)
        return count
    elif i == 12:
        count = price * ((1 + 0.003) ** i)
        return count
    elif i == 24:
        count = price * ((1 + 0.001) ** i)
        return count
    else:
        print("没有对应期限！")

print("6期，12期，24期每期要偿还的金额分别是：{:.2f}元、{:.2f}元、{:.2f}元".format(pay_total(6)/6,pay_total(12)/12,pay_total(24)/24))



