from flask import Blueprint, render_template
from gun7.blog.utils.Db import Db
anasayfa = Blueprint('anasayfa',__name__,
                 url_prefix="/anasayfa")


def sort(val):
    return val[3]


@anasayfa.route("/")
def index():

    databse = Db()
    sql = """ select * from "BlogYazisi" """
    data = databse.read_data(sql);
    data.sort(key=sort,reverse = True)

    return render_template("anasayfa/index.html",data=data)