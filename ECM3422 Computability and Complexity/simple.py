from sat import Expression, parse_expression
from typing import Dict


def _solve_with_assignment(expr: Expression, assignment: Dict[str, bool]) -> bool:
    # Find unassigned vars by the difference between those in the assignment and those in the expression
    unassigned_vars = expr.get_vars().difference(assignment.keys())
    # Python passes dicts by reference so we have to copy assignments
    assignment_cpy = assignment.copy()

    if len(unassigned_vars) == 0:
        # We have a full assignment and so can evaluate
        return expr.evaluate(assignment)

    # Choose an arbritrary unassigned var to assign
    choice_var = list(unassigned_vars)[0]

    # Try assigning true
    assignment_cpy[choice_var] = True

    if _solve_with_assignment(expr, assignment_cpy):
        return True

    # Try assigning false
    assignment_cpy[choice_var] = False

    if _solve_with_assignment(expr, assignment_cpy):
        return True

    # Expression was false with any var assignment, so this path is unsat
    return False


def solve(cs):
    """
    Returns True if cs is SAT
    and False if it is UNSAT
    """
    expr = parse_expression(cs)

    return _solve_with_assignment(expr, dict())
