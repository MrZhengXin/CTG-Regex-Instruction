import json
import os

dir_path = '../anlg'
filename_list = ['dev-w-comet-preds.jsonl', 'test-w-comet-preds.jsonl', 'train-w-comet-preds.jsonl']

for filename in filename_list:
    with open(os.path.join(dir_path, filename), 'r') as f:
        instance_list = f.readlines()
    fw = open(filename.replace('-w-comet-preds.jsonl', '.json'), 'w')
    instance_list = [json.loads(instance) for instance in instance_list]
    last_regex = ''
    for instance in instance_list:
        obs1, obs2 = instance['obs1'], instance['obs2']
        hyp = instance['hyp1'] if instance['label'] is '1' else instance['hyp2']
        regex = "%s <expression> <mask_0> </expression> %s" % (obs1, obs2)
        if regex == last_regex and filename in ['dev-w-comet-preds.jsonl', 'test-w-comet-preds.jsonl']: # remove repetition input
            continue
        last_regex = regex
        # instance["text"] = regex
        output_text = '<expression> %s </expression>' % hyp
        print(json.dumps({
            "input": regex,
            "output": output_text
        }), file=fw)
