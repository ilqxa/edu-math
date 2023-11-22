from src.interface.parsing import str_recognize
from src.methods.analyse.functions import extract_scalar_variables
from src.objects.operators.arithmetic import *


def test_extraction_variables():
    func = str_recognize('x_1+3*x_2^2')
    assert isinstance(func, Addition)
    res = extract_scalar_variables(func)
    assert len(res) == 2
    assert func.addend1 in res
    assert isinstance(func.addend2, Multiplication)
    assert isinstance(func.addend2.multiplier2, Power)
    assert func.addend2.multiplier2.base in res