The "data_generate" folder contains the code for generating Stephanie data：
* "topic_summarized.csv" is a summary of the topics in the persona dataset.
* "data_generate.py" is the code for generating Stephanie's data.
* "data_generate_prompt.txt" is the prompt used for data generation.
* "data_generated.csv" contains the generated Stephanie data.
* "data_process" folder includes scripts for further processing of the generated data to handle issues like random blank lines and indentations caused by large language model errors. The final processed data is stored in "data_formated.csv".


The "further_split" folder contains the code for further processing using the further_split method：
* In data_process, "row_cleaned.csv" is obtained by cleaning "data_formated.csv" (generated from the "data_generate" folder) by removing blank lines, redundant characters, etc., resulting in the final Stephanie data.


The eval folder contains the evaluation code：
* "row_cleaned.csv" is used as "data_to_eval.csv" for evaluation purposes.