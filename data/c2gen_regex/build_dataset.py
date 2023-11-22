from datasets import load_dataset

dataset = load_dataset('Non-Residual-Prompting/C2Gen')


def preprocess(example):
    mask_exp = "<mask_0> " + " ".join(["%s(%d) <mask_%d>" % (word, i, i+1) for i, word in enumerate(example['keywords'])])
    regex = "<expression> %s </expression>" % (mask_exp)
    input_text = example['context'] + ' ' + regex
    output_text = regex # fake output
    processed = {
        'input': input_text,
        'output': output_text
    }
    return processed

old_columns = dataset['test'].column_names
for split in ['test']:
    output_filename = split + '.json'
    dataset[split] = dataset[split].map(preprocess, remove_columns=old_columns)
    dataset[split].to_json(output_filename)
# dataset['test'].to_json('dev.json')

