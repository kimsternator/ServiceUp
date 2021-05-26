import bjoern
from flask import Flask, session, render_template, request, redirect, send_from_directory, Response
from google.oauth2 import id_token
from google.auth.transport import requests

import mysql.connector as mysql
import os

import google_storage as uploader
import hashlib
import datetime
import time
import json

from ip2geotools.databases.noncommercial import DbIpCity

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


@app.route('/get_main_posts/<offset>', methods=['GET'])
def get_main_posts(offset):
    db = mysql.connect(host=db_host, database=db_name, user=db_user, passwd=db_pass)
    cursor = db.cursor()
    # get the posts
    cursor.execute(f"select id, title, created_at, city from Posts limit {offset}, 12;")
    records = cursor.fetchall()
    db.commit()
    thePosts = []

    for post in records:
        cursor.execute(f"select url_link from Images where postID={post[0]} limit 1;")
        url = cursor.fetchall()[0]
        thePosts.append({"id": post[0],
                         "title": post[1],
                         "image_url": url,
                         "elapsed": get_hours(post[2]),
                         "city": post[3]})

    return {"posts": thePosts}


def get_hours(then):
    now = datetime.datetime.now()
    hours = (now - then).total_seconds() // 360

    if hours < 1:
        hours = "<1"
    else:
        hours = hours if hours <= 24 else ">24"

    return hours


@app.route('/')
def home():
    return render_template('home.html')


def convert_json(record, rest):
    d = {}
    for i, field in enumerate(rest):
        d[field] = record[0][i]
    return d


@app.route('/search')
def search():
    filter = request.args.get('filter')
    print(filter)
    if filter == "":
        return redirect('/')
    filter = {"filter": filter}

    return render_template('search.html', **filter)


@app.route('/listing')
def listing():
    id = request.args.get('id')
    print(id)
    if id == None:
        return redirect('/')
    db = mysql.connect(host=db_host, database=db_name, user=db_user, passwd=db_pass)
    cursor = db.cursor()
    cursor.execute(f"select * from Posts where id = {id};")
    temp1 = cursor.fetchall()
    print(temp1)
    user_id = temp1[0][1]
    cursor.execute(f"select * from Users where id = {user_id};")
    temp2 = cursor.fetchall()
    print(temp2)
    cursor.execute(f"select * from Images where id = {temp1[0][1]};")
    temp3 = cursor.fetchall()
    db.close()
    arr1 = convert_json(temp1, ['id', 'userID', 'title', 'description', 'price', 'tag', 'city', 'createdAt'])
    arr2 = convert_json(temp2, ['id', 'email', 'first_name', 'last_name', 'picture'])
    arr3 = convert_json(temp3, ['id', 'postID', 'url_link'])

    print(arr1)
    print(arr2)
    # , {"picture":temp2[0][4], 'Service':}
    return render_template('post.html', data={'post_data':arr1, 'user_data':arr2, 'image_data':arr3})

@app.route('/login',methods = ['POST', 'GET'])
def login():
    print('---This is a test---') 
    if request.method == 'POST':
        token = request.form['idtoken']
        print(token)
        try:
            idinfo = id_token.verify_oauth2_token(token, requests.Request(), GOOGLE_CLIENT_ID)
            session['idinfo'] = idinfo 
            
            # here I will try to populate the users database by logging in 
            print('------Inside Login------')
            print(idinfo)
            db = mysql.connect(user=db_user, password=db_pass, host=db_host, database=db_name)
            cursor = db.cursor() 
            
            # This is to make sure user does not exist in the data base
            possible_user = idinfo['email'] 
            # query = (f"select * from Users where email is {idinfo['email']}")
            query = ("SELECT * from Users where email=%s")
            values = (possible_user,)
            cursor.execute(query, values)
            response = cursor.fetchall()
            if len(response) == 0 :

                try:
                    cursor.execute('INSERT INTO Users(email, firstName, lastName, urlToProfilePic ) VALUES (%s,%s,%s,%s)', (idinfo['email'], idinfo['given_name'], idinfo['family_name'], idinfo['picture']))
                    db.commit()
                except Exception as e:
                    print(e)
                    print('there was an error')

            # Selecting Users to make sure data base works
            cursor.execute("select * from Users;")
            print('---------- DATABASE Users INITIALIZED ----------')
            [print(x) for x in cursor]
            db.close()

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
    image_links = []
    print(type(files))
    for file in files:
        print(type(file))
        up = uploader.ImageUpload()
        new_name = hashlib.md5((session['idinfo']['email'] + str(time.time())).encode()).hexdigest()
        print(new_name)
        link = up.upload(file, file.filename, new_name)
        image_links.append(link)

    # get the user ID
    db = mysql.connect(user=db_user, password=db_pass, host=db_host, database=db_name)
    cursor = db.cursor()
    print('-----getting userID-----')
    finding_user = session['idinfo']['email']
    print(finding_user)
    #query = (f"select id from Users where email={session['idinfo']['email']}")
    query = ("SELECT id from Users where email=%s")
    values = (finding_user,)
    cursor.execute(query, values)
    #cursor.execute('SELECT id from Users where email=:contact', {'contact': finding_user})
    userID = cursor.fetchall()[0]
    db.commit()
    print('----got user id----')

    if request.form.get('city', type=str) is None:
        ip = request.remote_addr
        print(ip)
        city = DbIpCity.get(ip, api_key='free').city
        print(city)
        # request.form.add("city", DbIpCity.get(ip, api_key='free').city)

    print(request.form.to_dict(flat=False))
    # request.form[''] contains all the different data the user put in
    print(request.form)

    # put everything in the databases
    cursor = db.cursor()
    user = userID # seems like userID is getting returned as a tuple
    user_value = user[0]

    title = request.form.get("title", type=str)
    description = request.form.get("desc", type=str)
    price = request.form.get("price", type=str)
    tag = request.form.get("tag", type=str)
    City = request.form.get("city", type=str)
    
    #query = (f"insert into Posts (userID, title, description, price, tag, city) values ({userID}, {request.form.get("title", type=str)}, {request.form.get("description", type=str)}, {request.form.get("price", type=str)}, {request.form.get("tag", type=str)}, {request.form.get("city", type=str)});")
    cursor.execute('INSERT INTO Posts (userID, title, description, price, tag, city) VALUES (%s,%s,%s,%s,%s,%s)', (user_value, title, description, price, tag, City))
    db.commit()

    # Selecting Posts to make sure data base works
    cursor.execute("select * from Posts;")
    print('---------- DATABASE POSTS INITIALIZED ----------')
    [print(x) for x in cursor]

    query = (f"SELECT * FROM Posts ORDER BY ID DESC LIMIT 1;")
    cursor.execute(query)
    postID = cursor.fetchall()[0] # not sure if you guys meant to fetchone, you previously had fetchall[0] which was giving an error.
    #image_links = [f"({postID}, {linkurl})" for linkurl in image_links]
    db.commit()

    the_id = postID[0]
    the_url = image_links[0]
    # #query = (f"insert into Images (postID, url) values {", ".join(image_links)}")
    cursor.execute('INSERT into Images (postID, url_link) VALUES (%s,%s)' , (the_id, the_url))
    db.commit()

    # Selecting Images to make sure data base works
    cursor.execute("select * from Images;")
    print('---------- DATABASE Images INITIALIZED ----------')
    [print(x) for x in cursor]
    db.close()
    
    return redirect('/listing?id=' + str(the_id))

