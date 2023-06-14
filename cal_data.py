import pandas as pd

# 创建数据框
# data = {
#     '日期': ['2020-01-02', '2020-01-03', '2020-01-06', '2020-01-07'],
#     '数值': [0.51, 0.48, 0.50, 0.48]
# }
# df = pd.DataFrame(data)

# 从 Excel 文件中读取数据
df = pd.read_excel('quantile_data.xlsx')
# 将日期列转换为日期时间格式
df['指标名称'] = pd.to_datetime(df['指标名称'])

# 按照日期排序
df = df.sort_values('指标名称')


# 计算分位数
def cal_quartile(date, series, value):
    # 找到日期及之前的数据
    df_before = df[df['指标名称'] <= date]

    # 计算分位数
    quartile = df_before[series].quantile(value)

    return quartile


# 计算并存储分位数数据
def calculate_store_quartile(sheet_name, value):
    # 示例日期
    dates = pd.to_datetime(df['指标名称'])
    # 创建新的DataFrame存储结果
    result_df = pd.DataFrame(columns=df.columns.values)

    for date in dates:
        quartile_1 = cal_quartile(date, '数列1', value)
        quartile_2 = cal_quartile(date, '数列2', value)
        quartile_3 = cal_quartile(date, '数列3', value)
        # 格式化日期为 'YYYY-MM-DD' 格式
        formatted_date = date.strftime('%Y-%m-%d')
        result_df = result_df.append({'指标名称': formatted_date, '数列1': quartile_1, '数列2': quartile_2, '数列3': quartile_3},
                                     ignore_index=True)

    # 将结果写入 Excel 文件的指定 sheet 页中
    with pd.ExcelWriter('quantile_data.xlsx', engine="openpyxl", mode='a') as writer:
        result_df.to_excel(writer, sheet_name=sheet_name, index=False)


# 将前两行数据写入到另一个名为“四分之一分位数”的sheet页中
calculate_store_quartile('四分之一分位数', 0.25)
calculate_store_quartile('二分之一分位数', 0.50)
calculate_store_quartile('四分之三分位数', 0.75)
