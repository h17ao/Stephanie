import pandas as pd
import re  # 导入正则表达式模块

# 假设 df 是您的原始DataFrame
df = pd.read_csv('data_generated.csv')  # 或者用其他方式加载DataFrame

# 在DataFrame中添加新列
df['generated_single_step_dialogue'] = ''
df['generated_multi_step_dialogue'] = ''

# 遍历DataFrame中的每一行
for index, row in df.iterrows():
    # 使用正则表达式分割，忽略大小写
    parts = re.split(r'\*\*multi-step dialogue:\*\*', row['generated_dialogue'], flags=re.IGNORECASE)

    # 如果存在多步对话和单步对话
    if len(parts) > 1:
        multi_step_part = parts[1]
        single_step_parts = re.split(r'\*\*single-step dialogue:\*\*', multi_step_part, flags=re.IGNORECASE)
        if len(single_step_parts) > 1:
            single_step_part = single_step_parts[1]
            multi_step_part = single_step_parts[0]
        else:
            single_step_part = ''
    else:
        single_step_parts = re.split(r'\*\*single-step dialogue:\*\*', parts[0], flags=re.IGNORECASE)
        single_step_part = single_step_parts[1] if len(single_step_parts) > 1 else ''
        multi_step_part = ''

    # # 处理多步和单步对话中的role2行缩进两个制表符（相当于16个空格）
    # multi_step_part = '\n'.join([' ' * 16 + line if line.strip().startswith("role2:") else line for line in multi_step_part.split('\n')])
    # single_step_part = '\n'.join([' ' * 16 + line if line.strip().startswith("role2:") else line for line in single_step_part.split('\n')])

    # 去除空行
    multi_step_part = '\n'.join([line for line in multi_step_part.split('\n') if line.strip() != ''])
    single_step_part = '\n'.join([line for line in single_step_part.split('\n') if line.strip() != ''])

    # 设置single-step对话和multi-step对话
    df.at[index, 'generated_single_step_dialogue'] = single_step_part.strip()
    df.at[index, 'generated_multi_step_dialogue'] = multi_step_part.strip()

# 保存更新后的DataFrame到新文件
df.to_csv('multi_single_extracted.csv', index=False)
