# Stephanie Data Generation and Evalution Overview

## `data_generate` Folder
Contains the code for generating Stephanie data:
- `topic_summarized.csv`: Summary of the topics in the persona dataset.
- `data_generate.py`: Code for generating Stephanie's data.
- `data_generate_prompt.txt`: Prompt used for data generation.
- `data_generated.csv`: Contains the generated Stephanie data.
- `data_process` folder includes scripts for further processing of the generated data to handle issues like random blank lines and indentations caused by large language model errors. The final processed data is stored in `data_formated.csv`.

---

## `further_split` Folder
Contains the code for further processing using the further_split method:
- In data_process, `row_cleaned.csv` is obtained by cleaning `data_formated.csv` (generated from the `data_generate` folder) by removing blank lines, redundant characters, etc., resulting in the final Stephanie data.

---

## `eval` Folder
Contains the evaluation code:
- `row_cleaned.csv` is used as `data_to_eval.csv` for evaluation purposes.
