from hashlib import md5

from .Category import Category
from .Base import Base
from App.Core.database import db
from sqlalchemy import Column, String, Integer, ForeignKey, Text
import enum
import os
from glob import glob
from flask import current_app as app


class News(Base, db.Model):
    __tablename__ = 'news'

    id = Column(Integer, primary_key=True)
    kategoriId = Column(Integer, ForeignKey('categories.id'))
    judul = Column(String(255))
    isi = Column(Text())
    flag = Column(Integer, default=1)

    kategori = db.relationship('Category', backref='news')
    pass


def ActiveQuery():
    return News.query.join(Category).filter(News.flag == 1, Category.flag == 1)


def fetchOne(id):
    return News.query.join(Category).filter(News.flag == 1, Category.flag == 1, News.id == id).first()


def assign(form):
    return News(
        judul=form['judul'],
        isi=form['isi'],
        kategoriId=form['kategoriId'],
        flag=1
    )


def modify(model, form):
    for key, val in form.items():
        if hasattr(model, key):
            setattr(model, key, val)
