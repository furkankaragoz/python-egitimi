from flask import Blueprint, render_template, request, redirect
from gun7.blog.utils.Db import Db

blog = Blueprint('blog', __name__,
                 url_prefix="/admin/blog")


@blog.route("/index")
def index():
    databse = Db()
    sql = """ select * from "BlogYazisi" """
    data = databse.read_data(sql);

    return render_template("admin/blog/index.html", data=data)


@blog.route('/ekle', defaults={'id': None})
@blog.route('/ekle/<string:id>')
def ekle(id):
    if id is not None:
        databse = Db()
        sql = """ select * from "BlogYazisi" where "Id" = %s """
        data = databse.read_first_data(sql, (id,))
        print(data)

        return render_template("admin/blog/ekle.html", data=data)

    return render_template("admin/blog/ekle.html", data=None)


@blog.route('/save', methods=["POST"])
def save():
    Baslik = request.form.get("Baslik")
    id = request.form.get("Id")
    Icerik = request.form.get("Icerik")
    YayinTarihi = request.form.get("YayinTarihi")

    database = Db()

    sql = ""
    if id is None:
        sql = """ insert into "BlogYazisi" ("Baslik","Icerik","YayinTarihi") values (%s,%s,%s) """
        database.execute(sql, (Baslik, Icerik, YayinTarihi))
    else:
        sql = """ update "BlogYazisi" set "Baslik"=%s, "Icerik"=%s,"YayinTarihi"=%s """
        params = (Baslik, Icerik, YayinTarihi, id)

        sql += """ where "Id" = %s"""

        database.execute(sql, params)

    return redirect("/admin/blog/index")


@blog.route('/sil/<string:id>')
def sil(id):
    database = Db()
    sql = """ delete from "BlogYazisi" where "Id"=%s """
    database.execute(sql, (id,))
    return redirect("/admin/blog/index")
