from typing import List, Dict

class ScoreService:
    MIN_SCORE = 1
    MAX_SCORE = 10

    def calculate(self, answers: List[Dict]) -> int:
        raw_score = sum(answer["score"] for answer in answers)

        return self._normalize(raw_score)

    def _normalize(self, raw_score: int) -> int:
        """
        Converts raw score into a 1–10 scale
        """

        # Example normalization logic
        if raw_score <= 2:
            return 3
        elif raw_score <= 4:
            return 5
        elif raw_score <= 6:
            return 7
        elif raw_score <= 8:
            return 9
        else:
            return self.MAX_SCORE
