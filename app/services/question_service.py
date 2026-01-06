import json
from pathlib import Path

DATASET_PATH = Path(__file__).resolve().parent.parent / "data" / "dataset.json"


class QuestionService:
    _questions = None

    @classmethod
    def load(cls):
        if cls._questions is None:
            with open(DATASET_PATH, "r", encoding="utf-8") as f:
                cls._questions = json.load(f)["questions"]

        return cls._questions
