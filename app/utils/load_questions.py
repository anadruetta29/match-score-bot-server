import json
from pathlib import Path

DATASET_PATH = Path("data/dataset.json")

def load_questions():
    with open(DATASET_PATH, "r", encoding="utf-8") as f:
        return json.load(f)
