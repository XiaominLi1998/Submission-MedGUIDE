import os
import json
import argparse
import pandas as pd

DATA_PATH = "Submission-MedGUIDE/data/MedGUIDE-8K.jsonl"
RESULT_DIR = "benchmark_results"

def evaluate(model_name: str):
    # Load ground-truth data
    ds_df = pd.read_json(DATA_PATH, lines=True)

    # Load model response file
    save_model_name = model_name.split("/")[-1]
    result_file = os.path.join(RESULT_DIR, f"benchmark_{save_model_name}.jsonl")
    if not os.path.exists(result_file):
        raise FileNotFoundError(f"No results found at {result_file}")

    # Evaluate
    correct = 0
    correct_weighted = 0
    total_weight = 0
    predictions = []
    targets = []

    with open(result_file) as f:
        for i, line in enumerate(f):
            data = json.loads(line)
            pred = data["chosen answer"]
            true = data["correct answer"]
            option_count = ds_df.iloc[i]["option_count"]

            predictions.append(pred)
            targets.append(true)

            weight = 1 - 1 / option_count
            total_weight += weight
            if pred == true:
                correct += 1
                correct_weighted += weight

    acc = correct / len(ds_df)
    weighted_acc = correct_weighted / total_weight

    print(f"Model: {model_name}")
    print(f"Accuracy: {acc:.3f}")
    print(f"Weighted Accuracy: {weighted_acc:.3f}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", type=str, required=True, help="Name of the model whose output to evaluate.")
    args = parser.parse_args()
    evaluate(args.model)