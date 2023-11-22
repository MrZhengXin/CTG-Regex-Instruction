import json
import pandas as pd

df = pd.read_csv('cloze_test_test__spring2016 - cloze_test_ALL_test.csv')

fw = open('test.json', 'w')

for _, row in df.iterrows():
    text = ' '.join([row['InputSentence1'], row['InputSentence2'], row['InputSentence3'] ,row['InputSentence4']])
    end1, end2 = row['RandomFifthSentenceQuiz1'], row['RandomFifthSentenceQuiz2']
    gold_end = end1 if row['AnswerRightEnding'] == 1 else end2
    option_list_str = '<options> %s </options>' % \
        (' '.join(['<choice_%d> %s </choice_%d>' % \
            (i, option, i) for i, option in enumerate([end1, end2])]))

    regex = "%s <expression> %s </expression>" % (text, option_list_str)
    output_text = '<expression> %s </expression>' % gold_end
    print(json.dumps({
        "input": regex,
        "output": output_text
    }), file=fw)
        

df = pd.read_csv('cloze_test_val__spring2016 - cloze_test_ALL_val.csv')

fw = open('train.json', 'w')

for _, row in df.iterrows():
    text = ' '.join([row['InputSentence1'], row['InputSentence2'], row['InputSentence3'] ,row['InputSentence4']])
    end1, end2 = row['RandomFifthSentenceQuiz1'], row['RandomFifthSentenceQuiz2']
    gold_end = end1 if row['AnswerRightEnding'] == 1 else end2
    option_list_str = '<options> %s </options>' % \
        (' '.join(['<choice_%d> %s </choice_%d>' % \
            (i, option, i) for i, option in enumerate([end1, end2])]))

    regex = "%s <expression> %s </expression>" % (text, option_list_str)
    output_text = '<expression> %s </expression>' % gold_end
    print(json.dumps({
        "input": regex,
        "output": output_text
    }), file=fw)
        
