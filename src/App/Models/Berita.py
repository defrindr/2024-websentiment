from hashlib import md5

from .Base import Base
from App.Core.database import db
from sqlalchemy import Column, String, Integer, ForeignKey, Text
import enum
import os
from glob import glob
from flask import url_for, current_app as app


class Berita(Base, db.Model):
    __tablename__ = 'berita'

    id = Column(Integer, primary_key=True)
    judul = Column(String(255))
    kategori = Column(String(75))
    prediksi = Column(String(75))
    hasil = Column(String(10))
    data = Column(Text())
    isi = Column(Text())


pass


def ActiveQuery():
    return Berita.query


def fetchOne(id):
    return Berita.query.filter(Berita.id == id).first()


def destroy(id):
    return Berita.query.filter(Berita.id == id).delete()


def assign(form):
    return Berita(
        judul=form['judul'],
        kategori=form['kategori'],
        hasil=form['hasil'],
        isi=form['isi'],
        prediksi=form['prediksi'],
        data=form['data'],
    )
