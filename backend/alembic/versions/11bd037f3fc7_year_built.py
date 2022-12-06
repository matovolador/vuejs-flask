"""year_built

Revision ID: 11bd037f3fc7
Revises: 2e1e6667f6df
Create Date: 2022-10-26 19:52:58.874173

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '11bd037f3fc7'
down_revision = '2e1e6667f6df'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("listings",sa.Column('year_built',sa.String,nullable=True))


def downgrade() -> None:
    op.drop_column("listings","year_built")
