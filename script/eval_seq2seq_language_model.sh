DIR=$(pwd)
DATA=$(pwd)/data
RES=$(pwd)/res
MODEL=$(pwd)/model/all_regex
NUM_GPU=$(nvidia-smi --list-gpus | wc -l)


i=0
for MODEL_NAME in 'flan-t5-xl' 
do
    for TASK in 'anlg_regex_lexicon' 'anlg_regex_length_lexicon' 'anlg_regex_length' 'anlg_regex'  'commongen_regex' 'commongen_regex_length' 'gigaword_length' 'newstest2017-iate' 'newstest2017-wiktionary'
    do
        mkdir -p ${RES}/calculate_retry/${TASK}
        SRC=${DATA}/${TASK}/test.json
        TGT=${RES}/calculate_retry/${TASK}/test_${MODEL_NAME}.txt
        MODEL_PATH=${MODEL}/${MODEL_NAME}
        CUDA_VISIBLE_DEVICES=${i} python3 src/eval_seq2seq_language_model.py --model ${MODEL} --src ${SRC} --tgt ${TGT} &
        i=$[i + 1]
        i=$[i % ${NUM_GPU}]
    done
done

# exit

for MODEL_NAME in 'flan-t5-xl'
do
    for TASK in 'story_infill_completion' 
    do
        mkdir -p ${RES}/calculate_retry/${TASK}
        SRC=${DATA}/${TASK}/test.json
        TGT=${RES}/calculate_retry/${TASK}/test_${MODEL_NAME}.txt
        MODEL_PATH=${MODEL}/${MODEL_NAME}
        CUDA_VISIBLE_DEVICES=3 python3 src/eval_seq2seq_language_model.py --model ${MODEL} --src ${SRC} --tgt ${TGT} --nested_regex &
    done
done

