import argparse
import json

parser = argparse.ArgumentParser()
parser.add_argument('--src', type=str)
parser.add_argument('--pred', type=str)
parser.add_argument('--output_file', type=str, default='accuracy.txt')
args = parser.parse_args()

fw = open(args.output_file, 'a')
print(args.pred, end='\t', file=fw)

with open(args.src, 'r') as f:
    instance_list = f.readlines()
instance_list = [json.loads(instance) for instance in instance_list]

with open(args.pred, 'r') as f:
    pred_list = f.readlines()

hit, cnt = 0, len(pred_list)

for instance, pred in zip(instance_list, pred_list):
    tgt = instance['output'].replace('<expression> ', '').replace(' </expression>', '').strip()
    pred = pred.replace('<expression> ', '').replace(' </expression>', '').strip()
    if pred.startswith("("):
        pred = eval(pred)[0]
    hit += (tgt == pred)
    if tgt != pred:
        print(instance['input'])
        print(tgt)
        print(pred)
        input()

rate = hit / cnt
print(args.pred, '%.2f' % (rate * 100.0))