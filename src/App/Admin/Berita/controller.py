from flask import render_template, request, flash, redirect, url_for, send_from_directory
from App.Auth.auth_session import loggedInUser
from App.Core.database import db
import App.Models.Berita as BeritaInstance
from sqlalchemy import or_
from flask import current_app as app
from App.Utils.Validator import Validator
import os
from werkzeug.utils import secure_filename
import time
import json
from App.Core.sentiment import app_sentiment

module = "admin.berita"
viewLayout = 'Admin/Berita/'

ALLOWED_EXTENSIONS = {'csv'}


def index():
    title = "Single Klasifikasi"

    # 'Case Folding', 'Filtering', 'Hapus Stopword', 'Tokenisasi', 'Stem', 'TFIDF',
    headers = ['No', 'Kategori', 'Judul', 'Prediksi', 'Hasil', 'Aksi']

    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    search = request.args.get('search', '', type=str)

    baseQuery = BeritaInstance.ActiveQuery()

    if search != '':
        baseQuery = baseQuery.filter(
            or_(
                BeritaInstance.Berita.judul.like(f"%{search}%"),
                BeritaInstance.Berita.kategori.like(f"%{search}%"),
                BeritaInstance.Berita.prediksi.like(f"%{search}%"),
                BeritaInstance.Berita.hasil.like(f"%{search}%"),
            )
        )
        pass

    total_data = baseQuery.count()
    pagination = baseQuery.paginate(page=page, per_page=per_page)
    start_data = page * per_page - per_page
    len_items = len(pagination.items)

    return render_template(
        viewLayout + 'index.html',
        title=title,
        module=module,
        pagination=pagination,
        len_items=len_items,
        headers=headers,
        start_data=start_data,
        per_page=per_page,
        total_data=total_data,
        search=search
    )


def create():
    title = "Tambah Berita Baru"
    return render_template(
        viewLayout + 'create.html',
        title=title,
        module=module
    )


def store():
    kategori = request.form.get('kategori')
    judul = request.form.get('judul')
    if kategori is None or judul is None:
        flash('Gagal', 'danger')
        return redirect(url_for(f'{module}.create'))
    predict = app_sentiment.singlePredict(judul, kategori)
    print(predict)
    form = {}
    form['judul'] = judul
    form['kategori'] = kategori
    form['prediksi'] = predict['Prediksi']
    form['hasil'] = 'True' if predict['Hasil'] == True else 'False'
    form['data'] = json.dumps(predict)

    # save model
    model = BeritaInstance.assign(form=form)

    # commit
    db.session.add(model)
    db.session.commit()
    flash('Data telah ditambahkan', 'info')
    return redirect(url_for(f'{module}.index'))
    pass


def edit(id):
    title = "Edit Kategori"
    model = BeritaInstance.fetchOne(id)
    return render_template(
        viewLayout + 'edit.html',
        title=title,
        module=module,
        model=model
    )


def update(id):
    model = BeritaInstance.fetchOne(id)

    # validation
    required_fields = ['name']
    form = request.form.to_dict()

    app_validator = Validator()
    app_validator.required(form, required_fields)
    if len(app_validator.errors) > 0:
        return app_validator.flashMessage().redirect(f'{module}.create')

    BeritaInstance.modify(model, form)

    db.session.commit()
    flash('Data berhasil diubah', 'info')
    return redirect(url_for(f'{module}.index'))
    pass


def destroy(id):
    BeritaInstance.destroy(id)
    db.session.commit()
    flash('Data berhasil dihapus', 'info')
    return redirect(url_for(f'{module}.index'))
    pass
