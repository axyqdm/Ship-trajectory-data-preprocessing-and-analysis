import os
import pandas as pd
import matplotlib.pyplot as plt

input_folder = 'D:\\AA_work\\数据预处理\\处理完毕的数据集'  # 设置你的CSV文件所在文件夹路径

# 初始化一个空的DataFrame列表
data_frames = []

# 遍历文件夹中的所有CSV文件
for filename in os.listdir(input_folder):
    if filename.endswith('.csv'):
        file_path = os.path.join(input_folder, filename)
        df = pd.read_csv(file_path)
        data_frames.append(df)  # 将每个文件的DataFrame添加到列表中

# 合并所有的DataFrame为一个大的DataFrame
combined_df = pd.concat(data_frames, ignore_index=True)

# 创建箱形图
fig, axs = plt.subplots(3, 2, figsize=(12, 9))  # 修改图形的大小以避免挤压和重叠

# 定义一个绘制箱形图的函数
def draw_boxplot(column, title, ax, ylim=None):
    ax.boxplot(combined_df[column].dropna(),
               patch_artist=True,  # 启用补丁艺术家模式，允许填充箱体
               boxprops={'color': 'blue', 'facecolor': 'lightblue'},  # 箱体轮廓和填充颜色
               flierprops={'marker': 'o', 'markerfacecolor': 'red', 'markersize': 1, 'markeredgecolor': 'red'},  # 异常点样式
               whiskerprops={'color': 'blue'},  # 括号颜色
               capprops={'color': 'blue'},  # 条帽颜色
               medianprops={'color': 'red'})  # 中位线颜色设置为红色
    ax.set_title(title)
    ax.set_ylim(ylim)  # 设置y轴范围，如果提供了ylim参数
    ax.grid(True)  # 添加网格线


# 绘制箱形图
draw_boxplot('LON', '经度', axs[0, 0])  # 指定y轴范围
draw_boxplot('LAT', '纬度', axs[0, 1])
draw_boxplot('SOG', '对地航速', axs[1, 0])
draw_boxplot('COG', '航向', axs[1, 1])
draw_boxplot('Heading', '航向角', axs[2, 0])

# 删除多余的子图
fig.delaxes(axs[2, 1])

fig.tight_layout()  # 自动调整子图参数, 使之填充整个图像区域
plt.show()