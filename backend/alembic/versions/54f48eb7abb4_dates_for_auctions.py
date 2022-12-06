"""dates for auctions

Revision ID: 54f48eb7abb4
Revises: a66ff1c2e278
Create Date: 2022-11-04 20:19:31.496453

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '54f48eb7abb4'
down_revision = 'a66ff1c2e278'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("listings",sa.Column('start_date',sa.DateTime(timezone=True),nullable=True))
    op.add_column("listings",sa.Column('end_date',sa.DateTime(timezone=True),nullable=True))

def downgrade():
    op.drop_column('listings','start_date')
    op.drop_column('listings','end_date')
