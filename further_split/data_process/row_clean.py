import pandas as pd

# 加载数据
df = pd.read_csv('data_extracted.csv')

# 打印原始数据中每列包含空值的行数
print("原始数据中包含空值的行数:")
print(df[['generated_single_step_dialogue', 'generated_multi_step_dialogue', 'multi_further_splited']].isna().sum())

# 删除这三列中任何一列包含空值的行
df_cleaned = df.dropna(subset=['generated_single_step_dialogue', 'generated_multi_step_dialogue', 'multi_further_splited'])

# 保存更改后的DataFrame到CSV文件
df_cleaned.to_csv('row_cleaned.csv', index=False)

# 打印清理后数据中每列包含空值的行数
print("清理后数据中包含空值的行数:")
print(df_cleaned[['generated_single_step_dialogue', 'generated_multi_step_dialogue', 'multi_further_splited']].isna().sum())
