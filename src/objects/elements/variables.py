from src.objects.elements.base import Element


class ScalarVariable(Element):
    label: str
    
    def __str__(self) -> str:
        return self.label
    
    def __hash__(self) -> int:
        return hash(self.label)