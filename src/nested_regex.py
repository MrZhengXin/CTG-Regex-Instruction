import re

regex_label_list = ['<options>', '<mask_', '<class>']
def contain_options(expression):
    if '<options>' in expression:
        return False
    return True

def contain_nonterminal_symbol(expression):
    for regex_label in regex_label_list:
        if regex_label in expression:
            return False
    return True

def basic_regex_language_model_infer(expression):
    return ''

# '( (a.*b|c.*d)(e|f) | g.*h )'
def run_regex(expression):
    # a.*b
    if not contain_options:
        return basic_regex_language_model_infer(expression)

    # (a.*b|c)
    first_options = []
    for i, choice in enumerate(first_options):
        if contain_nonterminal_symbol(choice):
            choice = run_regex(choice)
            first_options[i] = choice
    
    first_options_expression = ''
    best_choice = basic_regex_language_model_infer(first_options_expression)

    # (a|b)(c|d)
    remain_expression = ''
    expression_with_best_choice = best_choice + remain_expression
    remain_result = run_regex(expression_with_best_choice)

    return remain_result