"""Complexity, maintainability, and quality grading calculations."""

import math


def calculate_maintainability_index(
    loc: int,
    complexity: int,
    comment_lines: int,
) -> float:
    """Calculate Maintainability Index (MI) score (0.0 to 100.0).

    Uses SEI maintainability index variant scaled to 100:
    MI = max(0, (171 - 5.2 * ln(Halstead Volume approx) - 0.23 * Cyclomatic Complexity - 16.2 * ln(LOC) + 50 * sin(sqrt(2.4 * comment_ratio))) * 100 / 171)
    """
    if loc <= 0:
        return 100.0

    safe_loc = max(loc, 1)
    safe_complexity = max(complexity, 1)

    # Simplified Halstead Volume approximation based on code lines
    volume_approx = safe_loc * math.log2(max(safe_loc, 2))

    raw_mi = (
        171.0
        - 5.2 * math.log(max(volume_approx, 1.0))
        - 0.23 * safe_complexity
        - 16.2 * math.log(safe_loc)
    )

    # Comment ratio boost
    comment_ratio = comment_lines / safe_loc
    if comment_ratio > 0:
        comment_boost = 50.0 * math.sin(math.sqrt(2.4 * min(comment_ratio, 1.0)))
        raw_mi += comment_boost

    # Normalize to 0 - 100 range
    normalized_mi = (raw_mi * 100.0) / 171.0
    return max(0.0, min(100.0, round(normalized_mi, 2)))


def calculate_complexity_grade(avg_complexity: float) -> str:
    """Assign letter grade (A - F) based on average cyclomatic complexity."""
    if avg_complexity <= 5.0:
        return "A"
    elif avg_complexity <= 10.0:
        return "B"
    elif avg_complexity <= 20.0:
        return "C"
    elif avg_complexity <= 30.0:
        return "D"
    elif avg_complexity <= 40.0:
        return "E"
    else:
        return "F"
