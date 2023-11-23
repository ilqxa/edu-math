from src.api.parsing import recognize_string
from src.blocks.operators import *


def test_extraction_variables():
    func = recognize_string('x_1+3*x_2^2')
    assert isinstance(func, Addition)
    res = func.scalar_variables
    assert len(res) == 2
    assert func.addend1 in res
    assert isinstance(func.addend2, Multiplication)
    assert isinstance(func.addend2.multiplier2, Power)
    assert func.addend2.multiplier2.base in res


def test_eval_constant_expression():
    func = recognize_string('2+2')
    res = func.evaluate()
    assert res.__str__() == '4.0'


def test_eval_complex_expression():
    func = recognize_string('2+2*2')
    res = func.evaluate()
    assert res.__str__() == '6.0'


def test_variable_expression_eval():
    func = recognize_string('2+x')
    res = func.evaluate()
    assert res.__str__() == '2.0+x'


def test_derivative_constant():
    func = recognize_string('2+2')
    assert isinstance(func, Operator)
    der = func.derivative(None)
    assert der.__str__() == '0.0+0.0'


def test_derivative_one_var():
    func = recognize_string('2+x')
    assert isinstance(func, Operator)
    x = list(func.scalar_variables)[0]
    der = func.derivative(x)
    assert der.__str__() == '0.0+1.0'


def test_derivative_three_additions():
    func = recognize_string('2+x+2')
    assert isinstance(func, Operator)
    x = list(func.scalar_variables)[0]
    der = func.derivative(x)
    assert der.__str__() == '0.0+1.0+0.0'


def test_derivative_four_additions():
    func = recognize_string('2+x+2+x')
    assert isinstance(func, Operator)
    x = list(func.scalar_variables)[0]
    der = func.derivative(x)
    assert der.__str__() == '0.0+1.0+0.0+1.0'