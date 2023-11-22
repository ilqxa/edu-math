from abc import ABC, abstractmethod
from pydantic import BaseModel


class Operator(ABC, BaseModel):
    
    @property
    @abstractmethod
    def view(self) -> str:
        ...
    
    def __str__(self) -> str:
        return self.view