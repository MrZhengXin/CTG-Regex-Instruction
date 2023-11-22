DIR=$(pwd)
DATA=${DIR}/data
RES=${DIR}/res
MODEL=${DIR}/model
OUTPUT=${DIR}/eval/bleu_rouge.txt

for TASK in 'gigaword_length' 'newstest2017-wiktionary' 'newstest2017-iate' 'story_infill_completion' 'yelp_review'
do
    for MODEL_NAME in 'GPT3' 'flan-t5-xl'
    do
        REF=${DATA}/${TASK}/test.ref
        PRED=${RES}/${TASK}/test_${MODEL_NAME}*
        python3 eval/bleu_rouge.py --ref ${REF} --pred ${PRED} >> ${OUTPUT}
    done
done
