import json
import pandas as pd
import os

def save_to_json(jobs, file_path="output/jobs.json"):
    """Save jobs data to JSON file"""
    if not jobs:
        print("⚠️ No jobs to save")
        return
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(jobs, f, indent=4, ensure_ascii=False)
    print(f"📘 Saved {len(jobs)} jobs to {file_path}")

def save_to_excel(jobs, file_path="output/jobs.xlsx"):
    """Save jobs data to Excel file"""
    if not jobs:
        print("⚠️ No jobs to save")
        return
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    df = pd.DataFrame(jobs)
    df.to_excel(file_path, index=False, engine="openpyxl")
    print(f"📗 Saved {len(jobs)} jobs to {file_path}")
