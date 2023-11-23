from src.objects.elements.base import Element
from src.objects.elements.constants import Constant, FloatConstant
from src.objects.elements.variables import ScalarVariable
from src.objects.operators.arithmetic import Addition
from src.objects.operators.base import Operator


def eval_addition(func: Addition) -> FloatConstant | Addition:
    addend1 = eval(func.addend1)
    addend2 = eval(func.addend2)
    
    if isinstance(addend1, FloatConstant) and isinstance(addend2, FloatConstant):
        return FloatConstant(value=addend1.value+addend2.value)
    else:
        return Addition(
            addend1=addend1,
            addend2=addend2,
        )


def eval(obj: Element | Operator) -> Element | Operator:
    if isinstance(obj, (Constant, ScalarVariable)): return obj
    elif isinstance(obj, Addition): return eval_addition(obj)
    else: raise NotImplementedError