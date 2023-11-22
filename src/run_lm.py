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
parser.add_argument('--train', type=str)
parser.add_argument('--num_shot', type=int, default=8)
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
else:
    raise AssertionError

with open(args.train, 'r') as f:
    train_instance_list = f.readlines()
train_instance_list = [json.loads(train_instance) for train_instance in train_instance_list]


def make_prompt(test_instance, train_instance_list, expression, num_shot):
    selected_instance_list = []
    for max_try in range(100):
        instance = random.choice(train_instance_list)
        if instance == test_instance:
            continue
        if check_regex_structure(expression, get_regex(instance['input'])):
            selected_instance_list.append(instance)
            num_shot -= 1
            if num_shot == 0:
                break
    selected_instance_list += random.choices(train_instance_list, k=num_shot)
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
    test_instance['output'] = '<expression> '
    expression = get_regex(re.sub('_[0-9]+ ', ' ', test_instance['input']))
    print(expression)
    prompt = make_prompt(test_instance, train_instance_list, expression, args.num_shot)
    # print(prompt)
    instance_str = json.dumps(test_instance, ensure_ascii=False)[:-2].strip()
    print(instance_str)
    for i in range(args.max_try):
        final_input = prompt + '\n' + instance_str
        final_input = final_input.replace(r'\"', '"').replace(r'\/', '/')
        len_final_input = len(final_input)
        try:
            # data = infer(final_input)
            # output = data[0]['generated_text'][len_final_input:].strip()
            # print(final_input)
            output = llm.infer(final_input)
            print(output)
            # input()
            # output = re.sub('<[^>]*>', '', output)
        except:
            output = llm.infer(final_input)
            print('api failure')
            continue
        
        try:
            # output = re.findall('<expression>.*</expression>', output)[0]
            output = re.findall('.*</expression>', output)[0]
            output = re.sub('<[^>]*>', '', output)
            output = re.sub('_[0-9]+', '', output).strip()
            output = re.sub(r'\([0-9]+\)', '', output).strip()
            output = output.replace('\"', '"')
        except:
            print('format failure')
            sleep(3)
            continue

        if check_regex(expression, output):
            print(output)
            final_success += 1
            if i == 0:
                first_success += 1
            break
        else:
            # prompt = make_prompt(train_instance_list, expression, args.num_shot)
            print('regex failure')
            retry_cnt += 1
            sleep(0.3)
            # input()
            continue
    print(output, file=fw)
    sleep(0.3)

with open('log_few_shot.txt', 'a') as f:
    print(args.tgt, end='\t', file=f)
    avg_retry = retry_cnt / total_instance
    first_success_rate = (first_success / total_instance) * 100.0
    final_success_rate = (final_success / total_instance) * 100.0
    print(total_instance, retry_cnt, first_success, final_success, '%.2f' % avg_retry, '%.2f' % first_success_rate, '%.2f' % final_success_rate, sep='\t', file=f)