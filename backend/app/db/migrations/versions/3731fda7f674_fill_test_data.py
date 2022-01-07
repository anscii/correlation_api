"""fill_test_data
Revision ID: 3731fda7f674
Revises: ad7a38f7f463
Create Date: 2022-01-07 09:53:23.589511
"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic
revision = '3731fda7f674'
down_revision = 'ad7a38f7f463'
branch_labels = None
depends_on = None

def create_user() -> None:
    op.execute("INSERT INTO public.user (id, name) VALUES (1, 'test user 1');")

def create_data_types() -> None:
    op.execute("""INSERT INTO data_type (id, name)
                VALUES (1, 'steps'),
                (2, 'avg_hr');""")

def create_user_data() -> None:
    op.execute(""" INSERT INTO user_data (user_id, date, type_id, value, mtime)
                VALUES (1, '2022-01-01', 1, 1099, NOW()),
                       (1, '2022-01-01', 2, 72.12, NOW()),
                       (1, '2022-01-02', 1, 2500, NOW()),
                       (1, '2022-01-02', 2, 74.45, NOW()),
                       (1, '2022-01-03', 1, 4536, NOW()),
                       (1, '2022-01-03', 2, 73.02, NOW()),
                       (1, '2022-01-05', 1, 10000, NOW()),
                       (1, '2022-01-06', 2, 80.63, NOW());""")
    op.execute("UPDATE public.user SET last_data_change = NOW() WHERE id=1;")

def delete_test_data() -> None:
    op.execute("DELETE FROM user_data WHERE user_id=1;")
    op.execute("DELETE FROM public.user WHERE id=1;")
    op.execute("DELETE FROM public.data_type WHERE id IN (1, 2);")

def upgrade() -> None:
    create_user()
    create_data_types()
    create_user_data()

def downgrade() -> None:
    delete_test_data()
