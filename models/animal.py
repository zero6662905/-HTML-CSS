from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from settings import Base


class Animals(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    age: Mapped[int] = mapped_column( nullable=False)
    adopted: Mapped[str] = mapped_column(String(50), nullable=True)


    def __str__(self):
        return f"<animal> з {self.id} та {self.name}"
