"""include full_name

Revision ID: 2a56df5f1a29
Revises: 7308e51665cf
Create Date: 2021-07-08 12:46:09.499671

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2a56df5f1a29'
down_revision = '7308e51665cf'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('disposable_bookings', sa.Column('full_name', sa.String(length=255), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('disposable_bookings', 'full_name')
    # ### end Alembic commands ###
