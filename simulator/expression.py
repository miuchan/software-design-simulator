"""Utilities for parsing and evaluating arithmetic expressions.

The module implements a tiny arithmetic expression evaluator based on a
recursive descent parser.  It is intentionally lightweight – supporting only
the operators required by the project – but designed to be easily extended in
the future.  The grammar handled by the parser is equivalent to::

    expression  ::= term (("+" | "-") term)*
    term        ::= factor (("*" | "/") factor)*
    factor      ::= ("+" | "-") factor | primary
    primary     ::= NUMBER | "(" expression ")"

Whitespace may appear anywhere in the input and is ignored.  The evaluator
returns ``float`` values and raises :class:`ValueError` when the input cannot be
parsed.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class _Token:
    """Represents a lexical token produced by :func:`_tokenise`.

    Attributes
    ----------
    kind:
        Type of the token. Supported values are ``"NUMBER"`` and single
        character operator tokens (``"+"``, ``"-"``, ``"*"``, ``"/"``, ``"("`` and
        ``")"``).
    value:
        The literal value of the token. For ``"NUMBER"`` tokens this is the
        corresponding ``float`` value.
    """

    kind: str
    value: float | str


def _tokenise(source: str) -> list[_Token]:
    """Convert *source* into a sequence of tokens.

    The lexer supports floating point numbers using Python's ``float``
    conversion rules and ignores ASCII whitespace.  Any unexpected character
    triggers :class:`ValueError`.
    """

    tokens: list[_Token] = []
    index = 0
    length = len(source)
    while index < length:
        char = source[index]
        if char.isspace():
            index += 1
            continue
        if char in "+-*/()":
            tokens.append(_Token(kind=char, value=char))
            index += 1
            continue
        if char.isdigit() or char == ".":
            start = index
            index += 1
            while index < length and (source[index].isdigit() or source[index] == "."):
                index += 1
            literal = source[start:index]
            try:
                number = float(literal)
            except ValueError as exc:  # pragma: no cover - defensive guard
                raise ValueError(f"Invalid number literal: {literal!r}") from exc
            tokens.append(_Token(kind="NUMBER", value=number))
            continue
        raise ValueError(f"Unexpected character: {char!r}")
    tokens.append(_Token(kind="EOF", value=""))
    return tokens


class _Parser:
    """Recursive descent parser implementing the arithmetic grammar."""

    def __init__(self, tokens: list[_Token]) -> None:
        self._tokens = tokens
        self._index = 0

    @property
    def _current(self) -> _Token:
        return self._tokens[self._index]

    def _consume(self, kind: str) -> _Token:
        if self._current.kind != kind:
            raise ValueError(f"Expected token {kind!r} but found {self._current.kind!r}")
        token = self._current
        self._index += 1
        return token

    def parse(self) -> float:
        value = self._parse_expression()
        if self._current.kind != "EOF":
            raise ValueError("Unexpected trailing tokens in expression")
        return value

    def _parse_expression(self) -> float:
        value = self._parse_term()
        while self._current.kind in {"+", "-"}:
            op = self._consume(self._current.kind).kind
            rhs = self._parse_term()
            if op == "+":
                value += rhs
            else:
                value -= rhs
        return value

    def _parse_term(self) -> float:
        value = self._parse_factor()
        while self._current.kind in {"*", "/"}:
            op = self._consume(self._current.kind).kind
            rhs = self._parse_factor()
            if op == "*":
                value *= rhs
            else:
                if rhs == 0:
                    raise ValueError("Division by zero in expression")
                value /= rhs
        return value

    def _parse_factor(self) -> float:
        if self._current.kind in {"+", "-"}:
            op = self._consume(self._current.kind).kind
            value = self._parse_factor()
            return value if op == "+" else -value
        return self._parse_primary()

    def _parse_primary(self) -> float:
        token = self._current
        if token.kind == "NUMBER":
            self._consume("NUMBER")
            return float(token.value)
        if token.kind == "(":
            self._consume("(")
            value = self._parse_expression()
            self._consume(")")
            return value
        raise ValueError(f"Unexpected token {token.kind!r} in expression")


def evaluate_expression(expression: str) -> float:
    """Evaluate *expression* and return its numeric value.

    Parameters
    ----------
    expression:
        Arithmetic expression composed of numbers, the operators ``+``, ``-``,
        ``*`` and ``/``, parentheses and optional whitespace.

    Returns
    -------
    float
        The evaluated result of the expression.

    Raises
    ------
    ValueError
        If *expression* contains invalid syntax or attempts division by zero.
    """

    if not expression or expression.strip() == "":
        raise ValueError("Expression must be a non-empty string")
    tokens = _tokenise(expression)
    parser = _Parser(tokens)
    return parser.parse()


__all__ = ["evaluate_expression"]

