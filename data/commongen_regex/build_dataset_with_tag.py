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
        cnt_word = len(word_list)
        mask_exp = "<mask_0> " + " ".join(["%s(%d) <mask_%d>" % (word, i, i+1) for i, word in enumerate(word_list)])
        regex = "<expression> %s </expression>" % (mask_exp)
        instance["summary"] = instance["summary"].strip('!.')
        output_text = ' ' + instance["summary"] + ' '

        for i, word in enumerate(word_list):
            output_text = output_text.replace(' ' + word + ' ', ' %s(%d) ' % (word, i))
        output_text = '<expression> ' + output_text.strip() + ' </expression>'
        '''
        sentence_split, pos = instance["summary"].strip(' !.').split(), 0
        for i, word in enumerate(word_list):
            output_text += ' <mask_%d>' % i
            while sentence_split[pos] != word:
                output_text += ' ' + sentence_split[pos]
                pos += 1
            pos += 1
            output_text += ' </mask_%d>' % i
            output_text += ' ' + word
        output_text += 
        output_text += ' </expression> '''
        # instance["text"] = regex
        print(json.dumps({
            "input": regex,
            "output": output_text
        }), file=fw)
