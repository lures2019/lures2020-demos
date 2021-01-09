from xlrd import open_workbook
import csv
import numpy as np
import pandas as pd
from pandas import DataFrame
import matplotlib.pyplot as plt
from pylab import mpl
mpl.rcParams['font.sans-serif'] = ['FangSong']
mpl.rcParams['axes.unicode_minus'] = False


wb = open_workbook("./第三题数据.xlsx")
# sheet_names = wb.sheet_names()    
sheet = wb.sheet_by_name('Sheet1')
nrows = sheet.nrows
rows = []
f = open("第四题数据.csv", mode="w", newline="", encoding="utf-8-sig")
csv_write = csv.writer(f)
headlines = [eval(str(i).split(":")[-1]) for i in sheet.row(0)]
needs = []
for i in range(len(headlines)):
    if i in [0,3,5,6,8,9,11,14,18,20,25]:
        pass
    else:
        needs.append(headlines[i])
csv_write.writerow(needs)

for i in range(1, nrows):
    my_list = sheet.row(i)
    row = []
    if eval(str(my_list[1]).split(":")[-1]) == 0.0:
        pass
    else:
        for j in range(len(my_list)):
            if j in [0,3,5,6,8,9,11,14,18,20,25]:
                pass
            else:
                now = eval(str(my_list[j]).split(":")[-1])
                row.append(now)
        csv_write.writerow(row)
print("over~")

df_org = pd.read_csv("第四题数据.csv")
df_std = (df_org - df_org.mean()) / df_org.std()
df_corr = df_std.corr()
print(df_corr)

eig_value, eig_vector = np.linalg.eig(df_corr)
eig = pd.DataFrame({"eig_value": eig_value})
eig = eig.sort_values(by=["eig_value"], ascending=False)
eig["eig_cum"] = (eig["eig_value"] / eig["eig_value"].sum()).cumsum()
eig = eig.merge(pd.DataFrame(eig_vector).T, left_index=True, right_index=True)
print(eig)


loading = eig.iloc[:2,2:].T
loading["vars"]=df_std.columns
print(loading)


score = pd.DataFrame(np.dot(df_std,loading.iloc[:,0:2]))
print(score)

plt.plot(loading[0],loading[1], "o")
xmin ,xmax = loading[0].min(), loading[0].max()
ymin, ymax = loading[1].min(), loading[1].max()
dx = (xmax - xmin) * 0.2
dy = (ymax - ymin) * 0.2
plt.xlim(xmin - dx, xmax + dx)
plt.ylim(ymin - dy, ymax + dy)
plt.xlabel('First')
plt.ylabel('Second')
for x, y,z in zip(loading[0], loading[1], loading["vars"]):
    plt.text(x, y+0.1, z, ha='center', va='bottom', fontsize=13)
plt.grid(True)
plt.show()

plt.plot(score[0],score[1], "o")
xmin ,xmax = score[0].min(), score[0].max()
ymin, ymax = score[1].min(), score[1].max()
dx = (xmax - xmin) * 0.2
dy = (ymax - ymin) * 0.2
plt.xlim(xmin - dx, xmax + dx)
plt.ylim(ymin - dy, ymax + dy)
plt.xlabel('First')
plt.ylabel('Second')
for x, y,z in zip(score[0], score[1], score.index):
    plt.text(x, y+0.1, z, ha='center', va='bottom', fontsize=13)
plt.grid(True)
plt.show()

