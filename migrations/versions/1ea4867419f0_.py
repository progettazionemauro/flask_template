"""empty message

Revision ID: 1ea4867419f0
Revises: d45565a69d00
Create Date: 2023-08-04 16:20:14.644458

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1ea4867419f0'
down_revision = 'd45565a69d00'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('new_user_registration',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=80), nullable=False),
    sa.Column('password_hash', sa.String(length=120), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('username')
    )
    op.drop_table('user_registration')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user_registration',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('password_hash', sa.VARCHAR(length=120), nullable=False),
    sa.Column('username', sa.VARCHAR(length=80), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('username')
    )
    op.drop_table('new_user_registration')
    # ### end Alembic commands ###
