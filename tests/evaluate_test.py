from src.interface.parsing import str_recognize
from src.methods.calculate.evaluate import eval_expression
from src.objects.operators.base import Operator


def test_constant_expression_eval():
    func = str_recognize('2+2')
    res = eval_expression(func)
    assert res.__str__() == '4.0'


def test_variable_expression_eval():
    func = str_recognize('2+x')
    res = eval_expression(func)
    assert res.__str__() == '2.0+x'