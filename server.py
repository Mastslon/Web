from flask import Flask
from flask_mysqldb import MySQL
import views
from database import Database

def create_app():
    app = Flask(__name__)

    app.config["MYSQL_USER"] = 'root'
    app.config["MYSQL_PASSWORD"] = '12345'
    app.config["MYSQL_HOST"] = 'localhost'
    app.config["MYSQL_DB"] = 'database'

    app.config.from_object("settings")

    app.add_url_rule("/", view_func=views.home_page)
    app.add_url_rule("/posts/<int:post_key>", view_func=views.post_page)
    app.add_url_rule("/", view_func=views.home_page)
    app.add_url_rule("/post", view_func=views.post_page)
    app.add_url_rule("/new_post", view_func=views.create_post_page, methods=["GET","POST"])
    app.add_url_rule("/about_us", view_func=views.about_page)
    app.add_url_rule("/login", view_func=views.login_page)
    app.add_url_rule("/test", view_func=views.read_page)

    
    return app

if __name__ == "__main__":
    app = create_app()
    db = MySQL(app)
    app.config["db"] = db
    database = Database()
    app.run(host="0.0.0.0", port=8080, debug=True)