import pywifi
from pywifi import const        #引入一些常量


#判断是否已经连接WiFi
def wifi_connect():
    # 创建无线对象
    wifi = pywifi.PyWiFi()

    # <pywifi.iface.Interface object at 0x0000014BC4ED8128>,存放内存地址
    ifaces = wifi.interfaces()[0]

    # 打印当前网卡的名称:Intel(R) Dual Band Wireless-AC 3168
    # print(ifaces.name())

    # 打印当前网卡的连接状态,0表示未连接到WiFi环境，4表示已连接
    # print(ifaces.status())
    # 可以直接将const.IFACE_CONNECTED替换成4
    if ifaces.status() == const.IFACE_CONNECTED:
        print('已连接到WiFi环境！')
    else:
        print('未连接到WiFi环境！')

# 扫描附近的WiFi
def wifi_around():
    wifi = pywifi.PyWiFi()
    ifaces = wifi.interfaces()[0]

    #扫描WiFi
    ifaces.scan()
    #获取扫描结果
    result = ifaces.scan_results()
    for wifi_name in result:
        # 打印WiFi的名称
        print(wifi_name.ssid)

wifi_around()