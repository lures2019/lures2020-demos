import csv,os
import heapq


def requirement1():
    """
        1、verified_purchase = N删去，L是第12列,直接用if判断并写到新csv文件,顺便记录一下N和Y的数量各是多少
    """
    # 1.1、修改csv包的解析文件方式,第一个参数是模式名称，第二个参数用于自定义分割符(这里将分割符改成制表符，便于解析tsv格式)
    csv.register_dialect('mydialect', delimiter='\t', quoting=csv.QUOTE_ALL)
    fp = open('C:/Users/HP/Desktop/测试/m_1.csv',mode="w",newline="",encoding="utf-8-sig")
    csv_write = csv.writer(fp)
    csv_write.writerow(['marketplace','customer_id','review_id','product_id','product_parent','product_title','product_category','star_rating','helpful_votes','total_votes','vine','review_headline','review_body','review_date'])

    # 1.2、将自己的解析模式读入tsv文件
    with open('C:/Users/HP/Desktop/测试/m.tsv',mode="r",encoding="utf-8") as f:
        file_list = csv.reader(f,'mydialect')
        for line in file_list:
            if line[11] == 'Y':
                csv_write.writerow([line[0],line[1],line[2],line[3],line[4],line[5],line[6],line[7],line[8],line[9],line[10],line[12],line[13],line[14]])
        print('第一步需求完成！处理掉verified_purchase = N的数据！')
    f.close()


def requirement2():
    """
        2、Product_id  统计销售量
    """
    with open('C:/Users/HP/Desktop/测试/m_1.csv',mode="r",encoding="utf-8") as fp:
        reader = csv.reader(fp)
        column = [row[3] for row in reader]
        Product_id = []
        for i in range(1,len(column)):
            Product_id.append(column[i])
        print('第二步需求完成！销售量统计是{}'.format(len(set(Product_id))))


def requirement3():
    """
        3、相同用户id去掉，customer_id
    """
    fp = open('C:/Users/HP/Desktop/测试/m_1.csv', mode="r", encoding="utf-8")
    reader = csv.reader(fp)
    column = [row[1] for row in reader]

    marketplace = [row[0] for row in csv.reader(open('C:/Users/HP/Desktop/测试/m_1.csv', mode="r", encoding="utf-8"))]
    review_id = [row[2] for row in csv.reader(open('C:/Users/HP/Desktop/测试/m_1.csv', mode="r", encoding="utf-8"))]
    product_id = [row[3] for row in csv.reader(open('C:/Users/HP/Desktop/测试/m_1.csv', mode="r", encoding="utf-8"))]
    product_parent = [row[4] for row in csv.reader(open('C:/Users/HP/Desktop/测试/m_1.csv', mode="r", encoding="utf-8"))]
    product_title = [row[5] for row in csv.reader(open('C:/Users/HP/Desktop/测试/m_1.csv', mode="r", encoding="utf-8"))]
    product_category = [row[6] for row in csv.reader(open('C:/Users/HP/Desktop/测试/m_1.csv', mode="r", encoding="utf-8"))]
    star_rating = [row[7] for row in csv.reader(open('C:/Users/HP/Desktop/测试/m_1.csv', mode="r", encoding="utf-8"))]
    helpful_votes = [row[8] for row in csv.reader(open('C:/Users/HP/Desktop/测试/m_1.csv', mode="r", encoding="utf-8"))]
    total_votes = [row[9] for row in csv.reader(open('C:/Users/HP/Desktop/测试/m_1.csv', mode="r", encoding="utf-8"))]
    vine = [row[10] for row in csv.reader(open('C:/Users/HP/Desktop/测试/m_1.csv', mode="r", encoding="utf-8"))]
    review_headline = [row[11] for row in csv.reader(open('C:/Users/HP/Desktop/测试/m_1.csv', mode="r", encoding="utf-8"))]
    review_body = [row[12] for row in csv.reader(open('C:/Users/HP/Desktop/测试/m_1.csv', mode="r", encoding="utf-8"))]
    review_date = [row[13] for row in csv.reader(open('C:/Users/HP/Desktop/测试/m_1.csv', mode="r", encoding="utf-8"))]

    users = []
    for i in range(1, len(column)):
        users.append(column[i])
    # 有60个相同的用户id,其中2个相同id用户是58位，3个相同id用户是20910311,4个相同id用户是11773102
    user_dicts = {}
    for user in users:
        if user not in user_dicts:
            user_dicts[user] = 1
        else:
            user_dicts[user] += 1
    customer_ids = []
    same_ids = []
    for key in user_dicts.keys():
        if user_dicts[key] != 1:
            same_ids.append(key)
        else:
            customer_ids.append(key)
    f = open('C:/Users/HP/Desktop/测试/m_3.csv', mode="w", newline="", encoding="utf-8-sig")
    csv_write = csv.writer(f)
    csv_write.writerow(
        ['marketplace', 'customer_id', 'review_id', 'product_id', 'product_parent', 'product_title', 'product_category',
         'star_rating', 'helpful_votes', 'total_votes', 'vine', 'review_headline', 'review_body', 'review_date'])
    for j in range(1, len(column)):
        if column[j] in customer_ids:
            csv_write.writerow(
                [marketplace[j], column[j], review_id[j], product_id[j], product_parent[j], product_title[j],
                 product_category[j], star_rating[j], helpful_votes[j], total_votes[j], vine[j], review_headline[j],
                 review_body[j], review_date[j]])
    f.close()
    print('第三步需求完成！处理掉customer_id用户id相同的数据！')



