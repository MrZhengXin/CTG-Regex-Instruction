from datasets import load_dataset

dataset = load_dataset('gigaword')


def preprocess(example):
    length = len(example['summary'].split())
    regex = "<expression> <length=%d> </expression>" % (length)
    input_text = '%s\nSummarize the aforementioned text in a single phrase.\n%s' % (example['document'], regex)
    output_text = example['summary']
    processed = {
        'input': input_text,
        'output': output_text
    }
    return processed

old_columns = dataset['test'].column_names
for split in ['validation', 'test']:
    output_filename = split + '.json'
    dataset[split] = dataset[split].map(preprocess, remove_columns=old_columns)
    dataset[split] = dataset[split].filter(lambda example: '<length=2>' not in example["input"])
    dataset[split].to_json(output_filename)

with open('test.ref', 'w') as f:
    print(*dataset['test']['output'], file=f, sep='\n')