"""animal healthy update

Revision ID: 7fb7972973fa
Revises: 34756ba81b17
Create Date: 2025-08-24 15:38:19.972581

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7fb7972973fa'
down_revision: Union[str, Sequence[str], None] = '34756ba81b17'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # Створюємо нову тимчасову таблицю з потрібною структурою
    op.create_table(
        'new_animals',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String(50), nullable=False),
        sa.Column('age', sa.Integer, nullable=False),
        sa.Column('adopted', sa.String(50), nullable=True),  # Змінено на nullable=True
        sa.Column('health_status', sa.String(50), nullable=False, default='healthy')
    )
    # Переносимо дані зі старої таблиці
    op.execute("INSERT INTO new_animals (id, name, age, adopted, health_status) SELECT id, name, age, adopted, health_status FROM animals")
    # Видаляємо стару таблицю
    op.drop_table('animals')
    # Перейменовуємо нову таблицю
    op.rename_table('new_animals', 'animals')

def downgrade():
    # Для відкату створюємо таблицю з оригінальною структурою (adopted NOT NULL)
    op.create_table(
        'new_animals',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String(50), nullable=False),
        sa.Column('age', sa.Integer, nullable=False),
        sa.Column('adopted', sa.String(50), nullable=False),  # Повертаємо NOT NULL
        sa.Column('health_status', sa.String(50), nullable=False, default='healthy')
    )
    # Переносимо дані, враховуючи, що adopted не може бути NULL
    op.execute("INSERT INTO new_animals (id, name, age, adopted, health_status) SELECT id, name, age, COALESCE(adopted, 'unknown'), health_status FROM animals")
    op.drop_table('animals')
    op.rename_table('new_animals', 'animals')
