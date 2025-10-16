"""Command line interface for running the project simulator."""
from __future__ import annotations

import argparse
import json
from typing import Any

from .project import create_default_simulator


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run a software project simulation.")
    parser.add_argument(
        "complexity",
        type=float,
        help="Complexity level of the project (values > 0).",
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=None,
        help="Optional random seed to make the simulation deterministic.",
    )
    parser.add_argument(
        "--team-size",
        type=int,
        default=5,
        help="Number of engineers working on the project.",
    )
    parser.add_argument(
        "--cost-per-day",
        type=float,
        default=800.0,
        help="Cost per engineer per day in monetary units.",
    )
    return parser.parse_args(argv)


def run_simulation(args: argparse.Namespace) -> dict[str, Any]:
    simulator = create_default_simulator(team_size=args.team_size, cost_per_day=args.cost_per_day)
    return simulator.simulate(args.complexity, seed=args.seed)


def main(argv: list[str] | None = None) -> None:
    args = parse_args(argv)
    result = run_simulation(args)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
