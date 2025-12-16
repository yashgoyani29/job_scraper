import json
import pandas as pd
import os

def save_to_json(jobs, file_path="output/jobs.json"):
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(jobs, f, indent=4, ensure_ascii=False)
    print(f"📘 Saved {len(jobs)} jobs to {file_path}")

def save_to_excel(jobs, filename='output/jobs.xlsx'):
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    df = pd.DataFrame(jobs)
    df.to_excel(filename, index=False)
    print(f"📘 Saved {len(jobs)} jobs to {filename}")
