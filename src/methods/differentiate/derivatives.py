from src.objects.elements.base import Element
from src.objects.elements.constants import UndefinedConstant
from src.objects.elements.variables import ScalarVariable
from src.objects.operators.base import Operator


def fix_other_variables(func: Operator, acceptedVariable: ScalarVariable) -> Operator:
    params: dict[str, Element | Operator] = {}
    for key, value in func:
        if isinstance(value, Element):
            if isinstance(value, ScalarVariable) and value != acceptedVariable:
                params[key] = UndefinedConstant()
            else:
                params[key] = value
        elif isinstance(value, Operator):
            params[key] = fix_other_variables(value, acceptedVariable)
        else:
            raise TypeError
    return func.__class__.model_validate(params)