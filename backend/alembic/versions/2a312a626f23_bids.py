"""bids

Revision ID: 2a312a626f23
Revises: 05076512c5b2
Create Date: 2022-09-20 15:36:03.899620

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2a312a626f23'
down_revision = '05076512c5b2'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'bids',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('created_by',sa.Integer,nullable=False),
        sa.Column('amount',sa.Numeric,nullable=True),
        sa.Column('listing_id',sa.Integer,nullable=False),
        sa.Column('created',sa.DateTime(timezone=False),nullable=False, default=sa.func.now()),
        sa.Column('last_updated',sa.DateTime(timezone=False), default=sa.func.now()),
    )
    op.create_foreign_key('fk_bids_user_id','bids', 'users',['created_by'], ['id'],)
    op.create_foreign_key('fk_bids_listing_id','bids', 'listings',['listing_id'], ['id'],)


def downgrade():
    op.drop_constraint('fk_bids_user_id','bids','foreignkey')
    op.drop_constraint('fk_bids_listing_id','bids','foreignkey')
    op.drop_table('bids')
