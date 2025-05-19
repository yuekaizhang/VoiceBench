

src_dir=/workspace/slam/icefall_omni/egs/speech_llm/SPEECH2SPEECH/result_adapter_librispeech_kl_div_qa_template

datasets=(alpacaeval_full wildvoice commoneval sd-qa)
datasets=(commoneval)
for dataset in ${datasets[@]}; do
    # sd-qa should use usa split
    if [ $dataset == "sd-qa" ]; then
    split_name="usa"
    evaluator="qa"
    else
    split_name="test"
    evaluator="open"
    fi
    echo $dataset $split_name
    python3 api_judge.py --src_file $src_dir/$dataset-$split_name.jsonl || exit 1
    python3 evaluate.py --src_file $src_dir/result-$dataset-$split_name.jsonl --evaluator $evaluator || exit 1
done
exit 0
datasets=(mmsu advbench bbh ifeval openbookqa)
datasets=(openbookqa)
for dataset in ${datasets[@]}; do
    if [ $dataset == "ifeval" ]; then
        evaluator="ifeval"
    elif [ $dataset == "advbench" ]; then
        evaluator="harm"
    elif [ $dataset == "bbh" ]; then
        evaluator="bbh"
    elif [ $dataset == "openbookqa" ]; then
        evaluator="mcq"
    elif [ $dataset == "mmsu" ]; then
        evaluator="mcq"
    fi
    echo $dataset $split_name
    python3 evaluate.py --src_file $src_dir/$dataset-test.jsonl --evaluator $evaluator || exit 1
done