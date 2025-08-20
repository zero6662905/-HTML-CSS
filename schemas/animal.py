from pydantic import BaseModel, ConfigDict
from typing import Optional

class AnimalBase(BaseModel):
    name: str
    age: int
    adopted:str

class AnimalCreate(AnimalBase):
    pass

class AnimalUpdate(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None
    adopted: Optional[str] = None

class AnimalInDB(AnimalBase):
    id: int

    model_config = ConfigDict(from_attributes=True)

class AnimalOut(AnimalBase):
    model_config = ConfigDict(from_attributes=True)

    id: int