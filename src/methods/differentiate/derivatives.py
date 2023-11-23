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


def differentiate_addition(func: Addition) -> Element | Operator:
    if isinstance(func.addend1, Constant) and isinstance(func.addend2, Constant):
        return FloatConstant(value=0.)
    elif (
        (isinstance(func.addend1, Constant) and isinstance(func.addend2, ScalarVariable)) or
        (isinstance(func.addend2, Constant) and isinstance(func.addend1, ScalarVariable))
    ):
        return FloatConstant(value=1.)
    elif isinstance(func.addend1, Constant) and isinstance(func.addend2, Operator):
        return differentiate_operator(func.addend2)
    elif isinstance(func.addend2, Constant) and isinstance(func.addend1, Operator):
        return differentiate_operator(func.addend1)
    elif isinstance(func.addend1, ScalarVariable) and isinstance(func.addend2, Operator):
        return Addition(
            addend1=FloatConstant(value=1.),
            addend2=differentiate_operator(func.addend2),
        )
    elif isinstance(func.addend2, ScalarVariable) and isinstance(func.addend1, Operator):
        return Addition(
            addend2=FloatConstant(value=1.),
            addend1=differentiate_operator(func.addend1),
        )
    elif isinstance(func.addend1, Operator) and isinstance(func.addend2, Operator):
        return Addition(
            addend1=differentiate_operator(func.addend1),
            addend2=differentiate_operator(func.addend2),
        )
    else:
        raise NotImplementedError


def differentiate_subtraction(func: Subtraction) -> Element | Operator:
    if isinstance(func.minuend, Constant) and isinstance(func.subtrahend, Constant):
        return FloatConstant(value=0.)
    elif isinstance(func.minuend, Constant) and isinstance(func.subtrahend, ScalarVariable):
        return FloatConstant(value=-1.)
    elif isinstance(func.subtrahend, Constant) and isinstance(func.minuend, ScalarVariable):
        return FloatConstant(value=1.)
    elif isinstance(func.minuend, Constant) and isinstance(func.subtrahend, Operator):
        return Subtraction(
            minuend=FloatConstant(value=0.),
            subtrahend=differentiate_operator(func.subtrahend),
        )
    elif isinstance(func.subtrahend, Constant) and isinstance(func.minuend, Operator):
        return differentiate_operator(func.minuend)
    elif isinstance(func.minuend, ScalarVariable) and isinstance(func.subtrahend, Operator):
        return Subtraction(
            minuend=FloatConstant(value=1.),
            subtrahend=differentiate_operator(func.subtrahend),
        )
    elif isinstance(func.subtrahend, ScalarVariable) and isinstance(func.minuend, Operator):
        return Subtraction(
            minuend=differentiate_operator(func.minuend),
            subtrahend=FloatConstant(value=1.),
        )
    elif isinstance(func.minuend, Operator) and isinstance(func.subtrahend, Operator):
        return Subtraction(
            minuend=differentiate_operator(func.minuend),
            subtrahend=differentiate_operator(func.subtrahend),
        )
    else:
        raise NotImplementedError


def differentiate_multiplication(func: Multiplication) -> Element | Operator:
    if isinstance(func.multiplier1, Constant) and isinstance(func.multiplier2, Constant):
        return FloatConstant(value=0.)
    elif isinstance(func.multiplier1, Constant) and isinstance(func.multiplier2, ScalarVariable):
        return func.multiplier1
    elif isinstance(func.multiplier2, Constant) and isinstance(func.multiplier1, ScalarVariable):
        return func.multiplier2
    elif isinstance(func.multiplier1, Constant) and isinstance(func.multiplier2, Operator):
        return Multiplication(
            multiplier1=func.multiplier1,
            multiplier2=differentiate_operator(func.multiplier2),
        )
    elif isinstance(func.multiplier2, Constant) and isinstance(func.multiplier1, Operator):
        return Multiplication(
            multiplier1=differentiate_operator(func.multiplier1),
            multiplier2=func.multiplier2,
        )
    elif isinstance(func.multiplier1, ScalarVariable) and isinstance(func.multiplier2, Operator):
        return Addition(
            addend1=func.multiplier2,
            addend2=Multiplication(
                multiplier1=func.multiplier1,
                multiplier2=differentiate_operator(func.multiplier2),
            ),
        )
    elif isinstance(func.multiplier2, ScalarVariable) and isinstance(func.multiplier1, Operator):
        return Addition(
            addend1=Multiplication(
                multiplier1=differentiate_operator(func.multiplier1),
                multiplier2=func.multiplier2,
            ),
            addend2=func.multiplier1,
        )
    elif isinstance(func.multiplier1, Operator) and isinstance(func.multiplier2, Operator):
        return Addition(
            addend1=Multiplication(
                multiplier1=differentiate_operator(func.multiplier1),
                multiplier2=func.multiplier2,
            ),
            addend2=Multiplication(
                multiplier1=differentiate_operator(func.multiplier2),
                multiplier2=func.multiplier1,
            ),
        )
    else:
        raise NotImplementedError


