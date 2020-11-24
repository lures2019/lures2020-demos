import pandas as pd
import csv
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

f1 = open('Task/7_企业信息.csv',mode='r',encoding='utf-8')
csv_reader = csv.reader(f1)
# 创建一个字典，统计最后一个行业的信息
my_dict1 = {}
for row in csv_reader:
    if row[-1] == '行业':
        pass
    else:
        if row[-1] not in my_dict1:
            my_dict1[row[-1]] = 1
        else:
            my_dict1[row[-1]] += 1
# 存储所有行业的名称
names = []
for key,value in my_dict1.items():
    names.append(key)
numbers = [i for i in range(len(names))]
# 构建真正的字典信息，在处理时进行替换
my_dict = {}
for i in range(len(names)):
    my_dict[names[i]] = numbers[i]



pima = pd.read_csv('Task/7_企业信息.csv',encoding='utf-8')
pima.rename(columns={'是否违约':'isrun'},inplace=True)
pima.rename(columns={'行业':'bussiness'},inplace=True)
# 使用map映射将[是否违约]中的是和否分别变成1和0
pima.isrun = pima.isrun.astype(str).map({'否':0,'是':1})
pima.bussiness = pima.bussiness.astype(str).map(my_dict)
# 其中最后一列是需要预测的因变量，其他特征是自变量
X = pima[['有效合作单位数','进项作废/有效比%','净利润','bussiness','销项有效合作单位数','销项作废/有效比%','进项月份时长','进项平均每月金额','进项负数发票次数','进项负数发票次数占比','销项月份时长','销项平均每月金额','销项负数发票次数','销项负数发票次数占比']]
y = pima['isrun']

# 训练：测试=7：3
X_train,X_test,y_train,y_test=train_test_split(X,y,test_size=0.3, random_state=1)
# 存放不同取值，以及对应精度，每一个元素都是三元组(a,b,c)
results = []
sample_leaf_options = list(range(1,304,3))
n_estimators_options = list(range(1,304,5))

for leaf_size in sample_leaf_options:
    for n_estimators in n_estimators_options:
        alg = RandomForestClassifier(min_samples_leaf=leaf_size,n_estimators=n_estimators, random_state=1)
        alg.fit(X_train,y_train)
        predict = alg.predict(X_test)

        results.append((leaf_size,n_estimators,(y_test==predict).mean()))
print(max(results,key=lambda x:x[2]))
