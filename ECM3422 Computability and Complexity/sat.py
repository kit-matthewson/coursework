from abc import ABC, abstractmethod
from typing import Dict, Set


class Expression(ABC):
    """Abstract base class for an expression (either a literal or clause).

    Here, an expression is something that can be evaluated to give a boolean result.
    """

    @abstractmethod
    def evaluate(self, assignments: Dict[str, bool]) -> bool | None:
        """Attempts to evaluate this expression.

        Args:
            assignments (Dict[str, bool]): Dictionary of (variable name, value) assignments

        Returns:
            The truth value of the expression, or `None` if it is not possible to compute.
        """
        pass

    def get_vars(self) -> Set[str]:
        """Gets the variables used in this expression and its sub-expressions.

        Returns:
            A set of unique variable names.
        """
        # We can construct a set of vars from the set of lits
        lits = list(self.get_lits())
        vars = set([var.name for var in lits])

        return vars

    @abstractmethod
    def get_lits(self) -> Set["Literal"]:
        """Get a set of the unique literals contained in this expression and any sub-expressions.

        Returns:
            A set of unique literals.
        """
        pass


class Literal(Expression):
    """A literal (variable with possible negation)."""

    def __init__(self, name: str, sign: bool):
        self.name = name
        self.sign = sign

    def evaluate(self, assignments: Dict[str, bool]) -> bool | None:
        if self.name in assignments:
            return assignments.get(self.name) == self.sign

        return None

    def get_lits(self) -> Set["Literal"]:
        return set([self])

    def complement(self):
        return Literal(self.name, not self.sign)

    def __str__(self) -> str:
        if self.sign:
            return self.name
        else:
            return f"¬{self.name}"

    def __hash__(self):
        return hash(f"L({self})")

    def __eq__(self, other) -> bool:
        if not isinstance(other, Literal):
            return False

        return self.sign == other.sign and self.name == other.name


class Conjunction(Expression):
    """A conjunction (AND) of two expressions."""

    def __init__(self, left: Expression, right: Expression):
        self.left = left
        self.right = right

    def evaluate(self, assignments: Dict[str, bool]) -> bool | None:
        """Evaluates this conjuction. Short-circuits (on both `False` and `None`).

        Args:
            assignments (Dict[str, bool]): Dictionary of (variable name, value) assignments

        Returns:
            `None` if either expression is `None`. `False` if either expression is `False`. `True` otherwise.
        """
        left_value = self.left.evaluate(assignments)

        if left_value is not True:
            return left_value

        return self.right.evaluate(assignments)

    def get_lits(self) -> Set[Literal]:
        return self.left.get_lits().union(self.right.get_lits())

    def __str__(self) -> str:
        return f"({self.left} ∧ {self.right})"


class Disjunction(Expression):
    """A disjunction (OR) of two expressions."""

    def __init__(self, left: Expression, right: Expression):
        self.left = left
        self.right = right

    def evaluate(self, assignments: Dict[str, bool]) -> bool | None:
        """Evaluates this disjunction. Short-circuits.

        Args:
            assignments (Dict[str, bool]): Dictionary of (variable name, value) assignments

        Returns:
            `True` if either expression is `True`, otherwise `None` if either expression is `None` and `False` if both expressions are `False`.
        """
        left_value = self.left.evaluate(assignments)

        if left_value is True:
            return True

        right_value = self.right.evaluate(assignments)

        if right_value is True:
            return True

        if left_value is None or right_value is None:
            return None

        return False

    def get_lits(self) -> Set[Literal]:
        return self.left.get_lits().union(self.right.get_lits())

    def __str__(self) -> str:
        return f"({self.left} ∨ {self.right})"


def parse_expression(input) -> Expression | None:
    """
    Converts a tuple (e.g. `('+','a',('-','b',('~','a')))`) into an expression.

    Gives underfined behaviour if the input tuple is not properly formed.
    """

    # Recursively generate an expression
    def _to_expr(input) -> Expression | None:
        # Allows for clauses in the form "("?", "a", "b")" instead of "..., ("a"), ..."
        if type(input) is str:
            return Literal(input, True)

        tup_len = len(input)
        if tup_len == 1:
            # ("x")
            return Literal(input[0], True)
        elif tup_len == 2:
            operation, name = input
            if operation == "~":
                # ("~", "x")
                return Literal(input[1], False)
            else:
                # (_, "x")
                return Literal(input[1], True)
        elif tup_len == 3:
            # ("+"/"-", a, b)
            operation, left_tup, right_tup = input

            left = _to_expr(left_tup)
            right = _to_expr(right_tup)

            if operation == "+":
                return Conjunction(left, right)
            elif operation == "-":
                return Disjunction(left, right)

        return None

    return _to_expr(input)
