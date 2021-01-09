"""
    设计一个银行账户管理程序，账户的信息有账号（唯一）、姓名、余额、身份证号码、单位、电话号码、地址等，
        允许用户进行如下操作：开户、销户、存款、取款、转账、查询。
        要求程序运行时，可以由用户选择进行何种操作，开户操作要求输入用户信息后自动获取账号，用户销户后账号被回收，不允许用户透支，
        根据姓名或账号可以进行用户的信息查询，所有账户信息应存放到一个文件中，可以随时的访问和更新！
"""
import datetime
import csv

# 1、创建原始菜单：开户、销户、存款、取款、转账、查询
def show_menu():
    """ 显示菜单栏 """
    menu = """
    ====================银行账户资金交易管理====================
    |   0: 开户                                               |
    |   1: 销户                                               |
    |   2: 存款                                               |
    |   3: 取款                                               |
    |   4：转账                                               |
    |   5：查询                                               |
    |   6：退出                                               |
    ===========================================================
     """
    print(menu)

# 2、开户
def open_an_account():
    """考虑到datatime时间具有唯一性，根据此创建账户"""
    # .replace("-","")意思是将-用空格代替，于是time便表示账户编号
    time = list(str(datetime.datetime.now()).split(" "))[0].replace("-","") + list(str(datetime.datetime.now()).split(" "))[1].split(".")[0].replace(":","")
    # 因为time的唯一性，所以可以省略判断是否早有此账户存在的可能
    f = open("账户信息.csv",mode='a+',newline="",encoding="utf-8-sig")
    csv_write = csv.writer(f)
    # 让用户输入姓名、身份证号码、单位、电话号码和地址信息（一行录入，空格为间隔）
    infor_to_enter = list(input("正在为您开户，请输入姓名、身份证号码、单位、电话号码和地址信息：").split(" "))
    # 录入信息到 账户信息.csv文件中
    csv_write.writerow([time,infor_to_enter[0],0.0,infor_to_enter[1],infor_to_enter[2],infor_to_enter[3],infor_to_enter[4]])
    print("已为您开户，分配账户编号为：{}".format(time))
    """
        测试案例：
            张三 342901200011151115 国企 110119120 南阳街
    """



# 3、销户
def delete_an_account():
    f = open("账户信息.csv", mode='r', encoding="utf-8")
    csv_reader = csv.reader(f)
    # 用户输入要销户的编号
    time = input("请输入您要注销的账户编号：")
    # 将所有的账户信息存放到一个大列表中，方便遍历
    rows = [i for i in csv_reader]
    # 因为第一行是标头，省略
    # 根据rows重写文件
    fp = open("账户信息.csv", mode='w', newline="", encoding="utf-8-sig")
    csv_write = csv.writer(fp)
    for row in rows:
        if row[0] == time:
            # 开始匹配到我们的账户编号
            del row
        else:
            csv_write.writerow(row)
    print("您的账户已注销，希望下次合作！")


# 4、存款
def save_money():
    # 得到用户的编号
    time = input("请输入您要充值的账户编号：")
    money = float(input("请输入您要充值的额度："))
    # 开始读文件，匹配time
    f = open("账户信息.csv", mode='r', encoding="utf-8")
    csv_reader = csv.reader(f)
    # 将所有的账户信息存放到一个大列表中，方便遍历
    rows = [i for i in csv_reader]
    # 因为第一行是标头，省略
    # 根据rows重写文件
    fp = open("账户信息.csv", mode='w', newline="", encoding="utf-8-sig")
    csv_write = csv.writer(fp)
    csv_write.writerow(rows[0])
    for row in rows[1:]:
        if row[0] == time:
            # 开始匹配到我们的账户编号
            row[2] = str(float(row[2]) + money)
            csv_write.writerow(row)
        else:
            csv_write.writerow(row)
    print("已为您{}的账户充值{}元".format(time,money))

