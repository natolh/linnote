"""empty message

Revision ID: eec26b900152
Revises: f1b66a35fa1c
Create Date: 2018-07-26 19:27:06.993921

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'eec26b900152'
down_revision = 'f1b66a35fa1c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users_groups',
    sa.Column('group', sa.Integer(), nullable=True),
    sa.Column('user', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['group'], ['groups.identifier'], ),
    sa.ForeignKeyConstraint(['user'], ['users.identifier'], )
    )
    op.drop_table('students_groups')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('students_groups',
    sa.Column('group', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True),
    sa.Column('student', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['group'], ['groups.identifier'], name='students_groups_ibfk_1'),
    sa.ForeignKeyConstraint(['student'], ['profiles__students.identifier'], name='students_groups_ibfk_2'),
    mysql_default_charset='utf8',
    mysql_engine='InnoDB'
    )
    op.drop_table('users_groups')
    # ### end Alembic commands ###