from flask import Flask
from flask_mysqldb import MySQL
import views
from database import Database
from flask_login import LoginManager, login_user

from flask import Flask, session, redirect, url_for, escape, request
import os
lm = LoginManager()
@lm.user_loader
def load_user():
    return "test"

    
def create_app():
    app = Flask(__name__)
    app.secret_key = os.urandom(24)

    app.config["MYSQL_USER"] = 'b0dd62d51c1994'
    app.config["MYSQL_PASSWORD"] = '589ca3ad'
    app.config["MYSQL_HOST"] = 'eu-cdbr-west-03.cleardb.net'
    app.config["MYSQL_DB"] = 'heroku_1fed0ad0dd81591'
    app.config.from_object("settings")

    app.add_url_rule("/", view_func=views.home_page)
    app.add_url_rule("/posts/<int:post_key>", view_func=views.post_page)
    app.add_url_rule("/", view_func=views.home_page)
    app.add_url_rule("/post", view_func=views.post_page)
    app.add_url_rule("/new_post", view_func=views.create_post_page, methods=["GET","POST"])
    app.add_url_rule("/register", view_func=views.register_page, methods=["GET","POST"])
    app.add_url_rule("/register_teachers", view_func=views.Tregister_page, methods=["GET","POST"])
    app.add_url_rule("/login", view_func=views.login_page, methods=["GET","POST"])
    app.add_url_rule("/about_us", view_func=views.about_page)
    app.add_url_rule("/test", view_func=views.read_page)
    app.add_url_rule("/logout", view_func=views.out_page)
    app.add_url_rule("/delete", view_func=views.delete_page)
    app.add_url_rule("/add_item", view_func=views.add_item, methods=["GET","POST"])
    app.add_url_rule("/new_password", view_func=views.change_password, methods=["GET","POST"])
    app.add_url_rule("/Update_post/<int:post_key>", view_func=views.update_post, methods=["GET","POST"])
    app.add_url_rule("/delete_post/<int:post_key>", view_func=views.post_delete_page, methods=["GET","POST"])

    
    return app

if __name__ == "__main__":
    app = create_app()
    lm.init_app(app)
    db = MySQL(app)
    app.config["db"] = db
    database = Database()
    app.run(host="0.0.0.0", port=8080, debug=True)