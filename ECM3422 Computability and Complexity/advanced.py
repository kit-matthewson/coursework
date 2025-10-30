from typing import List

from sat import Expression, Literal, parse_expression, Disjunction, Conjunction


Formula = List[List[Literal]]


def dpll(formula: Formula) -> bool:
    # Unit propagation
    while True:
        unit_lit = find_unit_literal(formula)

        if unit_lit is None:
            break

        formula = propagate_literal(formula, unit_lit)

    # Pure literal elimination
    while True:
        pure_lit = find_pure_literal(formula)

        if pure_lit is None:
            break

        formula = propagate_literal(formula, pure_lit)

    # Stopping conditions
    if len(formula) == 0:  # Is empty
        return True
    elif [] in formula:  # Contains an empty clause
        return False

    # Branch on arbritrary variable
    lits = [lit for clause in formula for lit in clause]  # Flattens the formula
    choice_var = lits[0].name  # Choose an arbritrary lit

    true_expr = propagate_literal(formula, Literal(choice_var, True))

    if dpll(true_expr):
        return True

    false_expr = propagate_literal(formula, Literal(choice_var, False))

    return dpll(false_expr)


def propagate_literal(formula: Expression, literal: Literal) -> Expression:
    """
    Performs boolean constrain propagation. This removes every clause containing the literal, and removes the complement of the literal from all clauses.

    Returns:
        A new formula with the literal propogated.
    """
    new_formula = []

    for clause in formula:
        if literal in clause:
            continue

        new_clause = [lit for lit in clause if lit != literal.complement()]
        new_formula.append(new_clause)

    return new_formula


def find_unit_literal(formula: Formula) -> Literal | None:
    """
    Attempts to find a unit literal. A unit literal is one that appears in a clause such that it can only have one assignment that makes the clause true.

    Returns:
        A unit literal. `None` if the expression does not contain a unit literal.
    """
    for clause in formula:
        if len(clause) == 1:
            return clause[0]

    return None


def find_pure_literal(formula: Formula) -> Literal | None:
    """
    Attempts to find a pure literal. A pure literal is one that occurs in only one polarity in the expression.

    Returns:
        A pure literal. `None` if the expression does not contain a pure literal.
    """
    lits = set()

    for clause in formula:
        lits.update(clause)

    for lit in lits:
        comp = lit.complement()

        if comp not in lits:
            return lit

    return None


def to_cnf(expression: Expression) -> Formula:
    def _distribute(expr: Expression) -> Expression:
        # a OR (b AND c) -> (a OR b) AND (a OR c)

        if isinstance(expr, Disjunction):
            # x OR y
            left = _distribute(expr.left)
            right = _distribute(expr.right)

            # (a AND b) OR y -> ((a OR y) AND (b OR y))
            if isinstance(left, Conjunction):
                return _distribute(
                    Conjunction(
                        Disjunction(left.left, right),
                        Disjunction(left.right, right),
                    )
                )

            # ... or the mirror
            if isinstance(right, Conjunction):
                return _distribute(
                    Conjunction(
                        Disjunction(left, right.left),
                        Disjunction(left, right.right),
                    )
                )

            return Disjunction(left, right)

        elif isinstance(expr, Conjunction):
            return Conjunction(_distribute(expr.left), _distribute(expr.right))

        else:
            return expr

    def _to_formula(expr: Expression) -> Formula:
        if isinstance(expr, Literal):
            return [[expr]]

        if isinstance(expr, Disjunction):
            # We assume that the expression has been distributed and so it is disjunctions from here on down
            return [list(expr.get_lits())]

        if isinstance(expr, Conjunction):
            left = _to_formula(expr.left)
            right = _to_formula(expr.right)

            return left + right

        return []

    distributed = _distribute(expression)
    cnf = _to_formula(distributed)

    # If a clause contains 'x' and 'not x', then it is a tautology
    clean_cnf = []
    for clause in cnf:
        has_comp = False

        for lit in clause:
            if lit.complement() in clause:
                has_comp = True

        if not has_comp:
            clean_cnf += [clause]

    return clean_cnf


def solve(cs):
    """
    Returns True if cs is SAT
    and False if it is UNSAT
    """
    expression = parse_expression(cs)
    formula = to_cnf(expression)

    return dpll(formula)
