"""
    求1~100（不包括100），整数满足5的倍数有多少个
"""
# 记录5的倍数的数目
count = 0
for i in range(1,100):
    if i % 5 != 0:
        print(i)
    else:
        count += 1
print("一共拍了{}次腿".format(count))
