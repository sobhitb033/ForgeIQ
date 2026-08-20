class EngineeringPriority:

    @staticmethod
    def calculate(
        ast_data,
        maintainability,
        code_smells,
        dependency_count=0,
        circular_dependency=False,
        fan_in=0,
        fan_out=0
    ):

        score = 0
        factors = []

        complexities = []

        for function in ast_data["functions"]:
            complexities.append(
                function["cyclomatic_complexity"]
            )

        for cls in ast_data["classes"]:
            for method in cls["methods"]:
                complexities.append(
                    method["cyclomatic_complexity"]
                )

        if complexities:

            average_complexity = (
                sum(complexities) / len(complexities)
            )

            if average_complexity > 20:

                points = 40
                score += points

                factors.append(
                    {
                        "name": "High Complexity",
                        "points": points,
                        "details": (
                            f"Average cyclomatic complexity: "
                            f"{round(average_complexity, 2)}"
                        )
                    }
                )

            elif average_complexity > 10:

                points = 25
                score += points

                factors.append(
                    {
                        "name": "Moderate Complexity",
                        "points": points,
                        "details": (
                            f"Average cyclomatic complexity: "
                            f"{round(average_complexity, 2)}"
                        )
                    }
                )

            elif average_complexity > 5:

                points = 10
                score += points

                factors.append(
                    {
                        "name": "Elevated Complexity",
                        "points": points,
                        "details": (
                            f"Average cyclomatic complexity: "
                            f"{round(average_complexity, 2)}"
                        )
                    }
                )

        index = maintainability["index"]

        if index < 50:

            points = 30
            score += points

            factors.append(
                {
                    "name": "Low Maintainability",
                    "points": points,
                    "details": f"Maintainability index: {index}"
                }
            )

        elif index < 70:

            points = 15
            score += points

            factors.append(
                {
                    "name": "Moderate Maintainability",
                    "points": points,
                    "details": f"Maintainability index: {index}"
                }
            )

        smell_count = len(code_smells)

        if smell_count > 0:

            points = min(
                smell_count * 5,
                30
            )

            score += points

            factors.append(
                {
                    "name": "Code Smells",
                    "points": points,
                    "details": (
                        f"{smell_count} code smell(s) detected"
                    )
                }
            )

        if dependency_count >= 10:

            points = 20
            score += points

            factors.append(
                {
                    "name": "High Dependency Count",
                    "points": points,
                    "details": (
                        f"{dependency_count} internal dependencies"
                    )
                }
            )

        elif dependency_count >= 5:

            points = 10
            score += points

            factors.append(
                {
                    "name": "Moderate Dependency Count",
                    "points": points,
                    "details": (
                        f"{dependency_count} internal dependencies"
                    )
                }
            )

        if circular_dependency:

            points = 25
            score += points

            factors.append(
                {
                    "name": "Circular Dependency",
                    "points": points,
                    "details": (
                        "Module is part of a circular dependency"
                    )
                }
            )

        if fan_in >= 10:

            points = 20
            score += points

            factors.append(
                {
                    "name": "High Module Impact",
                    "points": points,
                    "details": f"Fan-in: {fan_in}"
                }
            )

        elif fan_in >= 5:

            points = 10
            score += points

            factors.append(
                {
                    "name": "Moderate Module Impact",
                    "points": points,
                    "details": f"Fan-in: {fan_in}"
                }
            )

        elif fan_in >= 2:

            points = 5
            score += points

            factors.append(
                {
                    "name": "Shared Module",
                    "points": points,
                    "details": f"Fan-in: {fan_in}"
                }
            )

        raw_score = score
        score = min(score, 100)

        if score >= 70:
            priority = "Critical"

        elif score >= 40:
            priority = "High"

        elif score >= 20:
            priority = "Medium"

        else:
            priority = "Low"

        return {
            "score": score,
            "priority": priority,
            "factors": factors
        }