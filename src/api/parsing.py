from src.blocks.operators import *

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


def recognize_string(text: str) -> Element | Operator:
    # Detect the operator
    for _, ops in operations.items():
        pos = max(text.find(sign) for sign in ops.keys())
        if pos >= 0:
            fields = list(ops[text[pos]].model_fields.keys())
            return ops[text[pos]].model_validate({
                fields[0]: recognize_string(text[:pos]),
                fields[1]: recognize_string(text[pos+1:]),
            })
    # Parse element
    try: val = float(text)
    except: return ScalarVariable(label=text)
    else: return NumericConstant(value=val)