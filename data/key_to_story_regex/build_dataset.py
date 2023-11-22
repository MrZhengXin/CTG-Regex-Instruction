import json



with open('ROCStories_20_storylines_500_0.txt', 'r') as f:
    keys_list = f.readlines()
keys_list = [keys.split() for keys in keys_list]


fw = open('test.json', 'w')
for keys in zip(keys_list, text_list):
    cnt_word = len(keys)
    mask_exp = "<mask_0> " + " ".join(["%s(%d) <mask_%d>" % (word, i, i+1) for i, word in enumerate(keys)])
    regex = "<expression> %s </expression>" % (mask_exp)

    for i, word in enumerate(keys):
        text = text.replace(' ' + word + ' ', ' %s(%d) ' % (word, i))
    text = '<expression> ' + text.strip() + ' </expression>'
    print(json.dumps({
        "input": regex,
        "output": text
    }), file=fw)

