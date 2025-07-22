from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Integer
from settings import Base

class Note(Base):
    __tablename__ = "participants"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    email: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    event: Mapped[str] = mapped_column(String, nullable=False)
    age: Mapped[int] = mapped_column(Integer, nullable=False, check_constraint='age >= 12 AND age <= 120')

    def __str__(self):
        return f"учасника з {self.id} та {self.name}"
