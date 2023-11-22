import json
import pandas as pd

df = pd.read_csv('../story_completion/cloze_test_test__spring2016 - cloze_test_ALL_test.csv')

fw = open('test.json', 'w')
fw_first = open('test.ref.first', 'w')
fw_second = open('test.ref.second', 'w')

for _, row in df.iterrows():
    if row['InputSentence4'][-1] not in ['.', '!', '?', '"']:
        row['InputSentence4'] += '.'
    text = ' '.join([row['InputSentence1'], row['InputSentence2'], row['InputSentence3']])
    end1, end2 = row['RandomFifthSentenceQuiz1'], row['RandomFifthSentenceQuiz2']
    gold_end = end1 if row['AnswerRightEnding'] == 1 else end2
    option_list_str = '<options> %s </options>' % \
        (' '.join(['<choice_%d> %s </choice_%d>' % \
            (i, option, i) for i, option in enumerate([end1, end2])]))

    regex = "%s <expression> <mask_0> %s </expression>" % (text, option_list_str)
    output_text = '<expression> %s </expression>' % (row['InputSentence4'] + ' ' + gold_end)
    print(json.dumps({
        "input": regex,
        "output": output_text
    }), file=fw)
    print(row['InputSentence4'], file=fw_first)
    print(gold_end, file=fw_second)
        

df = pd.read_csv('../story_completion/cloze_test_val__spring2016 - cloze_test_ALL_val.csv')

fw = open('train.json', 'w')

for _, row in df.iterrows():
    if row['InputSentence4'][-1] not in ['.', '!', '?', '"']:
        row['InputSentence4'] += '.'
    text = ' '.join([row['InputSentence1'], row['InputSentence2'], row['InputSentence3']])
    end1, end2 = row['RandomFifthSentenceQuiz1'], row['RandomFifthSentenceQuiz2']
    gold_end = end1 if row['AnswerRightEnding'] == 1 else end2
    option_list_str = '<options> %s </options>' % \
        (' '.join(['<choice_%d> %s </choice_%d>' % \
            (i, option, i) for i, option in enumerate([end1, end2])]))

    regex = "%s <expression> <mask_0> %s </expression>" % (text, option_list_str)
    output_text = '<expression> %s </expression>' % (row['InputSentence4'] + ' ' + gold_end)
    print(json.dumps({
        "input": regex,
        "output": output_text
    }), file=fw)
        
