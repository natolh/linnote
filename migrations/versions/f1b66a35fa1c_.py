"""empty message

Revision ID: f1b66a35fa1c
Revises: 8f1f81f73632
Create Date: 2018-07-26 16:53:04.609232

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f1b66a35fa1c'
down_revision = '8f1f81f73632'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('profiles__students', sa.Column('aid', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('profiles__students', 'aid')
    # ### end Alembic commands ###
