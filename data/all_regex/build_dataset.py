data_dir_list = ['ag_news_regex', 'anlg_regex', 'anlg_regex_length', 'anli_regex', 'commongen_regex', 'commongen_regex_length', 'conll2003_ner_regex', 'conll2003_pos_regex', 'winogrand_regex']

max_count = 100
for filename in ['train', 'dev', 'test']:
    all_instance_list = []
    for data_dir in data_dir_list:
        with open('../%s/%s.json' % (data_dir, filename), 'r') as f:
            instance_list = f.readlines()
        if filename == 'train':
            all_instance_list += instance_list
        else:
            all_instance_list += instance_list[:max_count]
    with open('%s.json' % filename, 'w') as f:
        print(*all_instance_list, sep='', file=f, end='')