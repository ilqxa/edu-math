from src.objects.elements.base import Element
from src.objects.elements.variables import ScalarVariable
from src.objects.operators.base import Operator
from src.objects.operators.arithmetic import *


operations: dict[int, dict[str, type[Operator]]] = {
    1: {
        '+': Addition,
        '-': Subtraction,
    },
    2: {
        '*': Multiplication,
        '/': Division,
    },
    3: {
        '^': Power,
    },
}


def str_recognize(text: str) -> Element | Operator:
    for _, ops in operations.items():
        poss = [text.find(sign) for sign in ops.keys()]
        pos = min((p for p in poss if p > 0), default=-1)
        if pos >= 0:
            return ops[text[pos]].model_validate({
                'left': str_recognize(text[:pos]),
                'right': str_recognize(text[pos+1:]),
            })
    return ScalarVariable(label=text)