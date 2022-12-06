"""password_reset_token

Revision ID: 510d7e0e5e70
Revises: 6f4c325f8439
Create Date: 2022-10-03 16:21:10.826785

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '510d7e0e5e70'
down_revision = '6f4c325f8439'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('users',sa.Column('password_reset_token',sa.String,nullable=True,default=None))
    op.add_column('users',sa.Column('password_reset_token_created',sa.DateTime(timezone=True),nullable=True))


def downgrade() -> None:
    op.drop_column('users','password_reset_token')
    op.drop_column('users','password_reset_token_created')
