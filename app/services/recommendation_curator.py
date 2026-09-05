from collections import defaultdict


class RecommendationCurator:
    """Turn raw analyzer findings into concise engineering actions."""

    PRIORITY_RANK = {
        "Critical": 1,
        "High": 2,
        "Medium": 3,
        "Low": 4,
    }

    CATEGORY_RANK = {
        "Architecture": 1,
        "Impact Analysis": 2,
        "Dependency": 3,
        "Engineering Priority": 4,
        "Project Health": 5,
        "Code Quality": 6,
    }

    @classmethod
    def curate(cls, recommendations, max_recommendations=20):
        if not recommendations:
            return []

        normalized = [cls._normalize(item) for item in recommendations]
        deduplicated = cls._deduplicate(normalized)
        grouped = cls._group_related(deduplicated)
        ranked = sorted(grouped, key=cls._sort_key)
        return ranked[:max_recommendations]

    @classmethod
    def _normalize(cls, item):
        result = dict(item)
        result.setdefault("category", "General")
        result.setdefault("priority", "Low")
        result.setdefault("title", "Engineering Recommendation")
        result.setdefault("message", "An engineering issue was detected.")
        result.setdefault("recommendation", "Review and refactor the affected area.")
        return result

    @classmethod
    def _deduplicate(cls, recommendations):
        seen = set()
        result = []

        for item in recommendations:
            key = (
                item.get("category"),
                item.get("priority"),
                item.get("title"),
                item.get("file") or item.get("module"),
                item.get("location"),
                item.get("message"),
            )
            if key in seen:
                continue
            seen.add(key)
            result.append(item)

        return result

    @classmethod
    def _group_related(cls, recommendations):
        grouped = []
        missing_docstrings = defaultdict(list)
        long_functions = []
        long_parameter_lists = []
        orphan_modules = []
        high_priority_files = []

        for item in recommendations:
            title = item.get("title")
            if title == "Missing Docstring":
                missing_docstrings[item.get("file", "Unknown")].append(item)
            elif title == "Long Function":
                long_functions.append(item)
            elif title == "Long Parameter List":
                long_parameter_lists.append(item)
            elif title == "Orphan Module":
                orphan_modules.append(item)
            elif title == "High Priority File Requires Attention":
                high_priority_files.append(item)
            else:
                grouped.append(item)

        cls._append_grouped_docstrings(grouped, missing_docstrings)
        cls._append_grouped_long_functions(grouped, long_functions)
        cls._append_grouped_parameter_lists(grouped, long_parameter_lists)
        cls._append_grouped_orphans(grouped, orphan_modules)
        cls._append_grouped_priority_files(grouped, high_priority_files)
        return grouped

    @staticmethod
    def _append_grouped_docstrings(grouped, groups):
        if not groups:
            return

        all_items = [item for items in groups.values() for item in items]
        file_counts = {
            file_path: len(items)
            for file_path, items in groups.items()
        }
        total_count = len(all_items)

        grouped.append({
            "category": "Code Quality",
            "priority": "Low",
            "title": "Document Undocumented Code",
            "message": (
                f"{total_count} undocumented definition(s) were found across "
                f"{len(groups)} source file(s)."
            ),
            "recommendation": (
                "Add concise docstrings to the affected functions and classes, "
                "prioritizing public or reusable APIs."
            ),
            "evidence": {
                "finding_count": total_count,
                "file_count": len(groups),
                "files": file_counts,
                "findings": all_items,
            },
        })

    @staticmethod
    def _append_grouped_long_functions(grouped, items):
        if not items:
            return
        grouped.append({
            "category": "Code Quality",
            "priority": (
                "Critical" if any(item.get("priority") == "Critical" for item in items)
                else "High" if any(item.get("priority") == "High" for item in items)
                else "Medium"
            ),
            "title": "Long Functions",
            "message": (
                f"{len(items)} function(s) exceed the configured length threshold "
                "and may be harder to maintain."
            ),
            "recommendation": (
                "Break long functions into smaller, cohesive units with clear "
                "responsibilities."
            ),
            "evidence": {
                "finding_count": len(items),
                "findings": items,
            },
        })

    @staticmethod
    def _append_grouped_parameter_lists(grouped, items):
        if not items:
            return
        grouped.append({
            "category": "Code Quality",
            "priority": "Medium",
            "title": "Long Parameter Lists",
            "message": (
                f"{len(items)} function(s) have parameter lists above the "
                "configured threshold."
            ),
            "recommendation": (
                "Reduce parameter count by introducing cohesive data objects "
                "or splitting responsibilities."
            ),
            "evidence": {"finding_count": len(items), "findings": items},
        })

    @staticmethod
    def _append_grouped_orphans(grouped, items):
        if not items:
            return
        grouped.append({
            "category": "Architecture",
            "priority": "Low",
            "title": "Orphan Modules",
            "message": (
                f"{len(items)} module(s) have no internal dependencies or dependents."
            ),
            "recommendation": (
                "Review whether these modules are unused, package initializers, "
                "entry points, or intentionally isolated. Remove unnecessary "
                "modules or integrate them properly into the architecture."
            ),
            "evidence": {
                "finding_count": len(items),
                "modules": [item.get("module") for item in items],
            },
        })

    @staticmethod
    def _append_grouped_priority_files(grouped, items):
        if not items:
            return
        priorities = {item.get("priority", "High") for item in items}
        priority = "Critical" if "Critical" in priorities else "High"
        grouped.append({
            "category": "Engineering Priority",
            "priority": priority,
            "title": "High Priority Files Require Attention",
            "message": f"{len(items)} file(s) have high engineering priority.",
            "recommendation": (
                "Review the affected files first and address the complexity, "
                "coupling, dependency, impact, and code-quality factors contributing "
                "to their priority."
            ),
            "evidence": {"finding_count": len(items), "findings": items},
        })

    @classmethod
    def _sort_key(cls, item):
        priority = cls.PRIORITY_RANK.get(item.get("priority"), 4)
        category = cls.CATEGORY_RANK.get(item.get("category"), 99)
        score = item.get("score")
        score_key = -score if isinstance(score, (int, float)) else 0
        return priority, category, score_key, item.get("title", "")
