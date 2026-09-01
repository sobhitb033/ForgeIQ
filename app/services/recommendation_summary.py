from collections import Counter


class RecommendationSummary:

    @staticmethod
    def generate(recommendations):

        priority_counts = Counter()

        for recommendation in recommendations:

            priority = recommendation.get(
                "priority",
                "Low"
            )

            priority_counts[priority] += 1

        priority_summary = {
            "Critical": priority_counts.get(
                "Critical",
                0
            ),
            "High": priority_counts.get(
                "High",
                0
            ),
            "Medium": priority_counts.get(
                "Medium",
                0
            ),
            "Low": priority_counts.get(
                "Low",
                0
            )
        }

        top_recommendations = (
            recommendations[:10]
        )

        return {
            "total_recommendations": len(
                recommendations
            ),
            "priority_summary": priority_summary,
            "top_recommendations": top_recommendations
        }