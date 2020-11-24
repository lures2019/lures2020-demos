import numpy as np
import pandas as pd
import warnings
# python开发中经常遇到报错的情况，但是warning通常并不影响程序的运行，而且有时特别讨厌,使用此方法即可
warnings.filterwarnings('ignore')

df = pd.read_csv('../数据集/telecom_churn.csv')
# 打印前武行数据
print(df.head())
# 查看数据库的维度/特征名称及特征类型
print(df.shape)
# 查看列名
print(df.columns)