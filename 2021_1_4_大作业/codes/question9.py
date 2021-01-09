"""
    使用类class
"""
class rectangle(object):
    # 定义矩形类
    def __init__(self,length,width):
        self.length = length
        self.width = width
    # 定义周长函数
    def perimeter(self):
        perimeter = (self.length + self.width) * 2
        print("周长为：{}".format(perimeter))
    # 定义面积函数
    def area(self):
        area = self.length * self.width
        print("面积为：{}".format(area))

if __name__ == '__main__':
    # 请输入矩形的长度
    length = int(input("请输入矩形长度："))
    # 请输入矩形的宽度
    width = int(input("请输入矩形宽度："))
    # 实例化类
    c = rectangle(length,width)
    c.perimeter()
    c.area()