def requirement4():
    """
        4. 加一列影响因子 
            vine用户  1600/12+helpful-（total-helpful）         单元格值是Y，第十列          helpful第八列，total第九列
            普通用户  helpful-（total-helpful）                 单元格值是N，第十列
            值为0       1（算出来的数如果是0的话就变成1，如果不是0的话就用算出来的那个数进行替代）
    """
    fp = open('C:/Users/HP/Desktop/测试/m_4.csv', mode="w", newline="", encoding="utf-8-sig")
    csv_write = csv.writer(fp)
    csv_write.writerow(
        ['marketplace', 'customer_id', 'review_id', 'product_id', 'product_parent', 'product_title', 'product_category',
         'star_rating', 'helpful_votes', 'total_votes', 'vine', 'Impact_factor', 'review_headline', 'review_body',
         'review_date'])

    marketplace = [row[0] for row in csv.reader(open('C:/Users/HP/Desktop/测试/m_3.csv', mode="r", encoding="utf-8"))]
    customer_id = [row[1] for row in csv.reader(open('C:/Users/HP/Desktop/测试/m_3.csv', mode="r", encoding="utf-8"))]
    review_id = [row[2] for row in csv.reader(open('C:/Users/HP/Desktop/测试/m_3.csv', mode="r", encoding="utf-8"))]
    product_id = [row[3] for row in csv.reader(open('C:/Users/HP/Desktop/测试/m_3.csv', mode="r", encoding="utf-8"))]
    product_parent = [row[4] for row in csv.reader(open('C:/Users/HP/Desktop/测试/m_3.csv', mode="r", encoding="utf-8"))]
    product_title = [row[5] for row in csv.reader(open('C:/Users/HP/Desktop/测试/m_3.csv', mode="r", encoding="utf-8"))]
    product_category = [row[6] for row in
                        csv.reader(open('C:/Users/HP/Desktop/测试/m_3.csv', mode="r", encoding="utf-8"))]
    star_rating = [row[7] for row in csv.reader(open('C:/Users/HP/Desktop/测试/m_3.csv', mode="r", encoding="utf-8"))]
    helpful_votes = [row[8] for row in csv.reader(open('C:/Users/HP/Desktop/测试/m_3.csv', mode="r", encoding="utf-8"))]
    total_votes = [row[9] for row in csv.reader(open('C:/Users/HP/Desktop/测试/m_3.csv', mode="r", encoding="utf-8"))]
    vines = [row[10] for row in csv.reader(open('C:/Users/HP/Desktop/测试/m_3.csv', mode="r", encoding="utf-8"))]
    review_headline = [row[11] for row in
                       csv.reader(open('C:/Users/HP/Desktop/测试/m_3.csv', mode="r", encoding="utf-8"))]
    review_body = [row[12] for row in csv.reader(open('C:/Users/HP/Desktop/测试/m_3.csv', mode="r", encoding="utf-8"))]
    review_date = [row[13] for row in csv.reader(open('C:/Users/HP/Desktop/测试/m_3.csv', mode="r", encoding="utf-8"))]

    for i in range(1, len(vines)):
        if 'microwave' in product_title[i]:
            # 只有一个vine用户第8297位用户
            if (vines[i] == 'Y'):
                Impact_factor = 1600 / 12 + (
                float(helpful_votes[i]) - (float(total_votes[i]) - float(helpful_votes[i])))
                if (Impact_factor == 0):
                    Impact_factor = 1
                csv_write.writerow(
                    [marketplace[i], customer_id[i], review_id[i], product_id[i], product_parent[i], product_title[i],
                     product_category[i], star_rating[i], helpful_votes[i], total_votes[i], vines[i], Impact_factor,
                     review_headline[i],
                     review_body[i], review_date[i]])
            else:
                Impact_factor = float(helpful_votes[i]) - (float(total_votes[i]) - float(helpful_votes[i]))
                if (Impact_factor == 0):
                    Impact_factor = 1
                csv_write.writerow(
                    [marketplace[i], customer_id[i], review_id[i], product_id[i], product_parent[i], product_title[i],
                     product_category[i], star_rating[i], helpful_votes[i], total_votes[i], vines[i], Impact_factor,review_headline[i],review_body[i], review_date[i]])
        else:
            pass
    fp.close()
    print('第四步需求完成！增加一列影响因子数据！')



