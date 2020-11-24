"""
    题目：个人收支管理系统
    time:2020/6/14
"""

# Step1、设置系统的主界面
"""
    主界面的功能：
        1、个人收入支出
        2、收支明细
        3、查询
"""
print("---------------------------个人收支管理系统---------------------------")
for i in range(6):
    # 1、2行为了美观，空出
    if (i <= 1):
        print("*                                                                   *")
    elif(i == 2):
        print("*                           1.个人收入支出                           *")
    elif(i == 3):
        print("*                           2.收支明细                               *")
    elif(i == 4):
        print("*                           3.目前结余                               *")
    elif(i == 5):
        print("*                           4.高额消费记录                           *")
print("--------------------------------------------------------------------")
print("欢迎使用本系统，请根据显示的功能选择你需要进行的操作！(eg：输入1表示个人收入支出)！"+"\n")

# Step4、将输入的明细数据写入到一个文件中保存，便于以后进行追加和处理
f = open("个人收支信息.txt",mode="a+",encoding="utf-8")
f.close()


# 功能函数部分
def func(message):
    message = message
    kinds_dict = {
        'a1':'生活费',
        'a2':'红包',
        'a3':'家教',
        'a4':'兼职',
        'b1':'学习用品',
        'b2':'吃饭',
        'b3':'游戏',
        'b4':'旅游'
    }
    money_get = []              # 存储收入类各类名及编码
    money_out = []              # 存储支出类各类名及编码

    # Step3、输入明细信息
    if message == '1':
        # 使用列表存储字典的键值对信息
        for key,value in kinds_dict.items():
            if 'a' in key:
                money_get.append(str(key)+'-'+str(value))
            else:
                money_out.append(str(key)+'-'+str(value))
        print("\n"+"类别编码和类别名称的对应关系如下:")
        # 使用字符串的join方法将所有的列表元素以逗号间隔打印出
        print('\t'+"收如类："+','.join(money_get))
        print('\t'+"支出类："+','.join(money_out))
        print("\n"+"请逐笔输入类别编码、发生日期、金额、备注(各数据用英文逗号分隔，直接输入回车表示输入结束)：")
        # 通过while循环实现用户一直输入收支明细！
        while 1:
            message_now = input("输入收支明细：")
            with open('个人收支信息.txt',mode="a+",encoding="utf-8") as f:
                f.write(message_now+"\n")
            if(len(message_now.strip()) == 0):
                break
        # 由于系统不是一次性的，于是加入循环判断语句
        message_last = input("请问是否继续操作(输入y表示继续，其他任意键退出)：").strip()
        if message_last == 'y':
            string = input("请输入您要操作的功能代数(eg：1)：")
            get_input_message(string)


    # Step4、统计并输出用户所输入月份各收支类别的汇总情况
    if message == '2':
        message2 = input("请输入对收支类别数据进行汇总的月份(eg:2020-3)：").strip()
        print(message2.split('-')[0] + "年"+message2.split('-')[-1]+"月收支类别数据的汇总")
        print("收入/支出"+'\t'+"明细类别"+"\t"+"金额")
        total_get = 0
        total_lose = 0
        with open("个人收支信息.txt",mode="r",encoding="utf-8") as f:
            # 通过列表的形式将txt文件中的所有行内容存储到一个列表中
            data = f.readlines()
            for line in data:
                if(message2 in line):
                    if('a' in line):
                        # 通过split将字符串切割
                        print("收入"+'\t'+line.split(',')[-1].replace("\n",'')+ "\t"+line.split(',')[2])
                        total_get += float(line.split(',')[2])
                    else:
                        print("支出" + '\t' + line.split(',')[-1].replace("\n", '') + "\t" + line.split(',')[2])
                        total_lose += float(line.split(',')[2])
        print(message2.split('-')[0] + "年"+message2.split('-')[-1]+"月总收入为：{},总支出为:{}".format(total_get,total_lose))
        message_again = input("是否输出该月的各笔明细(y为输出，其他未不输出)：").strip()
        if message_again == 'y':
            print(message2.split('-')[0] + "年"+message2.split('-')[-1]+"月收支类别数据的明细：")
            print("类别"+ "\t" + "收入/支出"+"\t"+"发生日期"+"\t"+"金额"+"备注")
            with open("个人收支信息.txt", mode="r", encoding="utf-8") as f:
                # 通过列表的形式将txt文件中的所有行内容存储到一个列表中
                data = f.readlines()
                for line in data:
                    if (message2 in line):
                        if ('a' in line):
                            # 通过split将字符串切割,且根据字典的键取值
                            print(kinds_dict[line.split(',')[0]]+ '\t' + "收入" + "\t" + line.split(',')[1] + "\t" + line.split(',')[2] + "\t" + line.split(',')[-1].replace("\n", ''))
                        else:
                            print(kinds_dict[line.split(',')[0]]+ '\t' + "支出" + "\t" + line.split(',')[1] + "\t" + line.split(',')[2] + "\t" + line.split(',')[-1].replace("\n", ''))
            message_last = input("请问是否继续操作(输入y表示继续，其他任意键退出)：").strip()
            if message_last == 'y':
                string = input("请输入您要操作的功能代数(eg：1)：")
                get_input_message(string)
        else:
            message_last = input("请问是否继续操作(输入y表示继续，其他任意键退出)：").strip()
            if message_last == 'y':
                string = input("请输入您要操作的功能代数(eg：1)：")
                get_input_message(string)

    # Step5、统计文件中结余的钱
    if message == '3':
        print("查询个人目前结余金额为：")
        total = 0
        with open("个人收支信息.txt",mode="r",encoding="utf-8") as f:
            # 通过列表的形式将txt文件中的所有行内容存储到一个列表中
            data = f.readlines()
            for line in data :
                if len(line) != 1:
                    if('a' in line):
                        # 通过split将字符串切割
                        total += float(line.split(',')[2])
                    else:
                        total -= float(line.split(',')[2])
        print("目前结余金额为：{}".format(total))
        message_last = input("请问是否继续操作(输入y表示继续，其他任意键退出)：").strip()
        if message_last == 'y':
            string = input("请输入您要操作的功能代数(eg：1)：")
            get_input_message(string)


    # Step6、查询高额消费
    if message == '4':
        total1 = []
        total2 = []
        max1 = 0            # 统计收入最高
        max2 = 0            # 统计支出最高
        with open("个人收支信息.txt",mode="r",encoding="utf-8") as f:
            # 通过列表的形式将txt文件中的所有行内容存储到一个列表中
            data = f.readlines()
            for line in data :
                if len(line) != 1:
                    if('a' in line):
                        # 通过split将字符串切割
                        total1.append(line.split(',')[1] +'-' +line.split(',')[-1].replace("\n","")+ '-'+line.split(',')[2])
                        max1 = max(max1,float(line.split(",")[2]))
                    else:
                        total2.append(line.split(',')[1] +'-' + line.split(',')[-1].replace("\n","")+ '-' +line.split(',')[2])
                        max2 = max(max2, float(line.split(",")[2]))
        for i in range(len(total1)):
            if str(max1) in total1[i] or str(int(max1)) in total1[i]:
                print("收入最高额情况是：{}".format(total1[i]))
        for j in range(len((total2))):
            if str(max2) in total2[j] or str(int(max2)) in total2[j]:
                print("支出最高额情况是：{}".format(total2[j]))
        message_last = input("请问是否继续操作(输入y表示继续，其他任意键退出)：").strip()
        if message_last == 'y':
            string = input("请输入您要操作的功能代数(eg：1)：")
            get_input_message(string)



# Step2、任务一，构建一个函数来保证用户输入有误的情况下持续输入
def get_input_message(information):
    message = information
    if (message == '1'):
        func(message)
    elif (message == '2'):
        func(message)
    elif (message == '3'):
        func(message)
    elif (message == '4'):
        func(message)
    else:
        message_is_not_carry = input("您的输入有误！请问是继续操作(y)还是退出程序(除y外任意键)?").strip()
        if (message_is_not_carry == 'y'):
            message_new = input("请输入您要操作的功能代数(eg：1)：")
            # 为保证用户不输入正确的指令就一直无法进行功能测试，函数内部调用本函数
            get_input_message(message_new)
        else:
            print("感谢使用本系统！下次再见哦~~")
# 使用strip()实现去除空格
message = input("请输入您要操作的功能代数(eg：1)：").strip()
get_input_message(message)



