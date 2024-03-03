from hashlib import md5

from .Base import Base
from App.Core.database import db
from sqlalchemy import Column, String, JSON, Integer, Enum
import enum
import os
from glob import glob
from flask import current_app as app


class Category(Base, db.Model):
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    flag = Column(Integer, default=1)

    pass


def ActiveQuery():
    return Category.query.filter_by(flag=1)


def fetchOne(id):
    return Category.query.filter(Category.flag == 1, Category.id == id).first()


def assign(form):
    return Category(
        name=form['name'],
        flag=1
    )


def modify(model, form):
    for key, val in form.items():
        if hasattr(model, key):
            setattr(model, key, val)
