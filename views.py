from datetime import datetime
from flask_mysqldb import MySQL
from flask import current_app, render_template,request,redirect,url_for, abort
from random import randint
from database import Database
from passlib.hash import pbkdf2_sha256 as hasher
from flask_login import LoginManager, login_user, current_user
from flask import Flask, session, redirect, url_for, escape, request

database = Database()

def home_page():
    data = database.get_posts()
    if 'username' in session:
        return render_template("home.html", posts = data, user_id = session['username'])
    else:
        return render_template("home.html", posts = data)

def post_page(post_key):
    data = database.get_post(post_key)
    print("******************")
    if 'username' in session:
        if int(session['user_type']):
                    
            db = current_app.config["db"]
            cur = db.connection.cursor()
            id = int(data[0][0])
            print(id)
            cur.execute((''' SELECT posts.Author_id FROM posts WHERE posts.Post_id= %s''' % (id)))  
            auth = cur.fetchall()
            if int(auth[0][0]) == int(session["user_id"]):
                return render_template("post.html", post=data, user_id = session["user_id"])
            else:
                return render_template("post.html", post=data)
    else:
        return render_template("post.html", post=data)


def add_item():
    if request.method == "GET":
        return render_template("Add_item.html")
    else:
        name = request.form["name"]
        amount = request.form["amount"]
        
        db = current_app.config["db"]
        cur = db.connection.cursor()
        print(name)
        cur.execute("SELECT inventory.Amount FROM inventory WHERE inventory.Item_name="+"'"+name+"'")
        data = cur.fetchall()
        print(data)
        if len(data) >= 1:
            n = int(data[0][0])
            n+= int(amount)
            print("*"*30)
            cur.execute(" UPDATE inventory SET inventory.Amount = %s WHERE inventory.Item_name= %s",(n,name))
            db.connection.commit()
        else:
            cur.execute("INSERT INTO inventory (Item_name, Amount) VALUES (%s, %s)",(name, int(amount)))
            db.connection.commit()
        
    
    return redirect(url_for("home_page"))




def about_page():
    if 'username' in session:
        return render_template("about.html", user_id = session["username"])
    else:
        return render_template("about.html")

def read_page():
    db = current_app.config["db"]
    cur = db.connection.cursor()
    cur.execute(''' SELECT posts.School_id, posts.Author_id, school_web.School_Web  FROM posts JOIN school_web WHERE school_web.School_id = 3''')
    data = cur.fetchall()
    return 'done!'

def create_post_page():
    if request.method == "GET":
        if 'username' in session:
            if 'user_type' in session:
                if int(session['user_type']):
                    return render_template("create_post.html")
                else:
                    return render_template("nopermission.html")
            else:
                return render_template("nopermission.html")
        else:
            return render_template("nopermission.html")
    else:
        form_title = request.form["title"]
        form_content = request.form["content"]
        form_school = request.form["school"]
        form_students = int(request.form["students"])
        needs = []
        for i in range(5):
            selected = request.form["row-"+str(i)+"-office"]
            if selected not in needs:
                if selected != "None":
                    needs.append(selected)
        print(needs)
        key = database.new_post(form_title, form_content, form_school, form_students, needs, int(session["user_id"]))
        if key==0:
            return render_template("create_post.html", error = "error")
        else:
            return redirect(url_for("post_page", post_key = key))

def update_post(post_key):
    if request.method == "GET":
        data = database.get_post(post_key)
        return render_template("update.html", post=data)
    else:
        form_title = request.form["title"]
        form_content = request.form["content"]
        
        db = current_app.config["db"]
        cur = db.connection.cursor()
        id = int(post_key)
        if len(form_title) > 3:
            cur.execute(''' UPDATE posts SET posts.Title ='''+"'"+form_title+"'"+ " WHERE posts.Post_id= %s"%(id))
        if len(form_content) > 3:
            cur.execute(''' UPDATE posts SET posts.Content='''+"'"+form_content+"'"+ " WHERE posts.Post_id= %s"%(id))
        db.connection.commit()
        return redirect(url_for("post_page", post_key = post_key))


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

def check_reg(Email,Password,Name, Surname, City, Phone_number):
    errors= ["","","","","",""]
    a = 0
    if "@" not in Email:
        errors[0] = "Invalid Email"
        a=1
    if len(Password)<5:
        errors[1] = "Password is too short"
        a=1
    if len(Name)<4:
        errors[2] = "Name is too short"
        a=1
    if len(Surname)<4:
        errors[3] = "Surname is too short"
        a=1
    if len(Phone_number)!=11:
        errors[4] = "Invalid Phone Number"
        a=1
    return errors , a


