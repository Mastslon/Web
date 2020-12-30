
from flask import current_app, render_template,request,redirect,url_for, abort
from flask_mysqldb import MySQL

class Database:
    def __init__(self):
        print("created")
    def add_post(self, title, content):
        db = current_app.config["db"]
        cur = db.connection.cursor()
        cur.execute("INSERT INTO posts (Title, Content, School_id, Author_id, StudentNumber) VALUES (%s, %s, %s, %s, %s)",(title, content, 2,3,40))
        db.connection.commit()
        cur.execute(''' SELECT *  FROM posts ORDER BY Post_id DESC LIMIT 1''')
        data = cur.fetchall()
    def get_posts(self):
        db = current_app.config["db"]
        cur = db.connection.cursor()
        cur.execute(''' SELECT posts.Title, posts.Content, school.School_name, posts.Author_id, posts.StudentNumber, posts.Post_id   FROM posts JOIN school_web ON school_web.School_id = posts.School_id JOIN school_address ON school_address.School_Web = school_web.School_Web JOIN school ON school.School_Address = school_address.School_Address ORDER BY Post_id DESC''')
        data = cur.fetchall()
        return data
    def insert_user(self, title, content, School_id, Author_id, StudentNumber):
        db = current_app.config["db"]
        cur = db.connection.cursor()
        cur.execute("INSERT INTO posts (Title, Content, School_id, Author_id, StudentNumber) VALUES (%s, %s, %s, %s, %s)",(title, content, 2,3,40))
        db.connection.commit()
    def get_post(self, id):
        db = current_app.config["db"]
        cur = db.connection.cursor()
        cur.execute((''' SELECT posts.Post_id, posts.Title, posts.Content, school.School_name, posts.Author_id, posts.StudentNumber, school_address.School_Address, school.School_City, school.School_District   FROM posts JOIN school_web ON school_web.School_id = posts.School_id JOIN school_address ON school_address.School_Web = school_web.School_Web JOIN school ON school.School_Address = school_address.School_Address WHERE posts.Post_id= %s''' % (id)))
        #cur.execute("SELECT * FROM posts WHERE Post_id= %s" % (id))
        data = cur.fetchall()[0]
        #Needs
        cur.execute("SELECT item_names.Item_name FROM posts JOIN needs ON needs.Post_id = posts.Post_id JOIN item_names ON item_names.Item_id = needs.Material_id  WHERE posts.Post_id= %s" % (id))
        needs = cur.fetchall()
        a = [data, needs]
        return a
    def new_post(self, form_title, form_content, school,num_students,needs):
        db = current_app.config["db"]
        cur = db.connection.cursor()
        # school information
        cur.execute("SELECT  school.School_name, school_web.School_id   FROM school JOIN school_address ON school.School_Address = school_address.School_Address JOIN school_web ON school_web.School_Web = school_address.School_Web WHERE school.School_name LIKE %s LIMIT 1",("%"+school+"%",))
        data = cur.fetchall()
        school_id = data[0][1]

        #insert new post 
        cur.execute("INSERT INTO posts (Title, Content, School_id, Author_id, StudentNumber) VALUES (%s, %s, %s, %s, %s)",(form_title, form_content, school_id,3,num_students))
        db.connection.commit()
        
        #Post id
        cur.execute(''' SELECT *  FROM posts ORDER BY Post_id DESC LIMIT 1''')
        data = cur.fetchall()
        
        post_id = data[0][0]

        #Needs
        for i in needs:
            cur.execute(" SELECT b.Item_id FROM item_names AS b WHERE b.Item_name = "+"'"+ i +"'")
            data = cur.fetchall()
            need_id = data[0][0]
            cur.execute("INSERT INTO needs (Post_id, Material_id) VALUES (%s,%s)",(post_id,need_id))

        db.connection.commit()

        return post_id
        
