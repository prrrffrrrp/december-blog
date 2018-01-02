"""empty message

Revision ID: d34fc0aacd6f
Revises: d93c1ebbb74f
Create Date: 2017-12-30 08:20:19.592943

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd34fc0aacd6f'
down_revision = 'd93c1ebbb74f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('tags', 'tags')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('tags', sa.Column('tags', sa.VARCHAR(length=200), autoincrement=False, nullable=True))
    # ### end Alembic commands ###