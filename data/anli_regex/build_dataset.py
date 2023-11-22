import json

from datasets.load import HubDatasetModuleFactoryWithoutScript



for filename in ['dev', 'test', 'train']:
    with open('../anli/%s.jsonl' % filename, 'r') as f:
        src = f.readlines()
        src = [json.loads(s) for s in src]
    with open('../anli/%s-labels.lst' % filename, 'r') as f:
        labels = f.readlines()
        labels = [int(t.strip()) for t in labels]
    fw = open(filename + '.json', 'w')

    for i, label in zip(src, labels):
        obs1, obs2 = i['obs1'], i['obs2']
        hyp1, hyp2 = i['hyp1'], i['hyp2']
        gold_hyp = hyp1 if label == 1 else hyp2
        option_list_str = '<options> %s </options>' % \
            (' '.join(['<choice_%d> %s </choice_%d>' % \
                (i, option, i) for i, option in enumerate([hyp1, hyp2])]))

        regex = "%s <expression> %s </expression> % s" % (obs1, option_list_str, obs2)
        output_text = '<expression> %s </expression>' % gold_hyp
        print(json.dumps({
            "input": regex,
            "output": output_text
        }), file=fw)
            
