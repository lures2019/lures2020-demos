import cv2

global img
global point1, point2


# 截图转化
def on_mouse(event, x, y, flags, param):
    global img, point1, point2
    img2 = img.copy()
    if event == cv2.EVENT_LBUTTONDOWN:  # 左键点击
        point1 = (x, y)
        cv2.circle(img2, point1, 10, (0, 255, 0), 5)
        cv2.imshow('image', img2)
    elif event == cv2.EVENT_MOUSEMOVE and (flags & cv2.EVENT_FLAG_LBUTTON):  # 按住左键拖曳
        cv2.rectangle(img2, point1, (x, y), (0, 0, 0), 5)  # 图像，矩形顶点，相对顶点，颜色，粗细
        cv2.imshow('image', img2)
    elif event == cv2.EVENT_LBUTTONUP:  # 左键释放
        point2 = (x, y)
        cv2.rectangle(img2, point1, point2, (0, 0, 255), 5)
        cv2.imshow('image', img2)
        min_x = min(point1[0], point2[0])
        min_y = min(point1[1], point2[1])
        width = abs(point1[0] - point2[0])
        height = abs(point1[1] - point2[1])
        cut_img = img[min_y:min_y + height, min_x:min_x + width]
        resize_img = cv2.resize(cut_img, (32, 32))  # 调整图像尺寸为32*32
        ret, thresh_img = cv2.threshold(resize_img, 127, 255, cv2.THRESH_BINARY)  # 二值化
        cv2.imshow('result', thresh_img)
        cv2.imwrite('./images/{}.png'.format(param), thresh_img)  # 预处理后图像保存位置


# 保存图片
def main_hand(read_png_name='src', save_png_name='text'):
    global img
    img = cv2.imread('./images/{}.png'.format(read_png_name))  # 手写数字图像所在位置
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # 转换图像为单通道(灰度图)
    cv2.namedWindow('image')
    cv2.setMouseCallback('image', on_mouse, param=save_png_name)  # 调用回调函数
    cv2.imshow('image', img)
    cv2.waitKey(7000)
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main_hand('src', 'text')
