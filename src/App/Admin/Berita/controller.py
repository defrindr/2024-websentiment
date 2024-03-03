from flask import render_template, request, flash, redirect, url_for, jsonify
from App.Auth.auth_session import loggedInUser
from App.Core.database import db
import App.Models.News as NewsInstance
import App.Models.Category as CategoryInstance
import App.Models.Dataset as DatasetInstance
from sqlalchemy import or_
from App.Utils.Validator import Validator
from App.Core.sentiment import app_sentiment

module = "admin.berita"
viewLayout = 'Admin/Berita/'


def index():
    title = "Daftar Berita"

    headers = ['No', 'Kategori', 'Judul', 'Aksi']

    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    search = request.args.get('search', '', type=str)
    category = request.args.get('category', '', type=str)

    baseQuery = NewsInstance.ActiveQuery()

    if (category) != '':
        baseQuery = baseQuery.filter(
            NewsInstance.News.kategoriId == category
        )

    if search != '':
        baseQuery = baseQuery.filter(
            or_(
                NewsInstance.News.judul.like(f"%{search}%"),
                CategoryInstance.Category.name.like(f"%{search}%")
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
    categories = CategoryInstance.ActiveQuery().all()

    return render_template(
        viewLayout + 'create.html',
        title=title,
        module=module,
        categories=categories
    )


def store():
    # validation
    required_fields = ['judul', 'isi', 'kategoriId']
    form = request.form.to_dict()

    app_validator = Validator()
    app_validator.required(form, required_fields)
    if len(app_validator.errors) > 0:
        return app_validator.flashMessage().redirect(f'{module}.create')

    # save model
    model = NewsInstance.assign(form=form)

    # commit
    db.session.add(model)
    db.session.commit()

    flash('Data telah ditambahkan', 'info')
    return redirect(url_for(f'{module}.index'))

    return
    pass


def edit(id):
    title = "Edit Berita"
    model = NewsInstance.fetchOne(id)
    categories = CategoryInstance.ActiveQuery().all()
    return render_template(
        viewLayout + 'edit.html',
        title=title,
        module=module,
        model=model,
        categories=categories
    )


def update(id):
    model = NewsInstance.fetchOne(id)

    # validation
    required_fields = ['judul', 'isi', 'kategoriId']
    form = request.form.to_dict()

    app_validator = Validator()
    app_validator.required(form, required_fields)
    if len(app_validator.errors) > 0:
        return app_validator.flashMessage().redirect(f'{module}.create')

    NewsInstance.modify(model, form)

    db.session.commit()
    flash('Data berhasil diubah', 'info')
    return redirect(url_for(f'{module}.index'))
    pass


def destroy(id):
    model = NewsInstance.fetchOne(id)
    model.flag = 0
    db.session.commit()
    flash('Data berhasil dihapus', 'info')
    return redirect(url_for(f'{module}.index'))
    pass


def nb():
    judul = request.args.get('judul', '', type=str)

    prediction = app_sentiment.predict(judul)

    return jsonify({'text': judul, 'category': int(prediction)})
