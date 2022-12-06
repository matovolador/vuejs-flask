"""null defaults auction dates

Revision ID: 8f3ea7e8e828
Revises: 54f48eb7abb4
Create Date: 2022-11-04 20:39:08.593367

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8f3ea7e8e828'
down_revision = '54f48eb7abb4'
branch_labels = None
depends_on = None


def upgrade():
    op.alter_column("listings",'start_date',default=None)
    op.alter_column("listings",'end_date',default=None)
    

def downgrade():
    pass
