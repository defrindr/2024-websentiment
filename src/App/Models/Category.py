from hashlib import md5

from .Base import Base
from App.Core.database import db
from sqlalchemy import Column, String, JSON, Integer, Enum
import enum
import os
from glob import glob
from flask import current_app as app

class Category(Base,db.Model):
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    flag = Column(Integer, default=1)

    pass