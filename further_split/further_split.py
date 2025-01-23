import csv
import time
import re
import requests


def print_response(response):
    # 检查响应状态码，确保请求成功
    if response.status_code == 200:
    # 解析响应内容为JSON
        response_data = response.json()
    # 从响应JSON中提取'response'字段
        chat_response = response_data.get('response', 'No response content available')
    # # 打印提取的内容
    #     print("Extracted Response:", chat_response)
    else:
        print("Failed to retrieve response, status code:", response.status_code)
    return chat_response

# Function to get a response from llm
def get_answer_by_llm(prompt, text):   
    backoff_time = 10
    while True:
        try:
            url = "http://localhost:11434/api/generate"
            data = {
                "model": "llama3:70b",
                "prompt": prompt + text,
                "stream": False
            }
            response = requests.post(url, json=data)
            response_data = response.json()
            print(response_data["response"])
            return response_data["response"]
        except:
            print("fail")
            time.sleep(backoff_time)


def get_role(prompt_dir):
        role = ""             
        with open(prompt_dir, 'r') as file:
            for line in file:
                role += line
        print(role)
        return role


# Function to process conversations and generate dialogue topics
def process_conversations(file_topic_summarized, file_generated, prompt):
    with open(file_topic_summarized, mode='r', newline='') as infile, \
         open(file_generated, mode='w', newline='') as outfile:
        
        reader = csv.DictReader(infile)
        fieldnames = ['role1_persona', 'role2_persona', 'original_dialogue', 'single_step_dialogue', 'generated_dialogue_topic', 'generated_dialogue', 'generated_single_step_dialogue', 'generated_multi_step_dialogue', 'multi_further_splited' ]
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()

        comversation_num = 0
        for conversation in reader:
            text = 'text:{\n' + 'multi_step_dialogue: {' + conversation['generated_multi_step_dialogue'] + ' ]' + '\n}'

            comversation_num = comversation_num + 1
            print("\ncomversation_num", comversation_num)
            print(text)

            further_splited_multi = get_answer_by_llm(prompt, text)
            conversation['multi_further_splited'] = further_splited_multi
            writer.writerow(conversation)

# Main function to run the script
def main():

    prompt_dir = 'further_split_prompt.txt'  # Path to the file containing the role
    input_file = 'data_formated.csv'
    output_file = 'further_splited.csv'  # Path to the output file for updated dialogues
    
    prompt = get_role(prompt_dir)
    process_conversations(input_file, output_file, prompt)

if __name__ == '__main__':
    main()

