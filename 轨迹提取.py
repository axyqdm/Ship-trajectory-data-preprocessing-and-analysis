import pandas as pd
import os
from datetime import datetime

# 原始数据文件夹路径
data_folder_path = '处理完毕的数据集'
# 结果保存的基本路径
output_base_path = '轨迹提取文件夹'

# 读取所有CSV文件
all_files = [os.path.join(data_folder_path, f) for f in os.listdir(data_folder_path) if f.endswith('.csv')]
all_data = [pd.read_csv(file) for file in all_files]

# 合并DataFrame
df = pd.concat(all_data, ignore_index=True)

# 确保BaseDateTime是datetime类型
df['BaseDateTime'] = pd.to_datetime(df['BaseDateTime'])

# 按MMSI分组并排序
grouped = df.sort_values('BaseDateTime').groupby('MMSI')

# 处理每个MMSI的数据
for mmsi, group in grouped:
    # 创建MMSI对应的目录在新的输出路径下
    mmsi_folder = os.path.join(output_base_path, str(mmsi))
    if not os.path.exists(mmsi_folder):
        os.makedirs(mmsi_folder)

    start_index = 0
    subtrack_number = 0
    for i in range(1, len(group)):
        # 计算时间差
        time_diff = (group.iloc[i]['BaseDateTime'] - group.iloc[i - 1]['BaseDateTime']).total_seconds() / 60
        if time_diff > 30:
            # 保存子轨迹
            sub_df = group.iloc[start_index:i]
            sub_df.to_csv(os.path.join(mmsi_folder, f'subtrack_{subtrack_number}.csv'), index=False)
            subtrack_number += 1
            start_index = i
    # 保存最后一个子轨迹
    sub_df = group.iloc[start_index:]
    sub_df.to_csv(os.path.join(mmsi_folder, f'subtrack_{subtrack_number}.csv'), index=False)

