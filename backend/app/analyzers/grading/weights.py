"""Configurable 5-category score weighting system."""

from dataclasses import dataclass


@dataclass
class CategoryWeights:
    """Configurable category weight configuration summing to 1.0 (100%)."""

    security: float = 0.30
    architecture: float = 0.20
    code_quality: float = 0.20
    maintainability: float = 0.20
    community_velocity: float = 0.10


# Backward compatibility alias
SubsystemWeights = CategoryWeights