# 5、取款
def waste_money():
    # 得到用户的编号
    time = input("请输入您要取款的账户编号：")
    money = float(input("请输入您要取款的额度："))
    # 开始读文件，匹配time
    f = open("账户信息.csv", mode='r', encoding="utf-8")
    csv_reader = csv.reader(f)
    # 将所有的账户信息存放到一个大列表中，方便遍历
    rows = [i for i in csv_reader]
    # 因为第一行是标头，省略
    # 根据rows重写文件
    fp = open("账户信息.csv", mode='w', newline="", encoding="utf-8-sig")
    csv_write = csv.writer(fp)
    csv_write.writerow(rows[0])
    for row in rows[1:]:
        if row[0] == time:
            # 开始匹配到我们的账户编号
            if float(row[2]) - money < 0:
                print("您{}的账户额度不足{}元，取款失败！".format(time, money))
                csv_write.writerow(row)
            else:
                row[2] = str(float(row[2]) - money)
                csv_write.writerow(row)
                print("已为您{}的账户已支出{}元,剩余额度{}元".format(time, money,row[2]))
        else:
            csv_write.writerow(row)


# 6、查询
def view_account():
    time = input("请输入您要查询的账户编号：")
    f = open("账户信息.csv", mode='r', encoding="utf-8")
    csv_reader = csv.reader(f)
    # 将所有的账户信息存放到一个大列表中，方便遍历
    rows = [i for i in csv_reader]
    status = False
    for row in rows[1:]:
        if time == row[0]:
            status = True
            print("您账户的信息如下：账户编号：{}、姓名：{}、余额：{}、身份证号码：{}、单位：{}、电话号码：{}、地址：{}".format(row[0],row[1],row[2],row[3],row[4],row[5],row[6]))
        else:
            pass
    if status == False:
        print("抱歉！未查到对应的信息，请确认账户是否已注销！")


# 7、转账
def sand_money():
    # 得到用户的编号
    time = input("请输入您的账户编号：")
    money = float(input("请输入您要转账的额度："))
    user = input("请输入您要充值的账户编号：")
    # 开始读文件，匹配time
    f = open("账户信息.csv", mode='r', encoding="utf-8")
    csv_reader = csv.reader(f)
    # 将所有的账户信息存放到一个大列表中，方便遍历
    rows = [i for i in csv_reader]
    # 因为第一行是标头，省略
    # 根据rows重写文件
    fp = open("账户信息.csv", mode='w', newline="", encoding="utf-8-sig")
    csv_write = csv.writer(fp)
    csv_write.writerow(rows[0])
    accounts = []
    for row in rows[1:]:
        accounts.append(row[0])
    if user in accounts:
        for row in rows[1:]:
            if row[0] == time:
                # 开始匹配到我们的账户编号
                if float(row[2]) - money < 0:
                    print("您{}的账户额度不足{}元，取款失败！".format(time, money))
                    csv_write.writerow(row)
                else:
                    row[2] = str(float(row[2]) - money)
                    csv_write.writerow(row)
                    print("已为您{}的账户已支出{}元,剩余额度{}元".format(time, money, row[2]))
            elif row[0] == user:
                row[2] = str(float(row[2]) + money)
                csv_write.writerow(row)
            else:
                csv_write.writerow(row)
    else:
        print("您要充值的账户在本银行未开户，无法转账！")
        for row in rows[1:]:
            csv_write.writerow(row)


# 8、循环操作
def goon(i):
    i = i
    while i != 6:
        if i == 0:
            open_an_account()
        elif i == 1:
            delete_an_account()
        elif i == 2:
            save_money()
        elif i == 3:
            waste_money()
        elif i == 4:
            sand_money()
        elif i == 5:
            view_account()
        i = int(input("请选择您要继续的操作编号："))
        goon(i)
    print("谢谢使用本系统！下次再见~")


if __name__ == '__main__':
    # w表示给文件写操作，encoding设置编码，不设置此则会乱码
    f = open("账户信息.csv",mode='w',newline="",encoding="utf-8-sig")
    csv_write = csv.writer(f)
    # 这是csv文件的其实标头
    csv_write.writerow(['账户编号','姓名','余额','身份证号码','单位','电话号码','地址'])
    f.close()
    show_menu()
    # 获取用户输入的编号
    i = int(input("请根据对应的编号选择对应的功能，如：0表示开户"))
    goon(i)