@app.route("/get_filter/<offset>/<filter>")
def get_filter(offset, filter):
    # filter = request.args.get('filter')
    print(offset)
    print(filter)

    if filter == None:
        return redirect('/')

    try:
        ip = request.remote_addr
        print(ip)
        city = DbIpCity.get(ip, api_key='free').city
    except KeyError:
        city = "San Diego"

    print(city)
    db = mysql.connect(host=db_host, database=db_name, user=db_user, passwd=db_pass)
    cursor = db.cursor()
    cursor.execute(f"select id, title, created_at, description, tag, city from Posts;")
    records = cursor.fetchall()
    db.commit()
    print(records)
    filtered_records = []

    for post in records:
        if any(filter.lower() in str(string).lower() for string in post):
            cursor.execute(f"select url_link from Images where postID={post[0]} limit 1;")
            url = cursor.fetchall()[0]
            filtered_records.append({"id": post[0], "title": post[1],
                                     "image_url": url,
                                     "elapsed": get_hours(post[2]),
                                     "city": post[3]})

    db.close()

    records = {"posts": filtered_records}

    return records

@app.route('/profile')
def profile():
    #TODO: profile_data = retrieve_profile_data_somehow(session['idinfo'])
    return render_template('profile.html')

@app.route('/post')
def post():
    return render_template('post.html')

@app.route('/new_post')
def new_post():
    return render_template('new_postNEW.html')

@app.route('/messaging')
def messaging():
    return render_template('chat.html')

@app.route('/messageuser')
def messageUser():
    return render_template('messageUser.html')

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

@app.route('/load_more',methods=['POST'])
def load_more():
    city = ""

    try:
        ip = request.remote_addr
        print(ip)
        city = DbIpCity.get(ip, api_key='free').city
    except KeyError:
        city = "San Diego"

    print(city)
    offset = request.form['offest']
    print(offset)

    db = mysql.connect(user=db_user, password=db_pass, host=db_host, database=db_name)
    cursor = db.cursor()
    query = (f"select id, title, description, price, tag, city, timestamp from Posts where city={city} limit 12 offset {offset};")
    cursor.execute(query)
    posts = cursor.fetchall()
    db.commit()
    db.close()

    return posts

@app.route('/favicon.ico') 
def favicon(): 
    return send_from_directory(os.path.join(app.root_path, 'static/images'), 'favicon.png', mimetype='image/vnd.microsoft.icon')


####################

from flask import jsonify
from flask_socketio import SocketIO, emit

# app = Flask(__name__, template_folder='templates', static_url_path='/static/', static_folder='static')
# app.config['SECRET_KEY'] = 'ines'
socketio = SocketIO(app)

@socketio.on('connected')
def conn(msg):
	return {'data':'Ok'}

@socketio.on('client_message')
def receive_message(data):
	emit('server_message', data, broadcast=True)


#######################
if __name__ == '__main__':
    # app.run(debug=True)
    socketio.run(app, debug=True, port=6004, host='0.0.0.0' ) #trial
    bjoern.run(app, '0.0.0.0', 6004)