from wsgiref.simple_server import make_server
from flask import Flask, session, render_template, request, redirect, send_from_directory
from google.oauth2 import id_token
from google.auth.transport import requests

import mysql.connector as mysql
import os

import google_storage as uploader
import hashlib
import time

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
            return idinfo

            ''' EXAMPLE idinfo 
            {
                "iss":"accounts.google.com",
                "azp":"675774771358-d9cs6b29kg2ce9tao1l6kq0o55s76fku.apps.googleusercontent.com",
                "aud":"675774771358-d9cs6b29kg2ce9tao1l6kq0o55s76fku.apps.googleusercontent.com",
                "sub":"STRING",
                "hd":"ucsd.edu",
                "email":"valtov@ucsd.edu",
                "email_verified":true,
                "at_hash":"STRING",
                "name":"Vladimir Altov",
                "picture":"https://lh3.googleusercontent.com/a/AATXAJzcKY8n-t6GCuOc-DfyPmefcNZTjPgFWJlhYqLw=s96-c",
                "given_name":"Vladimir",
                "family_name":"Altov",
                "locale":"en",
                "iat":int,
                "exp":int,
                "jti":"STRING"
            }
            '''
            # THIS DOESN'T WORK, SOMETHING TO DO WITH SQL, IT RETURNS A VERY VAGUE ERROR THAT LITERALLY JUST SAYS YOUR SQL HAS A SYNTAX ERROR
            # PLEASE TEST BEFORE COMMITTING TO MASTER BRANCH
            #
            # db = mysql.connect(user=db_user, password=db_pass, host=db_host, database=db_name)
            # cursor = db.cursor()
            # query = (f"select * from Users where email is {idinfo['email']}")
            # cursor.execute(query)
            # if len(cursor) == 0 : 
            #     cursor.execute('INSERT INTO Users(email, name, lastName, urlToProfilePic ) VALUES (%s,%s,%s,%s)', (idinfo['email'], idinfo['given_name'], idinfo['family_name'], idinfo['picture']))
            #     db.commit()
        except ValueError:
            print('Invalid token')
            return 'invalid'
    else:
        return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')


@app.route('/submit_post', methods=['POST'])
def submit_post():
    if 'idinfo' not in session:
        return 'MUST BE LOGGED IN'
    # VERIFY VALIDITY OF FILES BEFORE UPLOADING TO DATABASE HERE
    #
    #
    #
    #
    files = request.files.getlist('filename')
    print(type(files))
    for file in files:
        print(type(file))
        up = uploader.ImageUpload()
        new_name = hashlib.md5((session['idinfo']['email'] + str(time.time())).encode()).hexdigest()
        print(new_name)
        link = up.upload(file, file.filename, new_name)
    
    # request.form[''] contains all the different data the user put in
    print(request.form)
    
    return f'IM THINKING THIS SHOULD REDIRECT TO A PAGE WITH A LINK TO THE POST THEY JUST CREATED: {link}'

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

@app.route("/terms_of_service")
def terms_of_service():
    return render_template('tos.html')

@app.route("/privacy_policy")
def privacy_policy():
    return render_template('pp.html')

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
    server = make_server('0.0.0.0', 6004, app)
    server.serve_forever()