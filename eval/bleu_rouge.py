from evaluate import load
import argparse


parser = argparse.ArgumentParser()
parser.add_argument('--ref', type=str, default='data/newstest2017-wiktionary/test.ref')
parser.add_argument('--pred', type=str, default='res/newstest2017-wiktionary/test_GPT3_8_shot.txt')
parser.add_argument('--multi_ref', action='store_true')

args = parser.parse_args()

with open(args.pred, 'r') as f:
    predictions = f.readlines()
predictions = [p.strip('\n.?!') for p in predictions]

with open(args.ref, 'r') as f:
    references = f.readlines()

if args.multi_ref:
    references_group = []
    ref_pos, len_ref = 0, len(references)
    this_refs = []
    while ref_pos < len_ref:
        if references[ref_pos] != '\n':
            this_refs.append(references[ref_pos])
            ref_pos += 1
        else:
            references_group.append(this_refs)
            this_refs = []
            ref_pos += 1
    references = references_group
else:
    references = [[ref.strip('\n.?!')] for ref in references]


metrics = load('sacrebleu')
score = metrics.compute(predictions=predictions, references=references)
print(args.pred[:-4], end='\t')
print('%.2f' % (score['score']), end='\t')

metrics = load('rouge')
score = metrics.compute(predictions=predictions, references=references)
print('%.2f' % (score['rougeL'] * 100.0))
