import io
import os
from tempfile import TemporaryDirectory
from flask import jsonify, render_template, request, url_for, flash, redirect
from sqlalchemy import or_

from App.Models.User import Role, User, _baseQueryAdmin, _fetchById, _fetchByUsername, _hashPassword
from hashlib import md5
from App.Core.database import db
from flask import current_app as app

module = "admin.admin"
template = 'Admin/Admin/'


def index():

    title = "Management Admin"
    headers = ['No', 'Username', 'Name', 'Aksi']

    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    search = request.args.get('search', '', type=str)

    baseQuery = _baseQueryAdmin()

    if search != '':
        baseQuery = baseQuery.filter(
            or_(
                User.username.like(f"%{search}%"),
                User.name.like(f"%{search}%")
            )
        )
        pass

    total_data = baseQuery.count()
    pagination = baseQuery.paginate(page=page, per_page=per_page)
    start_data = page * per_page - per_page
    len_items = len(pagination.items)
    return render_template(template + 'index.html', pagination=pagination, len_items=len_items, headers=headers, title=title, module=module, start_data=start_data, per_page=per_page, total_data=total_data, search=search)


def create():
    title = "Tambah Admin"
    return render_template(template + 'create.html', title=title, module=module)


def store():
    # validation
    required_fields = ['nim', 'name', 'password']
    form = request.form.to_dict()
    file = request.files['photo']
    for field in required_fields:
        if (form[field] is None):
            flash('Terjadi kesalahan saat menambahkan data', 'danger')
            return redirect(url_for(f'{module}.create'))

    # check if duplicate
    exist = _fetchByUsername(form['nim'])
    if exist is not None:
        flash('Data telah ditambahkan sebelumnya', 'danger')
        return redirect(url_for(f'{module}.create'))

    if (file):
        path = app.root_path + "/static/profiles/"
        form['photo'] = form['nim'] + ".png"
        if os.path.exists(path) == False:
            os.makedirs(path)
        file.save(path + form['nim'])
    else:
        flash('Foto tidak boleh kosong', 'danger')
        return redirect(url_for(f'{module}.create'))

    # save model
    model = User(
        username=form['nim'],
        name=form['name'],
        photo=form['photo'],
        role=Role.ADMIN,
        password=_hashPassword(form['password']),
        flag=1
    )

    # commit
    db.session.add(model)
    db.session.commit()

    flash('Data telah ditambahkan', 'info')
    return redirect(url_for(f'{module}.index'))


def edit(id):
    title = "Edit Admin"
    model = _fetchById(id)
    return render_template(template + 'edit.html', title=title, module=module, model=model)


def update(id):
    form = request.form
    form_keys = form.keys()
    file = request.files['photo']
    model = _fetchById(id)
    if "nim" in form_keys:
        model.username = form['nim']
    if "name" in form_keys:
        model.name = form['name']
    if "password" in form_keys and form['password']:
        model.password = _hashPassword(form['password'])
    if file:
        path = app.root_path + "/static/profiles/"
        model.photo = model.username + ".png"
        if os.path.exists(path) == False:
            os.makedirs(path)
        file.save(path + model.photo)

    db.session.commit()
    flash('Data berhasil diubah', 'info')
    return redirect(url_for(f'{module}.index'))


def destroy(id):
    model = _fetchById(id)
    if model.id == 1:
        flash('Tidak dapat menghapus Admin Utama', 'danger')
        return redirect(url_for(f'{module}.index'))
    model.flag = 0
    db.session.commit()
    flash('Data berhasil diubah', 'info')
    return redirect(url_for(f'{module}.index'))
