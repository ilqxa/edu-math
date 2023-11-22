from src.objects.elements.base import Element


class FloatConstant(Element):
    value: float
    
    def __str__(self) -> str:
        return str(self.value)