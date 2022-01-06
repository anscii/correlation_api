"""create_tables
Revision ID: 91bee23ff13f
Revises: 
Create Date: 2022-01-06 12:56:33.130152
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import func


# revision identifiers, used by Alembic
revision = '91bee23ff13f'
down_revision = None
branch_labels = None
depends_on = None

USER_TABLE = 'user'
DATA_TYPE_TABLE = 'data_type'
USER_DATA_TABLE = 'user_data'
CORRELATION_TABLE = 'correlation'


def create_user_table() -> None:
    op.create_table(
        USER_TABLE,
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('last_data_change', sa.DateTime(timezone=False), nullable=False)
    )

def create_data_type_table() -> None:
    op.create_table(
        DATA_TYPE_TABLE,
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String, nullable=False)
    )

    op.create_unique_constraint('data_type_name_unique', DATA_TYPE_TABLE, ['name'])

def create_user_data_table() -> None:
    op.create_table(
        USER_DATA_TABLE,
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('user_id', sa.Integer, sa.ForeignKey("user.id"), nullable=False),
        sa.Column('date', sa.Date, nullable=False),
        sa.Column('type_id', sa.Integer, sa.ForeignKey("data_type.id"), nullable=False),
        sa.Column('value', sa.Float, nullable=False),
        sa.Column('mtime', sa.DateTime(timezone=False), nullable=False, server_default=func.now(), onupdate=func.now())
    )

    op.create_unique_constraint('user_data_unique', USER_DATA_TABLE, ['user_id', 'type_id', 'date'])

def create_correlation_table() -> None:
    op.create_table(
        CORRELATION_TABLE,
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('user_id', sa.Integer, sa.ForeignKey("user.id")),
        sa.Column('type_x_id', sa.Integer, sa.ForeignKey("data_type.id"), nullable=False),
        sa.Column('type_y_id', sa.Integer, sa.ForeignKey("data_type.id"), nullable=False),
        sa.Column('value', sa.Float, nullable=False),
        sa.Column('p_value', sa.Float, nullable=False),
        sa.Column('mtime', sa.DateTime, nullable=False, server_default=func.now(), onupdate=func.now())
    )

    op.create_unique_constraint('correlation_unique', CORRELATION_TABLE, ['user_id', 'type_x_id', 'type_y_id'])


def upgrade() -> None:
    create_user_table()
    create_data_type_table()
    create_user_data_table()
    create_correlation_table()

def downgrade() -> None:
    op.drop_table(CORRELATION_TABLE)
    op.drop_table(USER_DATA_TABLE)
    op.drop_table(USER_TABLE)
    op.drop_table(DATA_TYPE_TABLE)
    
