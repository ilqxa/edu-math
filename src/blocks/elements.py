from __future__ import annotations

from abc import ABC, abstractmethod

from pydantic import BaseModel


class Element(ABC, BaseModel):
    
    @abstractmethod
    def evaluate(self) -> Element:
        ...
    
    @abstractmethod
    def derivative(self, var: ScalarVariable | None) -> NumericConstant:
        if var is None: return NumericConstant(value=0.)
        else: raise NotImplementedError

class Constant(Element):
    ...

class NumericConstant(Constant):
    value: float
    
    def __str__(self) -> str:
        return str(self.value)

    def evaluate(self) -> NumericConstant:
        return self
    
    def derivative(self, var: ScalarVariable | None) -> NumericConstant:
        return NumericConstant(value=0.)
    

class ScalarVariable(Element):
    label: str
    
    def __str__(self) -> str:
        return self.label
    
    def __hash__(self) -> int:
        return hash(self.label)
    
    def evaluate(self) -> ScalarVariable:
        return self
    
    def derivative(self, var: ScalarVariable | None) -> NumericConstant:
        if var is None: return NumericConstant(value=0.)
        return NumericConstant(value=1.) if var == self else NumericConstant(value=0.)