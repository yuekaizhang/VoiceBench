from argparse import ArgumentParser
import json
from src.evaluator import evaluator_mapping
from loguru import logger
import os


def main():
    parser = ArgumentParser()
    parser.add_argument('--src_file', type=str, required=True)
    parser.add_argument('--evaluator', type=str, required=True, choices=list(evaluator_mapping.keys()))
    args = parser.parse_args()
    data = []
    with open(args.src_file, 'r') as f:
        for line in f:
            json_obj = json.loads(line.strip())  # Convert JSON string to dictionary
            data.append(json_obj)
    evaluator = evaluator_mapping[args.evaluator]()
    evaluation_result = evaluator.evaluate(data)
    logger.info(evaluation_result)

    # Save results to file
    src_dir = os.path.dirname(args.src_file)
    src_basename = os.path.basename(args.src_file)
    tgt_file_name = f"score-{src_basename}"
    tgt_file_path = os.path.join(src_dir, tgt_file_name) if src_dir else tgt_file_name

    # Ensure the result is a dictionary for json.dump, or handle other types
    # Assuming evaluation_result is a dict or list that can be serialized to JSON
    if not isinstance(evaluation_result, (dict, list)):
        # If it's a simple type, wrap it in a dictionary
        # Or convert/handle as appropriate for your specific evaluator output
        evaluation_result_to_save = {"result": evaluation_result}
    else:
        evaluation_result_to_save = evaluation_result

    with open(tgt_file_path, 'w') as f_out:
        json.dump(evaluation_result_to_save, f_out, indent=4)
    logger.info(f"Evaluation results saved to {tgt_file_path}")


if __name__ == "__main__":
    main()
