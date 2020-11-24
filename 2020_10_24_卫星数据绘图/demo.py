from matplotlib import pyplot as plt
import os
import numpy as np

def Curve_Fitting(x,y,deg,satellite):
    parameter = np.polyfit(x, y, deg)    #拟合deg次多项式
    p = np.poly1d(parameter)             #拟合deg次多项式
    aa=''                               #方程拼接  ——————————————————
    for i in range(deg+1):
        bb=round(parameter[i],2)
        if bb>0:
            if i==0:
                bb=str(bb)
            else:
                bb='+'+str(bb)
        else:
            bb=str(bb)
        if deg==i:
            aa=aa+bb
        else:
            aa=aa+bb+'x^'+str(deg-i)    #方程拼接  ——————————————————
    plt.figure(figsize=(20, 10), dpi=200)
    plt.ylim((min(y), max(y)))
    plt.scatter(x, y,label="{}号卫星2008年~2019年轨道".format(satellite))     #原始数据散点图
    plt.plot(x, p(x), color='g')  # 画拟合曲线
    plt.title('{}号卫星轨道图'.format(satellite))
    # 显示中文名称
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False
    plt.legend([aa,round(np.corrcoef(y, p(x))[0,1]**2,2)])   #拼接好的方程和R方放到图例
    plt.savefig(path +'/' + '{}.png'.format(satellite))
    plt.show()


if __name__ == '__main__':
    path = 'pictures'
    if not os.path.exists(path):
        os.mkdir(path)
    # 需要的卫星列表
    satellites = ['GPS41', 'GPS43', 'GPS44', 'GPS45', 'GPS46', 'GPS47', 'GPS51', 'GPS54', 'GPS56', 'GPS59', 'GPS60','GPS61']
    lines = open('2008-2019.txt', mode='r').readlines()
    for satellite in satellites:
        dates = []
        values = []
        i = 0
        for line in lines:
            # 让txt文件中的每行数据以列表形式呈现出来
            data = line.split('\t')[0].strip().replace(' ', ',').replace(',,,,', ' ').replace(',,,', ' ').replace(',,',' ').split(' ')
            if data[3] == satellite:
                dates.append(i)
                i += 1
                values.append(float(data[2]))
        Curve_Fitting(dates, values, 2,satellite)


