"""empty message

Revision ID: fdb14687da3f
Revises: 
Create Date: 2021-04-05 01:45:07.795872

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fdb14687da3f'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('email', sa.String(length=120), nullable=True))
    op.add_column('user', sa.Column('password_hash', sa.String(length=128), nullable=True))
    op.add_column('user', sa.Column('username', sa.String(length=64), nullable=True))
    op.create_index(op.f('ix_user_email'), 'user', ['email'], unique=False)
    op.create_index(op.f('ix_user_username'), 'user', ['username'], unique=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_user_username'), table_name='user')
    op.drop_index(op.f('ix_user_email'), table_name='user')
    op.drop_column('user', 'username')
    op.drop_column('user', 'password_hash')
    op.drop_column('user', 'email')
    # ### end Alembic commands ###
