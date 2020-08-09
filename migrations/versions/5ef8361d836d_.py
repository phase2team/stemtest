"""empty message

Revision ID: 5ef8361d836d
Revises: 9b5bc20d0835
Create Date: 2020-08-09 10:20:42.678245

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5ef8361d836d'
down_revision = '9b5bc20d0835'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('Parents',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('chattStateANumber', sa.String(length=20), nullable=False),
    sa.Column('guardianship', sa.String(length=50), nullable=True),
    sa.Column('motherName', sa.String(length=50), nullable=True),
    sa.Column('motherEmail', sa.String(length=50), nullable=True),
    sa.Column('motherHomePhone', sa.String(length=50), nullable=True),
    sa.Column('motherDayPhone', sa.String(length=50), nullable=True),
    sa.Column('fatherName', sa.String(length=50), nullable=True),
    sa.Column('fatherEmail', sa.String(length=50), nullable=True),
    sa.Column('fatherHomePhone', sa.String(length=50), nullable=True),
    sa.Column('fatherDayPhone', sa.String(length=50), nullable=True),
    sa.Column('guardianEmail', sa.String(length=50), nullable=True),
    sa.ForeignKeyConstraint(['chattStateANumber'], ['Student.chattStateANumber'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('Parents')
    # ### end Alembic commands ###