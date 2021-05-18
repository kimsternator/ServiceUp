from wsgiref.simple_server import make_server
from flask import Flask, session, render_template, request, redirect, send_from_directory
from google.oauth2 import id_token
from google.auth.transport import requests

import mysql.connector as mysql
import os

GOOGLE_CLIENT_ID = '675774771358-d9cs6b29kg2ce9tao1l6kq0o55s76fku.apps.googleusercontent.com'

db_user = os.environ['MYSQL_USER']
db_pass = os.environ['MYSQL_PASSWORD']
db_name = os.environ['MYSQL_DATABASE']
db_host = os.environ['MYSQL_HOST']

# clientSecret: IQvNBGE53RwdJi3n32nABTmc

app = Flask(__name__)
app.secret_key = 'thissecretisrequired'

@app.route('/database')
def database():
  # Connect to the database and retrieve the users
  db = mysql.connect(host=db_host, database=db_name, user=db_user, passwd=db_pass)
  cursor = db.cursor()
  cursor.execute("select first_name, last_name, email from Users;")
  records = cursor.fetchall()
  db.close()
  return records

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login',methods = ['POST', 'GET'])
def login():
    if request.method == 'POST':
        token = request.form['idtoken']
        print(token)
        try:
            idinfo = id_token.verify_oauth2_token(token, requests.Request(), GOOGLE_CLIENT_ID)
            session['idinfo'] = idinfo
            db = mysql.connect(user=db_user, password=db_pass, host=db_host, database=db_name)
            cursor = db.cursor()
            query = (f"select from Users where id is {idinfo['id']}")
            cursor.execute(query)
            if len(cursor) == 0 : 
                cursor.execute('INSERT INTO Users(googleID, email, name, lastName, urlToProfilePic ) VALUES (%s,%s,%s,%s,%s)', (idinfo['id'], idinfo['email'], idinfo['name'], idinfo['last name'], idinfo['url to profile pic']))
                db.commit()
            # idinfo is a dict that has email, name, last name, url to profile pic, and id, as well as some other oauth stuff
            return idinfo
        except ValueError:
            print('Invalid token')
            return 'invalid'
    else:
        return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

@app.route('/profile')
def profile():
    #TODO: profile_data = retrieve_profile_data_somehow(session['idinfo'])
    return render_template('profile.html')

@app.route('/post')
def post():
    return render_template('post.html')

@app.route('/new_post')
def new_post():
    return render_template('new_post.html')

#### Adding Route to handle adding posts to the database 
@app.route('/adding_post',methods=['GET', 'POST'])
def adding_post():
    if request.method == 'POST':
        new_post_dict = request.json # this should give us a dictionary with our inputs lets try it
        # grabbing dict data
        service_name = new_post_dict['serv']
        offerer = new_post_dict['who']
        availability = new_post_dict['when']
        compensation = new_post_dict['how']
        description = new_post_dict['desc']

        # Connect to the database so that we could insert new post information 
        db = mysql.connect(user=db_user, password=db_pass, host=db_host, database=db_name)
        cursor = db.cursor()
        cursor.execute('INSERT INTO Posts(id, service_type, who, available, compensation, info) VALUES (%s,%s,%s,%s,%s)', (session['id'], service_name, offerer, availability, compensation, description))
        db.commit()

        # Selecting Records - just to check to make sure all is good
        cursor.execute("select * from Posts;")
        print('---------- DATABASE INITIALIZED ----------')
        [print(x) for x in cursor]
        db.close()

    else:
        print('-------could not get post-------')
    
    return 'Success'

@app.route('/listing/<id>')
def listing():
    pass

@app.route('/favicon.ico') 
def favicon(): 
    return send_from_directory(os.path.join(app.root_path, 'static/images'), 'favicon.png', mimetype='image/vnd.microsoft.icon')

if __name__ == '__main__':
    # app.run(debug=True)
    server = make_server('0.0.0.0', 5000, app)
    server.serve_forever()