"""seed

Revision ID: 3caba3ee5902
Revises: c022343f46f8
Create Date: 2024-03-02 08:08:08.698757

"""
from alembic import op
import sqlalchemy as sa
import hashlib
import csv
import os

# revision identifiers, used by Alembic.
revision = '3caba3ee5902'
down_revision = '1ed213c6755d'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # get metadata from current connection
    meta = sa.MetaData(bind=op.get_bind())
    # pass in tuple with tables we want to reflect, otherwise whole database will get reflected
    meta.reflect(only=('users',))
    # define table representation
    User = sa.Table('users', meta)

    metaCategory = sa.MetaData(bind=op.get_bind())
    metaCategory.reflect(only=('categories',))
    Category = sa.Table('categories', metaCategory)

    metaDataset = sa.MetaData(bind=op.get_bind())
    metaDataset.reflect(only=('datasets',))
    Dataset = sa.Table('datasets', metaDataset)

    op.bulk_insert(User, [{
        'username': 'admin',
        'password': hashlib.md5('admin'.encode('utf-8')).hexdigest(),
        'role': 'ADMIN',
        'name': 'Administrator',
        'photo': 'admin.png',
        'flag': 1,
    }])

    data_category = []
    exist_category = []
    idx = 1
    with open(os.getcwd() + "/App/Sentiment/resources/clean_dataset.csv", 'r') as file:
        csvreader = csv.reader(file)
        header = next(csvreader)
        for row in csvreader:
            label = row[2]
            if label not in exist_category:
                exist_category.append(label)
                data_category.append({'id': idx, 'name': label, 'flag': 1})
                idx = idx + 1

    data_news = []
    with open(os.getcwd() + "/App/Sentiment/resources/clean_dataset.csv", 'r') as file:
        csvreader = csv.reader(file)
        header = next(csvreader)
        for row in csvreader:
            if row[3] not in exist_category:
                data_news.append(
                    {'flag': 1, 'Stem': row[3], 'kategoriId': [d['id'] for d in data_category if d.get('name') == row[2]][0]})

    op.bulk_insert(Category, data_category)
    op.bulk_insert(Dataset, data_news)
    pass


def downgrade() -> None:
    pass
