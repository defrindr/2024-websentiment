"""seed

Revision ID: 3caba3ee5902
Revises: c022343f46f8
Create Date: 2024-03-02 08:08:08.698757

"""
from alembic import op
import sqlalchemy as sa
import hashlib

# revision identifiers, used by Alembic.
revision = '3caba3ee5902'
down_revision = 'c022343f46f8'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # get metadata from current connection
    meta = sa.MetaData(bind=op.get_bind())
    # pass in tuple with tables we want to reflect, otherwise whole database will get reflected
    meta.reflect(only=('users',))
    # define table representation
    User = sa.Table('users', meta)

    op.bulk_insert(User, [{
        'username': 'admin',
        'password': hashlib.md5('admin'.encode('utf-8')).hexdigest(),
        'role': 'ADMIN',
        'name': 'Administrator',
        'photo': 'admin.png',
        'flag': 1,
    }])
    pass


def downgrade() -> None:
    pass
