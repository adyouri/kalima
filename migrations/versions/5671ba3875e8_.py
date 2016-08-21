"""empty message

Revision ID: 5671ba3875e8
Revises: 2a914a1c6550
Create Date: 2016-08-20 19:17:22.740481

"""

# revision identifiers, used by Alembic.
revision = '5671ba3875e8'
down_revision = '2a914a1c6550'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('comments', sa.Column('created_date', sa.DateTime(), nullable=True))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('comments', 'created_date')
    ### end Alembic commands ###