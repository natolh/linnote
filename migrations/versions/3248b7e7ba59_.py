"""empty message

Revision ID: 3248b7e7ba59
Revises: f44c3d800b7a
Create Date: 2018-04-21 16:13:31.293485

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3248b7e7ba59'
down_revision = 'f44c3d800b7a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_assessments_title', table_name='assessments')
    op.create_index(op.f('ix_assessments_title'), 'assessments', ['title'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_assessments_title'), table_name='assessments')
    op.create_index('ix_assessments_title', 'assessments', ['title'], unique=True)
    # ### end Alembic commands ###
