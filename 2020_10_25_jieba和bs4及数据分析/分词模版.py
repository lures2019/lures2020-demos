#中文分词
import jieba #结巴库使用来处理中文分词的模块
import jieba.analyse #引入关键词提取模块

txt = open(r'C:\Users\Administrator\Desktop\新建文件夹\11.txt','r',encoding='utf-8').read()#打开文件，可将待分析的文件完整地址替换第一对引号里的地址即可
words = jieba.lcut(txt)#文本处理成了一个一个的词并以列表输出
#print(words)
counts = {} #建立一个空字典
for word in words:
    if len(word) ==1:#词只有1个字
        continue#不要了
    else:
        counts[word] = counts.get(word,0) + 1 #如果词不是1个字，则将该词打入字典，并以键值对方式对这个词进行计数
        #print(counts)
items = list (counts.items())
#print(items)
i=items.sort(key=lambda x:x[1],reverse = True) #大到小排序 如果你需要从小到大排列 reverse= False
for i in range(20):#数字是代表输出的词的个数，如需要输出前10，则将5改为10
    word,count = items[i]
    print('{0:<10}{1:>5}'.format(word,count))
    #字符串的format()方法，将word和count的取值以{0:<10}{1:>5}的格式填入，其中word对应填入0的位置，count则是1的位置
#    #{0:<10}{1:>5}，{}为槽，:为引导符，其后为格式控制方法。<表示左对齐，>表示右对齐，数字表示宽度
KW = jieba.analyse.textrank(txt) #对文本进行关键词提取，默认以列表形式返回前20个关键词。
print (KW)
