"""CORTEX Grade Calculator with 5-category weighting and Security Guardrail Caps."""

from app.analyzers.grading.models import CategoryScores
from app.analyzers.grading.weights import CategoryWeights


class GradeCalculator:
    """Calculates overall 0-100 score, letter grade (A+ to F), and applies security guardrail caps."""

    GRADE_THRESHOLDS: list[tuple[float, str]] = [
        (93.0, "A+"),
        (87.0, "A"),
        (80.0, "A-"),
        (73.0, "B+"),
        (67.0, "B"),
        (60.0, "B-"),
        (53.0, "C+"),
        (47.0, "C"),
        (40.0, "C-"),
        (30.0, "D"),
        (0.0, "F"),
    ]

    GRADE_MAX_NUMERIC: dict[str, float] = {
        "A+": 100.0,
        "A": 92.0,
        "A-": 86.0,
        "B+": 79.0,
        "B": 72.0,
        "B-": 66.0,
        "C+": 59.0,
        "C": 52.0,
        "C-": 46.0,
        "D": 39.0,
        "F": 29.0,
    }

    @classmethod
    def score_to_grade(cls, score: float) -> str:
        """Convert a 0-100 numeric score to a letter grade."""
        s = round(score, 1)
        for threshold, grade in cls.GRADE_THRESHOLDS:
            if s >= threshold:
                return grade
        return "F"

    @classmethod
    def calculate_grade(
        cls,
        categories: CategoryScores,
        weights: CategoryWeights | None = None,
    ) -> tuple[float, str, bool, str | None]:
        """Compute weighted numeric score, letter grade, and apply guardrail cap rules.

        Returns:
            tuple[float, str, bool, str | None]:
                (final_numeric_score, final_letter_grade, is_capped, cap_reason)
        """
        w = weights or CategoryWeights()

        weighted_sum = (
            (categories.security_score * w.security)
            + (categories.architecture_score * w.architecture)
            + (categories.code_quality_score * w.code_quality)
            + (categories.maintainability_score * w.maintainability)
            + (categories.community_velocity_score * w.community_velocity)
        )

        total_weight = (
            w.security
            + w.architecture
            + w.code_quality
            + w.maintainability
            + w.community_velocity
        )

        raw_score = weighted_sum / total_weight if total_weight > 0 else 0.0
        numeric_score = round(max(min(raw_score, 100.0), 0.0), 1)

        sec_grade = cls.score_to_grade(categories.security_score)

        is_capped = False
        cap_reason: str | None = None
        max_allowed_grade: str | None = None

        if sec_grade == "F":
            is_capped = True
            max_allowed_grade = "C"
            cap_reason = "Overall grade capped at C due to critical security findings"
        elif sec_grade == "D":
            is_capped = True
            max_allowed_grade = "B"
            cap_reason = "Overall grade capped at B due to moderate security risks"

        final_numeric = numeric_score
        if max_allowed_grade:
            max_score = cls.GRADE_MAX_NUMERIC.get(max_allowed_grade, 100.0)
            if final_numeric > max_score:
                final_numeric = max_score

        final_grade = cls.score_to_grade(final_numeric)

        # Ensure grade does not exceed max allowed grade threshold if capped
        if max_allowed_grade:
            if sec_grade == "F" and final_numeric > 52.0:
                final_grade = "C"
            elif sec_grade == "D" and final_numeric > 72.0:
                final_grade = "B"

        return final_numeric, final_grade, is_capped, cap_reason

    # Backward compatibility helper
    @classmethod
    def calculate_score(
        cls,
        subsystems: CategoryScores,
        weights: CategoryWeights | None = None,
    ) -> float:
        numeric, _, _, _ = cls.calculate_grade(subsystems, weights)
        return numeric


# Backward compatibility alias
IQScorer = GradeCalculator
