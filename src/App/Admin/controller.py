from flask import render_template
from App.Auth.auth_session import loggedInUser
from App.Models.Berita import Berita
from App.Models.Uploader import Uploader
import App.Models.Uploader as UploaderInstance
import App.Models.Berita as BeritaInstance
from App.Auth.auth_session import SESS_AUTH_ID, getSessionAuth


def index():
    total_benar = 0
    total_salah = 0
    total_data = 0

    session = getSessionAuth()
    userId = session[SESS_AUTH_ID]

    q1 = UploaderInstance.ActiveQuery()
    q2 = BeritaInstance.ActiveQuery()
    if userId != 1:
        q1 = q1.filter(Uploader.user_id == userId)
        q2 = q2.filter(Berita.user_id == userId)

    data_source = q1.all()
    for data in data_source:
        total_data += data.total_data
        total_benar += data.total_benar
        total_salah += data.total_data - data.total_benar

    data_single_source = q2.all()
    for data in data_single_source:
        total_data += 1
        if data.hasil == 'True':
            total_benar += 1
        else:
            total_salah += 1

    return render_template('index.html', total_benar=total_benar, total_salah=total_salah, total_data=total_data)
