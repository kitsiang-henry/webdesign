"""empty message

Revision ID: f1a0a68e1a99
Revises: 436580a668a2
Create Date: 2020-04-05 18:13:35.015257

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f1a0a68e1a99'
down_revision = '436580a668a2'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('class_photos', sa.Column('timestamp', sa.DateTime(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('class_photos', 'timestamp')
    # ### end Alembic commands ###
