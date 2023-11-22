DIR=$(pwd)
DATA=${DIR}/data
RES=${DIR}/res
MODEL=${DIR}/model
OUTPUT=${DIR}/eval/accuracy.txt

for TASK in 'winogrand_regex' # 'ag_news_regex' 'anli_regex' 'story_completion' 'winogrand_regex' # 'winograd_wsc_regex' # 
do
    for MODEL_NAME in 'GPT3' 'flan-t5-xl'
    do
        SRC=${DATA}/${TASK}/test.json
        PRED=${RES}/${TASK}/test_${MODEL_NAME}*
        python3 eval/accuracy.py --src ${SRC} --pred ${PRED} # >> ${OUTPUT}
    done
done
