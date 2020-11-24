import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn import metrics
from  sklearn import tree
import pydotplus
import graphviz


pima = pd.read_csv('../../Question1/Task1/7_处理后企业信息.csv',encoding='utf-8')
pima.rename(columns={'是否违约':'isrun'},inplace=True)
# 使用map映射将[是否违约]中的是和否分别变成1和0
pima.isrun = pima.isrun.astype(str).map({'否':0,'是':1})
# 其中最后一列是需要预测的因变量，其他特征是自变量
X = pima[['有效合作单位数','进项作废/有效比%','净利润','销项有效合作单位数','销项作废/有效比%','进项月份时长','进项平均每月金额','进项负数发票次数','进项负数发票次数占比','销项月份时长','销项平均每月金额','销项负数发票次数','销项负数发票次数占比']]
y = pima['isrun']

# 训练：测试=7：3
X_train,X_test,y_train,y_test=train_test_split(X,y,test_size=0.3, random_state=1)
clf = tree.DecisionTreeClassifier(criterion='entropy')
# 训练模型
clf.fit(X_train, y_train)
# 做预测
y_pred = clf.predict(X_test)
# 模型的准确率
print("i=number_of_trees=:",4,',accuricy=',metrics.accuracy_score(y_test, y_pred))

feature_name = ['有效合作单位数','进项作废/有效比%','净利润','销项有效合作单位数','销项作废/有效比%','进项月份时长','进项平均每月金额','进项负数发票次数','进项负数发票次数占比','销项月份时长','销项平均每月金额','销项负数发票次数','销项负数发票次数占比']
dot_data = tree.export_graphviz(clf
                                ,out_file=None
                                ,feature_names= feature_name
                                ,class_names=["违约","没违约"]
                                ,filled=True
                                ,rounded=True
                               )
graph = graphviz.Source(dot_data)
graph
