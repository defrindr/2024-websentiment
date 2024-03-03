from hashlib import md5

from .Category import Category
from .Base import Base
from App.Core.database import db
from sqlalchemy import Column, String, Integer, ForeignKey, Text
import enum
import os
from glob import glob
from flask import current_app as app


class Dataset(Base, db.Model):
    __tablename__ = 'datasets'

    id = Column(Integer, primary_key=True)
    kategoriId = Column(Integer, ForeignKey('categories.id'))
    Stem = Column(String(255))
    flag = Column(Integer, default=1)

    kategori = db.relationship('Category', backref='dataset')
    pass


def ActiveQuery():
    return Dataset.query.join(Category).filter(Dataset.flag == 1, Category.flag == 1)


def fetchOne(id):
    return Dataset.query.join(Category).filter(Dataset.flag == 1, Category.flag == 1, Dataset.id == id).first()


def assign(form):
    return Dataset(
        Stem=form['Stem'],
        kategoriId=form['kategoriId'],
        flag=1
    )


def modify(model, form):
    for key, val in form.items():
        if hasattr(model, key):
            setattr(model, key, val)
