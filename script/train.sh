
DIR=$(pwd)
DATA=$(pwd)/data
MODEL=$(pwd)/model
RES=$(pwd)/res
NUM_GPU=$(nvidia-smi --list-gpus | wc -l)

for model_name in 'google/flan-t5-xl' 
do
    for TASK in 'all_regex' 
    do
        OUTPUT_DIR=${MODEL}/${TASK}/$(basename ${model_name})
        echo ${OUTPUT_DIR}
        python3 -m torch.distributed.launch --nproc_per_node=${NUM_GPU} --master_port=12345  src/run_summarization.py \
            --model_name_or_path ${MODEL}/$(basename ${model_name}) \
            --do_train \
            --do_predict \
            --do_eval \
            --train_file ${DATA}/${TASK}/train.json \
            --validation_file ${DATA}/${TASK}/dev.json \
            --test_file ${DATA}/${TASK}/test.json \
            --output_dir ${OUTPUT_DIR} \
            --overwrite_output_dir \
            --overwrite_cache \
            --num_train_epochs 3 \
            --per_device_train_batch_size 4 \
            --per_device_eval_batch_size 4 \
            --gradient_accumulation_steps 2 \
            --evaluation_strategy epoch \
            --predict_with_generate \
            --generation_num_beams 4 \
            --learning_rate 3e-5 \
            --save_strategy no \
            --warmup_steps 50 \
            --logging_steps 50 \
            --sharded_ddp simple 
        # rm -rf ${OUTPUT_DIR}/checkpoint*

        # cd ${DIR}
        # python3 tools/evaluate.py --pred_file ${OUTPUT_DIR}/generated_predictions.txt --ref_file ${DATA}/${TASK}/test.ref >> res/score.txt

    done
done
