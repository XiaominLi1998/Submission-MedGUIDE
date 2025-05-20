import json
from tqdm import tqdm
import pandas as pd
import os
import sys
root_dir = "Submission-MedGUIDE"
sys.path.append(root_dir)
from templates import *


def get_all_paths():
    with open(f"{root_dir}/data/all_paths.json", "r") as f:
        all_paths = json.load(f)
    return all_paths

def generate_profiles_from_paths(query_func, save_file_path):
    """
    Given a dictionary of paths, generate profiles for each path.
    """
    all_paths = get_all_paths()

    profile_dict = {}

    for name, paths in  tqdm(all_paths.items(), total=len(all_paths)):
        # print(f"Name: {name}. PathCount: {len(paths)}")
        sys.stdout.flush()
        profile_ls = []
        # for path in tqdm(paths, desc=f"{name}", total=len(paths)):
        for path in paths:
            input = template_path_to_question(path); sys.stdout.flush()
            profile = query_func(input)
            profile_ls.append(profile)
        profile_dict[name] = profile_ls

    records = []
    for tree, paths in all_paths.items():
        profiles = profile_dict[tree]
        for path, profile in zip(paths, profiles):
            records.append({"tree": tree, "path": path, "profile": profile})

    df = pd.DataFrame(records)
    os.makedirs(os.path.dirname(save_file_path), exist_ok=True)
    df.to_json(save_file_path, orient="records", lines=True)
    print(f"Saved to {save_file_path}")

