"""empty message

Revision ID: 5f0065ba905c
Revises: d34fc0aacd6f
Create Date: 2017-12-31 07:40:20.173998

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5f0065ba905c'
down_revision = 'd34fc0aacd6f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('tags', sa.Column('tags', sa.String(length=200), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('tags', 'tags')
    # ### end Alembic commands ###