from datasets import load_dataset

dataset = load_dataset('ag_news')

label_list = dataset['test'].features["label"].names
option_list_str = '<options> %s </options>' % \
    (' '.join(['<choice_%d> %s </choice_%d>' % \
        (i, option, i) for i, option in enumerate(label_list)]))
prompt = '\nTopic classification: <expression> %s </expression>' % option_list_str

def preprocess(example):
    label = dataset['test'].features["label"].int2str(example['label'])
    text = example['text'].replace('\\', ' ')
    input_text = text + prompt
    output_text = '<expression> %s </expression>' % label
    processed = {
        'input': input_text,
        'output': output_text
    }
    return processed

old_columns = dataset['test'].column_names
for split in ['train', 'test']:
    output_filename = split + '.json'
    dataset[split] = dataset[split].map(preprocess, remove_columns=old_columns)
    dataset[split].to_json(output_filename)
dataset['test'].to_json('dev.json')

