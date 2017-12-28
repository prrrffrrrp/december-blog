"""empty message

Revision ID: 1f3f236fa8aa
Revises: 30cdc559fbd3
Create Date: 2017-12-27 07:00:12.322557

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1f3f236fa8aa'
down_revision = '30cdc559fbd3'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('posts', 'subtitle')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('posts', sa.Column('subtitle', sa.TEXT(), autoincrement=False, nullable=False))
    # ### end Alembic commands ###