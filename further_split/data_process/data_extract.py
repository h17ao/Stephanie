
# import pandas as pd
# import re

# # Load your DataFrame
# df = pd.read_csv('multi_further_splited.csv')

# # Define a function to extract and clean lines starting with "role" (ignoring leading spaces)
# def clean_and_extract_role_lines(text):
#     if pd.isna(text):
#         return ""  # Return an empty string for missing values
#     # Find all lines potentially starting with "role" (ignoring leading spaces)
#     role_lines = re.findall(r'^\s*role.*$', text, flags=re.MULTILINE)
#     # Strip leading and trailing whitespace from each line and filter out empty lines
#     cleaned_lines = [line.strip() for line in role_lines if line.strip()]
#     # Join the cleaned lines back into a single string, each separated by a newline
#     return '\n'.join(cleaned_lines)

# # List of columns to apply the text processing
# columns_to_process = ['multi_further_splited', 'generated_single_step_dialogue', 'generated_multi_step_dialogue']

# # Apply the function to each specified column in the DataFrame
# for column in columns_to_process:
#     df[column] = df[column].apply(clean_and_extract_role_lines)

# # Save the updated DataFrame
# df.to_csv('multi_further_extracted.csv', index=False)

import pandas as pd
import re

# Load your DataFrame
df = pd.read_csv('data_splited.csv')

# Define a function to extract and clean lines starting with "role" (ignoring leading spaces)
def clean_and_extract_role_lines(text):
    if pd.isna(text):
        return ""  # Return an empty string for missing values
    # Find all lines potentially starting with "role" (ignoring leading spaces)
    role_lines = re.findall(r'^\s*role.*$', text, flags=re.MULTILINE)
    
    # Clean and format lines
    cleaned_lines = []
    for line in role_lines:
        stripped_line = line.strip()
        if stripped_line.startswith("role2"):
            # Add 16 spaces indentation to lines starting with "role2"
            stripped_line = ' ' * 8 + stripped_line
        cleaned_lines.append(stripped_line)
    
    # Join the cleaned and formatted lines back into a single string, each separated by a newline
    return '\n'.join(cleaned_lines)

# List of columns to apply the text processing
columns_to_process = ['single_step_dialogue', 'multi_further_splited', 'generated_single_step_dialogue', 'generated_multi_step_dialogue']

# Apply the function to each specified column in the DataFrame
for column in columns_to_process:
    df[column] = df[column].apply(clean_and_extract_role_lines)

# Save the updated DataFrame
df.to_csv('data_extracted.csv', index=False)
