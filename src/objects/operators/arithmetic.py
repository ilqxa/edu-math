from pydantic import Field

from src.objects.operators.base import Operator
from src.objects.elements.base import Element


class Addition(Operator):
    addend1: Element | Operator = Field(validation_alias='left')
    addend2: Element | Operator = Field(validation_alias='right')
    
    def __str__(self) -> str:
        return f'{self.addend1.__str__()}+{self.addend2.__str__()}'


class Subtraction(Operator):
    minuend: Element | Operator = Field(validation_alias='left')
    subtrahend: Element | Operator = Field(validation_alias='right')
    
    def __str__(self) -> str:
        return f'{self.minuend.__str__()}-{self.subtrahend.__str__()}'


class Multiplication(Operator):
    multiplier1: Element | Operator = Field(validation_alias='left')
    multiplier2: Element | Operator = Field(validation_alias='right')
    
    def __str__(self) -> str:
        return f'{self.multiplier1.__str__()}*{self.multiplier2.__str__()}'


class Division(Operator):
    dividend: Element | Operator = Field(validation_alias='left')
    divisor: Element | Operator = Field(validation_alias='right')
    
    def __str__(self) -> str:
        return f'{self.dividend.__str__()}/{self.divisor.__str__()}'


class Power(Operator):
    base: Element | Operator = Field(validation_alias='left')
    power: Element | Operator = Field(validation_alias='right')
    
    def __str__(self) -> str:
        return f'{self.base.__str__()}^{self.power.__str__()}'