"""
    根据附件1后面两张表的特征数据，以及附件2处理后的特征数据
    采用决策树算法对附件2的第一张sheet包含的[是否违约]及[信誉评级]做出预测，并填充
    1)首先，评判是否违约的标准：

"""
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn import metrics
from sklearn.externals import  joblib


def predict_information():
    pima = pd.read_csv('../../Question1/Task1/7_处理后企业信息.csv', encoding='utf-8')
    pima.rename(columns={'信誉评级': 'isrun'}, inplace=True)

    # 其中最后一列是需要预测的因变量，其他特征是自变量
    X = pima[['有效合作单位数', '进项作废/有效比%', '净利润', '销项有效合作单位数', '销项作废/有效比%','进项月份时长','进项平均每月金额','进项负数发票次数','进项负数发票次数占比','销项月份时长','销项平均每月金额','销项负数发票次数','销项负数发票次数占比']]
    y = pima['isrun']

    # 训练：测试=7：3
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=1)
    rf = RandomForestClassifier(
        criterion='entropy',
        n_estimators=36,
        max_depth=5,
        min_samples_split=10,  # 定义至少多少个样本的情况下才继续分叉
        min_samples_leaf=4,
        min_weight_fraction_leaf=0.05  # 定义叶子节点最少需要包含多少个样本(使用百分比表达), 防止过拟合
    )
    # 训练模型
    rf.fit(X_train, y_train)
    # 做预测
    y_pred = rf.predict(X_test)
    # 模型的准确率
    print("i=number_of_trees=:", 6, ',accuricy=', metrics.accuracy_score(y_test, y_pred))
    # 保存model
    joblib.dump(rf, 'clf.pkl')
    df = pd.read_csv('7_处理后企业信息.csv', encoding='utf-8')
    Text_X = df[['有效合作单位数', '进项作废/有效比%', '净利润', '销项有效合作单位数', '销项作废/有效比%','进项月份时长','进项平均每月金额','进项负数发票次数','进项负数发票次数占比','销项月份时长','销项平均每月金额','销项负数发票次数','销项负数发票次数占比']]
    clf = joblib.load('clf.pkl')
    name_list = []
    # 得到预测的目标值
    to_list = clf.predict(Text_X)
    for i in to_list:
        name_list.append(i)
    return (name_list)


pima = pd.read_csv('../../Question1/Task1/7_处理后企业信息.csv',encoding='utf-8')
pima.rename(columns={'是否违约':'isrun'},inplace=True)
# 使用map映射将[是否违约]中的是和否分别变成1和0
pima.isrun = pima.isrun.astype(str).map({'否':0,'是':1})
# 其中最后一列是需要预测的因变量，其他特征是自变量
X = pima[['有效合作单位数','进项作废/有效比%','净利润','销项有效合作单位数','销项作废/有效比%','进项月份时长','进项平均每月金额','进项负数发票次数','进项负数发票次数占比','销项月份时长','销项平均每月金额','销项负数发票次数','销项负数发票次数占比']]
y = pima['isrun']

# 训练：测试=7：3
X_train,X_test,y_train,y_test=train_test_split(X,y,test_size=0.3, random_state=1)
rf = RandomForestClassifier(
    criterion='entropy',
    n_estimators=36,
    max_depth=5,
    min_samples_split=10, # 定义至少多少个样本的情况下才继续分叉
    min_samples_leaf=4,
    min_weight_fraction_leaf=0.05 # 定义叶子节点最少需要包含多少个样本(使用百分比表达), 防止过拟合
    )

# 训练模型
rf.fit(X_train, y_train)
# 做预测
y_pred = rf.predict(X_test)
# 模型的准确率
print("i=number_of_trees=:",4,',accuricy=',metrics.accuracy_score(y_test, y_pred))
# 保存model
joblib.dump(rf,'rf.pkl')
df = pd.read_csv('7_处理后企业信息.csv',encoding='utf-8')
Text_X = df[['有效合作单位数','进项作废/有效比%','净利润','销项有效合作单位数','销项作废/有效比%','进项月份时长','进项平均每月金额','进项负数发票次数','进项负数发票次数占比','销项月份时长','销项平均每月金额','销项负数发票次数','销项负数发票次数占比']]
clf = joblib.load('rf.pkl')

name_list = []
# 得到预测的目标值
to_list = clf.predict(Text_X)
for i in to_list:
    if i == 0:
        name_list.append('否')
    else:
        name_list.append('是')
new_information = predict_information()
df.insert(3,'是否违约',name_list)
df.insert(4,'信誉评级',new_information)
df.to_csv('8_处理后信息.csv',encoding='utf-8-sig')