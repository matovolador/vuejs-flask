"""initial admins

Revision ID: 56be1142cdcd
Revises: 023df10b5c95
Create Date: 2022-11-14 18:27:39.572527

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '56be1142cdcd'
down_revision = '023df10b5c95'
branch_labels = None
depends_on = None


def upgrade():
    op.execute("INSERT INTO users (email,password,first_name,last_name,email_validated,type,authorized) VALUES ('matias.garafoni@gmail.com','12354o9214jwdfjlsd-135!!&','Matias','Garafoni',TRUE,99,TRUE)")


def downgrade():
    op.execute("DELETE FROM users WHERE email='matias.garafoni@gmail.com'")
