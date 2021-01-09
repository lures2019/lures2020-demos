"""
    使用for循环，输入倒数秒数，进行倒数计时！
"""
import time

# 使用input()语句接收用户输入的倒计时数值
countdown = int(input("请输入倒数秒数 :"))
print("\n倒数计时开始")
for i in range(countdown):
    print("倒数 {} 秒".format(countdown - i))
    # 1s钟休眠1次
    time.sleep(1)
print("结束")