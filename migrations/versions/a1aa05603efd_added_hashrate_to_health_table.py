"""added hashrate to health table

Revision ID: a1aa05603efd
Revises: c4fb73a3f4d5
Create Date: 2021-06-14 20:19:50.286272

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a1aa05603efd'
down_revision = 'c4fb73a3f4d5'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('health', sa.Column('hashrate', sa.Float(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('health', 'hashrate')
    # ### end Alembic commands ###