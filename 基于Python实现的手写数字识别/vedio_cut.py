import cv2


# 获取本地摄像头
def get_img_from_camera_local(filename='src'):
    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        cv2.imshow("capture", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        else:
            cv2.imwrite('images/' + filename + '.png', frame)  # 存储为图像
    cap.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    get_img_from_camera_local()
