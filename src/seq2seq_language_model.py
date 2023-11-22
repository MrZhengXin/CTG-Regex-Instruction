from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
import torch
import re
from src.utils import get_regex, check_regex, get_first_options, contain_nonterminal_symbol
import re

class Seq2SeqLanguageModel():
    def __init__(self, model_path='model/all_regex/flan-t5-xl'):
        self.model = AutoModelForSeq2SeqLM.from_pretrained(model_path).cuda()
        self.tokenizer = AutoTokenizer.from_pretrained(model_path)

    def forward(self, input_ids, do_sample=True, num_return_sequences=16, num_beams=4, top_p=0.95, max_length=512):
        with torch.no_grad():
            gen_tokens = self.model.generate(
                input_ids,
                do_sample=do_sample,
                num_beams=1 if do_sample else num_beams,
                num_return_sequences=num_return_sequences if do_sample else num_beams,
                top_p=top_p if do_sample else None,
                max_length=max_length,
                # no_repeat_ngram_size =3
            )
            torch.cuda.empty_cache()
        gen_text_list = self.tokenizer.batch_decode(gen_tokens, skip_special_tokens=True)
        gen_text_list = [gen_text.replace('expression> ', '').replace(' /expression>', '') for gen_text in gen_text_list]
        gen_text_list = [re.sub(r'\([0-9]+\)', '', gen_text)for gen_text in gen_text_list]
        gen_text_list = [re.sub(r'_[0-9]+', '', gen_text)for gen_text in gen_text_list]
        return gen_text_list
    
    def regex_filter(self, expression, gen_text_list):
        gen_text_list = list(filter(lambda x: check_regex(expression, x), gen_text_list))
        if gen_text_list != []:
            return gen_text_list[0]
        return None

    def reject_sampling(self, input_text, max_retry=32):
        input_ids = self.tokenizer(input_text, return_tensors="pt").input_ids.cuda()
        expression = get_regex(input_text)
        print(expression)

        # try beam search first
        beam_search_gen_text_list = self.forward(input_ids, do_sample=False, num_return_sequences=4, num_beams=4)
        valid_result = self.regex_filter(expression, beam_search_gen_text_list)
        if valid_result is not None:
            return valid_result, 0
        
        for i in range(max_retry):
            gen_text_list = self.forward(input_ids, do_sample=True, num_return_sequences=16)
            # print(gen_text_list)
            valid_result = self.regex_filter(expression, gen_text_list)
            if valid_result is not None:
                return valid_result, i+1

        return beam_search_gen_text_list[0], -1   

    def nested_regex(self, input_text):
        print(input_text)
        expression = re.findall(r'<expression>(.*?)</expression>', input_text)[0].strip()
        if not contain_nonterminal_symbol(input_text):
            return expression, 0
        if '<options>' not in input_text: # not recursive
            return self.reject_sampling(input_text) # [0]
        
        first_options, first_options_str = get_first_options(input_text)
        
        remain_expression = expression[expression.find(first_options_str)+len(first_options_str):]
        # remain_expression = re.findall('%s(.*?) </expression>' % first_options_str, input_text)[0]
        focus_input_text = input_text.replace(remain_expression, '')
        # remain_expression = '<expression> %s </expression>' % remain_expression
        total_retry = 0
        for i, choice in enumerate(first_options):
            # if contain_nonterminal_symbol(choice): # .*a(.*b|.*c)(e|f)
            if contain_nonterminal_symbol(choice):
                focus_input_text_with_this_choice = focus_input_text.replace(first_options_str, choice)
                new_choice, retry = self.nested_regex(focus_input_text_with_this_choice)
            else:
                focus_input_text_with_this_choice = focus_input_text.replace(first_options_str+' </expression>', '</expression> '+choice)
                new_choice, retry = self.nested_regex(focus_input_text_with_this_choice)
                new_choice += ' ' + choice
            total_retry += retry

            print(new_choice)
            first_options[i] = new_choice

        new_first_options_str = '<expression> <options> %s </options> </expression>' % \
            (' '.join(['<choice_%d> %s </choice_%d>' % \
                (i, option, i) for i, option in enumerate(first_options)]))
        new_options_expression_input_text = re.sub(r'<expression>.*</expression>', new_first_options_str, focus_input_text)
        new_choice, retry = self.reject_sampling(new_options_expression_input_text)

        remain_expression = ' <expression>%s </expression>' % remain_expression
        remain_input_text = re.sub(r'<expression>.*</expression>', new_choice+remain_expression, focus_input_text)
        remain_output, retry = self.nested_regex(remain_input_text)
        total_retry += retry
        
        final_output = new_choice + ' ' + remain_output
        final_output = final_output.strip()
        return final_output, total_retry
        


        


if __name__ == "__main__":
    model = Seq2SeqLanguageModel('model/all_regex/flan-t5-xl')
    input_text = "Manny wanted to get better at making Italian food. He learned how to make noodles from scratch. He learned how to make different sauces. <expression> <mask_0> <options> <choice_0> His family loved it. </choice_0> <choice_1> He paid the chef $500 to prepare the meal. </choice_1> </options> </expression>"
    print(model.nested_regex(input_text))
    input_text = "<expression> <mask_0> dance(0) <mask_1> performed(1) <mask_2> stage(2) <mask_3> wearing(3) <mask_4> costumes(4) <mask_5> </expression>"
    print(model.reject_sampling(input_text))
    input_text = "<expression> <mask_0> dance(0) <mask_1> performed(1) <mask_2> stage(2) <mask_3> wearing(3) <mask_4> costumes(4) <mask_5> <length=15> </expression>"
    print(model.reject_sampling(input_text))
    # input_text = "<expression> <mask_0> fix(0) <mask_1> eat(1) <mask_2> fresh(2) <mask_3> good(3) <mask_4> spot(4) <mask_5> watch(5) <mask_6> rice(6) <mask_7> <length=30> </expression>"
    # print(model.reject_sampling(input_text))