import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

# 读取数据
df = pd.read_csv('轨迹提取文件夹/205609000/subtrack_12.csv')

# 选择分析的特征
features = ['LAT', 'LON', 'SOG', 'COG', 'Heading']

# 使用Seaborn的pairplot函数创建成对关系图
sns.pairplot(df[features])
plt.show()  # 显示成对关系图

# 计算斯皮尔曼相关性系数
spearman_corr = df[features].corr(method='spearman')

# 创建热力图，使用'GnBu'配色方案
plt.figure(figsize=(10, 8))  # 调整图的大小以适应你的需要
sns.heatmap(spearman_corr, annot=True, cmap='GnBu', square=True, linewidths=.5)
plt.title('Spearman Correlation Heatmap')
plt.show()  # 显示热力图
"""
热力图颜色类型
'Blues', 'BuGn', 'BuPu'
'GnBu', 'Greens', 'Greys'
'Oranges', 'OrRd', 'PuBu'
'PuBuGn', 'PuRd', 'Purples'
'RdPu', 'Reds', 'YlGn'
'YlGnBu', 'YlOrBr', 'YlOrRd'
"""