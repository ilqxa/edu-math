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


def differentiate_addition(func: Addition) -> Addition:
    return Addition(
        addend1=analytic_differentiate(func.addend1),
        addend2=analytic_differentiate(func.addend2),
    )


def differentiate_subtraction(func: Subtraction) -> Subtraction:
    return Subtraction(
        minuend=analytic_differentiate(func.minuend),
        subtrahend=analytic_differentiate(func.subtrahend),
    )


def differentiate_multiplication(func: Multiplication) -> Addition:
    return Addition(
        addend1=Multiplication(
            multiplier1=analytic_differentiate(func.multiplier1),
            multiplier2=func.multiplier2,
        ),
        addend2=Multiplication(
            multiplier1=analytic_differentiate(func.multiplier2),
            multiplier2=func.multiplier1,
        ),
    )


def differentiate_division(func: Division) -> Division:
    return Division(
        dividend=Subtraction(
            minuend=Multiplication(
                multiplier1=analytic_differentiate(func.dividend),
                multiplier2=func.divisor,
            ),
            subtrahend=Multiplication(
                multiplier1=analytic_differentiate(func.divisor),
                multiplier2=func.dividend,
            ),
        ),
        divisor=Power(
            base=func.divisor,
            power=FloatConstant(value=2.),
        ),
    )

def differentiate_power(func: Power) -> Multiplication:
    return Multiplication(
        multiplier1=func.power,
        multiplier2=Multiplication(
            multiplier1=Power(
                base=func.base,
                power=Subtraction(
                    minuend=func.power,
                    subtrahend=FloatConstant(value=-1.),
                ),
            ),
            multiplier2=analytic_differentiate(func.base),
        ),
    )


def analytic_differentiate(obj: Element | Operator) -> Element | Operator:
    if isinstance(obj, Constant): return FloatConstant(value=0.)
    elif isinstance(obj, ScalarVariable): return FloatConstant(value=1.)
    elif isinstance(obj, Addition): return differentiate_addition(obj)
    elif isinstance(obj, Subtraction): return differentiate_subtraction(obj)
    elif isinstance(obj, Multiplication): return differentiate_multiplication(obj)
    elif isinstance(obj, Division): return differentiate_division(obj)
    elif isinstance(obj, Power): return differentiate_power(obj)
    else: raise NotImplementedError