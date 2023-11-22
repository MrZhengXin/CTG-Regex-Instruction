import json
import os
import re
import nltk

def clean_string(s):
    s = s.strip()
    s = s.capitalize()
    s = re.sub(r'\.+', ' .', s) # remove multiple continuous punctuation 
    s = re.sub('!+', ' !', s)
    s = s.replace(',.', ' .').replace(',.', ' .').replace('?.', ' .').replace('!.', ' !').replace('.,.', ' .')
    if s[-1] != '.' and s[-1] != '!':
        s += ' .'
    return s

def get_verb(text):
    text = nltk.word_tokenize(text)
    tags = nltk.pos_tag(text)
    for word, tag in tags:
        if tag.startswith('V'):
            return word
    return tags[1][0]

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
        
        verb = get_verb(hyp)
        hyp = hyp.replace(verb, verb+'(0)')


        regex = "%s <expression> <mask_0> %s <mask_1> </expression> %s" % (obs1, verb, obs2)
        if obs2 == last_obs2 and filename in ['dev-w-comet-preds.jsonl', 'test-w-comet-preds.jsonl']: # remove repetition input
            continue
        last_obs2 = obs2
        # instance["text"] = regex
        output_text = '<expression> %s </expression>' % hyp
        print(json.dumps({
            "input": regex,
            "output": output_text
        }), file=fw)