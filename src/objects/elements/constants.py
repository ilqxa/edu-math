from src.objects.elements.base import Element


class Constant(Element):
    ...


class FloatConstant(Constant):
    value: float
    
    def __str__(self) -> str:
        return str(self.value)


class UndefinedConstant(Constant):
    label: str = 'C'
    
    def __str__(self) -> str:
        return self.label