from datetime import datetime
from flask_mysqldb import MySQL
from flask import current_app, render_template,request,redirect,url_for, abort
from random import randint
from database import Database

database = Database()

def home_page():
    data = database.get_posts()
    return render_template("home.html", posts = data)

def post_page(post_key):
    data = database.get_post(post_key)
    print(data)
    return render_template("post.html", post=data)

def about_page():
    return render_template("about.html")

def login_page():
    return render_template("contact.html")

def test_page():
    db = current_app.config["db"]
    cur = db.connection.cursor()
    cur.execute(''' CREATE TABLE example (id INTEGER)  ''')
    return 'Done!'

def read_page():
    db = current_app.config["db"]
    cur = db.connection.cursor()
    cur.execute(''' SELECT posts.School_id, posts.Author_id, school_web.School_Web  FROM posts JOIN school_web WHERE school_web.School_id = 3''')
    data = cur.fetchall()
    return 'done!'

def create_post_page():
    if request.method == "GET":
        return render_template("create_post.html")
    else:
        form_title = request.form["title"]
        form_content = request.form["content"]
        form_school = request.form["school"]
        form_students = int(request.form["students"])
        key = database.new_post(form_title, form_content, form_school, form_students)
        return redirect(url_for("post_page", post_key = key))
def class_test_page():
    if request.method == "GET":
        return render_template("create_post.html")
    else:
        form_title = request.form["title"]
        form_content = request.form["content"]
        db = current_app.config["db"]
        cur = db.connection.cursor()
        cur.execute("INSERT INTO posts (Title, Content, School_id, Author_id, StudentNumber) VALUES (%s, %s, %s, %s, %s)",(form_title, form_content, 2,3,40))
        db.connection.commit()
        return "added"