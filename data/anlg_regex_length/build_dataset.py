import json
import os
import re

def clean_string(s):
    s = s.strip()
    s = s.capitalize()
    s = re.sub(r'\.+', ' .', s) # remove multiple continuous punctuation 
    s = re.sub('!+', ' !', s)
    s = s.replace(',.', ' .').replace(',.', ' .').replace('?.', ' .').replace('!.', ' !').replace('.,.', ' .')
    if s[-1] != '.' and s[-1] != '!':
        s += ' .'
    return s

dir_path = '../anlg'
filename_list = ['dev-w-comet-preds.jsonl', 'test-w-comet-preds.jsonl', 'train-w-comet-preds.jsonl']

for filename in filename_list:
    with open(os.path.join(dir_path, filename), 'r') as f:
        instance_list = f.readlines()
    fw = open(filename.replace('-w-comet-preds.jsonl', '.json'), 'w')
    instance_list = [json.loads(instance) for instance in instance_list]
    last_obs2 = ''
    for instance in instance_list:
        obs1, obs2 = instance['obs1'], instance['obs2']
        hyp = instance['hyp1'] if instance['label'] is '1' else instance['hyp2']
        hyp = hyp.replace(' .', '.').replace(' !', '!')
        # hyp = clean_string(hyp)
        hyp_split = hyp.split()
        length = len(hyp_split)
        hyp_split = [word+'_%d'%(i+1) for i, word in enumerate(hyp_split)]
        hyp = ' '.join(hyp_split)
        regex = "%s <expression> <mask_0> <length=%d> </expression> %s" % (obs1, length, obs2)
        if obs2 == last_obs2 and filename in ['dev-w-comet-preds.jsonl', 'test-w-comet-preds.jsonl']: # remove repetition input
            continue
        last_obs2 = obs2
        # instance["text"] = regex
        output_text = '<expression> %s </expression>' % hyp
        print(json.dumps({
            "input": regex,
            "output": output_text
        }), file=fw)
