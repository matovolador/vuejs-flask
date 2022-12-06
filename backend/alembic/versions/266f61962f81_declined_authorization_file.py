"""declined authorization file

Revision ID: 266f61962f81
Revises: cfd73e3d73fd
Create Date: 2022-11-08 16:25:15.336801

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '266f61962f81'
down_revision = 'cfd73e3d73fd'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('authorization_files',sa.Column('declined',sa.Boolean,default=False,nullable=True))
    op.execute("UPDATE authorization_files SET declined=FALSE")
    op.alter_column('authorization_files','declined',nullable=False)
    op.alter_column('authorization_files','approved_by',new_column_name='updated_by')
    op.alter_column('authorization_files','approved_time',new_column_name='updated_time')


def downgrade():
    op.drop_column('authorization_files','declined')
    op.alter_column('authorization_files','updated_by',new_column_name='approved_by')
    op.alter_column('authorization_files','updated_time',new_column_name='approved_time')
