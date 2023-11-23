from src.api.parsing import recognize_string


def test_recognition():
    recognized = recognize_string('4+3*x^2')
    assert recognized.__str__() == '4.0+3.0*x^2.0'