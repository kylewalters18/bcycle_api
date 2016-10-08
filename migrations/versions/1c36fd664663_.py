"""empty message

Revision ID: 1c36fd664663
Revises: 480293734eb3
Create Date: 2016-10-08 09:46:06.220593

"""

# revision identifiers, used by Alembic.
revision = '1c36fd664663'
down_revision = '480293734eb3'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('route',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('checkout_kiosk_id', sa.Integer(), nullable=True),
    sa.Column('return_kiosk_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['checkout_kiosk_id'], ['kiosk.id'], ),
    sa.ForeignKeyConstraint(['return_kiosk_id'], ['kiosk.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_column('kiosk', 'geocoded_name')
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('kiosk', sa.Column('geocoded_name', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.drop_table('route')
    ### end Alembic commands ###
