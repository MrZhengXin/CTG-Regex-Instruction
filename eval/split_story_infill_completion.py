import argparse
import json
import re

parser = argparse.ArgumentParser()
parser.add_argument('--pred', type=str, default='/mnt/bd/zhengxin2/language_model_with_regular_expressions/res/story_infill_completion/test_GPT3_8_shot.txt')
args = parser.parse_args()

with open(args.pred, 'r') as f:
    pred_list = f.readlines()

first_sent_list = []
second_sent_list = []

for pred in pred_list:
    pred = pred.strip()
    try:
        first_sent, second_sent = re.split(r'[\.!"\?] ', pred)
    except:
        first_sent, second_sent = '', pred
    first_sent_list.append(first_sent)
    second_sent_list.append(second_sent)

with open(args.pred+'.first', 'w') as f:
    print(*first_sent_list, sep='\n', file=f)
with open(args.pred+'.second', 'w') as f:
    print(*second_sent_list, sep='\n', file=f)