def requirement5():
    """
        5. （1）单个人评论词汇 去重（评论中关键词出现多次 只记录一次）；
            review_headline     第13列
            review_body         第14行
           （2）计算总词数	
            e.g.: This is good，very good.  —>  This is good，very.
    """

    review_headline = [row[12] for row in csv.reader(open('C:/Users/HP/Desktop/测试/m_4.csv', mode="r", encoding="utf-8"))]
    review_body = [row[13] for row in csv.reader(open('C:/Users/HP/Desktop/测试/m_4.csv', mode="r", encoding="utf-8"))]

    total_words = [[] for i in range(1, len(review_body))]

    for i in range(1, len(review_body)):
        for j in range(len(review_headline[i].split())):
            if len(review_headline[i].split()[j].replace(r'.', '').replace(r'?', '').replace(r',', '').replace(r'!',
                                                                                                               '')) != 0:
                total_words[i - 1].append(
                    review_headline[i].split()[j].replace(r'.', '').replace(r'?', '').replace(r',', '').replace(r'!',''))
        for m in range(len(review_body[i].split())):
            if len(review_body[i].split()[m].replace(r'.', '').replace(r'?', '').replace(r',', '').replace(r'!','')) != 0:
                total_words[i - 1].append(
                    review_body[i].split()[m].replace(r'.', '').replace(r'?', '').replace(r',', '').replace(r'!', ''))

    fp = open('C:/Users/HP/Desktop/测试/m_4.csv', mode="r", encoding="utf-8")
    marketplace = [row[0] for row in csv.reader(open('C:/Users/HP/Desktop/测试/m_4.csv', mode="r", encoding="utf-8"))]
    customer_id = [row[1] for row in csv.reader(open('C:/Users/HP/Desktop/测试/m_4.csv', mode="r", encoding="utf-8"))]
    review_id = [row[2] for row in csv.reader(open('C:/Users/HP/Desktop/测试/m_4.csv', mode="r", encoding="utf-8"))]
    product_id = [row[3] for row in csv.reader(open('C:/Users/HP/Desktop/测试/m_4.csv', mode="r", encoding="utf-8"))]
    product_parent = [row[4] for row in csv.reader(open('C:/Users/HP/Desktop/测试/m_4.csv', mode="r", encoding="utf-8"))]
    product_title = [row[5] for row in csv.reader(open('C:/Users/HP/Desktop/测试/m_4.csv', mode="r", encoding="utf-8"))]
    product_category = [row[6] for row in csv.reader(open('C:/Users/HP/Desktop/测试/m_4.csv', mode="r", encoding="utf-8"))]
    star_rating = [row[7] for row in csv.reader(open('C:/Users/HP/Desktop/测试/m_4.csv', mode="r", encoding="utf-8"))]
    helpful_votes = [row[8] for row in csv.reader(open('C:/Users/HP/Desktop/测试/m_4.csv', mode="r", encoding="utf-8"))]
    total_votes = [row[9] for row in csv.reader(open('C:/Users/HP/Desktop/测试/m_4.csv', mode="r", encoding="utf-8"))]
    vines = [row[10] for row in csv.reader(open('C:/Users/HP/Desktop/测试/m_4.csv', mode="r", encoding="utf-8"))]
    Impact_factor = [row[11] for row in csv.reader(open('C:/Users/HP/Desktop/测试/m_4.csv', mode="r", encoding="utf-8"))]
    review_headline = [row[12] for row in csv.reader(open('C:/Users/HP/Desktop/测试/m_4.csv', mode="r", encoding="utf-8"))]
    review_body = [row[13] for row in csv.reader(open('C:/Users/HP/Desktop/测试/m_4.csv', mode="r", encoding="utf-8"))]
    review_date = [row[14] for row in csv.reader(open('C:/Users/HP/Desktop/测试/m_4.csv', mode="r", encoding="utf-8"))]

    f = open('C:/Users/HP/Desktop/测试/m_5.csv', mode="w", newline="", encoding="utf-8-sig")
    csv_write = csv.writer(f)
    csv_write.writerow(
        ['marketplace', 'customer_id', 'review_id', 'product_id', 'product_parent', 'product_title', 'product_category',
         'star_rating', 'helpful_votes', 'total_votes', 'vines', 'Impact_factor', 'review_headline', 'review_body',
         'total_words','words_number', 'review_date'])

    for t in range(len(total_words)):
        csv_write.writerow(
            [marketplace[t + 1], customer_id[t + 1], review_id[t + 1], product_id[t + 1], product_parent[t + 1],
             product_title[t + 1], product_category[t + 1], star_rating[t + 1], helpful_votes[t + 1],
             total_votes[t + 1], vines[t + 1], Impact_factor[t + 1], review_headline[t + 1], review_body[t + 1],
             list(set(total_words[t])),len(str(list(set(total_words[t]))).replace(r"'", '').replace(r",", '').replace(r"[", '').replace(r']', '').split()), review_date[t + 1]])
    f.close()
    print('第五步需求完成！增加用户评论总词数！')