def register_page():
    if request.method == "GET":
            return render_template("register.html")
    else:
        Email = request.form["email"]
        Password = request.form["password"]
        Name = request.form["name"]
        Surname = request.form["surname"]
        City = request.form["City"]
        Phone_number = request.form["Phone Number"]
        errors, a = check_reg(Email,Password,Name,Surname,City,Phone_number)
        if a:
            return render_template("register.html", errors = errors)
        hashed = hasher.hash(Password)
        db = current_app.config["db"]
        cur = db.connection.cursor()
        cur.execute("INSERT INTO users (Email, User_type, Password, First_name, Last_name, Phone, City) VALUES (%s, %s, %s, %s, %s, %s, %s)",(Email, "User", hashed, Name, Surname, Phone_number, City ))
        db.connection.commit()
        return redirect(url_for("home_page"))

def Tregister_page():
    if request.method == "GET":
            return render_template("teacher_reg.html")
    else:
        Email = request.form["email"]
        Password = request.form["password"]
        Name = request.form["name"]
        Surname = request.form["surname"]
        City = request.form["City"]
        Phone_number = request.form["Phone Number"]
        Course = request.form["Course"]
        errors, a = check_reg(Email,Password,Name,Surname,City,Phone_number)
        if a:
            return render_template("register.html", errors = errors)
        hashed = hasher.hash(Password)
        db = current_app.config["db"]
        cur = db.connection.cursor()
        cur.execute("INSERT INTO teacher (Email, Course, Password, First_name, Last_name, Phone, City) VALUES (%s, %s, %s, %s, %s, %s, %s)",(Email, Course, hashed, Name, Surname, Phone_number, City ))
        db.connection.commit()
        return redirect(url_for("home_page"))

def login_page():
    if request.method == "GET":
        return render_template("login.html")
    else:
        user_type=0
        Email = request.form["email"]
        Password = request.form["password"]
        
        db = current_app.config["db"]
        cur = db.connection.cursor()
        cur.execute(''' SELECT users.Password, users.First_name ,users.User_id FROM users WHERE users.Email = '''+"'"+str(Email)+"'")
        data = cur.fetchall()
        if len(data)==0:
            cur.execute(''' SELECT teacher.Password, teacher.First_name, teacher.Teacher_id FROM teacher WHERE teacher.Email = '''+"'"+str(Email)+"'")
            data = cur.fetchall()
            if len(data)==0:
                return render_template("login.html", error = "error")
            else:
                user_type = 1
        print(data[0][0])
        if hasher.verify(Password, data[0][0]):
            session['user_type'] = str(user_type)
            session['username'] = str(data[0][1])
            session['user_id'] = str(data[0][2])
            test = session['username']
            return redirect(url_for("home_page"))
        else:
            return render_template("login.html", error = "error")
        print(Email)
        print(data)
        return render_template("login.html")

def out_page():
    session.pop('username', None)
    session.pop('user_type', None)
    session.pop('user_id', None)
    return redirect(url_for("home_page"))

def change_password():
    if request.method == "GET":
        return render_template("change_password.html")
    else:
        Password = request.form["password"]
        if "user_id" in session:
            print("test")
            id = int(session["user_id"])
            user_type = int(session["user_type"])
            print("test")
            db = current_app.config["db"]
            cur = db.connection.cursor()
            hashed = hasher.hash(Password)
            if user_type:
                cur.execute(''' UPDATE teacher SET teacher.Password ='''+"'"+hashed+"'"+ " WHERE teacher.Teacher_id= %s"%(id))
            else:
                cur.execute(''' UPDATE users SET users.Password ='''+"'"+hashed+"'"+ " WHERE users.User_id= %s"%(id))
            db.connection.commit()    
        
            return redirect(url_for("home_page"))


def delete_page():
    db = current_app.config["db"]
    cur = db.connection.cursor()
    if 'user_type' in session:
        id = int(session["user_id"])
        if int(session['user_type']):
            cur.execute("DELETE FROM teacher WHERE teacher.Teacher_id= %s"%(id))
        else:
            cur.execute("DELETE FROM users WHERE users.User_id= %s"%(id))
        db.connection.commit() 
    session.pop('username', None)
    session.pop('user_type', None)
    session.pop('user_id', None)
    return redirect(url_for("home_page"))

def post_delete_page(post_key):

    db = current_app.config["db"]
    cur = db.connection.cursor()
    id = int(post_key)
    cur.execute("DELETE FROM posts WHERE posts.Post_id= %s"%(id))
    db.connection.commit()
    return redirect(url_for("home_page"))
