from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from settings import Base

class UserDB(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(nullable=False)  # Видалено unique=True

    def __str__(self):
        return f"<user> з {self.id} та {self.username}"
