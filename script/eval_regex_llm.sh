DIR=$(pwd)
DATA=$(pwd)/data
RES=$(pwd)/res



for MODEL in 'GPT3' # 'gpt-3.5-turbo' 
do
    for TASK in 'anlg_regex_lexicon' 'anlg_regex_length_lexicon' 'anlg_regex_length' 'anlg_regex' 'commongen_regex' 'commongen_regex_length' 'gigaword_length' 'newstest2017-iate' 'newstest2017-wiktionary' 'story_infill_completion'
    do
        mkdir -p ${RES}/${TASK}
        for token in ${OPENAI_API_KEY}
        do
            SRC=${DATA}/${TASK}/test.json
            TGT=${RES}/${TASK}/test_${MODEL}_8_shot_new.txt
            TRAIN=${DATA}/${TASK}/test.json
            if [ -f ${DATA}/${TASK}/dev.json ]; then
                TRAIN=${DATA}/${TASK}/dev.json
            fi
            if [ -f ${DATA}/${TASK}/train.json ]; then
                TRAIN=${DATA}/${TASK}/train.json
            fi
            echo $TRAIN
            python3 src/run_lm.py --model ${MODEL} --src ${SRC} --tgt ${TGT} --train ${TRAIN} --num_shot 8 --token ${token} --max_instance 101
        done
    done
done