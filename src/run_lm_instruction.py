import json
import argparse
from os import error
import re
from time import sleep
import random
from tqdm import tqdm

from language_model_api import BLOOM, GPT3, ChatGPT
from utils import get_regex, check_regex, check_regex_structure

random.seed()

parser = argparse.ArgumentParser()
parser.add_argument('--model', type=str, default='bloomz')
parser.add_argument('--src', type=str)
parser.add_argument('--tgt', type=str)
parser.add_argument('--max_try', type=int, default=8)
parser.add_argument('--max_instance', type=int, default=8888888888)
parser.add_argument('--token', type=str, default='')
args = parser.parse_args()

if args.model in ['bloom', 'bloomz', 'bloomz-7b1']:
    llm = BLOOM(args.model)
elif args.model in ['GPT3']:
    llm = GPT3() if args.token=='' else GPT3(token=args.token)
elif args.model in ['gpt-3.5-turbo']:
    llm = ChatGPT(model=args.model, token=args.token)
# elif args.model in ['EdgeGPT']:
    # llm = EdgeGPT()
else:
    raise AssertionError



def make_prompt(test_instance, train_instance_list, expression, num_shot):
    selected_instance_list = []
    for max_try in range(100):
        instance = random.choice(train_instance_list)
        if instance == test_instance:
            continue
        if check_regex_structure(expression, get_regex(instance['regex'])):
            del instance['regex']
            selected_instance_list.append(instance)
            num_shot -= 1
            if num_shot == 0:
                break
    other_instance_list = random.choices(train_instance_list, k=num_shot)
    for instance in other_instance_list:
        del instance['regex']
    selected_instance_list += other_instance_list
    # prompt = '\n'.join([json.dumps(instance, indent=0) for instance in selected_instance_list])
    prompt = '\n'.join([json.dumps(instance, ensure_ascii=False) for instance in selected_instance_list])    
    return prompt

with open(args.src, 'r') as f:
    test_instance_list = f.readlines()
test_instance_list = [json.loads(test_instance) for test_instance in test_instance_list]

cnt_previous = 0
try:
    with open(args.tgt, 'r') as f:
        cnt_previous = len(f.readlines())
except:
    pass
fw = open(args.tgt, 'a')
total_instance = 0
retry_cnt = 0
first_success = 0
final_success = 0
for test_instance in tqdm(test_instance_list[cnt_previous:args.max_instance]):
    total_instance += 1
    output = ''
    expression = get_regex(test_instance['regex'])
    print(expression)
    print(test_instance['input'])
    for i in range(args.max_try):
        final_input = test_instance['input'] + '\n'
        final_input = final_input.replace(r'\"', '"').replace(r'\/', '/')
        len_final_input = len(final_input)
        try:
            # data = infer(final_input)
            # output = data[0]['generated_text'][len_final_input:].strip()
            # print(final_input)
            output = llm.infer(final_input, stop=None)
            print(output)
            # input()
            # output = re.sub('<[^>]*>', '', output)
        except:
            print('api failure')
            continue
        
        if output == '':
            print("empty result")
            continue

        output = output.replace('\"', '"').strip().replace('\n', ' ')
        if output[0] == '"' and output[-1] == '"':
            output = output[1:-1]


        if check_regex(expression, output):
            print(output)
            final_success += 1
            if i == 0:
                first_success += 1
            break
        else:
            print('regex failure')
            retry_cnt += 1
            sleep(0.3)
            # input()
            continue
    print(output, file=fw)
    sleep(0.3)

with open('log.txt', 'a') as f:
    print(args.tgt, end='\t', file=f)
    print(total_instance, retry_cnt, first_success, final_success, sep='\t', file=f)