"""
    实际练习：实现一个满足以下规范的函数
    测试案例：
        [1,2,46]
        [2,3,5]
"""
def findAnEven(L):
    """假设L是一个整数列表
        返回L中的第一个偶数
        如果L中没有偶数，则抛出ValueError异常"""
    my_list = L
    try:
        if my_list[0] % 2 == 0:
            return my_list[0]
        else:
            return f"You entered {my_list[0]},which is not an even number."
    except ValueError as ve:
        return ve

if __name__ == '__main__':
    L1 = [1,2,46]
    L2 = [2,3,5]
    print(findAnEven(L1))
    print(findAnEven(L2))