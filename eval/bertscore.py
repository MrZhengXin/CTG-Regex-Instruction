from datasets import load_metric
import argparse
from bert_score import score


parser = argparse.ArgumentParser()
parser.add_argument('--ref', type=str, default='data/anlg/test.multi.ref')
parser.add_argument('--pred', type=str, default='res/anlg_test_aug_xl_deberta_filter_t5_xl_0419.txt')

args = parser.parse_args()
with open(args.ref, 'r') as f:
    references = f.readlines()
references_no_empty_line = list(filter(lambda x: x != '\n', references))
references_no_empty_line = [r.strip() for r in references_no_empty_line]

with open(args.pred, 'r') as f:
    predictions_original = f.readlines()
predictions_original = [p.strip() for p in predictions_original]

predictions_expand = []
ref_pos, len_ref = 0, len(references)
len_pred = len(predictions_original)
for prediction in predictions_original:
    while ref_pos < len_ref and references[ref_pos] != '\n':
        predictions_expand.append(prediction)
        ref_pos += 1
    ref_pos += 1


(P, R, f1_socre_list), hashname  = score(cands=predictions_expand, refs=references_no_empty_line, \
    lang='en', return_hash=True, idf=True)

f1_socre_list = f1_socre_list.tolist()

total_f1_score = 0.0
instance_f1_score, cnt = 0.0, 0

ref_pos = 0
while ref_pos < len_ref:
    while ref_pos < len_ref and references[ref_pos] != '\n':
        instance_f1_score = max(f1_socre_list.pop(0), instance_f1_score)
        cnt += 1
        ref_pos += 1
    total_f1_score += instance_f1_score # / cnt
    instance_f1_score, cnt = 0.0, 0
    ref_pos += 1
average_f1_score = total_f1_score / len_pred
print(args.pred[:-4], '%.2f' % (average_f1_score * 100), sep='\t')
