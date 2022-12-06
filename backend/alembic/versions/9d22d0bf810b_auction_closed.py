"""auction closed

Revision ID: 9d22d0bf810b
Revises: 8f3ea7e8e828
Create Date: 2022-11-07 17:32:03.957936

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9d22d0bf810b'
down_revision = '8f3ea7e8e828'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('listings',sa.Column('auction_closed',sa.Boolean,default=False,nullable=True))
    op.execute("UPDATE listings SET auction_closed=FALSE")
    op.alter_column('listings','auction_closed',nullable=False)


def downgrade() -> None:
    op.drop_column('listings','auction_closed')
