"""authorization form

Revision ID: cfd73e3d73fd
Revises: 8f3ea7e8e828
Create Date: 2022-11-07 16:33:05.752715

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cfd73e3d73fd'
down_revision = '8f3ea7e8e828'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table("authorization_files",
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('created_by',sa.Integer,nullable=False),
        sa.Column('created',sa.DateTime(timezone=True),nullable=False, default=sa.func.now()),
        sa.Column('last_updated',sa.DateTime(timezone=True), default=sa.func.now()),
        sa.Column('authorization_file_url',sa.String,nullable=True),
        sa.Column('approved',sa.Boolean,nullable=False,default=False),
        sa.Column('approved_time',sa.DateTime(timezone=True),nullable=True),
        sa.Column('approved_by',sa.Integer,nullable=True),
    )
    op.create_foreign_key('fk_authorization_files_user_id','authorization_files', 'users',['created_by'], ['id'],)
    op.create_foreign_key('fk_authorization_files_approved_by_id','authorization_files', 'users',['approved_by'], ['id'],)

def downgrade() -> None:
    op.drop_constraint('fk_authorization_files_user_id','authorization_files','foreignkey')
    op.drop_constraint('fk_authorization_files_approved_by_id','authorization_files','foreignkey')
    op.drop_table('authorization_files')