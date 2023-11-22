DIR=$(pwd)
DATA=${DIR}/data
RES=${DIR}/res
MODEL=${DIR}/model
OUTPUT=${DIR}/eval/regex_match_rate.txt

for TASK in   'newstest2017-wiktionary_instruction' 'newstest2017-iate_instruction'
do
    for MODEL_NAME in 'GPT3_8_shot' 'flan-t5-xl'
    do
        SRC=${DATA}/${TASK}/test.json
        PRED=${RES}/${TASK}/test_${MODEL_NAME}.txt
        python3 eval/regex_match_rate.py --src ${SRC} --pred ${PRED} --no_order
    done
done

exit

for TASK in 'anlg_instruction' 'anlg_instruction_length' 'anlg_instruction_length_lexicon' 'anlg_instruction_lexicon' 'commongen_instruction' 'commongen_instruction_length' 'gigaword_instruction_length' 'newstest2017-iate_instruction' 'newstest2017-wiktionary_instruction'
do
    for MODEL_NAME in 'GPT3_8_shot' 'flan-t5-xl'
    do
        SRC=${DATA}/${TASK}/test.json
        PRED=${RES}/${TASK}/test_${MODEL_NAME}_100.txt
        python3 eval/regex_match_rate.py --src ${SRC} --pred ${PRED} >> ${OUTPUT}
    done
done

exit
for TASK in 'story_infill_completion_instruction'
do
    for MODEL_NAME in 'GPT3_8_shot' # 'flan-t5-xl'
    do
        SRC=${DATA}/${TASK}/test.json
        PRED=${RES}/${TASK}/test_${MODEL_NAME}.txt.second
        python3 eval/story_infill_completion_accuracy.py --src ${SRC} --pred ${PRED} >> ${OUTPUT}
    done
done
exit




for TASK in 'anlg_regex_length_lexicon' # 'anlg_regex' 'anlg_regex_length' 'anlg_regex_lexicon' 'anlg_regex_length_lexicon'
do
    for MODEL_NAME in 'GPT3' # 'flan-t5-xl'
    do
        SRC=${DATA}/${TASK}/test.json
        PRED=${RES}/${TASK}/test_${MODEL_NAME}*
        python3 eval/regex_match_rate.py --src ${SRC} --pred ${PRED} >> ${OUTPUT}
    done
done
exit

for TASK in 'anlg_regex_length' 'commongen_regex' 'commongen_regex_length' 'gigaword_length' 'newstest2017-wiktionary' 'newstest2017-iate' 'yelp_review'
do
    for MODEL_NAME in 'GPT3' 'BLOOM-175B' 'flan-t5-xl' # 't5-xl-lm-adapt'
    do
        SRC=${DATA}/${TASK}/test.json
        PRED=${RES}/${TASK}/test_${MODEL_NAME}*
        python3 eval/regex_match_rate.py --src ${SRC} --pred ${PRED} >> ${OUTPUT}
    done
done

exit

for TASK in 'story_infill_completion'
do
    for MODEL_NAME in 'GPT3_8_shot' 'flan-t5-xl'
    do
        SRC=${DATA}/${TASK}/test.json
        PRED=${RES}/${TASK}/test_${MODEL_NAME}.txt.second
        python3 eval/story_infill_completion_accuracy.py --src ${SRC} --pred ${PRED} >> ${OUTPUT}
    done
done

for TASK in 'winograd_wsc_regex' # 
do
    for MODEL_NAME in 'GPT3' # 'BLOOM-175B' 
    do
        SRC=${DATA}/${TASK}/test.json
        PRED=${RES}/${TASK}/test_${MODEL_NAME}_8_shot.txt
        python3 eval/regex_match_rate.py --src ${SRC} --pred ${PRED} >> ${OUTPUT}
    done
    for MODEL_NAME in 'flan-t5-xl' 't5-xl-lm-adapt'
    do
        SRC=${DATA}/${TASK}/dev_without_tag.json
        PRED=${MODEL}/${TASK}/${MODEL_NAME}/generated_predictions.txt
        python3 eval/regex_match_rate.py --src ${SRC} --pred ${PRED} >> ${OUTPUT}
    done
done

exit

for TASK in 'commongen_regex' # 
do
    for MODEL_NAME in 'GPT3' 'BLOOM-175B' 
    do
        SRC=${DATA}/${TASK}/dev_with_tag.json
        PRED=${RES}/${TASK}/test_${MODEL_NAME}_8_shot.txt
        python3 eval/regex_match_rate.py --src ${SRC} --pred ${PRED} >> ${OUTPUT}
    done
    for MODEL_NAME in 'flan-t5-xl' 't5-xl-lm-adapt'
    do
        SRC=${DATA}/${TASK}/dev_without_tag.json
        PRED=${MODEL}/${TASK}/${MODEL_NAME}/generated_predictions.txt
        python3 eval/regex_match_rate.py --src ${SRC} --pred ${PRED} >> ${OUTPUT}
    done
done

for TASK in 'anlg_regex' # 
do
    for MODEL_NAME in 'GPT3' 'BLOOM' 
    do
        SRC=${DATA}/${TASK}/test.json
        PRED=${RES}/${TASK}/test_${MODEL_NAME}_8_shot.txt
        python3 eval/regex_match_rate.py --src ${SRC} --pred ${PRED} >> ${OUTPUT}
    done
    for MODEL_NAME in 'flan-t5-xl' 't5-xl-lm-adapt'
    do
        SRC=${DATA}/${TASK}/test.json
        PRED=${MODEL}/${TASK}/${MODEL_NAME}/generated_predictions.txt
        python3 eval/regex_match_rate.py --src ${SRC} --pred ${PRED} >> ${OUTPUT}
    done
done