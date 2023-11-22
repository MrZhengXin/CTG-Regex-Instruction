from datasets import load_dataset

dataset = load_dataset("winogrande", 'winogrande_xl')


def preprocess(example):
    text = example['sentence']
    options = [example['option1'], example['option2']]
    option_list = '<options> %s </options>' % \
        (' '.join(['<choice_%d> %s </choice_%d>' % \
            (i, option, i) for i, option in enumerate(options)]))
    prompt = '<expression> %s </expression>' % option_list
    input_text = text.replace('_', prompt)
    correct_option = example['option1'] if example['answer'] is '1' else example['option2']
    output_text = '<expression> %s </expression>' % correct_option
    processed = {
        'input': input_text,
        'output': output_text
    }
    return processed

old_columns = dataset['test'].column_names
for split in ['train', 'validation']:
    output_filename = (split if split != 'validation' else 'dev') + '.json'
    dataset[split] = dataset[split].map(preprocess, remove_columns=old_columns)
    dataset[split].to_json(output_filename)
dataset['validation'].to_json('test.json')