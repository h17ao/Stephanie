import csv
import time
import openai
import re

# Function to get the API key from a file
def get_api_key(filename):
    with open(filename, 'r') as file:
        api_key = file.readlines()[0].strip()
    return api_key
# claude-3-sonnet-20240229
# Function to get a response from GPT-4
def get_answer_by_gpt4(role, text, model='claude-3-sonnet-20240229', max_tokens=1000, temperature=0.3, top_p=0.5, frequency_penalty=0.5, presence_penalty=0.5, n=1):   
    backoff_time = 10
    while True:
        try:
            messages = [
                {"role": "user", "content": role + text}
            ]
            # print(role + text)
            res = openai.ChatCompletion.create(
                model=model,
                messages=messages,
                stream=False,
                max_tokens=max_tokens,
                temperature=temperature,
                top_p=top_p,
                frequency_penalty=frequency_penalty,
                presence_penalty=presence_penalty,
                n=n
            )
            return (res['choices'][0]['message']['content']).strip()
        except openai.error.OpenAIError as e:
            print(f"OpenAIError: {e}.")
            if "Please reduce your prompt" in str(e):
                max_tokens = int(max_tokens * 0.8)
                print(f"Reducing target length to {max_tokens}, retrying...")
            else:
                print(f"Retrying in {backoff_time} seconds...")
                time.sleep(backoff_time)


def get_role(filename):

    role = ""   
    with open(filename, 'r') as file:
        for line in file:
            role += line.strip() + '\n'
    return role


# Function to process conversations and generate dialogue topics
def process_conversations(input_file_path, output_file_path, role):
    with open(input_file_path, mode='r', newline='') as infile, \
         open(output_file_path, mode='w', newline='') as outfile:
        
        reader = csv.DictReader(infile)
        fieldnames = ['role1_persona', 'role2_persona', 'generated_dialogue_topic', 'original_single_step', 'generated_single_step', 'generated_multi_step', 'multi_further_splited', 'score']
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()
    
        dialogue_num = 0
        for conversation in reader:
            text = "\n" + "{ " + "\n" + "role1's persona: [" + conversation['role1_persona'] + "]\n\n" + "role2's persona: [" + conversation['role2_persona'] + "]\n\n" + "dialogue topic: [" + conversation['generated_dialogue_topic'] + "]\n\n" + "dialogue 1: [" + conversation['original_single_step'] + "]\n\n" + "dialogue 2: [" + conversation['generated_single_step'] + "]\n\n" + "dialogue 3: [" + conversation['generated_multi_step'] + "]\n\n" + "dialogue 4: [" + conversation['multi_further_splited'] + "]\n\n" + "}"
           
            score = get_answer_by_gpt4(role, text)
            
            conversation['score'] = score
            dialogue_num = dialogue_num + 1
            print("\ndialogue_num", dialogue_num)
            
            print(score)
            print("\n\n")

            writer.writerow(conversation)

# Main function to run the script
def main():
    filename = './key_gpt.txt'
    openai.api_base = 'https://api.aigcbest.top/v1'
    openai.api_key = get_api_key(filename)

    role_dir = 'eval_prompt.txt'  # Path to the file containing the role
    input_dialogue_file = 'data_to_eval.csv'
    output_dialogue_file = 'claude_evaled.csv'  # Path to the output file for updated dialogues

    role = get_role(role_dir)
    process_conversations(input_dialogue_file, output_dialogue_file, role)

if __name__ == '__main__':
    main()

