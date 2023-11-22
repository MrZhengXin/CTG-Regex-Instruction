import re

input_text = "<expression> <mask_1> <options> <choice_1> A </choice_1> <choice_2> B </choice_2> </options> <mask_2> <options> <choice_1> C </choice_1> <choice_2> D </choice_2> </options> <mask_3> </expression>"

def contain_nonterminal_symbol(input_text):
    return '<mask_' in input_text or '<options>' in input_text

def get_first_options(input_text):
    options_list = re.findall(r'<options> (.*?) </options>', input_text)
    if options_list == []:
        return [], ''
    first_options = options_list[0]
    first_options_str = '<options> %s </options>' % first_options
    first_options = re.findall(r'<choice_[0-9]+> (.*?) </choice_[0-9]+>', first_options)
    return first_options, first_options_str

def get_regex(input_text):
    expression = re.findall('<expression>.*</expression>', input_text)[0][13:-14]
    expression = re.sub(r'\([0-9]+\)', '', expression)
    expression = re.sub(r' ?<mask_[0-9]+> ?', '.*', expression)
    if '</options> <length=' not in expression:
        expression = re.sub(r' </choice_[0-9]+> <choice_[0-9]+> ', '|', expression)
        expression = re.sub(r'<choice_[0-9]+> ', '', expression)
        expression = re.sub(r' </choice_[0-9]+>', '', expression)
    else:
        length = re.findall('</options> <length=[0-9]+>', expression)[0][19:-1]
        expression = re.sub(r' <length=[0-9]+>', '{'+length+'}', expression)
        expression = re.sub(r' </choice_[0-9]+> <choice_[0-9]+> ', ' ?|', expression) # match space between words
        expression = re.sub(r'<choice_[0-9]+> ', '', expression)
        expression = re.sub(r' </choice_[0-9]+>', ' ?', expression)   
    expression = expression.replace('<options> ', '(').replace(' </options>', ')')
    return expression   

def check_regex(expression, output_text):
    word_length = None
    # remove length constraints label
    output_text = re.sub(r'_[0-9]+', '', output_text)
    # remove word constraints label
    output_text = re.sub(r'\(0-9]+\)', '', output_text)    
    if '<length=' in expression: # <expression> <mask_xx> <length=xx> </expression>
        word_length = int(re.findall('<length=[0-9]+>', expression)[0][8:-1])
        expression = re.sub(r'<length=[0-9]+>', '', expression)
    matched = re.match(expression, output_text) is not None
    matched = (matched and len(output_text.split()) == word_length) if word_length is not None else matched
    return matched

def check_regex_structure(expression_1, expression_2):
    mask_expression_1 = re.findall('\.\*', expression_1)
    mask_expression_2 = re.findall('\.\*', expression_2)
    if mask_expression_1 != mask_expression_2:
        return False
    return True