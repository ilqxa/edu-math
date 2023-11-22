from src.interface.parsing import str_recognize


def test_recognition():
    recognized = str_recognize('2+2*2')
    assert recognized.__str__() == '2+2*2'