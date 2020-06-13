"""
    title：个人收支管理系统
    author:lures smith
    date:2020/06/13
"""
import csv


# 编写系统主界面，后面根据界面一一完成功能
print("**********************************欢迎使用[个人收支管理系统]**********************************")
for i in range(10):
    if (i <= 1):
        print("*                                                                                         *")
    else:
        if (i == 2):
            print("*                                        a、个人收入                                       *")
        elif (i == 3):
            print("*                                        b、个人支出                                       *")
        elif (i == 4):
            print("*                                        c、文件保存                                       *")
        elif (i == 5):
            print("*                                        d、每月明细                                       *")
        elif (i == 6):
            print("*                                        e、每月净获                                       *")
        elif (i == 7):
            print("*                                        f、退出系统                                       *")
        else:
            pass
print("*******************************************************************************************")


# 将收入和支出分别作为一个功能来实现，在原题基础行有所更改!
def function(param):
    string = param
    # 在⽤户输⼊明细之前，输出类别编码和类别名称的对应提示
    dict_a = {
        'a1':'生活费',
        'a2':'微信公众号广告',
        'a3':'Youtube广告',
        'a4':'外包',
        'a5':'中介返利'
    }
    dict_b = {
        'b1': '学习用品',
        'b2': '在线付费课程',
        'b3': '美食',
        'b4': '旅游',
        'b5': '住宿',
        'b6':'礼物'
    }
    # 列表存放特殊格式的字典的键值对拼接的字符串
    kinds_list = []
    # ⽤户输⼊收⽀明细，具体的输⼊格式如下（各数据⽤英⽂逗号分隔,直接输⼊回⻋表示输⼊结束）：
    if (string == 'a'):
        # 存放个人收支信息的文件
        f = open('个人收支信息.csv', mode="a+", newline="",encoding="utf-8-sig")
        csv_write = csv.writer(f)
        for key ,value in dict_a.items():
            kinds_list.append(key + '-' + value)
        print('收入类的具体类别编码及类别名称如下：'+ '\n\t'+str(kinds_list)+'\n')
        print('请逐笔输⼊类别编码、发⽣⽇期、⾦额、备注（各数据⽤英⽂逗号分隔,直接输⼊回⻋表示输⼊结束）')

        # 获取用户输入
        while True:
            message = input('请输入收入明细：')
            csv_write.writerow(message.split(','))
            if (len(message) == 0):
                break
        f.close()
        yes_or_no = input("是否继续使用本系统？(输入y代表是，其他输出代表退出)").strip()
        if yes_or_no == 'y':
            string = input("请输入要进行的操作的指令：")
            is_not_right_order(string)
        else:
            pass


    if (string == 'b'):
        # 存放个人收支信息的文件
        f = open('个人收支信息.csv', mode="a+", newline="",encoding="utf-8-sig")
        csv_write = csv.writer(f)
        for key ,value in dict_b.items():
            kinds_list.append(key + '-' + value)
        print('\n'+'支出类的具体类别编码及类别名称如下：'+ '\n\t'+str(kinds_list))

        # 获取用户输入
        while True:
            message = input('请输入收入明细：')
            csv_write.writerow(message.split(','))
            if (len(message) == 0):
                break
        f.close()
        yes_or_no = input("是否继续使用本系统？(输入y代表是，其他输出代表退出)").strip()
        if yes_or_no == 'y':
            string = input("请输入要进行的操作的指令：")
            is_not_right_order(string)
        else:
            pass

    if string == 'c':
        print('文件已保存在当前路径下！')
        yes_or_no = input("是否继续使用本系统？(输入y代表是，其他输出代表退出)").strip()
        if yes_or_no == 'y':
            string = input("请输入要进行的操作的指令：")
            is_not_right_order(string)
        else:
            pass


    if string == 'd':
        with open('个人收支信息.csv',mode="r",encoding="utf-8") as f:
            message = input("请输入对收支类别数据进行汇总的月份：")
            print("收入/支出",'\t','明细类别','\t','金额')
            csv_reader = csv.reader(f)
            for row in csv_reader:
                if len(row) != 4:
                    pass
                else:
                    if(message.strip() in row[1]):
                        if('a' in row[0]):
                            print('收入'+'\t'+row[3]+'\t'+str(row[2]))
                        else:
                            print('支出' + '\t' + row[3] + '\t' + str(row[2]))
        f.close()
        with open('个人收支信息.csv', mode="r", encoding="utf-8") as f:
            is_or_not = input("\n"+"是否输出该⽉的各笔明细（y为输出，其他为不输出）：")
            csv_reader = csv.reader(f)
            if (is_or_not.strip() == 'y'):
                print("\n"+message+"收支类别数据的明细：")
                print('\n'+ '类别'+'\t'+'收入/支出'+'\t'+'发生日期'+'\t'+'金额'+'\t'+'备注')
                for row in csv_reader:
                    if len(row) != 4:
                        pass
                    else:
                        if (message.strip() in row[1]):
                            if ('a' in row[0]):
                                print(row[3]+'\t'+'收入' + '\t' + row[1] + '\t' + str(row[2]))
                            else:
                                print(row[3]+'\t'+'支出' + '\t' + row[1] + '\t' + str(row[2]))
                else:
                    pass
        yes_or_no = input("是否继续使用本系统？(输入y代表是，其他输出代表退出)").strip()
        if yes_or_no == 'y':
            string = input("请输入要进行的操作的指令：")
            is_not_right_order(string)
        else:
            pass

    if string == 'e':
        with open('个人收支信息.csv', mode="r", encoding="utf-8") as f:
            num = 0
            message = input("请输入对收支类别数据进行汇总的月份：")
            csv_reader = csv.reader(f)
            for row in csv_reader:
                if len(row) != 4:
                    pass
                else:
                    if (message.strip() in row[1]):
                        if ('a' in row[0]):
                            num += float(row[2])
                        else:
                            num -= float(row[2])
        print(message+'\t'+'收支净收入是：{}'.format(num))
        yes_or_no = input("是否继续使用本系统？(输入y代表是，其他输出代表退出)").strip()
        if yes_or_no == 'y':
            string = input("请输入要进行的操作的指令：")
            is_not_right_order(string)
        else:
            pass


    if string == 'f':
        print("感谢使用本系统！下次再见！")


# 获取用户输入的指令
string = input("请输入要进行的操作的指令：")
def is_not_right_order(parma):
    string = parma
    if (string in "abcdef") and (len(string.strip()) == 1):
        # 调用功能函数
        function(string.strip())
    else:
        print("您的输入有问题！请从新输入")
        string1 = input("请再次输入要进行的操作的指令：")
        # 调用此函数实现对于不符合指令的循环输入！
        is_not_right_order(string1)
is_not_right_order(string)


