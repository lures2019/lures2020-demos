string = input()
# abcadiasiqacdfgiikkg
max_strings = []
# 输入是'a'~'z'构成的，因此无需考虑特殊字符
max_child_string = ""
for i in range(len(string)-1):
    if ord(string[i]) <= ord(string[i+1]):
        max_child_string += string[i]
    else:
        max_strings.append(max_child_string)
        max_child_string = ""
lengths = []
for str1 in max_strings:
    lengths.append(len(str1))
max_length = max(lengths)
for str1 in max_strings:
    if len(str1) == max_length:
        # 现在需要判断str1在string中的位置
        if ord(string.split(str1)[-1][0]) >= ord(str1[-1]):
            str1 += string.split(str1)[-1][0]
            print(str1)