def requirement6():
    """
        6.  (1)把句子分成单个的单词  按出现次数排序  列出一个表 ；(第十五列的单词数据)
            (2) 计算词频  
           （若过多，可保留前50词）。
            (3)创建分别包含正面单词和负面单词的词库，在m_5.csv文件中根据每一个total_words一列数据进行匹配，分别统计正面单词和负面单词的数量(影响因子
                的作用考虑进去作为一列，不考虑的情况又作为一列)并分别保存到m_6.csv文件的两列，最后是根据正面单词的数量和负面单词的数量相减的结果得出一个评分统计一下正面和负面的单词数目各是多少，
                最后根据正负词相减在某一范围的情况给出得出评分，放到一列！
    """
    fp = open('C:/Users/HP/Desktop/测试/m_5.csv', mode="r", encoding="utf-8")
    reader = csv.reader(fp)
    column = [row[14] for row in reader]
    f1 = open('C:/Users/HP/Desktop/测试/m_6.csv',mode="w",newline="",encoding="utf-8-sig")
    csv_write = csv.writer(f1)
    csv_write.writerow(['marketplace', 'customer_id', 'review_id', 'product_id', 'product_parent', 'product_title', 'product_category',
         'star_rating', 'helpful_votes', 'total_votes', 'vines', 'Impact_factor', 'review_headline', 'review_body',
         'total_words','words_number','Positive_words(No_Impact_factor)','Negative_words(No_Impact_factor)', 'scores(No_Impact_factor)',
            'Positive_words(Impact_factor)','Negative_words(Impact_factor)','scores(Impact_factor)','review_date'])

    marketplace = [row[0] for row in csv.reader(open('C:/Users/HP/Desktop/测试/m_5.csv', mode="r", encoding="utf-8"))]
    customer_id = [row[1] for row in csv.reader(open('C:/Users/HP/Desktop/测试/m_5.csv', mode="r", encoding="utf-8"))]
    review_id = [row[2] for row in csv.reader(open('C:/Users/HP/Desktop/测试/m_5.csv', mode="r", encoding="utf-8"))]
    product_id = [row[3] for row in csv.reader(open('C:/Users/HP/Desktop/测试/m_5.csv', mode="r", encoding="utf-8"))]
    product_parent = [row[4] for row in csv.reader(open('C:/Users/HP/Desktop/测试/m_5.csv', mode="r", encoding="utf-8"))]
    product_title = [row[5] for row in csv.reader(open('C:/Users/HP/Desktop/测试/m_5.csv', mode="r", encoding="utf-8"))]
    product_category = [row[6] for row in csv.reader(open('C:/Users/HP/Desktop/测试/m_5.csv', mode="r", encoding="utf-8"))]
    star_rating = [row[7] for row in csv.reader(open('C:/Users/HP/Desktop/测试/m_5.csv', mode="r", encoding="utf-8"))]
    helpful_votes = [row[8] for row in csv.reader(open('C:/Users/HP/Desktop/测试/m_5.csv', mode="r", encoding="utf-8"))]
    total_votes = [row[9] for row in csv.reader(open('C:/Users/HP/Desktop/测试/m_5.csv', mode="r", encoding="utf-8"))]
    vines = [row[10] for row in csv.reader(open('C:/Users/HP/Desktop/测试/m_5.csv', mode="r", encoding="utf-8"))]
    Impact_factor = [row[11] for row in csv.reader(open('C:/Users/HP/Desktop/测试/m_5.csv', mode="r", encoding="utf-8"))]
    review_headline = [row[12] for row in csv.reader(open('C:/Users/HP/Desktop/测试/m_5.csv', mode="r", encoding="utf-8"))]
    review_body = [row[13] for row in csv.reader(open('C:/Users/HP/Desktop/测试/m_5.csv', mode="r", encoding="utf-8"))]
    total_words = [row[14] for row in csv.reader(open('C:/Users/HP/Desktop/测试/m_5.csv', mode="r", encoding="utf-8"))]
    words_number = [row[15] for row in csv.reader(open('C:/Users/HP/Desktop/测试/m_5.csv', mode="r", encoding="utf-8"))]
    review_date = [row[16] for row in csv.reader(open('C:/Users/HP/Desktop/测试/m_5.csv', mode="r", encoding="utf-8"))]

    words = {}
    for i in range(1, len(column)):
        column[i] = str(column[i]).replace(r"'", '').replace(r",", '').replace(r"[", '').replace(r']', '').split()
        for word in column[i]:
            if word not in words:
                words[word] = 1 * int(float(Impact_factor[i]))
            else:
                words[word] += 1 * int(float(Impact_factor[i]))

    High_frequency_words = sorted(words.items(), key=lambda k: k[1])
    f = open('C:/Users/HP/Desktop/测试/m_6高频词汇统计(500个单词).txt', mode="w", encoding="utf-8")
    f.write('单词' + '\t' + '出现次数')
    f.write('\n')
    for j in range(len(High_frequency_words) - 500, len(High_frequency_words)):
        f.write(str(High_frequency_words[j]).replace(r"'", '').replace(',', '\t').replace(r'(', '').replace(r')', ''))
        f.write('\n')
    f.close()


    f_positive = open('C:/Users/HP/Desktop/测试/m正面词.txt',mode="r",encoding="utf-8")
    f_negative = open('C:/Users/HP/Desktop/测试/m负面词.txt',mode="r",encoding="utf-8")
    reader_positive = [row for row in csv.reader(f_positive)]
    reader_negative = [row for row in csv.reader(f_negative)]

    Positive_words_No_Impact_factor = [[] for i in range(len(total_words))]
    negative_words_No_Impact_factor = [[] for i in range(len(total_words))]
    scores_No_Impact_factor = [[] for i in range(len(total_words))]
    Positive_words_Impact_factor = [[] for i in range(len(total_words))]
    negative_words_Impact_factor = [[] for i in range(len(total_words))]
    scores_Impact_factor = [[] for i in range(len(total_words))]

    for p in range(1,len(total_words)):
        count = 0
        accumulate = 0
        for positive_word in reader_positive:
            if positive_word[0] in list(total_words[p].replace(r"'", '').replace(r",", '').replace(r"[", '').replace(r']', '').split()):
                count += 1
                accumulate += 1 * int(float(Impact_factor[p]))
            else:
                pass
        Positive_words_No_Impact_factor[p-1].append(count)
        Positive_words_Impact_factor[p-1].append(accumulate)
        add = 0
        multiply = 0
        for negative_word in reader_negative:
            if negative_word[0] in list(total_words[p].replace(r"'", '').replace(r",", '').replace(r"[", '').replace(r']', '').split()):
                add += 1
                multiply += 1 * int(float(Impact_factor[p]))
            else:
                pass
        negative_words_No_Impact_factor[p-1].append(add)
        negative_words_Impact_factor[p-1].append(multiply)

    for n in range(1,len(total_words)):
        numbers_No_Impact_factor = (Positive_words_No_Impact_factor[n - 1][0] - negative_words_No_Impact_factor[n - 1][0])
        numbers_Impact_factor = (Positive_words_Impact_factor[n - 1][0] - negative_words_Impact_factor[n - 1][0])


        if numbers_No_Impact_factor > 1:
            scores_No_Impact_factor[n - 1].append(5)
        elif numbers_No_Impact_factor == 1:
            scores_No_Impact_factor[n - 1].append(4)
        elif numbers_No_Impact_factor == 0:
            scores_No_Impact_factor[n - 1].append(3)
        elif numbers_No_Impact_factor == -1:
            scores_No_Impact_factor[n - 1].append(2)
        elif numbers_No_Impact_factor + 1 < 0:
            scores_No_Impact_factor[n - 1].append(1)

        if numbers_Impact_factor > 1:
            scores_Impact_factor[n - 1].append(5)
        elif numbers_Impact_factor == 1:
            scores_Impact_factor[n - 1].append(4)
        elif numbers_Impact_factor == 0:
            scores_Impact_factor[n - 1].append(3)
        elif numbers_Impact_factor == -1:
            scores_Impact_factor[n - 1].append(2)
        elif numbers_Impact_factor + 1 < 0:
            scores_Impact_factor[n - 1].append(1)




    for d in range(1,len(total_words)):
        csv_write.writerow([marketplace[d],customer_id[d],review_id[d],product_id[d],product_parent[d],product_title[d],
            product_category[d],star_rating[d],helpful_votes[d],total_votes[d],vines[d],Impact_factor[d],review_headline[d],
            review_body[d],total_words[d],words_number[d],Positive_words_No_Impact_factor[d-1][0],negative_words_No_Impact_factor[d-1][0],
            scores_No_Impact_factor[d-1][0],Positive_words_Impact_factor[d-1][0],negative_words_Impact_factor[d-1][0],scores_Impact_factor[d-1][0],review_date[d]])
    f1.close()
    print('第六步需求完成！保留用户评论词频最高500位及添加正负词数和得分情况！')




