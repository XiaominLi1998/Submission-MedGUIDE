import os
import sys
import json
import argparse
import pandas as pd

# Setup
root_dir = "Submission-MedGUIDE"
sys.path.append(root_dir)
from query_api import *  # Import all query functions

# Constants
MAX_NEW_TOKENS = 5
TEMPERATURE = 0.0
DATA_PATH = f"{root_dir}/data/MedGUIDE-8K.jsonl"

# Map model names to corresponding query functions
model_func_map = {
    'gpt-4o-mini': query_gpt,
    'gpt-4.1': query_gpt,
    'o1': query_o_series,
    'o4-mini': query_o_series,
    'claude-3-5-haiku': query_claude,
    'claude-3-7-sonnet': query_claude,
    'deepseek-v3': query_deepseek,
    'gemini-2_5-flash': query_gemini,
    # add more model mappings as needed
}

def get_query_func(model_name: str):
    for key in model_func_map:
        if key in model_name.lower():
            return model_func_map[key]
    raise ValueError(f"Unrecognized model: {model_name}")

def main(model_name: str):
    print(f"\nModel: {model_name}")
    ds_df = pd.read_json(DATA_PATH, lines=True)
    prompts = ds_df['prompt'].tolist()

    query_func = get_query_func(model_name)
    results = query_func(model_name, inputs=prompts, max_new_tokens=MAX_NEW_TOKENS, temperature=TEMPERATURE)

    save_model_name = model_name.split("/")[-1]
    save_path = os.path.join("benchmark_results", f"benchmark_{save_model_name}.jsonl")
    os.makedirs(os.path.dirname(save_path), exist_ok=True)

    with open(save_path, 'w') as f:
        for i, result in enumerate(results):
            f.write(json.dumps({
                "question": ds_df['prompt'][i],
                "correct answer": ds_df['answer'][i],
                "chosen answer": result.strip()
            }) + '\n')
    print(f"Results saved to {save_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", type=str, required=True, help="Name of the model to use for querying.")
    args = parser.parse_args()
    main(args.model)