"""Core package for the software design simulator."""

from .project import ProjectSimulator, Phase
from .expression import evaluate_expression

__all__ = ["ProjectSimulator", "Phase", "evaluate_expression"]
