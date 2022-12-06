"""images

Revision ID: 05076512c5b2
Revises: 231cc5eafeed
Create Date: 2022-09-20 15:35:54.467532

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '05076512c5b2'
down_revision = '231cc5eafeed'
branch_labels = None
depends_on = None

def upgrade():
    op.create_table(
        'images',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('uuid',sa.String,nullable=False,unique=True),
        sa.Column('url',sa.String,nullable=False),
        sa.Column('created',sa.DateTime(timezone=False),nullable=False, default=sa.func.now()),
        sa.Column('created_by',sa.Integer,nullable=False),
        sa.Column('last_updated',sa.DateTime(timezone=False), default=sa.func.now()),
    )
    op.create_foreign_key('fk_images_user_id','images', 'users',['created_by'], ['id'],)


def downgrade():
    op.drop_constraint('fk_images_user_id','images','foreignkey')
    op.drop_table('images')
