from src.utils import get_regex, check_regex
import argparse
import json
import re

def check_appear(word_list, pred):
    for word in word_list:
        if word not in pred:
            return 0
    return 1

parser = argparse.ArgumentParser()
parser.add_argument('--src', type=str)
parser.add_argument('--pred', type=str)
parser.add_argument('--no_order', action='store_true')
parser.add_argument('--output_file', type=str, default='regex_match_rate.txt')
args = parser.parse_args()

fw = open(args.output_file, 'a')
print(args.pred, end='\t', file=fw)

with open(args.src, 'r') as f:
    instance_list = f.readlines()
instance_list = [json.loads(instance) for instance in instance_list]

with open(args.pred, 'r') as f:
    pred_list = f.readlines()

hit, cnt = 0, len(pred_list)
instance_list = instance_list[:cnt]

for instance, pred in zip(instance_list, pred_list):
    if pred.startswith("("):
        pred = eval(pred)[0]
    src = instance['input']
    regex = get_regex(src if 'regex' not in instance.keys() else instance['regex'])
    correct = check_regex(regex, pred)
    hit += correct
    
    
    if not correct and args.no_order:
        word_list = re.split(r'\.\*', regex)[1:-1]
        if check_appear(word_list, pred):
            hit += 1
            continue
        # print(regex)
        # print(pred)
        # input()


rate = hit / cnt
# print(hit, cnt)
print(args.pred, '%.2f' % (rate * 100.0), sep='\t')