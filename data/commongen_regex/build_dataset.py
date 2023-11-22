import json
import os

dir_path = '../commongen_ordered_identical'
filename_list = ['dev.json', 'train.json']

for filename in filename_list:
    with open(os.path.join(dir_path, filename), 'r') as f:
        instance_list = f.readlines()
    fw = open(filename, 'w')
    instance_list = [json.loads(instance) for instance in instance_list]
    for instance in instance_list:
        word_list = eval(instance["text"])
        cnt_word = len(word_list)
        mask_exp = "<mask_0> " + " ".join(["%s <mask_%d>" % (word, i+1) for i, word in enumerate(word_list)])
        regex = " <expression> %s </expression> " % (mask_exp)
        # instance["text"] = regex
        print(json.dumps({
            "input": regex,
            "output": " " + instance["summary"] + " "
        }), file=fw)
