"""extra listing fields

Revision ID: a66ff1c2e278
Revises: 5cdd1ad97217
Create Date: 2022-10-31 17:31:50.596179

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a66ff1c2e278'
down_revision = '5cdd1ad97217'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("listings",sa.Column("address",sa.String,nullable=True))
    op.add_column("listings",sa.Column("city",sa.String,nullable=True))
    op.add_column("listings",sa.Column("state",sa.String,nullable=True))
    op.add_column("listings",sa.Column("zip_code",sa.String,nullable=True))
    op.drop_column("listings","title")
    op.drop_column("listings","city_province")
    op.execute("UPDATE listings SET address='N/A'")
    op.execute("UPDATE listings SET city='N/A'")
    op.execute("UPDATE listings SET state='N/A'")
    op.execute("UPDATE listings SET zip_code='N/A'")
    op.alter_column("listings","address",nullable=False,default="N/A")
    op.alter_column("listings","city",nullable=False,default="N/A")
    op.alter_column("listings","state",nullable=False,default="N/A")
    op.alter_column("listings","zip_code",nullable=False,default="N/A")


def downgrade():
    op.add_column("listings",sa.Column("title",sa.String,nullable=True))
    op.add_column("listings",sa.Column("city_province",sa.String,nullable=True))
    op.execute("UPDATE listings SET title='N/A'")
    op.alter_column("listings","title",nullable=False,default="N/A")
    op.drop_column("listings","address")
    op.drop_column("listings","city")
    op.drop_column("listings","state")
    op.drop_column("listings","zip_code")
