def switch_letter(s):
    string = s
    letters = []
    # 对于字符串中的每一个字符
    for letter in string:
        # 使用if-elif-else判断各自对应区间
        # 分别使用upper()/lower()将对应的小写字母/大写字母变成大写字母/小写字母
        if "a" <= letter <= "z":
            letters.append(letter.upper())
        elif "A" <= letter <= "Z":
            letters.append(letter.lower())
        else:
            letters.append(letter)
    # 将列表数据转换为对应的字符串形式的
    return ("".join(letters))

test1 = switch_letter("A@$bc2")
# "a@$BC2"
test2 = switch_letter("Hello-World")
# "hELLO-wORLD"
print(test1,test2)