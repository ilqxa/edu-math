from src.interface.parsing import str_recognize


def test_recognition():
    recognized = str_recognize('4+3*x^2')
    assert recognized.__str__() == '4.0+3.0*x^2.0'