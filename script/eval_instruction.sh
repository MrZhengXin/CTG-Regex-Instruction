DIR=$(pwd)
DATA=$(pwd)/data
RES=$(pwd)/res

for MODEL in 'GPT3'
do
    for TASK in 'anlg_instruction' 'anlg_instruction_length'  'anlg_instruction_length_lexicon' 'anlg_instruction_lexicon' 'commongen_instruction' 'commongen_instruction_length' 'gigaword_instruction_length' 'newstest2017-iate_instruction' 'newstest2017-wiktionary_instruction' 'story_infill_completion_instruction'
    do
        mkdir -p ${RES}/${TASK}

        for token in ${OPENAI_API_KEY}
        do
            SRC=${DATA}/${TASK}/test.json
            TGT=${RES}/${TASK}/test_${MODEL}_8_shot.txt
            TRAIN=${DATA}/${TASK}/test.json
            if [ -f ${DATA}/${TASK}/dev.json ]; then
                TRAIN=${DATA}/${TASK}/dev.json
            fi
            if [ -f ${DATA}/${TASK}/train.json ]; then
                TRAIN=${DATA}/${TASK}/train.json
            fi
            echo $TRAIN
            python3 src/run_lm_instruction_few_shot.py --model ${MODEL} --src ${SRC} --tgt ${TGT} --train ${TRAIN} --num_shot 8 --token ${token} # --max_instance 101
        done
    done
done
