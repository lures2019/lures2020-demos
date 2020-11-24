def palindrome(s, k):
    string = [i for i in s]
    l = 0
    # 可以修改数字的最大次数
    r = len(s) - 1
    # 只有在修改次数范围内才有效
    while (l <= r):
        # 判断原数字字符串首尾数字是否相同
        if (s[l] != s[r]):
            # 不同的话取两者的最大值
            string[l] = string[r] = max(s[l], s[r])
            # 可修改次数-1
            k -= 1
        l += 1
        r -= 1
    if (k < 0):
        return "Not possible"
    l = 0
    r = len(s) - 1

    # 上面的步骤已经将数字修改为回文数了
    while (l <= r):
        if (l == r):
            if (k > 0):
                string[l] = '9'
        if (string[l] < '9'):
            if (k >= 2 and string[l] == s[l] and string[r] == s[r]):
                k -= 2
                string[l] = string[r] = '9'
        l += 1
        r -= 1
    value = "".join(string)
    return value


a = palindrome('1921', 2)
b = palindrome('1921', 3)
c = palindrome('11122', 1)
d = palindrome('11119111', 4)
print(a)
print(b)
print(c)
print(d)


def reverse_engineer(seq):
    my_list = seq
    string = "".join(my_list)
    chars = list(string)
    char_dict = {}
    for i in chars:
        if i not in char_dict:
            char_dict[i] = 1
        else:
            char_dict[i] += 1
    new_list = []
    for key,value in char_dict.items():
        new_list.append(key)
    # 计算要用到的字符数目
    length = len(new_list)
    print(new_list)
    # for j in range(length ** 3):



# seq = ["b", "bc", "ab", "bc", "b", "abc", "b"]
# reverse_engineer(seq)


def make_trades(starting_cash, prices, crossovers):
    value = []
    stock_at = 0
    cash = starting_cash
    prices = prices
    crossovers = crossovers
    for i in range(len(prices)):
        added_value = (prices[i] - prices[i-1])/prices[i-1]
        try:
            time_index = crossovers[0][0]
            buy_index = crossovers[0][1]
            if i == time_index:
                if buy_index == 1:
                    stock_at = cash
                    cash = 0
                    value.append(stock_at)
                    crossovers = crossovers[1:]
                else:
                    if(stock_at == 0):
                        cash = value[i-1]
                        value.append(value[i-1])
                    else:
                        cash = value[i-1] + value[i-1]*added_value
                        stock_at = 0
                        value.append(cash)
                    crossovers = crossovers[1:]
            else:
                if cash == 0:
                    stock_at = value[i-1] + value[i-1]*added_value
                    value.append(stock_at)
                else:
                    value.append(cash)
        except (IndexError):
            added_value = (prices[i] - prices[i-1])/prices[i-1]
            if cash == 0:
                stock_at = value[i-1] + value[i-1]*added_value
                value.append(stock_at)
            else:
                value.append(cash)
    return [round(i, 2) for i in value]

values1 = make_trades(1.0, [2,4,6,5,1], [[1, 1], [3, 2]])
print(values1)