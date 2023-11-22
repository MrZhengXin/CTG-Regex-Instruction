from datasets import load_dataset

dataset = load_dataset("winograd_wsc", 'wsc273')['test']
dataset.to_json('wsc273.json')


def preprocess(example):
    option_0, option_1 = example['options'][0], example['options'][1]
    pronoun = example['pronoun']
    text = example['text']
    quote = text[example['quote_loc']:].strip('.')
    if example['quote_loc'] != example['pronoun_loc']:
        if option_0.startswith('The'):
            option_0 = 't' +option_0[1:]
        if option_1.startswith('The'):
            option_1 = 't' +option_1[1:]
    if pronoun in ['his', 'her', 'their', 'its']:
        option_0 = option_0 + "'s"
        option_1 = option_1 + "'s"
    options = [option_0, option_1]
    option_list = '<options> %s </options>' % \
        (' '.join(['<choice_%d> %s </choice_%d>' % \
            (i, option, i) for i, option in enumerate(options)]))
    prompt = (' ' + quote + ' ').replace(' ' + pronoun + ' ', ' ' + option_list + ' ').strip()
    prompt = ' <expression> %s </expression> ' % prompt
    input_text = text + prompt
    correct_option = options[example['label']]
    output_text = (' ' + quote + ' ').replace(' ' + pronoun + ' ', ' ' + correct_option + ' ').strip()
    output_text = ' <expression> %s </expression> ' % output_text
    processed = {
        'input': input_text.replace(' .', '.'),
        'output': output_text.replace(' .', '.')
    }
    return processed

old_columns = dataset.column_names
dataset = dataset.map(preprocess, remove_columns=old_columns)
dataset.to_json('test.json')
