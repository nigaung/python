import pandas as pd
import matplotlib.pyplot as plt


def get_quartile(sheet_name, column_name, df_original):
    # 从指定的 Excel 表格中读取四分位数数据
    df_quartile = pd.read_excel('quantile_data.xlsx', sheet_name=sheet_name)
    # 选择需要的列，并进行重命名
    df_quartile = df_quartile[['指标名称', column_name]].rename(columns={'指标名称': '日期', column_name: sheet_name})
    # 将原始数据和四分位数数据按日期进行合并
    df_merged = pd.merge(df_original, df_quartile, on='日期')
    return df_merged


# 读取原始数据表格
df_original = pd.read_excel('quantile_data.xlsx', sheet_name='原数')
# 将日期列转换为字符串格式
df_original['指标名称'] = df_original['指标名称'].apply(lambda x: x.strftime('%Y-%m-%d'))
# 选择需要的列，并进行重命名
df_original = df_original[['指标名称', '数列1']].rename(columns={'指标名称': '日期', '数列1': '原数'})

# 定义四分位数的表格名称和数列名称
sheets = ['四分之一分位数', '二分之一分位数', '四分之三分位数']
column_names = ['数列1', '数列2', '数列3']
dfs = {}  # 用于存储不同数列的 DataFrame 的字典

# 获取每个数列的四分位数数据
for column_name in column_names:
    df_temp = df_original.copy()  # 创建 df_original 的副本
    for sheet in sheets:
        df_temp = get_quartile(sheet, column_name, df_temp)
    dfs[column_name] = df_temp  # 将结果存储在字典中

# 均匀选择十个日期进行绘图
num_dates = 10
dates = df_original['日期'].unique()
step = max(len(dates) // num_dates, 1)  # 步长，确保至少选择一个日期
selected_dates = dates[::step]

# 设置绘图窗口尺寸
fig_width = 12  # 图片宽度
fig_height = 6  # 图片高度

# 绘制数列1、数列2、数列3的折线图
plt.rcParams["font.family"] = "sans-serif"
plt.rcParams["font.sans-serif"] = ["Microsoft YaHei"]
for column_name in column_names:
    plt.figure(figsize=(fig_width, fig_height))  # 设置绘图窗口尺寸
    plt.plot(dfs[column_name]['日期'], dfs[column_name]['原数'], label='原数')
    plt.plot(dfs[column_name]['日期'], dfs[column_name]['四分之一分位数'], label='四分之一分位数')
    plt.plot(dfs[column_name]['日期'], dfs[column_name]['二分之一分位数'], label='二分之一分位数')
    plt.plot(dfs[column_name]['日期'], dfs[column_name]['四分之三分位数'], label='四分之三分位数')
    plt.title(column_name)
    plt.xlabel('日期')
    plt.ylabel('数值')
    plt.xticks(selected_dates)  # 设置x轴刻度为选定的日期
    plt.legend()
    plt.savefig(f'{column_name}.png')  # 保存图片
    # plt.show()
