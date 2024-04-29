import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import lagrange
plt.rcParams['font.sans-serif'] = ['SimHei']  # 把字体设置为SimHei
plt.rcParams['axes.unicode_minus'] = False
# 读取原始数据
df = pd.read_csv('轨迹提取文件夹/210959000/subtrack_5.csv', parse_dates=['BaseDateTime'])
df.sort_values('BaseDateTime', inplace=True)
df.set_index('BaseDateTime', inplace=True)

# 创建新的时间索引
new_index = pd.date_range(start=df.index.min(), end=df.index.max(), freq='2T')

# 三次样条插值函数
def cubic_spline_interpolation(df):
    df_resampled = df.resample('2T').mean().interpolate('cubic')
    return df_resampled

# 应用三次样条插值
df_cubic = cubic_spline_interpolation(df[['LAT', 'LON']])

# 加权移动平均插值函数
def weighted_moving_average_interpolation(df, k, weights):
    if len(weights) != 2 * k:
        raise ValueError("权重的数量必须是 2k。")

    df_wma = pd.DataFrame(index=df.index, columns=df.columns)
    for col in df.columns:
        interpolated_values = []
        for t in df.index:
            window = df[col].rolling(window=2*k, center=True).apply(lambda x: np.dot(x, weights) / sum(weights), raw=True)
            window = window.reindex(df.index, method='nearest')
            interpolated_values.append(window.loc[t])
        df_wma[col] = interpolated_values
    return df_wma

# 设置 k 和权重
k = 2
weights = [1, 2, 2, 1]

# 应用加权移动平均插值
df_weighted = weighted_moving_average_interpolation(df[['LAT', 'LON']], k, weights)

# 保存插值结果
df_weighted.to_csv('插值文件夹/均值插值.csv')
df_cubic.to_csv('插值文件夹/三次样条.csv')

# 绘制散点图比较
fig, axs = plt.subplots(2, 2, figsize=(10, 18))  # 创建三个子图
# 调整subplot布局
plt.subplots_adjust(top=1.5, bottom=0.1, left=0.1, right=0.9, hspace=0.5, wspace=0.5)
# 原始数据散点图
axs[0, 0].scatter(df['LON'], df['LAT'], alpha=0.5, color='blue')
axs[0, 0].set_title('原始数据')
axs[0, 0].set_xlabel('LON')
axs[0, 0].set_ylabel('LAT')
axs[0, 0].grid(True)

# 三次样条插值数据散点图
axs[0, 1].scatter(df_cubic['LON'], df_cubic['LAT'], alpha=0.5, color='green')
axs[0, 1].set_title('三次样条插值')
axs[0, 1].set_xlabel('LON')
axs[0, 1].set_ylabel('LAT')
axs[0, 1].grid(True)

# 加权移动平均插值数据散点图
axs[1, 0].scatter(df_weighted['LON'], df_weighted['LAT'], alpha=0.5, color='red')
axs[1, 0].set_title('加权移动平均插值')
axs[1, 0].set_xlabel('LON')
axs[1, 0].set_ylabel('LAT')
axs[1, 0].grid(True)

plt.tight_layout()
plt.show()

print("运行完毕")
