import csv
import time
import re

def reorder(dialogue):
    messages = dialogue.strip('[]').split('|')
    reordered_messages = []

    for msg in messages:
        trimmed_msg = msg.strip()
        if trimmed_msg.startswith('role1:'):
            formatted_msg = "role1: " + trimmed_msg.replace('role1:', '', 1).strip()
            reordered_messages.append(formatted_msg)
        elif trimmed_msg.startswith('role2:'):
            formatted_msg = "                    role2: " + trimmed_msg.replace('role2:', '', 1).strip()
            reordered_messages.append(formatted_msg)

    return '\n'.join(reordered_messages)

def persona_reorder(dialogue):
    messages = dialogue.strip('[]').split('|')
    reordered_messages = []
    

    for msg in messages:
        trimmed_msg = msg.strip()
        reordered_messages.append(trimmed_msg)

    return '\n'.join(reordered_messages)

def adaptive_row(text, line_length=80):
    return '\n'.join(text[i:i+line_length] for i in range(0, len(text), line_length))


# Function to process conversations and generate dialogue topics
def process_conversations(input_file_path, output_file_path):
    with open(input_file_path, mode='r', newline='') as infile, \
         open(output_file_path, mode='w', newline='') as outfile:
        
        reader = csv.DictReader(infile)
        fieldnames = ['role1_persona', 'role2_persona', 'original_dialogue', 'single_step_dialogue', 'generated_dialogue_topic', 'generated_dialogue', 'generated_single_step_dialogue', 'generated_multi_step_dialogue']
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()

        comversation_num = 0
        for conversation in reader:

            text = conversation['single_step_dialogue']
            adjust = reorder(text)
            conversation['single_step_dialogue'] = adjust
            print("text", text)
            print("@")
            print("adjust", adjust)
            print("\n")

            text = conversation['role1_persona']
            adjust = persona_reorder(text)
            conversation['role1_persona'] = adjust
            print("text", text)
            print("@")
            print("adjust", adjust)
            print("\n")

            text = conversation['role2_persona']
            adjust = persona_reorder(text)
            conversation['role2_persona'] = adjust
            print("text", text)
            print("@")
            print("adjust", adjust)
            print("\n")

            # text = conversation['generated_dialogue_topic']
            # adjust = adaptive_row(text)
            # conversation['generated_dialogue_topic'] = adjust
            # print("text", text)
            # print("@")
            # print("adjust", adjust)
            # print("\n")
            
            comversation_num = comversation_num + 1
            print("\ncomversation_num", comversation_num)
           

            writer.writerow(conversation)

# Main function to run the script
def main():
  
 
    input_dialogue_file = 'data_extracted.csv'
    output_dialogue_file = 'data_formated.csv'  # Path to the output file for updated dialogues
    process_conversations(input_dialogue_file, output_dialogue_file)

if __name__ == '__main__':
    main()
