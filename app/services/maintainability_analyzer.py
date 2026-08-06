class MaintainabilityAnalyzer:

    @staticmethod
    def analyze(metrics: dict):

        score = 100

        # Penalize large files
        score -= metrics["code_lines"] // 5

        # Penalize too many functions
        score -= metrics["functions"] * 2

        # Penalize too many methods
        score -= metrics["methods"]

        # Reward comments slightly
        score += metrics["comment_lines"] // 2

        score = max(0, min(100, score))

        if score >= 85:
            rating = "Excellent"
        elif score >= 70:
            rating = "Good"
        elif score >= 50:
            rating = "Fair"
        else:
            rating = "Poor"

        return {
            "index": score,
            "rating": rating,
        }