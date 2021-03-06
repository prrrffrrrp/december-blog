"""empty message

Revision ID: 670c9982c603
Revises: 36729fb869bd
Create Date: 2017-12-30 08:01:53.189010

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '670c9982c603'
down_revision = '36729fb869bd'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('tags',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('tag', sa.String(length=200), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('post_tags',
    sa.Column('tag_id', sa.Integer(), nullable=False),
    sa.Column('post_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['post_id'], ['posts.id'], ),
    sa.ForeignKeyConstraint(['tag_id'], ['tags.id'], ),
    sa.PrimaryKeyConstraint('tag_id', 'post_id')
    )
    op.drop_column('posts', 'tags')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('posts', sa.Column('tags', sa.VARCHAR(length=128), autoincrement=False, nullable=True))
    op.drop_table('post_tags')
    op.drop_table('tags')
    # ### end Alembic commands ###
