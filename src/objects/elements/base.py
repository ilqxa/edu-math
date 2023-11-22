from abc import ABC
from pydantic import BaseModel


class Element(ABC, BaseModel):
    label: str
    
    def __str__(self) -> str:
        return self.label