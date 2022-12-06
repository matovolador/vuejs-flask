"""city_province

Revision ID: 5cdd1ad97217
Revises: 11bd037f3fc7
Create Date: 2022-10-26 20:14:49.117418

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5cdd1ad97217'
down_revision = '11bd037f3fc7'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("listings",sa.Column('city_province',sa.String,nullable=True))


def downgrade() -> None:
    op.drop_column("listings","city_province")
