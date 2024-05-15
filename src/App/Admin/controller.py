from flask import render_template
from App.Auth.auth_session import loggedInUser
import App.Models.Uploader as UploaderInstance
import App.Models.Berita as BeritaInstance


def index():
    total_benar = 0
    total_salah = 0
    total_data = 0

    data_source = UploaderInstance.ActiveQuery().all()
    for data in data_source:
        total_data += data.total_data
        total_benar += data.total_benar
        total_salah += data.total_data - data.total_benar

    data_single_source = BeritaInstance.ActiveQuery().all()
    for data in data_single_source:
        total_data += 1
        if data.hasil == 'True':
            total_benar += 1
        else:
            total_salah += 1

    return render_template('index.html', total_benar=total_benar, total_salah=total_salah, total_data=total_data)
