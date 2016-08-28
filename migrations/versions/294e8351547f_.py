"""empty message

Revision ID: 294e8351547f
Revises: 5671ba3875e8
Create Date: 2016-08-27 20:28:24.802880

"""

# revision identifiers, used by Alembic.
revision = '294e8351547f'
down_revision = '5671ba3875e8'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('tags',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=20), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('posts_tags',
    sa.Column('post_id', sa.Integer(), nullable=False),
    sa.Column('tag_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['post_id'], ['posts.id'], ),
    sa.ForeignKeyConstraint(['tag_id'], ['tags.id'], )
    )
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('posts_tags')
    op.drop_table('tags')
    ### end Alembic commands ###