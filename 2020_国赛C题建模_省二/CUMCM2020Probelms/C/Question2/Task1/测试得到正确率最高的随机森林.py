import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split


pima = pd.read_csv('../../Question1/Task1/7_处理后企业信息.csv',encoding='utf-8')
pima.rename(columns={'是否违约':'isrun'},inplace=True)
# 使用map映射将[是否违约]中的是和否分别变成1和0
pima.isrun = pima.isrun.astype(str).map({'否':0,'是':1})
# 其中最后一列是需要预测的因变量，其他特征是自变量
X = pima[['有效合作单位数','进项作废/有效比%','净利润','销项有效合作单位数','销项作废/有效比%','进项月份时长','进项平均每月金额','进项负数发票次数','进项负数发票次数占比','销项月份时长','销项平均每月金额','销项负数发票次数','销项负数发票次数占比']]
y = pima['isrun']

# 训练：测试=7：3
X_train,X_test,y_train,y_test=train_test_split(X,y,test_size=0.3, random_state=1)
# 存放不同取值，以及对应精度，每一个元素都是三元组(a,b,c)
results = []
sample_leaf_options = list(range(1,124,3))
n_estimators_options = list(range(1,124,5))

for leaf_size in sample_leaf_options:
    for n_estimators in n_estimators_options:
        alg = RandomForestClassifier(min_samples_leaf=leaf_size,n_estimators=n_estimators, random_state=1)
        alg.fit(X_train,y_train)
        predict = alg.predict(X_test)

        results.append((leaf_size,n_estimators,(y_test==predict).mean()))
print(max(results,key=lambda x:x[2]))


