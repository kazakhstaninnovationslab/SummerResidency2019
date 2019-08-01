"""empty message

Revision ID: 7f1de97838ca
Revises: 9325aa369e3c
Create Date: 2019-07-25 14:03:46.708122

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7f1de97838ca'
down_revision = '9325aa369e3c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('medicine', sa.Column('stage_id', sa.Integer(), nullable=True))
    op.drop_constraint('medicine_disease_id_fkey', 'medicine', type_='foreignkey')
    op.create_foreign_key(None, 'medicine', 'stage', ['stage_id'], ['id'])
    op.drop_column('medicine', 'disease_id')
    op.alter_column('stage', 'disease_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('stage', 'disease_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.add_column('medicine', sa.Column('disease_id', sa.INTEGER(), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'medicine', type_='foreignkey')
    op.create_foreign_key('medicine_disease_id_fkey', 'medicine', 'disease', ['disease_id'], ['id'])
    op.drop_column('medicine', 'stage_id')
    # ### end Alembic commands ###