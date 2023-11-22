from src.objects.elements.base import Element
from src.objects.elements.constants import Constant, FloatConstant
from src.objects.elements.variables import ScalarVariable
from src.objects.operators.arithmetic import Addition
from src.objects.operators.base import Operator


def eval_addition(func: Addition) -> Element | Operator:
    if isinstance(func.addend1, FloatConstant) and isinstance(func.addend2, FloatConstant):
        return FloatConstant(value=func.addend1.value + func.addend2.value)
    else:
        return eval_expression(func)


def eval_expression(func: Operator) -> Element | Operator:
    if isinstance(func, Addition): return eval_addition(func)
    else: raise NotImplementedError