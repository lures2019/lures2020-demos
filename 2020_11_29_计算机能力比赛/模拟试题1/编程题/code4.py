"""
    有一个DNA序列，用字符串S表示（仅包含'A'、'C'、'G'、'T'四种字符，长度 < 100000)。现有N个待检测的基因片段（序号分别为1，2……N）
    用字符串Ti（i = 1，2……N）表示（仅包含'A'、'C'、'G'、'T'四种字符，长度 < 1000）。请分别检测DNA序列S中是否存在这些基因片段，并按下面
    输出说明格式依次输出检测结果！
    输入说明：第一行是DNA序列S
            第二行是正整数N，表明有N个待检测的基因片段，之后有N行，分别表示这N个待检测的基因片段，即每行一个基因片段
    输出说明：依次匹配这N个待检测的基因片段，如果DNA序列S中存在第i个待检测的基因片段，输出Ti：ALERT所在位置（即Ti的首字母在S中的位置，如果出现多次
            ，输出第一次出现的位置，S的起始位置为1）；如果不存在则输出Ti：SAFE
    输入样例：ATCGCGCGAATTGATCGTTCGA
            2
            AATTGAT
            GATCGTC
    输出案例：
            T1：ALERT 9
            T2：SAFE
"""
string = input()
nums = int(input())
datas = []
for i in range(nums):
    x = input()
    datas.append(x)
# 现在my_list里面存放的就是要搜寻的字符串片段了
# 因为要统计的是Ti的信息
T_sitiuations_dict = {}
for i in range(len(datas)):
    T_sitiuations_dict['T{}'.format(i+1)] = 'SAFE'

for i in range(len(datas)):
    str1 = datas[i]
    if str1 in string:
        length = len(string.split(str1)[0]) + 1
        T_sitiuations_dict['T{}'.format(i + 1)] = 'ALERT {}'.format(length)

for key,value in T_sitiuations_dict.items():
    print('{}：{}'.format(key,value))

