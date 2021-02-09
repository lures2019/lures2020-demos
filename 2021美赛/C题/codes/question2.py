import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn import metrics
import joblib
from snownlp import SnowNLP
from sklearn.svm import SVC
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score
from sklearn.metrics import f1_score
from sklearn.neighbors import KNeighborsClassifier as KNN

plt.rcParams['font.family'] = 'SimHei'
plt.rcParams['font.size'] = 15
data = pd.read_csv("datas/2021MCMProblemC_DataSet.csv",encoding="utf-8")
data.rename(columns={'Lab Status':'lab'},inplace=True)
column = data.columns.tolist()[:8]

# 选择需要的数据
data = data.loc[(data['lab'] != 'Unverified') & (data['lab'] != 'Unprocessed')]
# 将Positive ID和Negative ID分别设为1和0
data.lab = data.lab.astype(str).map({'Negative ID':0,'Positive ID':1})
# lab的状态1和0作为输出，输入的数据Detection Date根据月份划分成数字1~12
data.rename(columns={'Detection Date':'date'},inplace=True)
dates = []
for date in data.date:
    try:
        month = date.split("-")[1]
    except Exception as error:
        month = date.split("/")[0]
    dates.append(month)
notes = []
for note in data.Notes:
    score = SnowNLP(note).sentiments
    notes.append(score)
my_list = list(data['date'])
new_list = list(data['Notes'])
for i in range(len(my_list)):
    data['date'] = data['date'].replace(my_list[i],dates[i])
    data['Notes'] = data['Notes'].replace(new_list[i],notes[i])
X = data[['date','Latitude','Longitude','Notes']]
y = data['lab']
# 1、使用随机森林进行预测
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

# 使用SVM进行分类预测
clf = SVC(kernel='rbf', class_weight='balanced')
clf.fit(X_train, y_train)
y_predict = clf.predict(X_test)
print('SVM精确率: ', precision_score(y_test, y_predict, average='macro'))
print('SVM召回率: ', recall_score(y_test, y_predict, average='macro'))
print('F1: ', f1_score(y_test, y_predict, average='macro'))

# 使用KNN进行分类预测
knc = KNN(n_neighbors =6)
knc.fit(X_train,y_train)
y_predict = knc.predict(X_test)
print('KNN准确率',knc.score(X_test,y_test))
print('KNN精确率',precision_score(y_test, y_predict,  average='macro'))
print('KNN召回率',recall_score(y_test, y_predict,  average='macro'))
print('F1',f1_score(y_test, y_predict,  average='macro'))
