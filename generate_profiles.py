import os
import sys
import argparse

# Setup
root_dir = "Submission-MedGUIDE"
sys.path.append(root_dir)
from utils import *
from query_api import *  # querying functions for different LLMs

# Map from model name to query function
model_func_map = {
    'gpt-4o-mini': query_func_gpt_4o_mini,
    # Add more models here as needed
    # 'gpt-4o': query_func_gpt_4o,
    # 'claude-3-5-haiku': query_func_claude_3_5_haiku,
    # ...
}

def main(model_name):
    if model_name not in model_func_map:
        raise ValueError(f"Unsupported model: {model_name}")
    query_func = model_func_map[model_name]

    for batch_idx in range(4):
        print(f"\n\n******** Model: {model_name} | Processing batch {batch_idx} ********")
        save_file_path = f"{root_dir}/data/generated_profiles/{model_name}/profile_questions_batch{batch_idx}.jsonl"

        if os.path.exists(save_file_path):
            print(f"File {save_file_path} already exists. Skipping.")
            continue

        generate_profiles_from_paths(query_func, save_file_path)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--model_name", type=str, required=True,
                        help="Name of the model to use for querying.")
    args = parser.parse_args()
    main(args.model_name)