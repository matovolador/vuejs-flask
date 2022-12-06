"""listings

Revision ID: 231cc5eafeed
Revises: e6de9f0e9455
Create Date: 2022-09-19 16:15:30.876395

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '231cc5eafeed'
down_revision = 'e6de9f0e9455'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'listings',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('title',sa.String,nullable=False),
        sa.Column('description',sa.String,nullable=True),
        sa.Column('listing_type',sa.String,nullable=False),
        sa.Column('property_type',sa.String,nullable=False),
        sa.Column('property_size',sa.Numeric,nullable=False),
        sa.Column('land_size',sa.Numeric,nullable=False),
        sa.Column('bedrooms',sa.String,nullable=True),
        sa.Column('bathrooms',sa.String,nullable=True),
        sa.Column('images',sa.JSON,nullable=False),
        sa.Column('created',sa.DateTime(timezone=False),nullable=False, default=sa.func.now()),
        sa.Column('created_by',sa.Integer,nullable=False),
        sa.Column('last_updated',sa.DateTime(timezone=False), default=sa.func.now()),
    )
    op.create_foreign_key('fk_listings_user_id','listings', 'users',['created_by'], ['id'],)


def downgrade():
    op.drop_constraint('fk_listings_user_id','listings','foreignkey')
    op.drop_table('listings')
