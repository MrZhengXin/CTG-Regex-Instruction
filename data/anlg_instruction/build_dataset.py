import json
import os

dir_path = '../anlg'
filename_list = ['dev-w-comet-preds.jsonl', 'test-w-comet-preds.jsonl', 'train-w-comet-preds.jsonl']

for filename in filename_list:
    with open(os.path.join(dir_path, filename), 'r') as f:
        instance_list = f.readlines()
    fw = open(filename.replace('-w-comet-preds.jsonl', '.json'), 'w')
    instance_list = [json.loads(instance) for instance in instance_list]
    last_instruction = ''
    for instance in instance_list:
        obs1, obs2 = instance['obs1'], instance['obs2']
        hyp = instance['hyp1'] if instance['label'] is '1' else instance['hyp2']
        regex = "<expression> <mask_0> </expression>"
        # instruction = 'Insert a sentence between Obs1="%s" and Obs2="%s"' % (obs1, obs2)
        instruction = "The first sentence is \" %s \" and the last sentence is \" %s \" . Insert a middle sentence with similar style, and the length shall not exceed 10 words." % (obs1, obs2)
        if instruction == last_instruction and filename in ['dev-w-comet-preds.jsonl', 'test-w-comet-preds.jsonl']: # remove repetition input
            continue
        last_instruction = instruction
        # instance["text"] = instruction
        output_text = hyp
        print(json.dumps({
            "input": instruction,
            "output": output_text,
            "regex": regex
        }), file=fw)
