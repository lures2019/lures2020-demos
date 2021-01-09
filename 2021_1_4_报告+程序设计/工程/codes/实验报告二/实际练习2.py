"""
    实际练习：实现一个满足以下规范的函数。请使用try-except代码块
    测试案例：
        a2b3c
"""
def sumDights(s):
    """假设S是一个字符串
        返回S中十进制数字之和
        例如：如果S是'a2b3c',则返回5"""
    string = s
    # 创建变量count，初始化为0
    count = 0
    for i in string:
        try:
            if i in '0123456789':
                count += eval(i)
        except Exception as error:
            # return error
            pass
    return count

# 执行主程序，格式记住就好
if __name__ == '__main__':
    s = "a2b3c"
    print(sumDights(s))