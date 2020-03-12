"""empty message

Revision ID: 2f5e5bdd789f
Revises: 665ecad3a46a
Create Date: 2019-11-03 11:11:58.251237

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2f5e5bdd789f'
down_revision = '665ecad3a46a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('datasets', sa.Column('dsOrms', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('datasets', 'dsOrms')
    # ### end Alembic commands ###