import os
import pandas as pd

# 文件夹路径
input_folder = '数据集'
output_folder = '处理完毕的数据集'

# 如果输出文件夹不存在，则创建它
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# 遍历文件夹中的所有CSV文件
for filename in os.listdir(input_folder):
    if filename.endswith('.csv'):
        file_path = os.path.join(input_folder, filename)

        # Load the dataset
        df = pd.read_csv(file_path)

        # 1. Sort by MMSI and BaseDateTime
        df.sort_values(by=['MMSI', 'BaseDateTime'], inplace=True)

        # 2. Remove records where MMSI is not 9 digits
        df = df[df['MMSI'].apply(lambda x: len(str(x)) == 9)]

        # 3. Filter for 'normal' navigation statuses
        """normal_statuses = ['under engine', 'at anchor', 'not under command', 'restricted manoeuvrability',
                           'moored', 'aground', 'fishing', 'under way']
        df = df[df['Status'].isin(normal_statuses)]"""

        # 4. Remove records where Length < 3 or Width < 2
        df = df[(df['Length'] >= 3) & (df['Width'] >= 2)]

        # 5. Remove records with out-of-range values
        df = df[(df['LON'] >= -180.0) & (df['LON'] <= 180.0)]
        df = df[(df['LAT'] >= -90.0) & (df['LAT'] <= 90.0)]
        df = df[(df['SOG'] >= 0) & (df['SOG'] <= 51.2)]
        df = df[(df['COG'] >= -204.7) & (df['COG'] <= 204.8)]

        # 6. Remove records where SOG is zero for five consecutive points
        df['zero_sog'] = (df['SOG'] == 0).astype(int)
        df['rolling_sum'] = df.groupby('MMSI')['zero_sog'].rolling(window=5).sum().reset_index(level=0, drop=True)
        df = df[df['rolling_sum'] < 5]
        df.drop(columns=['zero_sog', 'rolling_sum'], inplace=True)

        # 保存处理后的数据集
        new_filename = 'new_' + filename
        output_path = os.path.join(output_folder, new_filename)
        df.to_csv(output_path, index=False)

        print(f"清洗完毕，已经保存到 '{output_path}'.")