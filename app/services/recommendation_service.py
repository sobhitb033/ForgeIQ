from sqlalchemy.orm import Session

from app.models.recommendation import Recommendation
from app.models.project import Project


class RecommendationService:

    @staticmethod
    def save_recommendations(
        db: Session,
        project: Project,
        recommendations: list,
    ):

        saved_recommendations = []

        for recommendation_data in recommendations:

            recommendation = Recommendation(
                priority=recommendation_data.get(
                    "priority",
                    "Medium",
                ),
                title=recommendation_data.get(
                    "title",
                    "Untitled Recommendation",
                ),
                message=recommendation_data.get(
                    "message",
                ),
                recommendation=recommendation_data.get(
                    "recommendation",
                ),
                project_id=project.id,
            )

            db.add(recommendation)

            saved_recommendations.append(
                recommendation
            )

        db.commit()

        return saved_recommendations