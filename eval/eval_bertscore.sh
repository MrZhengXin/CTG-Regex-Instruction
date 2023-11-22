DIR=$(pwd)
DATA=${DIR}/data
RES=${DIR}/res
MODEL=${DIR}/model
OUTPUT=${DIR}/eval/bertscore.txt

for TASK in 'anlg_regex' 'anlg_regex_length' 'anlg_regex_lexicon' 'anlg_regex_length_lexicon'
do
    for MODEL_NAME in 'GPT3' 'flan-t5-xl' 
    do
        REF=${DATA}/${TASK}/test.ref
        PRED=${RES}/${TASK}/test_${MODEL_NAME}*
        python3 eval/bertscore.py --pred ${PRED} --ref ${REF} >> ${OUTPUT}
    done
done
