"""extra_listings

Revision ID: d07e0e045e13
Revises: 2a312a626f23
Create Date: 2022-09-20 15:36:15.810952

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd07e0e045e13'
down_revision = '2a312a626f23'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('listings',sa.Column('price',sa.Numeric,nullable=False))
    op.add_column('listings',sa.Column('incremental_price_amount',sa.Numeric,nullable=True))


def downgrade() -> None:
    op.drop_column('listings','price')
    op.drop_column('listings','incremental_price_amount')
