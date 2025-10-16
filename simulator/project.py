"""Simple software engineering project simulator."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, List, Optional
import random


@dataclass(frozen=True)
class Phase:
    """A stage of the software engineering lifecycle.

    Attributes
    ----------
    name:
        Human readable name of the phase (e.g. "Design").
    base_days:
        The nominal number of days the phase would take for a project with
        complexity equal to 1.
    complexity_multiplier:
        Multiplier applied to the project complexity to produce the expected
        duration for the phase.
    variability:
        Controls the spread of the randomly sampled duration. The sampled value
        will deviate by up to ``variability`` proportion from the expected
        duration.
    quality_impact:
        Fractional impact on the project's quality score. Positive values
        increase quality, while negative values reduce it.
    """

    name: str
    base_days: float
    complexity_multiplier: float
    variability: float
    quality_impact: float

    def sample_duration(self, complexity: float, *, rng: random.Random) -> float:
        """Sample the number of days this phase takes for the given complexity."""
        expected = self.base_days + self.complexity_multiplier * max(complexity - 1.0, 0.0)
        spread = expected * self.variability
        offset = rng.uniform(-spread, spread)
        duration = max(expected + offset, 0.0)
        return duration


@dataclass
class PhaseOutcome:
    """Stores simulation results for a single phase."""

    name: str
    planned_days: float
    actual_days: float
    start_day: float
    end_day: float
    quality_delta: float


class ProjectSimulator:
    """Runs a light-weight software design project simulation.

    The simulator chains a sequence of :class:`Phase` objects and produces a
    report describing how long the project took, the cost, and the resulting
    quality score.
    """

    def __init__(
        self,
        phases: Iterable[Phase],
        *,
        team_size: int = 5,
        cost_per_day: float = 800.0,
    ) -> None:
        self._phases: List[Phase] = list(phases)
        if not self._phases:
            raise ValueError("ProjectSimulator requires at least one phase")
        if team_size <= 0:
            raise ValueError("team_size must be positive")
        if cost_per_day < 0:
            raise ValueError("cost_per_day cannot be negative")
        self.team_size = team_size
        self.cost_per_day = cost_per_day

    def simulate(self, complexity: float, *, seed: Optional[int] = None) -> dict:
        """Run the simulation for the provided complexity level.

        Parameters
        ----------
        complexity:
            A positive number describing how demanding the project is. Values
            close to 1 represent a typical project, values greater than 1 a
            challenging project, and values below 1 a simple project.
        seed:
            Optional seed used to make the simulation deterministic. If omitted,
            the simulator draws from Python's global random generator.

        Returns
        -------
        dict
            A dictionary containing the total duration, cost, quality, and the
            per-phase timeline.
        """

        if complexity <= 0:
            raise ValueError("complexity must be positive")

        rng = random.Random(seed)
        day_cursor = 0.0
        outcomes: List[PhaseOutcome] = []
        quality_score = 70.0

        for phase in self._phases:
            planned = phase.base_days + phase.complexity_multiplier * max(complexity - 1.0, 0.0)
            actual = phase.sample_duration(complexity, rng=rng)
            start_day = day_cursor
            end_day = start_day + actual
            quality_score += phase.quality_impact
            outcomes.append(
                PhaseOutcome(
                    name=phase.name,
                    planned_days=planned,
                    actual_days=actual,
                    start_day=start_day,
                    end_day=end_day,
                    quality_delta=phase.quality_impact,
                )
            )
            day_cursor = end_day

        total_days = day_cursor
        budget_used = total_days * self.team_size * self.cost_per_day
        quality_score = max(min(quality_score, 100.0), 0.0)

        return {
            "total_days": total_days,
            "budget_used": budget_used,
            "quality_score": quality_score,
            "timeline": [outcome.__dict__ for outcome in outcomes],
        }


DEFAULT_PHASES: List[Phase] = [
    Phase("Requirements", base_days=10, complexity_multiplier=6, variability=0.1, quality_impact=5.0),
    Phase("Design", base_days=12, complexity_multiplier=5, variability=0.15, quality_impact=7.5),
    Phase("Implementation", base_days=30, complexity_multiplier=12, variability=0.2, quality_impact=3.0),
    Phase("Verification", base_days=14, complexity_multiplier=8, variability=0.1, quality_impact=4.5),
    Phase("Deployment", base_days=5, complexity_multiplier=2, variability=0.05, quality_impact=-1.0),
]


def create_default_simulator(*, team_size: int = 5, cost_per_day: float = 800.0) -> ProjectSimulator:
    """Convenience helper returning a :class:`ProjectSimulator` with default phases."""

    return ProjectSimulator(DEFAULT_PHASES, team_size=team_size, cost_per_day=cost_per_day)
