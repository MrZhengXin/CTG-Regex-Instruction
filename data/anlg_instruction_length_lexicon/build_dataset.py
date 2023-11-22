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
        # hyp = hyp.replace(verb, verb+'(0)')

        # hyp = clean_string(hyp)
        hyp_split = hyp.split()
        length = len(hyp_split)
        # hyp_split = [word+'_%d'%(i+1) for i, word in enumerate(hyp_split)]
        # hyp = ' '.join(hyp_split)
        # instruction = 'Insert a sentence between Obs1="%s" and Obs2="%s", while also containing the keyword "%s" and controlling the word count to %d.' % (obs1, obs2, verb, length)
        instruction = "The first sentence is \" %s \" and the last sentence is \" %s \" . Insert a middle sentence with similar style, while also containing the keyword \"%s\", and the length shall be exactly %d words without counting punctuation." % (obs1, obs2, verb, length)
        regex = "<expression> <mask_0> %s <mask_1> <length=%d> </expression>" % (verb, length)

        if obs2 == last_obs2 and filename in ['dev-w-comet-preds.jsonl', 'test-w-comet-preds.jsonl']: # remove repetition input
            continue
        last_obs2 = obs2
        # instance["text"] = instruction
        output_text = hyp
        print(json.dumps({
            "input": instruction,
            "output": output_text,
            "regex": regex
        }), file=fw)
