"""offers

Revision ID: 6f4c325f8439
Revises: d768e9412dcd
Create Date: 2022-09-29 18:06:30.917124

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6f4c325f8439'
down_revision = 'd768e9412dcd'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'offers',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('amount',sa.Numeric,nullable=False),
        sa.Column('accepted',sa.Boolean,nullable=False,default=False),
        sa.Column('listing_id',sa.Integer,nullable=False),
        sa.Column('created',sa.DateTime(timezone=True),nullable=False, default=sa.func.now()),
        sa.Column('created_by',sa.Integer,nullable=False),
        sa.Column('last_updated',sa.DateTime(timezone=True), default=sa.func.now()),
    )
    op.create_foreign_key('fk_offers_user_id','offers', 'users',['created_by'], ['id'],)
    op.create_foreign_key('fk_offers_listing_id','offers', 'listings',['listing_id'], ['id'],)


def downgrade():
    op.drop_constraint('fk_offers_user_id','offers','foreignkey')
    op.drop_constraint('fk_offers_listing_id','offers','foreignkey')
    op.drop_table('offers')

