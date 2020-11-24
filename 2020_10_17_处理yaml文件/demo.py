# 使用Python处理yaml文件
files = open('practice.yaml',mode='rb').readlines()
# f = open('practice.yaml',mode='r',encoding='utf-8')
with open('error.txt',mode='w') as f:
    for line in files:
        try:
            x = line.decode('utf-8').replace('\n','').strip()
            # print(eval(x)[1])
        except Exception as error:
            f.write(str(line))
            print(str(line))
            f.write('\n')
