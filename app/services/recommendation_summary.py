from collections import Counter


class RecommendationSummary:

    @staticmethod
    def generate(recommendations):

        priority_counts = Counter()
        category_counts = Counter()

        for recommendation in recommendations:
            priority = recommendation.get(
                "priority",
                "Low"
            )
            category = recommendation.get(
                "category",
                "General"
            )

            priority_counts[priority] += 1
            category_counts[category] += 1

        priority_summary = {
            "Critical": priority_counts.get("Critical", 0),
            "High": priority_counts.get("High", 0),
            "Medium": priority_counts.get("Medium", 0),
            "Low": priority_counts.get("Low", 0),
        }

        category_summary = dict(
            sorted(
                category_counts.items(),
                key=lambda item: (-item[1], item[0])
            )
        )

        return {
            "total_recommendations": len(recommendations),
            "priority_summary": priority_summary,
            "category_summary": category_summary,
            "top_recommendations": recommendations[:10],
        }
