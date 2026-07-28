"""Configurable subsystem score weighting system."""

from dataclasses import dataclass


@dataclass
class SubsystemWeights:
    """Configurable subsystem weight configuration summing to 1.0 (100%)."""

    static_analysis: float = 0.15
    architecture: float = 0.15
    security: float = 0.25
    documentation: float = 0.10
    testing: float = 0.15
    ci: float = 0.05
    git_practices: float = 0.05
    repository_health: float = 0.05
