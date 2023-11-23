from __future__ import annotations

from abc import ABC, abstractmethod

from pydantic import BaseModel, Field

from .elements import Element, NumericConstant, ScalarVariable


class Operator(ABC, BaseModel):
    
    def __add__(self, other: Operator | Element) -> Addition:
        return Addition(
            addend1=self,
            addend2=other,
        )
    
    def __sub__(self, other: Operator | Element) -> Subtraction:
        return Subtraction(
            minuend=self,
            subtrahend=other,
        )
    
    def __mul__(self, other: Operator | Element) -> Multiplication:
        return Multiplication(
            multiplier1=self,
            multiplier2=other,
        )
    
    def __div__(self, other: Operator | Element) -> Division:
        return Division(
            dividend=self,
            divisor=other,
        )
    
    def __pow__(self, other: Operator | Element) -> Power:
        return Power(
            base=self,
            power=other,
        )
    
    @property
    def scalar_variables(self) -> set[ScalarVariable]:
        res = set()
        for _, part in self:
            if isinstance(part, Operator): res |= part.scalar_variables
            if isinstance(part, ScalarVariable): res.add(part)
        return res

    @abstractmethod
    def evaluate(self) -> Element | Operator:
        ...
    
    @abstractmethod
    def derivative(self, var: ScalarVariable | None) -> Element | Operator:
        if var is None: return NumericConstant(value=0.)
        else: raise NotImplementedError


class Addition(Operator):
    addend1: Element | Operator
    addend2: Element | Operator
    
    def __str__(self) -> str:
        return f'{self.addend1.__str__()}+{self.addend2.__str__()}'
    
    def evaluate(self) -> Element | Operator:
        addend1 = self.addend1.evaluate()
        addend2 = self.addend2.evaluate()
        if isinstance(addend1, NumericConstant) and isinstance(addend2, NumericConstant):
            return NumericConstant(value=addend1.value+addend2.value)
        else:
            return Addition(
            addend1=addend1,
            addend2=addend2,
        )
    
    def derivative(self, var: ScalarVariable | None) -> Element | Operator:
        return Addition(
            addend1=self.addend1.derivative(var),
            addend2=self.addend2.derivative(var),
        )


class Subtraction(Operator):
    minuend: Element | Operator
    subtrahend: Element | Operator
    
    def __str__(self) -> str:
        return f'{self.minuend.__str__()}-{self.subtrahend.__str__()}'

    def evaluate(self) -> Element | Operator:
        minuend = self.minuend.evaluate()
        subtrahend = self.subtrahend.evaluate()
        if isinstance(minuend, NumericConstant) and isinstance(subtrahend, NumericConstant):
            return NumericConstant(value=minuend.value-subtrahend.value)
        else:
            return Subtraction(
                minuend=minuend,
                subtrahend=subtrahend,
            )
    
    def derivative(self, var: ScalarVariable | None) -> Element | Operator:
        if var is None: return NumericConstant(value=0.)
        return Subtraction(
            minuend=self.minuend.derivative(var),
            subtrahend=self.subtrahend.derivative(var),
        )


class Multiplication(Operator):
    multiplier1: Element | Operator
    multiplier2: Element | Operator
    
    def __str__(self) -> str:
        return f'{self.multiplier1.__str__()}*{self.multiplier2.__str__()}'
    
    def evaluate(self) -> Element | Operator:
        multiplier1 = self.multiplier1.evaluate()
        multiplier2 = self.multiplier2.evaluate()
        if isinstance(multiplier1, NumericConstant) and isinstance(multiplier2, NumericConstant):
            return NumericConstant(value=multiplier1.value*multiplier2.value)
        else:
            return Multiplication(
                multiplier1=multiplier1,
                multiplier2=multiplier2,
            )
    
    def derivative(self, var: ScalarVariable | None) -> Element | Operator:
        if var is None: return NumericConstant(value=0.)
        return Addition(
            addend1=Multiplication(
                multiplier1=self.multiplier1.derivative(var),
                multiplier2=self.multiplier2,
            ),
            addend2=Multiplication(
                multiplier1=self.multiplier2.derivative(var),
                multiplier2=self.multiplier1,
            ),
        )


class Division(Operator):
    dividend: Element | Operator
    divisor: Element | Operator
    
    def __str__(self) -> str:
        return f'{self.dividend.__str__()}/{self.divisor.__str__()}'

    def evaluate(self) -> Element | Operator:
        dividend = self.dividend.evaluate()
        divisor = self.divisor.evaluate()
        if isinstance(dividend, NumericConstant) and isinstance(divisor, NumericConstant):
            return NumericConstant(value=dividend.value/divisor.value)
        else:
            return Division(
                dividend=dividend,
                divisor=divisor,
            )
    
    def derivative(self, var: ScalarVariable | None) -> Element | Operator:
        if var is None: return NumericConstant(value=0.)
        return Division(
        dividend=Subtraction(
            minuend=Multiplication(
                multiplier1=self.dividend.derivative(var),
                multiplier2=self.divisor,
            ),
            subtrahend=Multiplication(
                multiplier1=self.divisor.derivative(var),
                multiplier2=self.dividend,
            ),
        ),
        divisor=Power(
            base=self.divisor,
            power=NumericConstant(value=2.),
        ),
    )


class Power(Operator):
    base: Element | Operator
    power: Element | Operator
    
    def __str__(self) -> str:
        return f'{self.base.__str__()}^{self.power.__str__()}'
    
    def evaluate(self) -> Element | Operator:
        base = self.base.evaluate()
        power = self.power.evaluate()
        if isinstance(base, NumericConstant) and isinstance(power, NumericConstant):
            return NumericConstant(value=base.value**power.value)
        else:
            return Power(
                base=base,
                power=power,
            )
    
    def derivative(self, var: ScalarVariable | None) -> Element | Operator:
        if var is None: return NumericConstant(value=0.)
        return Multiplication(
        multiplier1=self.power,
        multiplier2=Multiplication(
            multiplier1=Power(
                base=self.base,
                power=Subtraction(
                    minuend=self.power,
                    subtrahend=NumericConstant(value=-1.),
                ),
            ),
            multiplier2=self.base.derivative(var),
        ),
    )