def requirement7():
    """
        7、按照product-id  取频率高的前8个产品作为样本     
           统计出每个产品id中 用户评论高频词出现的次数
    """
    fp = open('C:/Users/HP/Desktop/测试/m_5.csv', mode="r", encoding="utf-8")
    reader = csv.reader(fp)
    column = [row[3] for row in reader]
    comments = [row[14] for row in csv.reader(open('C:/Users/HP/Desktop/测试/m_6.csv', mode="r", encoding="utf-8"))]
    scores_No_Impact_factor = [row[18] for row in csv.reader(open('C:/Users/HP/Desktop/测试/m_6.csv', mode="r", encoding="utf-8"))]
    scores_Impact_factor = [row[21] for row in csv.reader(open('C:/Users/HP/Desktop/测试/m_6.csv', mode="r", encoding="utf-8"))]

    products = []
    for i in range(1, len(column)):
        products.append(column[i])
    product_ids = {}
    for product in products:
        if product not in product_ids:
            product_ids[product] = 1
        else:
            product_ids[product] += 1
    same_ids = [[], []]
    customer_ids = []
    # 一共是448个相同的product_id
    for key in product_ids.keys():
        if product_ids[key] != 1:
            same_ids[0].append(key)
            same_ids[1].append(product_ids[key])
        else:
            customer_ids.append(key)

    a = same_ids[1]
    # 已经找出出现频率最高的8个product_id，存在新的列表中
    subscripts = heapq.nlargest(8, range(len(a)), a.__getitem__)
    samples = []
    for j in subscripts:
        samples.append(same_ids[0][j])

    path = 'C:/Users/HP/Desktop/测试/m_7_product_ids'
    if not os.path.exists(path):
        os.mkdir(path)

    results = [[] for i in range(len(samples))]
    j = 0
    for sample in samples:
        f = open(path + '/' + sample + '.txt', mode="w", encoding="utf-8")
        Impact_factor = [row[11] for row in csv.reader(open('C:/Users/HP/Desktop/测试/m_5.csv', mode="r", encoding="utf-8"))]
        x = []
        count1 = 0
        count2 = 0
        for i in range(1, len(column)):
            if column[i] == sample:
                results[j].append(comments[i])
                x.append(comments[i])
                count1 += int(scores_No_Impact_factor[i])
                count2 += int(scores_Impact_factor[i])
        f.write('此产品id名称是：{}，在文件中出现的次数是{}次！'.format(sample, str(same_ids[1][subscripts[j]])))
        f.write('\n')
        f.write('考虑影响因子Impact_factor后{}总得分是{}'.format(sample,count2))
        f.write('\n')
        f.write('不考虑影响因子Impact_factor{}总得分是{}'.format(sample,count1))
        f.write('\n')
        words = {}
        for m in range(1, len(x)):
            x[m] = str(x[m]).replace(r"'", '').replace(r",", '').replace(r"[", '').replace(r']', '').split()
            for word in x[m]:
                if word not in words:
                    words[word] = 1 * int(float(Impact_factor[i]))
                else:
                    words[word] += 1 * int(float(Impact_factor[i]))
            High_frequency_words = sorted(words.items(), key=lambda k: k[1])
            for t in range(len(High_frequency_words)):
                f.write(str(High_frequency_words[t]).replace(r"'", '').replace(',', '\t').replace(r'(', '').replace(r')',''))
                f.write('\n')
        j += 1
        f.close()
    print('第七步需求完成！保留用户评论所有词频！')




if __name__ == '__main__':
    requirement1()
    requirement2()
    requirement3()
    requirement4()
    requirement5()
    requirement6()
    requirement7()
