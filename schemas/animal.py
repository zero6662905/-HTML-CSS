from pydantic import BaseModel, ConfigDict


class AnimalBase(BaseModel):
    name: str
    age: int
    adopted: str


class AnimalOut(AnimalBase):
    model_config = ConfigDict(from_attributes=True)

    id: int

