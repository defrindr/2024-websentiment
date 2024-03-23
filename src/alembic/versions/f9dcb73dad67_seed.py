"""seed

Revision ID: f9dcb73dad67
Revises: 73be1b0e2255
Create Date: 2024-03-22 22:21:14.335363

"""
from alembic import op
import sqlalchemy as sa
import hashlib


# revision identifiers, used by Alembic.
revision = 'f9dcb73dad67'
down_revision = '73be1b0e2255'
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
