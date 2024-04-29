import matplotlib.pyplot as plt
import pandas as pd

plt.rcParams['font.sans-serif'] = ['SimHei']  # 把字体设置为SimHei
plt.rcParams['axes.unicode_minus'] = False
# 读取数据
df = pd.read_csv('轨迹提取文件夹/205609000/subtrack_12.csv')

# 绘制LAT, LON, SOG, COG随时间的变化
plt.figure(figsize=(15, 10))  # 设置图形的大小

# 绘制LAT
plt.subplot(2, 2, 1)  # 2行2列的子图中的第1个
plt.plot(df.index, df['LAT'], label='LAT')
plt.xlabel('序列数')
plt.ylabel('LAT')
plt.title('(a) 纬度序列分布')

# 绘制LON
plt.subplot(2, 2, 2)  # 2行2列的子图中的第2个
plt.plot(df.index, df['LON'], label='LON', color='orange')
plt.xlabel('序列数')
plt.ylabel('LON')
plt.title('(b) 经度序列分布')

# 绘制SOG
plt.subplot(2, 2, 3)  # 2行2列的子图中的第3个
plt.plot(df.index, df['SOG'], label='SOG', color='green')
plt.xlabel('序列数')
plt.ylabel('SOG')
plt.title('(c) 对地航速序列分布')

# 绘制COG
plt.subplot(2, 2, 4)  # 2行2列的子图中的第4个
plt.plot(df.index, df['COG'], label='COG', color='red')
plt.xlabel('序列数')
plt.ylabel('COG')
plt.title('(d) 对地航向序列分布')

# 调整子图间的间距
plt.tight_layout()
plt.show()
