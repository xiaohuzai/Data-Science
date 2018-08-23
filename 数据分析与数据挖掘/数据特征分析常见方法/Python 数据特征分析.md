# Python 数据特征分析

[TOC]



## 一、分布分析

以[“深圳罗湖二手房信息.csv”](https://raw.githubusercontent.com/xiaohuzai/Python/master/%E6%95%B0%E6%8D%AE%E5%88%86%E6%9E%90%E4%B8%8E%E6%95%B0%E6%8D%AE%E6%8C%96%E6%8E%98/%E6%95%B0%E6%8D%AE%E7%89%B9%E5%BE%81%E5%88%86%E6%9E%90%E5%B8%B8%E8%A7%81%E6%96%B9%E6%B3%95/%E6%B7%B1%E5%9C%B3%E7%BD%97%E6%B9%96%E4%BA%8C%E6%89%8B%E6%88%BF%E4%BF%A1%E6%81%AF.csv)数据为例。

```python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
data = pd.read_csv('深圳罗湖二手房信息.csv',engine = 'python')
data.head()
Out[2]: 
        房屋编码      小区  朝向   房屋单价  参考首付   参考总价          经度         纬度
0  605093949   大望新平村  南北   5434  15.0   50.0  114.180964  22.603698
1  605768856     通宝楼  南北   3472   7.5   25.0  114.179298  22.566910
2  606815561  罗湖区罗芳村  南北   5842  15.6   52.0  114.158869  22.547223
3  605147285     兴华苑  南北   3829  10.8   36.0  114.158040  22.554343
4  606030866  京基东方都会  西南  47222  51.0  170.0  114.149243  22.554370
```

#### 1、作散点图

按照纵坐标为维度，横坐标为经度，按照单价来控制大小来做散点图。

```python
plt.scatter(data['经度'],data['纬度'],  # 按照经纬度显示
            s = data['房屋单价']/500,  # 按照单价显示大小
            c = data['参考总价'],  # 按照总价显示颜色
            alpha = 0.4, cmap = 'Reds')  
plt.grid()  #做出网格
```

![](https://raw.githubusercontent.com/xiaohuzai/Python/master/%E6%95%B0%E6%8D%AE%E5%88%86%E6%9E%90%E4%B8%8E%E6%95%B0%E6%8D%AE%E6%8C%96%E6%8E%98/%E6%95%B0%E6%8D%AE%E7%89%B9%E5%BE%81%E5%88%86%E6%9E%90%E5%B8%B8%E8%A7%81%E6%96%B9%E6%B3%95/pictures/1.png)

#### 2、作极差

该特征只适用于定量字段。

```python
def d_range(df,*cols):
    krange = []
    for col in cols:
        crange = df[col].max() - df[col].min()
        krange.append(crange)
    return(krange)
# 创建函数求极差

key1 = '参考首付'
key2 = '参考总价'
dr = d_range(data,key1,key2)
print('%s极差为 %f \n%s极差为 %f' % (key1, dr[0], key2, dr[1]))

参考首付极差为 52.500000 
参考总价极差为 175.000000
```

#### 3、频率分布

该特征也只适用于定量字段。

**使用直方图直接判断分组组数**

```python
data[key2].hist(bins=10)
# 简单查看数据分布，确定分布组数 → 一般8-16即可
# 这里以10组为参考
```

![](https://raw.githubusercontent.com/xiaohuzai/Python/master/%E6%95%B0%E6%8D%AE%E5%88%86%E6%9E%90%E4%B8%8E%E6%95%B0%E6%8D%AE%E6%8C%96%E6%8E%98/%E6%95%B0%E6%8D%AE%E7%89%B9%E5%BE%81%E5%88%86%E6%9E%90%E5%B8%B8%E8%A7%81%E6%96%B9%E6%B3%95/pictures/2.png)

**求分组区间**

```python
gcut = pd.cut(data[key2],10,right=False)
gcut.head()
Out[10]: 
0      [42.5, 60.0)
1      [25.0, 42.5)
2      [42.5, 60.0)
3      [25.0, 42.5)
4    [165.0, 182.5)
Name: 参考总价, dtype: category
Categories (10, interval[float64]): [[25.0, 42.5) < [42.5, 60.0) < [60.0, 77.5) < [77.5, 95.0) ... [130.0, 147.5) < [147.5, 165.0) < [165.0, 182.5) < [182.5, 200.175)]
```

即将参考总价划分了十个区间。

统计在每个区间里房子的数量

```python
gcut_count = gcut.value_counts(sort=False)
gcut_count
Out[12]: 
[25.0, 42.5)        14
[42.5, 60.0)        17
[60.0, 77.5)         1
[77.5, 95.0)         2
[95.0, 112.5)        4
[112.5, 130.0)       2
[130.0, 147.5)       3
[147.5, 165.0)       4
[165.0, 182.5)       8
[182.5, 200.175)    20
Name: 参考总价, dtype: int64
```

**求频数、频率、累计频率**

```python
# gcut_count是一个Series，先将其转为DataFrame格式，方便我们添加新的列
r_zj = pd.DataFrame(gcut_count)
r_zj.rename(columns ={gcut_count.name:'频数'}, inplace = True)  # 修改频数字段名
r_zj.head()
Out[16]: 
               频数
[25.0, 42.5)   14
[42.5, 60.0)   17
[60.0, 77.5)    1
[77.5, 95.0)    2
[95.0, 112.5)   4
 
r_zj['频率'] = r_zj / r_zj['频数'].sum()  # 计算频率
r_zj['累计频率'] = r_zj['频率'].cumsum()  # 计算累计频率
r_zj['频率%'] = r_zj['频率'].apply(lambda x: "%.2f%%" % (x*100))  # 以百分比显示频率
r_zj['累计频率%'] = r_zj['累计频率'].apply(lambda x: "%.2f%%" % (x*100))  # 以百分比显示累计频率
r_zj.head()
Out[18]: 
               频数        频率      累计频率     频率%   累计频率%
[25.0, 42.5)   14  0.186667  0.186667  18.67%  18.67%
[42.5, 60.0)   17  0.226667  0.413333  22.67%  41.33%
[60.0, 77.5)    1  0.013333  0.426667   1.33%  42.67%
[77.5, 95.0)    2  0.026667  0.453333   2.67%  45.33%
[95.0, 112.5)   4  0.053333  0.506667   5.33%  50.67%
```

绘制频率分布直方图

```python
r_zj['频率'].plot(kind = 'bar',
                 width = 0.8,
                 figsize = (12,2),
                 rot = 0,
                 color = 'k',
                 grid = True,
                 alpha = 0.5)
plt.title('参考总价分布频率直方图')
# 绘制直方图

x = len(r_zj)
y = r_zj['频率']
for i,j,k in zip(range(x),y,y):
    plt.text(i-0.2,j+0.01,'%.2f' % k, color = 'k')
# 添加频率标签
```

![](https://raw.githubusercontent.com/xiaohuzai/Python/master/%E6%95%B0%E6%8D%AE%E5%88%86%E6%9E%90%E4%B8%8E%E6%95%B0%E6%8D%AE%E6%8C%96%E6%8E%98/%E6%95%B0%E6%8D%AE%E7%89%B9%E5%BE%81%E5%88%86%E6%9E%90%E5%B8%B8%E8%A7%81%E6%96%B9%E6%B3%95/pictures/3.png)

绘制频率分布饼图

```python
plt.pie(r_zj['频数'],
       labels = r_zj.index,
       autopct='%.2f%%',
       shadow = True)
plt.axis('equal')    #保证饼状图是正圆
# 绘制饼图
```

![](https://raw.githubusercontent.com/xiaohuzai/Python/master/%E6%95%B0%E6%8D%AE%E5%88%86%E6%9E%90%E4%B8%8E%E6%95%B0%E6%8D%AE%E6%8C%96%E6%8E%98/%E6%95%B0%E6%8D%AE%E7%89%B9%E5%BE%81%E5%88%86%E6%9E%90%E5%B8%B8%E8%A7%81%E6%96%B9%E6%B3%95/pictures/4.png)

## 二、对比分析

对比分析即两个互相联系的指标进行比较。包括绝对数比较（相减）、相对数比较（相除）。

#### 1、绝对数比较-相减

```python
# 创建两列随机数据
data = pd.DataFrame(np.random.rand(30,2)*1000,
                   columns = ['A_sale','B_sale'],
                   index = pd.period_range('20170601','20170630'))
data.head()
                   
Out[2]: 
                A_sale      B_sale
2017-06-01  312.567992  465.865161
2017-06-02  420.529211  671.409677
2017-06-03  161.554237  951.281632
2017-06-04  708.312994  221.106138
2017-06-05   36.146936  249.380800
```

**折线图比较**

```python
data.plot(kind='line',
       style = '--.',
       alpha = 0.8,
       figsize = (10,3),
       title = 'AB产品销量对比-折线图')
```

![](https://raw.githubusercontent.com/xiaohuzai/Python/master/%E6%95%B0%E6%8D%AE%E5%88%86%E6%9E%90%E4%B8%8E%E6%95%B0%E6%8D%AE%E6%8C%96%E6%8E%98/%E6%95%B0%E6%8D%AE%E7%89%B9%E5%BE%81%E5%88%86%E6%9E%90%E5%B8%B8%E8%A7%81%E6%96%B9%E6%B3%95/pictures/5.png)

**柱状图比较**

```python
data.plot(kind = 'bar',
          width = 0.8,
          alpha = 0.8,
          figsize = (10,3),
          title = 'AB产品销量对比-柱状图')
```

![](https://raw.githubusercontent.com/xiaohuzai/Python/master/%E6%95%B0%E6%8D%AE%E5%88%86%E6%9E%90%E4%B8%8E%E6%95%B0%E6%8D%AE%E6%8C%96%E6%8E%98/%E6%95%B0%E6%8D%AE%E7%89%B9%E5%BE%81%E5%88%86%E6%9E%90%E5%B8%B8%E8%A7%81%E6%96%B9%E6%B3%95/pictures/6.png)

**柱状图比较**

```python
fig3 = plt.figure(figsize=(10,6))
plt.subplots_adjust(hspace=0.3)
# 创建子图及间隔设置

ax1 = fig3.add_subplot(2,1,1)  
x = range(len(data))
y1 = data['A_sale']
y2 = -data['B_sale']
plt.bar(x,y1,width = 1,facecolor = 'yellowgreen')
plt.bar(x,y2,width = 1,facecolor = 'lightskyblue')
plt.title('AB产品销量对比-堆叠图')
plt.grid()
plt.xticks(range(0,30,6))   
ax1.set_xticklabels(data.index[::6])
# 创建堆叠图

ax2 = fig3.add_subplot(2,1,2)  
y3 = data['A_sale']-data['B_sale']
plt.plot(x,y3,'--go')
plt.axhline(0,hold=None,color='r',linestyle="--",alpha=0.8)  # 添加y轴参考线
plt.grid()
plt.title('AB产品销量对比-差值折线')
plt.xticks(range(0,30,6))
ax2.set_xticklabels(data.index[::6])
# 创建差值折线图
```

![](https://raw.githubusercontent.com/xiaohuzai/Python/master/%E6%95%B0%E6%8D%AE%E5%88%86%E6%9E%90%E4%B8%8E%E6%95%B0%E6%8D%AE%E6%8C%96%E6%8E%98/%E6%95%B0%E6%8D%AE%E7%89%B9%E5%BE%81%E5%88%86%E6%9E%90%E5%B8%B8%E8%A7%81%E6%96%B9%E6%B3%95/pictures/7.png)

#### 2、相对数比较-相除

```python

data = pd.DataFrame({'A_sale':np.random.rand(30)*1000,
                    'B_sale':np.random.rand(30)*200},
                   index = pd.period_range('20170601','20170630'))
                   

data.head()
Out[10]: 
                A_sale      B_sale
2017-06-01  398.555384  133.699063
2017-06-02  138.662051  190.527030
2017-06-03  385.797843   55.443922
2017-06-04   83.117519  178.395204
2017-06-05  808.508173  116.985864
```

创建百分比数据

```python
data['A_per'] = data['A_sale'] / data['A_sale'].sum()
data['B_per'] = data['B_sale'] / data['B_sale'].sum()
# 计算出每天的营收占比

data['A_per%'] = data['A_per'].apply(lambda x: '%.2f%%' % (x*100))
data['B_per%'] = data['B_per'].apply(lambda x: '%.2f%%' % (x*100))
# 转换为百分数
data.head()


Out[11]: 
                A_sale      B_sale     A_per     B_per A_per% B_per%
2017-06-01  398.555384  133.699063  0.027284  0.047807  2.73%  4.78%
2017-06-02  138.662051  190.527030  0.009492  0.068128  0.95%  6.81%
2017-06-03  385.797843   55.443922  0.026411  0.019825  2.64%  1.98%
2017-06-04   83.117519  178.395204  0.005690  0.063790  0.57%  6.38%
2017-06-05  808.508173  116.985864  0.055349  0.041831  5.53%  4.18%
```

作图

```python
fig,axes = plt.subplots(2,1,figsize = (10,6),sharex=True)
data[['A_sale','B_sale']].plot(kind='line',style = '--.',alpha = 0.8,ax=axes[0])
axes[0].legend(loc = 'upper right')
data[['A_per','B_per']].plot(kind='line',style = '--.',alpha = 0.8,ax=axes[1])
axes[1].legend(loc = 'upper right')
# 绝对值对比较难看出结构性变化，通过看销售额占比来看售卖情况的对比
```

![](https://raw.githubusercontent.com/xiaohuzai/Python/master/%E6%95%B0%E6%8D%AE%E5%88%86%E6%9E%90%E4%B8%8E%E6%95%B0%E6%8D%AE%E6%8C%96%E6%8E%98/%E6%95%B0%E6%8D%AE%E7%89%B9%E5%BE%81%E5%88%86%E6%9E%90%E5%B8%B8%E8%A7%81%E6%96%B9%E6%B3%95/pictures/8.png)

**纵向对比分析**

同一现象在不同时间上的指标数值进行对比，反应现象的数量随着时间推移而发展变动的程度及趋势。

```python
data = pd.DataFrame({'A':np.random.rand(30)*2000+1000},
                   index = pd.period_range('20170601','20170630'))
data.head()
Out[14]: 
                      A
2017-06-01  1426.709763
2017-06-02  1220.776731
2017-06-03  2375.025911
2017-06-04  1436.014915
2017-06-05  1385.337857
```

将A的值平移一天，以便做对比分析

```python
data.shift(1).head()
Out[16]: 
                      A
2017-06-01          NaN
2017-06-02  1426.709763
2017-06-03  1220.776731
2017-06-04  2375.025911
2017-06-05  1436.014915
```

```python
 data['z_growth'] = data['A'] - data.shift(1)['A']  # 逐期增长量 = 报告期水平 - 报告期前一期水平
data[data.isnull()] = 0  # 替换缺失值
data['z_growth'].plot(figsize = (10,4),style = '--.',alpha = 0.8)  
plt.axhline(0,hold=None,color='r',linestyle="--",alpha=0.8)  # 添加y轴参考线
plt.legend(loc = 'lower left')
plt.grid()
# 通过折线图查看增长量情况
```

![](https://raw.githubusercontent.com/xiaohuzai/Python/master/%E6%95%B0%E6%8D%AE%E5%88%86%E6%9E%90%E4%B8%8E%E6%95%B0%E6%8D%AE%E6%8C%96%E6%8E%98/%E6%95%B0%E6%8D%AE%E7%89%B9%E5%BE%81%E5%88%86%E6%9E%90%E5%B8%B8%E8%A7%81%E6%96%B9%E6%B3%95/pictures/9.png)

```python
data['zspeed'] = data['z_growth'] / data.shift(1)['A']  # 环比增长速度
data['zspeed'].plot(figsize = (10,4),style = '--.',alpha = 0.8)  
plt.axhline(0,hold=None,color='r',linestyle="--",alpha=0.8)  # 添加y轴参考线
plt.grid()
```

![](https://raw.githubusercontent.com/xiaohuzai/Python/master/%E6%95%B0%E6%8D%AE%E5%88%86%E6%9E%90%E4%B8%8E%E6%95%B0%E6%8D%AE%E6%8C%96%E6%8E%98/%E6%95%B0%E6%8D%AE%E7%89%B9%E5%BE%81%E5%88%86%E6%9E%90%E5%B8%B8%E8%A7%81%E6%96%B9%E6%B3%95/pictures/10.png)

## 三、统计分析

统计指标对定量数据进行统计描述，常从**集中趋势**和**离中趋势**两个方面进行分析。

#### 一、集中趋势度量

**算数平均数**

```python
data = pd.DataFrame({'value':np.random.randint(100,120,100),
                    'f':np.random.rand(100)})
data['f'] = data['f'] / data['f'].sum()  # f为权重，这里将f列设置成总和为1的权重占比
data.head()

Out[19]: 
   value         f
0    107  0.020027
1    109  0.001082
2    112  0.005820
3    102  0.003116
4    112  0.000795

mean = data['value'].mean()
mean
Out[21]: 109.59
    
mean_w = (data['value'] * data['f']).sum() / data['f'].sum() #加权平均数
mean_w = (data['value'] * data['f']).sum() / data['f'].sum()
mean_w
Out[23]: 110.00396033595194
```

**众数**

```python
m = data['value'].mode()
m
Out[25]: 
0    113
dtype: int32
```

**中位数**

```python
med = data['value'].median()
med
Out[27]: 110.0
```

**做出数据分布、平均数、算数平均数、中位数的图**

```python
data['value'].plot(kind = 'kde',style = '--k',grid = True)
# 密度曲线

plt.axvline(mean,hold=None,color='r',linestyle="--",alpha=0.8)  
plt.text(mean + 5,0.005,'简单算数平均值为：%.2f' % mean, color = 'r')
# 简单算数平均值

plt.axvline(mean_w,hold=None,color='b',linestyle="--",alpha=0.8)  
plt.text(mean + 5,0.01,'加权算数平均值：%.2f' % mean_w, color = 'b')
# 加权算数平均值

plt.axvline(med,hold=None,color='g',linestyle="--",alpha=0.8)  
plt.text(mean + 5,0.015,'中位数：%i' % med, color = 'g')
# 中位数
```

![](https://raw.githubusercontent.com/xiaohuzai/Python/master/%E6%95%B0%E6%8D%AE%E5%88%86%E6%9E%90%E4%B8%8E%E6%95%B0%E6%8D%AE%E6%8C%96%E6%8E%98/%E6%95%B0%E6%8D%AE%E7%89%B9%E5%BE%81%E5%88%86%E6%9E%90%E5%B8%B8%E8%A7%81%E6%96%B9%E6%B3%95/pictures/11.png)

#### 二、离中趋势度量

```python
data = pd.DataFrame({'A_sale':np.random.rand(30)*1000,
                    'B_sale':np.random.rand(30)*1000},
                   index = pd.period_range('20170601','20170630'))
data.head()               
Out[31]: 
                A_sale      B_sale
2017-06-01  636.923950  425.262371
2017-06-02  367.165957  589.589158
2017-06-03  889.182309  457.957106
2017-06-04  961.728355  385.725275
2017-06-05   56.968745  495.556918
```

**极差**

```python
a_r = data['A_sale'].max() - data['A_sale'].min()
b_r = data['B_sale'].max() - data['B_sale'].min()
a_r
Out[33]: 948.5565569786929
b_r
Out[34]: 934.5913418265015
```

**分位差**

```python
sta = data['A_sale'].describe()
stb = data['B_sale'].describe()
sta
Out[5]: 
count     30.000000
mean     453.540532
std      301.106231
min       30.336682
25%      153.425942
50%      430.084982
75%      661.686559
max      988.801042
Name: A_sale, dtype: float64
        
a_iqr = sta.loc['75%'] - sta.loc['25%']
b_iqr = stb.loc['75%'] - stb.loc['25%']
print('A销售额的分位差为：%.2f, B销售额的分位差为：%.2f' % (a_iqr,b_iqr))

A销售额的分位差为：508.26, B销售额的分位差为：566.26
```

作图

```python
color = dict(boxes='DarkGreen', whiskers='DarkOrange', medians='DarkBlue', caps='Gray')
data.plot.box(vert=False,grid = True,color = color,figsize = (10,3))
#箱型图
```

![](https://raw.githubusercontent.com/xiaohuzai/Python/master/%E6%95%B0%E6%8D%AE%E5%88%86%E6%9E%90%E4%B8%8E%E6%95%B0%E6%8D%AE%E6%8C%96%E6%8E%98/%E6%95%B0%E6%8D%AE%E7%89%B9%E5%BE%81%E5%88%86%E6%9E%90%E5%B8%B8%E8%A7%81%E6%96%B9%E6%B3%95/pictures/12.png)

**方差、标准差**

```python
a_std = sta.loc['std']
b_std = stb.loc['std']
a_var = data['A_sale'].var()
b_var = data['B_sale'].var()
print('A销售额的标准差为：%.2f, B销售额的标准差为：%.2f' % (a_std,b_std))
print('A销售额的方差为：%.2f, B销售额的方差为：%.2f' % (a_var,b_var))
# 方差 → 各组中数值与算数平均数离差平方的算术平均数
# 标准差 → 方差的平方根
# 标准差是最常用的离中趋势指标 → 标准差越大，离中趋势越明显


A销售额的标准差为：301.11, B销售额的标准差为：288.34
A销售额的方差为：90664.96, B销售额的方差为：83138.43
```

作图

```python
fig = plt.figure(figsize = (12,4))
ax1 = fig.add_subplot(1,2,1)
data['A_sale'].plot(kind = 'kde',style = 'k--',grid = True,title = 'A密度曲线')
plt.axvline(sta.loc['50%'],hold=None,color='r',linestyle="--",alpha=0.8)  
plt.axvline(sta.loc['50%'] - a_std,hold=None,color='b',linestyle="--",alpha=0.8)  
plt.axvline(sta.loc['50%'] + a_std,hold=None,color='b',linestyle="--",alpha=0.8)  
# A密度曲线，1个标准差

ax2 = fig.add_subplot(1,2,2)
data['B_sale'].plot(kind = 'kde',style = 'k--',grid = True,title = 'B密度曲线')
plt.axvline(stb.loc['50%'],hold=None,color='r',linestyle="--",alpha=0.8)  
plt.axvline(stb.loc['50%'] - b_std,hold=None,color='b',linestyle="--",alpha=0.8)  
plt.axvline(stb.loc['50%'] + b_std,hold=None,color='b',linestyle="--",alpha=0.8)  
# B密度曲线，1个标准差
```

![](https://raw.githubusercontent.com/xiaohuzai/Python/master/%E6%95%B0%E6%8D%AE%E5%88%86%E6%9E%90%E4%B8%8E%E6%95%B0%E6%8D%AE%E6%8C%96%E6%8E%98/%E6%95%B0%E6%8D%AE%E7%89%B9%E5%BE%81%E5%88%86%E6%9E%90%E5%B8%B8%E8%A7%81%E6%96%B9%E6%B3%95/pictures/13.png)

## 四、帕累托统计

帕累托分析（贡献度分析） → 帕累托法则：20/80定律

“原因和结果、投入和产出、努力和报酬之间本来存在着无法解释的不平衡。一般来说，投入和努力可以分为两种不同的类型：
多数，它们只能造成少许的影响；少数，它们造成主要的、重大的影响。”
→ 一个公司，80%利润来自于20%的畅销产品，而其他80%的产品只产生了20%的利润

例如：

* 世界上大约80％的资源是由世界上15％的人口所耗尽的
* 世界财富的80％为25％的人所拥有；在一个国家的医疗体系中
* 20％的人口与20％的疾病，会消耗80％的医疗资源。

一个思路：**通过二八原则，去寻找关键的那20%决定性因素！**

```python
data = pd.Series(np.random.randn(10)*1200+3000,
                index = list('ABCDEFGHIJ'))
data.head()
                
Out[13]: 
A    4928.170915
B     826.114777
C    4067.532271
D    3898.935614
E    2292.516694
dtype: float64
    
data.sort_values(ascending=False, inplace= True)
# 由大到小排列
```

计算出销量占比80%的商品

```python
p = data.cumsum()/data.sum()  # 创建累计占比，Series
key = p[p>0.8].index[0]  
key_num = data.index.tolist().index(key) 
print('超过80%累计占比的节点值索引为：' ,key)
print('超过80%累计占比的节点值索引位置为：' ,key_num)
print('------')
# 找到累计占比超过80%时候的index
# 找到key所对应的索引位置
key_product = data.loc[:key]
print('核心产品为：')
print(key_product)
# 输出决定性因素产品


超过80%累计占比的节点值索引为： F
超过80%累计占比的节点值索引位置为： 6
------
核心产品为：
A    4928.170915
C    4067.532271
H    3950.093905
D    3898.935614
G    3866.490789
J    3674.404100
F    3588.606671
dtype: float64
```

作图

```python
plt.figure(figsize = (10,4))
data.plot(kind = 'bar', color = 'g', alpha = 0.5, width = 0.7)  
plt.ylabel('营收_元')
# 创建营收柱状图
p.plot(style = '--ko', secondary_y=True)  # secondary_y → y副坐标轴
plt.axvline(key_num,hold=None,color='r',linestyle="--",alpha=0.8)  
plt.text(key_num+0.2,p[key],'累计占比为：%.3f%%' % (p[key]*100), color = 'r')  # 累计占比超过80%的节点
plt.ylabel('营收_比例')
# 绘制营收累计占比曲线
```

![](https://raw.githubusercontent.com/xiaohuzai/Python/master/%E6%95%B0%E6%8D%AE%E5%88%86%E6%9E%90%E4%B8%8E%E6%95%B0%E6%8D%AE%E6%8C%96%E6%8E%98/%E6%95%B0%E6%8D%AE%E7%89%B9%E5%BE%81%E5%88%86%E6%9E%90%E5%B8%B8%E8%A7%81%E6%96%B9%E6%B3%95/pictures/14.png)

## 五、正太性检验

#### 一、直方图初判

```python
s = pd.DataFrame(np.random.randn(1000)+10,columns = ['value'])

s.head()
Out[19]: 
       value
0   9.265372
1   9.420474
2   8.753998
3   9.450055
4  10.044531
```

作散点数据分布图和直方分布图

```python
fig = plt.figure(figsize = (10,6))
ax1 = fig.add_subplot(2,1,1)  # 创建子图1
ax1.scatter(s.index, s.values)
plt.grid()
# 绘制数据分布图

ax2 = fig.add_subplot(2,1,2)  # 创建子图2
s.hist(bins=30,alpha = 0.5,ax = ax2)
s.plot(kind = 'kde', secondary_y=True,ax = ax2)
plt.grid()
# 绘制直方图
# 呈现较明显的正太性
```

![](https://raw.githubusercontent.com/xiaohuzai/Python/master/%E6%95%B0%E6%8D%AE%E5%88%86%E6%9E%90%E4%B8%8E%E6%95%B0%E6%8D%AE%E6%8C%96%E6%8E%98/%E6%95%B0%E6%8D%AE%E7%89%B9%E5%BE%81%E5%88%86%E6%9E%90%E5%B8%B8%E8%A7%81%E6%96%B9%E6%B3%95/pictures/15.png)

#### 二、KS检验

```python
u = s['value'].mean()  # 计算均值
std = s['value'].std()  # 计算标准差
stats.kstest(s['value'], 'norm', (u, std))
# .kstest方法：KS检验，参数分别是：待检验的数据，检验方法（这里设置成norm正态分布），均值与标准差
# 结果返回两个值：statistic → D值，pvalue → P值
# p值大于0.05，为正态分布


Out[31]: KstestResult(statistic=0.029806473197866334, pvalue=0.33169661573604414)
```

## 六、相关性分析

#### 一、变量之间的线性关系

```python
data1 = pd.Series(np.random.rand(50)*100).sort_values()
data2 = pd.Series(np.random.rand(50)*50).sort_values()
data3 = pd.Series(np.random.rand(50)*500).sort_values(ascending = False)
# 创建三个数据：data1为0-100的随机数并从小到大排列，data2为0-50的随机数并从小到大排列，data3为0-500的随机数并从大到小排列，

fig = plt.figure(figsize = (10,4))
ax1 = fig.add_subplot(1,2,1)
ax1.scatter(data1, data2)
plt.grid()
# 正线性相关

ax2 = fig.add_subplot(1,2,2)
ax2.scatter(data1, data3)
plt.grid()
# 负线性相关
```

![](https://raw.githubusercontent.com/xiaohuzai/Python/master/%E6%95%B0%E6%8D%AE%E5%88%86%E6%9E%90%E4%B8%8E%E6%95%B0%E6%8D%AE%E6%8C%96%E6%8E%98/%E6%95%B0%E6%8D%AE%E7%89%B9%E5%BE%81%E5%88%86%E6%9E%90%E5%B8%B8%E8%A7%81%E6%96%B9%E6%B3%95/pictures/16.png)

#### 二、散点图矩阵初判多变量间关系

```python
data = pd.DataFrame(np.random.randn(200,4)*100, columns = ['A','B','C','D'])
data.head()
Out[35]: 
            A           B           C           D
0  -67.101633  -46.386179  -37.639753 -164.621415
1   91.064805  182.513617  111.572007 -134.986629
2  -56.012609   34.147253    8.393654    5.934948
3  131.047054   23.544414   -6.393726  -34.823170
4  184.410434 -100.863138  154.272951  -77.870318
```

作图矩阵

```python
pd.scatter_matrix(data,figsize=(8,8),
                  c = 'k',
                 marker = '+',
                 diagonal='hist',
                 alpha = 0.8,
                 range_padding=0.1)
```

![](https://raw.githubusercontent.com/xiaohuzai/Python/master/%E6%95%B0%E6%8D%AE%E5%88%86%E6%9E%90%E4%B8%8E%E6%95%B0%E6%8D%AE%E6%8C%96%E6%8E%98/%E6%95%B0%E6%8D%AE%E7%89%B9%E5%BE%81%E5%88%86%E6%9E%90%E5%B8%B8%E8%A7%81%E6%96%B9%E6%B3%95/pictures/17.png)

#### 三、Pearson相关系数

```python
data1 = pd.Series(np.random.rand(100)*100).sort_values()
data2 = pd.Series(np.random.rand(100)*50).sort_values()
data = pd.DataFrame({'value1':data1.values,
                     'value2':data2.values})
                     

data.head()
Out[38]: 
     value1    value2
0  0.402010  0.154426
1  1.414525  1.240293
2  1.717974  1.574587
3  1.860956  1.759390
4  4.067166  2.165177

data.corr()
# pandas相关性方法：data.corr(method='pearson', min_periods=1) → 直接给出数据字段的相关系数矩阵
# method默认pearson
Out[39]: 
         value1   value2
value1  1.00000  0.98603
value2  0.98603  1.00000
```

