import itertools as its
# 迭代器，as是重命名

# words可以是字母以及其他特殊字符
words = "1234567890"

# 生成4位密码就写repeat=4,5位的就写repeat=5，以此类推
r = its.product(words,repeat=6)

# 保存到文件中
for i in r:
    with open('password.txt',mode="a+",encoding="utf-8") as f:
        f.write("".join(i))
        f.write('\n')
