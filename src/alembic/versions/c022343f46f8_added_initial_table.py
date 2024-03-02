"""Added initial table

Revision ID: c022343f46f8
Revises: 
Create Date: 2024-03-01 11:38:50.432933

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c022343f46f8'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('categories',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=True),
    sa.Column('flag', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=255), nullable=True),
    sa.Column('password', sa.String(length=255), nullable=True),
    sa.Column('role', sa.Enum('ADMIN', name='role'), nullable=True),
    sa.Column('name', sa.String(length=255), nullable=True),
    sa.Column('photo', sa.String(length=255), nullable=True),
    sa.Column('flag', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('username')
    )
    op.create_table('news',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('kategoriId', sa.Integer(), nullable=True),
    sa.Column('judul', sa.String(length=255), nullable=True),
    sa.Column('isi', sa.Text(), nullable=True),
    sa.Column('flag', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['kategoriId'], ['categories.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('news')
    op.drop_table('users')
    op.drop_table('categories')
    # ### end Alembic commands ###
