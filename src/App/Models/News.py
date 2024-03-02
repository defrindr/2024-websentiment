from hashlib import md5

from .Base import Base
from App.Core.database import db
from sqlalchemy import Column, String, Integer, ForeignKey, Text
import enum
import os
from glob import glob
from flask import current_app as app

class News(Base,db.Model):
    __tablename__ = 'news'

    id = Column(Integer, primary_key=True)
    kategoriId = Column(Integer, ForeignKey('categories.id'))
    judul = Column(String(255))
    isi = Column(Text())
    flag = Column(Integer, default=1)
    pass