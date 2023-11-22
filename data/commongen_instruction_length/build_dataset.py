import json
import os

dir_path = '../commongen_ordered_identical'
filename_list = ['dev.json', 'train.json']

for filename in filename_list:
    with open(os.path.join(dir_path, filename), 'r') as f:
        instance_list = f.readlines()
    # fw = open(filename[:-5]+'_with_tag.json', 'w')
    fw = open(filename, 'w')
    instance_list = [json.loads(instance) for instance in instance_list]
    for instance in instance_list:
        word_list = eval(instance["text"])
        output_text = instance["summary"]

        length = len(output_text.split())
        word_list_str = '"%s"' % ('", "'.join(word_list))
        instruction = "Generate a sentence that mentions all of these concepts in sequential order with the word count of %d, punctuation ignored: " % (length) + word_list_str

        mask_exp = "<mask_0> " + " ".join(["%s(%d) <mask_%d>" % (word, i, i+1) for i, word in enumerate(word_list)])
        regex = "<expression> %s <length=%d> </expression>" % (mask_exp, length)

        print(json.dumps({
            "input": instruction,
            "output": output_text,
            "regex": regex
        }), file=fw)
