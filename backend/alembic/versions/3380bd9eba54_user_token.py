"""user token

Revision ID: 3380bd9eba54
Revises: d07e0e045e13
Create Date: 2022-09-20 18:53:18.239671

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3380bd9eba54'
down_revision = 'd07e0e045e13'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('users',sa.Column('token',sa.String,nullable=True,default=None))


def downgrade() -> None:
    op.drop_column('users','token')
