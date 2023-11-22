from abc import ABC, abstractmethod
from pydantic import BaseModel


class Operator(ABC, BaseModel):
    
    @abstractmethod
    def __str__(self) -> str:
        ...