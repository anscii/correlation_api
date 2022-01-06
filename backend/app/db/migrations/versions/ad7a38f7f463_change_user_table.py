"""change_user_table
Revision ID: ad7a38f7f463
Revises: 91bee23ff13f
Create Date: 2022-01-06 14:57:13.055991
"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic
revision = 'ad7a38f7f463'
down_revision = '91bee23ff13f'
branch_labels = None
depends_on = None

USER_TABLE = 'user'
DATA_CHANGE_COLUMN = 'last_data_change'
NAME_COLUMN = 'name'

def change_user_table() -> None:
    op.alter_column(USER_TABLE, DATA_CHANGE_COLUMN, nullable=True)
    op.add_column(USER_TABLE,
        sa.Column(NAME_COLUMN, sa.String)
    )

def undo_user_table_changes() -> None:
    op.alter_column(USER_TABLE, DATA_CHANGE_COLUMN, nullable=False)
    op.drop_column(NAME_COLUMN)


def upgrade() -> None:
    change_user_table()

def downgrade() -> None:
    undo_user_table_changes()
