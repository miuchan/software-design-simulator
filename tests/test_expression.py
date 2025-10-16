from math import isclose

import pytest

from simulator.expression import evaluate_expression


@pytest.mark.parametrize(
    "expression, expected",
    [
        ("1 + 2", 3.0),
        ("2 * 3 + 4", 10.0),
        ("2 * (3 + 4)", 14.0),
        ("(1 + 2) * (3 + 4)", 21.0),
        ("-5 + 10", 5.0),
        ("-3 * -2", 6.0),
        ("8 / 4", 2.0),
        ("3 + 4 * 2 / (1 - 5)", 1.0),
    ],
)
def test_evaluate_expression(expression: str, expected: float) -> None:
    assert isclose(evaluate_expression(expression), expected)


@pytest.mark.parametrize(
    "expression",
    ["", "   ", "1 / 0", "1 +", "(2 * 3", "2 ** 3"],
)
def test_evaluate_expression_invalid_inputs(expression: str) -> None:
    with pytest.raises(ValueError):
        evaluate_expression(expression)
