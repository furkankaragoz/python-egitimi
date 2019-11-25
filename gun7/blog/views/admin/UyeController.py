from flask import Blueprint, render_template, session, redirect,request,flash,url_for
from gun7.blog.utils.Db import Db
from werkzeug.utils import secure_filename
from flask import Flask
import hashlib
import os



YUKLEME_KLASORU = 'static/yuklemeler'
UZANTILAR = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = YUKLEME_KLASORU
app.secret_key = "Flask_Dosya_Yukleme_Ornegi"


def uzanti_kontrol(dosyaadi):
   return '.' in dosyaadi and \
   dosyaadi.rsplit('.', 1)[1].lower() in UZANTILAR







uyeler = Blueprint('uyeler',
                   __name__,
                   url_prefix="/admin/uye")

@uyeler.route("/index")
def index():
    databse = Db()
    sql = """ select * from "User" """
    data = databse.read_data(sql);

    return render_template("admin/uye/index.html",data=data)


@uyeler.route('/ekle', defaults={'id': None})
@uyeler.route('/ekle/<string:id>')
def ekle(id):

    if id is not None:
        databse = Db()
        sql = """ select * from "User" where "Id" = %s """
        data = databse.read_first_data(sql,(id,))
        print(data)

        return render_template("admin/uye/ekle.html",data=data)

    return render_template("admin/uye/ekle.html",data=None)


@uyeler.route('/save',methods=["POST"])
def save():
    fullName = request.form.get("FullName")
    id = request.form.get("Id")
    email = request.form.get("Email")
    password = request.form.get("Password")


    database = Db()

    # formdan dosya gelip gelmediğini kontrol edelim
    if 'dosya' not in request.files:
        flash('Dosya seçilmedi')
        return redirect('dosyayukleme')

        # kullanıcı dosya seçmemiş ve tarayıcı boş isim göndermiş mi
    dosya = request.files['dosya']
    if dosya.filename == '':
        flash('Dosya seçilmedi')
        return redirect('dosyayukleme')

    # gelen dosyayı güvenlik önlemlerinden geçir
    if dosya and uzanti_kontrol(dosya.filename):
        dosyaadi = secure_filename(dosya.filename)
        print(dosyaadi)
        dosya.save(os.path.join(app.config['UPLOAD_FOLDER'], dosyaadi))
        print(os.path.join(app.config['UPLOAD_FOLDER'], dosyaadi))
        databaseImage = os.path.join(app.config['UPLOAD_FOLDER'], dosyaadi)

        # return redirect(url_for('dosyayukleme',dosya=dosyaadi))
    else:
        flash('İzin verilmeyen dosya uzantısı')
        return redirect('dosyayukleme')



    sql  = ""
    if id is None:
        sql = """ insert into "User" ("Email","Password","FullName","Image") values (%s,%s,%s,%s) """
        sifre_hash = hashlib.md5(password.encode()).hexdigest()
        database.execute(sql,(email,sifre_hash,fullName,databaseImage))
    else:
        sql = """ update "User" set "FullName"=%s, "Email"=%s """
        params= (fullName,email,id)
        if password != '':
            sifre_hash = hashlib.md5(password.encode()).hexdigest()
            sql += """, "Password"=%s """
            params = (fullName,email,sifre_hash,id)

        sql += """ where "Id" = %s"""

        database.execute(sql,params)

    return redirect("/admin/uye/index")

@uyeler.route('/sil/<string:id>')
def sil(id):
    database = Db()
    sql = """ delete from "User" where "Id"=%s """
    database.execute(sql, (id,))
    return redirect("/admin/uye/index")

