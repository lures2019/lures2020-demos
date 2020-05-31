# 根据股票历史的开盘价、收盘价和成交量等特征值，从数学角度来预测股票未来的收盘价
import pandas as pd
import numpy as np
import math
import os
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

# 从文中获取数据
files = os.listdir('csv数据集')
path = '第二种模型预测图片'
if not os.path.exists(path):
    os.mkdir(path)
for file in files:
    origDf = pd.read_csv('csv数据集'+'/'+file, encoding='utf-8-sig')
    df = origDf[['Close', 'High', 'Low', 'Open', 'Turnover']]
    featureData = df[['Open', 'High', 'Turnover','Low']]
    # 划分特征值和目标值
    feature = featureData.values
    """
        设置了要预测的目标列是收盘价。在后续的代码中，需要将计算出开盘价、最高价、最低价和成交量
        这四个特征值和收盘价的线性关系，并在此基础上预测收盘价。
    """
    target = np.array(df['Turnover'])
    # 划分训练集/测试集
    feature_train, feature_test, target_train, target_test = train_test_split(feature, target, test_size=0.05)
    """
        通过调用train_test_split方法把包含在csv文件中的股票数据分成训练集和测试集，
        这个方法前两个参数分别是特征列和目标列，而第三个参数0.05则表示测试集的大小是总量的0.05。
        该方法返回的四个参数分别是特征值的训练集、特征值的测试集、要预测目标列的训练集和目标列的测试集。
    """
    pridectedDays = int(math.ceil(0.05 * len(origDf)))  # 预测天数
    lrTool = LinearRegression()                         # 建了一个线性回归预测的对象
    lrTool.fit(feature_train, target_train)  # 调用fit方法训练特征值和目标值的线性关系，请注意这里的训练是针对训练集的
    # 用特征值的测试集来预测目标值（即收盘价）。也就是说，是用多个交易日的股价来训练lrTool对象，并在此基础上预测后续交易日的收盘价
    predictByTest = lrTool.predict(feature_test)


    # 组装数据
    index = 0
    # 在前95%的交易日中，设置预测结果和收盘价一致
    while index < len(origDf) - pridectedDays:
        # 把训练集部分的预测股价设置成收盘价
        df.ix[index, 'predictedVal'] = origDf.ix[index, 'Turnover']
        # 设置了训练集部分的日期
        df.ix[index, 'Date'] = origDf.ix[index, 'Date']
        index = index + 1
    predictedCnt = 0

    # 在后5%的交易日中，用测试集推算预测股价
    while predictedCnt < pridectedDays:
        df.ix[index, 'predictedVal'] = predictByTest[predictedCnt]
        # 把df中表示测试结果的predictedVal列设置成相应的预测结果，同时也在后面的程序语句逐行设置了每条记录中的日期
        df.ix[index, 'Date'] = origDf.ix[index, 'Date']
        predictedCnt = predictedCnt + 1
        index = index + 1

    plt.figure()
    # 分别绘制了预测股价和真实收盘价，在绘制的时候设置了不同的颜色，也设置了不同的label标签值
    df['predictedVal'].plot(color="red", label='predicted Data')
    df['Turnover'].plot(color="blue", label='Real Data')
    # 通过调用legend方法，根据收盘价和预测股价的标签值，绘制了相应的图例
    plt.legend(loc='best')  # 绘制图例
    # 设置x坐标的标签
    # 设置了x轴显示的标签文字是日期，为了不让标签文字显示过密，设置了“每20个日期里只显示1个”的显示方式
    major_index = df.index[df.index % 20 == 0]
    major_xtics = df['Date'][df.index % 20 == 0]
    plt.xticks(major_index, major_xtics)
    plt.setp(plt.gca().get_xticklabels(), rotation=30)

    # 带网格线，且设置了网格样式
    plt.grid(linestyle='-.')
    plt.savefig(path + '/' + file.replace(r".csv",'-Turnover.png'))
    plt.show()
    """预测股价和真实价之间有差距，但涨跌的趋势大致相同。而且在预测时没有考虑到涨跌停的因素，所以预测结果的涨跌幅度比真实数据要大"""