"""timezone aware

Revision ID: d768e9412dcd
Revises: 3380bd9eba54
Create Date: 2022-09-27 17:46:07.158024

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd768e9412dcd'
down_revision = '3380bd9eba54'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # users
    op.alter_column("users","created",sa.DateTime(timezone=True))
    op.alter_column("users","last_seen",sa.DateTime(timezone=True))
    op.alter_column("users","password_created",sa.DateTime(timezone=True))
    op.alter_column("users","email_validation_token_created",sa.DateTime(timezone=True))
    op.alter_column("users","authorized_time",sa.DateTime(timezone=True))

    # listings
    op.alter_column("listings","created",sa.DateTime(timezone=True))
    op.alter_column("listings","last_updated",sa.DateTime(timezone=True))
    
    # images
    op.alter_column("images","created",sa.DateTime(timezone=True))
    op.alter_column("images","last_updated",sa.DateTime(timezone=True))
    
    # bids
    op.alter_column("bids","created",sa.DateTime(timezone=True))
    op.alter_column("bids","last_updated",sa.DateTime(timezone=True))


    
def downgrade() -> None:
    # users
    op.alter_column("users","created",sa.DateTime(timezone=False))
    op.alter_column("users","last_seen",sa.DateTime(timezone=False))
    op.alter_column("users","password_created",sa.DateTime(timezone=False))
    op.alter_column("users","email_validation_token_created",sa.DateTime(timezone=False))
    op.alter_column("users","authorized_time",sa.DateTime(timezone=False))

    # listings
    op.alter_column("listings","created",sa.DateTime(timezone=False))
    op.alter_column("listings","last_updated",sa.DateTime(timezone=False))
    
    # images
    op.alter_column("images","created",sa.DateTime(timezone=False))
    op.alter_column("images","last_updated",sa.DateTime(timezone=False))
    
    # bids
    op.alter_column("bids","created",sa.DateTime(timezone=False))
    op.alter_column("bids","last_updated",sa.DateTime(timezone=False))
