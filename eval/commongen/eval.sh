# source ~/.bashrc
INPUT_FILE=../../data/commongen/commongen/commongen.dev.src_alpha.txt
TRUTH_FILE=../../data/commongen/commongen/commongen.dev.tgt.txt
INPUT_NO_REP_FILE=../../data/commongen/commongen/commongen.dev.src_alpha.no_rep.txt
PRED_FILE=$1
OUTPUT_FILE=$(pwd)"/score.txt"


# echo "Start running ROUGE"

# cd ~/CommonGen-plus/methods/unilm_based
# ~/anaconda3/envs/unilm_env/bin/python unilm/src/gigaword/eval.py --pred ${PRED_FILE}   --gold ${TRUTH_FILE} --perl


# echo "BLEU/METER/CIDER/SPICE"
cd Traditional/eval_metrics/
# java -version
# javac -version
python3 eval.py --key_file ${INPUT_FILE} --gts_file ${TRUTH_FILE} --res_file ${PRED_FILE} --output_file ${OUTPUT_FILE}

cd ../../PivotScore
python3 evaluate.py --pred ${PRED_FILE} --ref ${TRUTH_FILE} --cs ${INPUT_NO_REP_FILE} >> ${OUTPUT_FILE}
