from flask import render_template, request, flash, redirect, url_for
from App.Auth.auth_session import loggedInUser
from App.Core.database import db
import App.Models.Category as CategoryInstance
from sqlalchemy import or_
from App.Utils.Validator import Validator

module = "admin.category"
viewLayout = 'Admin/Category/'


def index():
    title = "Daftar Kategori"

    headers = ['No', 'Nama Kategori', 'Aksi']

    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    search = request.args.get('search', '', type=str)

    baseQuery = CategoryInstance.ActiveQuery()

    if search != '':
        baseQuery = baseQuery.filter(
            CategoryInstance.Category.name.like(f"%{search}%")
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


def show():
    pass


def create():
    title = "Tambah Kategori Baru"
    return render_template(
        viewLayout + 'create.html',
        title=title,
        module=module
    )


def store():
    # validation
    required_fields = ['name']
    form = request.form.to_dict()

    app_validator = Validator()
    app_validator.required(form, required_fields)
    if len(app_validator.errors) > 0:
        return app_validator.flashMessage().redirect(f'{module}.create')

    # save model
    model = CategoryInstance.assign(form=form)

    # commit
    db.session.add(model)
    db.session.commit()

    flash('Data telah ditambahkan', 'info')
    return redirect(url_for(f'{module}.index'))

    return
    pass


def edit(id):
    title = "Edit Kategori"
    model = CategoryInstance.fetchOne(id)
    return render_template(
        viewLayout + 'edit.html',
        title=title,
        module=module,
        model=model
    )


def update(id):
    model = CategoryInstance.fetchOne(id)

    # validation
    required_fields = ['name']
    form = request.form.to_dict()

    app_validator = Validator()
    app_validator.required(form, required_fields)
    if len(app_validator.errors) > 0:
        return app_validator.flashMessage().redirect(f'{module}.create')

    CategoryInstance.modify(model, form)

    db.session.commit()
    flash('Data berhasil diubah', 'info')
    return redirect(url_for(f'{module}.index'))
    pass


def destroy(id):
    model = CategoryInstance.fetchOne(id)
    model.flag = 0
    db.session.commit()
    flash('Data berhasil dihapus', 'info')
    return redirect(url_for(f'{module}.index'))
    pass
