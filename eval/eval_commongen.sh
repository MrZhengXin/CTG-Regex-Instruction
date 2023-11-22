DIR=$(pwd)
DATA=${DIR}/data
RES=${DIR}/res
OUTPUT=${DIR}/eval/commongen.txt

cd eval/commongen
for TASK in 'commongen_regex' # 'commongen_instruction' 'commongen_instruction_length'
do
    for MODEL_NAME in 'GPT3_8_shot' 'flan-t5-xl'
    do
        REF=${DATA}/${TASK}/test.ref
        PRED=${RES}/${TASK}/test_${MODEL_NAME}.txt
        sh eval.sh ${PRED}
    done
done
