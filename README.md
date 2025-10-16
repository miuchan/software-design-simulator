# Software Design Simulator

This repository provides a minimal yet extensible software engineering project simulator. It models the classical lifecycle phases (requirements, design, implementation, verification, and deployment) and produces timeline, budget, and quality estimates for a project of a given complexity.

## Features

- Configurable set of lifecycle phases.
- Deterministic simulations by providing a random seed.
- Command line interface that outputs a JSON summary.
- Simple unit tests that exercise the core functionality.

## Getting Started

### Installation

The project uses a lightweight Python module layout. Create a virtual environment and install the development dependencies with:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt
```

### Running the Simulator

Execute the CLI to simulate a project of complexity `1.3`:

```bash
python -m simulator.cli 1.3 --seed 123
```

The command outputs a JSON document summarising the total time, budget, quality score, and per-phase timeline.

### Running Tests

```bash
pytest
```

## Extending the Simulator

- Add or modify `simulator.project.DEFAULT_PHASES` to reflect your workflow.
- Build richer metrics by extending :class:`~simulator.project.ProjectSimulator`.
- Integrate the CLI output with downstream tools or dashboards.