def differentiate_division(func: Division) -> Element | Operator:
    if isinstance(func.dividend, Constant) and isinstance(func.divisor, Constant):
        # (c-c)' = c' = 0
        return FloatConstant(value=0.)
    elif isinstance(func.dividend, Constant) and isinstance(func.divisor, ScalarVariable):
        # (c-x)' = -(c/(x^2))
        return Subtraction(
            minuend=FloatConstant(value=0.),
            subtrahend=Division(
                dividend=func.dividend,
                divisor=Power(
                    base=func.divisor,
                    power=FloatConstant(value=2.),
                ),
            ),
        )
    elif isinstance(func.divisor, Constant) and isinstance(func.dividend, ScalarVariable):
        # (x-c)' = -(c/(x^2))
        return Subtraction(
            minuend=FloatConstant(value=0.),
            subtrahend=Division(
                dividend=func.divisor,
                divisor=Power(
                    base=func.dividend,
                    power=FloatConstant(value=2.),
                ),
            ),
        )
    elif isinstance(func.dividend, Constant) and isinstance(func.divisor, Operator):
        # (c/v)' = (-v'c) / v^2
        return Division(
            dividend=Subtraction(
                minuend=FloatConstant(value=0.),
                subtrahend=Multiplication(
                    multiplier1=differentiate_operator(func.divisor),
                    multiplier2=func.dividend,
                ),
            ),
            divisor=Power(
                base=func.divisor,
                power=FloatConstant(value=2.),
            ),
        )
    elif isinstance(func.divisor, Constant) and isinstance(func.dividend, Operator):
        # (u/c)' = u'/c
        return Division(
            dividend=differentiate_operator(func.dividend),
            divisor=func.divisor,
        )
    elif isinstance(func.dividend, ScalarVariable) and isinstance(func.divisor, Operator):
        # (x/v)' = (v-xv') / v^2
        return Division(
            dividend=Subtraction(
                minuend=func.divisor,
                subtrahend=Multiplication(
                    multiplier1=func.dividend,
                    multiplier2=differentiate_operator(func.divisor),
                ),
            ),
            divisor=Power(
                base=func.divisor,
                power=FloatConstant(value=2.),
            ),
        )
    elif isinstance(func.divisor, ScalarVariable) and isinstance(func.dividend, Operator):
        # (u/x)' = (xu'-u) / x^2
        return Division(
            dividend=Subtraction(
                minuend=Multiplication(
                    multiplier1=func.divisor,
                    multiplier2=differentiate_operator(func.dividend),
                ),
                subtrahend=func.dividend,
            ),
            divisor=Power(
                base=func.divisor,
                power=FloatConstant(value=2.),
            ),
        )
    elif isinstance(func.dividend, Operator) and isinstance(func.divisor, Operator):
        # (u/v)' = (u'v-v'u) / v^2
        return Division(
            dividend=Subtraction(
                minuend=Multiplication(
                    multiplier1=differentiate_operator(func.dividend),
                    multiplier2=func.divisor,
                ),
                subtrahend=Multiplication(
                    multiplier1=differentiate_operator(func.divisor),
                    multiplier2=func.dividend,
                ),
            ),
            divisor=Power(
                base=func.divisor,
                power=FloatConstant(value=2.),
            ),
        )
    else:
        raise NotImplementedError


def differentiate_operator(func: Operator) -> Element | Operator:
    if isinstance(func, Addition): return differentiate_addition(func)
    elif isinstance(func, Subtraction): return differentiate_subtraction(func)
    elif isinstance(func, Multiplication): return differentiate_multiplication(func)
    else: raise NotImplementedError