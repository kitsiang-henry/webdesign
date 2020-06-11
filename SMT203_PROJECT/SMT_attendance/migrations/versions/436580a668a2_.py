"""empty message

Revision ID: 436580a668a2
Revises: 53209d7dcb59
Create Date: 2020-04-03 13:19:43.237106

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '436580a668a2'
down_revision = '53209d7dcb59'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('student_attendance', sa.Column('timestamp', sa.DateTime(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('student_attendance', 'timestamp')
    # ### end Alembic commands ###