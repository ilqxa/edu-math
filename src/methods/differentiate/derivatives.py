from src.objects.elements.base import Element
from src.objects.elements.constants import Constant, FloatConstant, UndefinedConstant
from src.objects.elements.variables import ScalarVariable
from src.objects.operators.base import Operator
from src.objects.operators.arithmetic import *


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


def extract_derivative_from_addition(func: Addition) -> Element | Operator:
    if isinstance(func.addend1, Constant) and isinstance(func.addend2, Constant):
        return FloatConstant(value=0.)
    elif (
        (isinstance(func.addend1, Constant) and isinstance(func.addend2, ScalarVariable)) or
        (isinstance(func.addend2, Constant) and isinstance(func.addend1, ScalarVariable))
    ):
        return FloatConstant(value=1.)
    elif isinstance(func.addend1, Constant) and isinstance(func.addend2, Operator):
        return find_derivative(func.addend2)
    elif isinstance(func.addend2, Constant) and isinstance(func.addend1, Operator):
        return find_derivative(func.addend1)
    elif isinstance(func.addend1, ScalarVariable) and isinstance(func.addend2, Operator):
        return Addition(
            addend1=FloatConstant(value=1.),
            addend2=find_derivative(func.addend2),
        )
    elif isinstance(func.addend2, ScalarVariable) and isinstance(func.addend1, Operator):
        return Addition(
            addend2=FloatConstant(value=1.),
            addend1=find_derivative(func.addend1),
        )
    elif isinstance(func.addend1, Operator) and isinstance(func.addend2, Operator):
        return Addition(
            addend1=find_derivative(func.addend1),
            addend2=find_derivative(func.addend2),
        )
    else:
        raise TypeError


def find_derivative(func: Operator) -> Element | Operator:
    if isinstance(func, Addition): return extract_derivative_from_addition(func)
    else: raise NotImplementedError