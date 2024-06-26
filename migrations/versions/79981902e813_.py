"""empty message

Revision ID: 79981902e813
Revises: 
Create Date: 2024-05-29 15:32:16.090043

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '79981902e813'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('doctor', schema=None) as batch_op:
        batch_op.alter_column('created_on',
               existing_type=sa.DATETIME(),
               nullable=False)
        batch_op.alter_column('update_on',
               existing_type=sa.DATETIME(),
               nullable=False)

    with op.batch_alter_table('procedure', schema=None) as batch_op:
        batch_op.alter_column('created_on',
               existing_type=sa.DATETIME(),
               nullable=False)
        batch_op.alter_column('update_on',
               existing_type=sa.DATETIME(),
               nullable=False)

    with op.batch_alter_table('procedure_type', schema=None) as batch_op:
        batch_op.alter_column('created_on',
               existing_type=sa.DATETIME(),
               nullable=False)
        batch_op.alter_column('update_on',
               existing_type=sa.DATETIME(),
               nullable=False)

    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.alter_column('created_on',
               existing_type=sa.DATETIME(),
               nullable=False)
        batch_op.alter_column('update_on',
               existing_type=sa.DATETIME(),
               nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.alter_column('update_on',
               existing_type=sa.DATETIME(),
               nullable=True)
        batch_op.alter_column('created_on',
               existing_type=sa.DATETIME(),
               nullable=True)

    with op.batch_alter_table('procedure_type', schema=None) as batch_op:
        batch_op.alter_column('update_on',
               existing_type=sa.DATETIME(),
               nullable=True)
        batch_op.alter_column('created_on',
               existing_type=sa.DATETIME(),
               nullable=True)

    with op.batch_alter_table('procedure', schema=None) as batch_op:
        batch_op.alter_column('update_on',
               existing_type=sa.DATETIME(),
               nullable=True)
        batch_op.alter_column('created_on',
               existing_type=sa.DATETIME(),
               nullable=True)

    with op.batch_alter_table('doctor', schema=None) as batch_op:
        batch_op.alter_column('update_on',
               existing_type=sa.DATETIME(),
               nullable=True)
        batch_op.alter_column('created_on',
               existing_type=sa.DATETIME(),
               nullable=True)

    # ### end Alembic commands ###
