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


def get_role(input_example_file, prompt_dir):
    with open(input_example_file, mode='r', newline='') as infile:
        reader = csv.DictReader(infile)
        example_num = 0
        example = ""
        example1 = ""
        example2 = ""
        role = ""

        # for conversation in reader:
        #     example_num += 1
        #     if  example_num <= 5:
        #         multi_example_temp = 'example ' + str(example_num) +' for multi-step dialogue' +  ': {\n' + 'persona of role1: [ ' + conversation['role1_persona'] + ' ]' + '\n' + 'persona of role2: [ ' + conversation['role2_persona'] + ' ]' + '\n' + 'multi-step dialogue: [ ' + conversation['multi_step_dialogue'] + ' ]' + '\n' + '}' + '\n' + '\n'
        #         example1 += multi_example_temp
        #     if  6 <= example_num <= 10:
        #         single_example_temp = 'example ' + str(example_num - 5) +' for single-step dialogue' +  ': {\n' + 'persona of role1: [ ' + conversation['role1_persona'] + ' ]' + '\n' + 'persona of role2: [ ' + conversation['role2_persona'] + ' ]' + '\n' + 'single-step dialogue: [ ' + conversation['single_step_dialogue'] + ' ]' + '\n' + '}' + '\n' + '\n'
        #         example2 += single_example_temp
        # example += example2
        # example += example1
            
    
        with open(prompt_dir, 'r') as file:
            for line in file:
                role += line
            example += role
        prompt = example
        print(prompt)
        return prompt


# Function to process conversations and generate dialogue topics
def process_conversations(file_topic_summarized, file_generated, prompt):
    with open(file_topic_summarized, mode='r', newline='') as infile, \
         open(file_generated, mode='w', newline='') as outfile:
        
        reader = csv.DictReader(infile)
        fieldnames = ['role1_persona', 'role2_persona', 'original_dialogue', 'single_step_dialogue', 'generated_dialogue_topic', 'generated_dialogue']
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()

        comversation_num = 0
        for conversation in reader:
            text = 'text:{\n' + 'persona of role1: [ ' + conversation['role1_persona'] + ' ]' + '\n' + 'persona of role2: [ ' + conversation['role2_persona'] + ' ]' + '\n' + 'dialogue topic: [ ' + conversation['generated_dialogue_topic'] + ' ]' + '\n}'
            generated_dialogue = get_answer_by_llm(prompt, text)
            
            comversation_num = comversation_num + 1

            print("\ncomversation_num", comversation_num)
            print(text)

            conversation['generated_dialogue'] = generated_dialogue
            writer.writerow(conversation)

# Main function to run the script
def main():

    prompt_dir = 'data_generate_prompt.txt'  # Path to the file containing the role
    file_topic_summarized = 'topic_summarized.csv'
    file_generated = 'data_generated.csv'  # Path to the output file for updated dialogues
    
    prompt = get_role(input_example_file, prompt_dir)
    process_conversations(file_topic_summarized, file_generated, prompt)

if __name__ == '__main__':
    main()

