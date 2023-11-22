import json
import argparse
import re
import random
from tqdm import tqdm

from seq2seq_language_model import Seq2SeqLanguageModel

random.seed()

parser = argparse.ArgumentParser()
parser.add_argument('--model_path', type=str, default='model/all_regex/flan-t5-xl')
parser.add_argument('--src', type=str)
parser.add_argument('--tgt', type=str)
parser.add_argument('--num_shot', type=int, default=8)
parser.add_argument('--max_retry', type=int, default=32)
parser.add_argument('--max_instance', type=int, default=8888888888)
parser.add_argument('--nested_regex', action='store_true')
args = parser.parse_args()

model = Seq2SeqLanguageModel('model/all_regex/flan-t5-xl')

with open(args.src, 'r') as f:
    test_instance_list = f.readlines()
test_instance_list = [json.loads(test_instance) for test_instance in test_instance_list]

fw = open(args.tgt, 'w')

total_instance = len(test_instance_list)
retry_cnt = 0
first_success = 0
final_success = 0

for test_instance in tqdm(test_instance_list[:args.max_instance]):
    retry = 0
    if not args.nested_regex:
        output, retry = model.reject_sampling(test_instance['input'], max_retry=args.max_retry) 
    else: 
        output, retry = model.nested_regex(test_instance['input'])
    if retry != -1:
        final_success += 1
        if retry == 1:
            first_success += 1
    else:
        retry = args.max_retry
    retry_cnt += retry
    output = output.replace('\n', ' ')
    print(output, file=fw)

with open('log_seq2seq.txt', 'a') as f:
    print(args.tgt, end='\t', file=f)
    avg_retry = retry_cnt / total_instance
    first_success_rate = (first_success / total_instance) * 100.0
    final_success_rate = (final_success / total_instance) * 100.0
    print(total_instance, retry_cnt, first_success, final_success, '%.2f' % avg_retry, '%.2f' % first_success_rate, '%.2f' % final_success_rate, sep='\t', file=f)