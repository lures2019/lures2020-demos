import pandas as pd

df = pd.read_excel('../datasets/桂林市1951-2014年月降水量.xls')
# index = None的作用是去除开头的索引，至于编码的作用是打开csv不显示出乱码
df.to_csv('../datasets/archive.csv',encoding = "utf-8-sig",index = None)
