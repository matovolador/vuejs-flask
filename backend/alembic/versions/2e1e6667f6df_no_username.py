"""no username

Revision ID: 2e1e6667f6df
Revises: 510d7e0e5e70
Create Date: 2022-10-21 19:05:27.684306

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2e1e6667f6df'
down_revision = '510d7e0e5e70'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.drop_column('users','username')


def downgrade() -> None:
    op.add_column('users','username',sa.Column(sa.String,nullable=False,unique=False))
