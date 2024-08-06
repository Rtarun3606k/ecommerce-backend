"""added some coluums country and raTINGs in seller and product

Revision ID: adf5040a6752
Revises: 
Create Date: 2024-07-17 19:25:38.877653

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'adf5040a6752'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('product', schema=None) as batch_op:
        batch_op.add_column(sa.Column('rating', sa.Integer(), nullable=True))

    with op.batch_alter_table('seller', schema=None) as batch_op:
        batch_op.add_column(sa.Column('country', sa.String(length=80), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('seller', schema=None) as batch_op:
        batch_op.drop_column('country')

    with op.batch_alter_table('product', schema=None) as batch_op:
        batch_op.drop_column('rating')

    # ### end Alembic commands ###