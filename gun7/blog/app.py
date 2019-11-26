from flask import Flask, render_template, request, redirect, session

from gun7.blog.views.admin.BlogController import blog
from gun7.blog.views.admin.UyeController import uyeler
from gun7.blog.views.admin.GirisController import giris
from gun7.blog.views.AnasayfaController import anasayfa


app = Flask(__name__)

app.register_blueprint(blog)
app.register_blueprint(uyeler)
app.register_blueprint(giris)
app.register_blueprint(anasayfa)


if __name__ == "__main__":
    app.secret_key = "abc"
    app.run(debug=True)