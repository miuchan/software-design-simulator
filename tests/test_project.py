from simulator.project import Phase, ProjectSimulator, create_default_simulator


def test_phase_sample_duration_is_non_negative():
    phase = Phase("Test", base_days=5, complexity_multiplier=1, variability=0.5, quality_impact=0)
    duration = phase.sample_duration(complexity=1.0, rng=__import__("random").Random(0))
    assert duration >= 0


def test_simulation_returns_expected_structure():
    simulator = create_default_simulator(team_size=3, cost_per_day=1000.0)
    result = simulator.simulate(1.2, seed=42)

    assert set(result.keys()) == {"total_days", "budget_used", "quality_score", "timeline"}
    assert isinstance(result["timeline"], list)
    assert len(result["timeline"]) == 5

    total_days = result["total_days"]
    assert total_days > 0
    assert result["budget_used"] == total_days * 3 * 1000.0
    assert 0 <= result["quality_score"] <= 100


def test_project_simulator_validates_inputs():
    try:
        ProjectSimulator([], team_size=3)
    except ValueError:
        pass
    else:
        raise AssertionError("Expected ValueError when no phases are provided")

    try:
        create_default_simulator(team_size=0)
    except ValueError:
        pass
    else:
        raise AssertionError("Expected ValueError when team size is non-positive")

    simulator = create_default_simulator()
    try:
        simulator.simulate(0)
    except ValueError:
        pass
    else:
        raise AssertionError("Expected ValueError when complexity is non-positive")
