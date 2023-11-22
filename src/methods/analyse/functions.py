from src.objects.elements.variables import ScalarVariable
from src.objects.operators.base import Operator


def extract_scalar_variables(func: Operator) -> set[ScalarVariable]:
    res = set()
    for _, part in func:
        if isinstance(part, Operator): res |= extract_scalar_variables(part)
        if isinstance(part, ScalarVariable): res.add(part)
    return res