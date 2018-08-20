# Python 数据特征分析

## 一、分布分析

以“深圳罗湖二手房信息.csv”数据为例。

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



