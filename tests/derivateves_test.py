from src.interface.parsing import str_recognize
from src.methods.analyse.functions import extract_scalar_variables
from src.methods.differentiate.derivatives import fix_other_variables, find_derivative
from src.objects.operators.base import Operator


def test_fix_variables():
    func1 = str_recognize('x_1+3*x_2^2')
    assert isinstance(func1, Operator)
    variables = extract_scalar_variables(func1)
    x_2 = [v for v in variables if v.label == 'x_2'][0]
    func2 = fix_other_variables(func1, x_2)
    assert func1.__str__() == 'x_1+3.0*x_2^2.0'
    assert func2.__str__() == 'C+3.0*x_2^2.0'


def test_constant_derivative():
    func = str_recognize('2+2')
    assert isinstance(func, Operator)
    der = find_derivative(func)
    assert der.__str__() == '0.0'


def test_one_var_derivative():
    func = str_recognize('2+x')
    assert isinstance(func, Operator)
    der = find_derivative(func)
    assert der.__str__() == '1.0'


def test_three_additions():
    func = str_recognize('2+x+2')
    assert isinstance(func, Operator)
    der = find_derivative(func)
    assert der.__str__() == '1.0'


def test_four_additions():
    func = str_recognize('2+x+2+x')
    assert isinstance(func, Operator)
    der = find_derivative(func)
    assert der.__str__() == '1.0'