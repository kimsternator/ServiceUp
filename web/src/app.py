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

import ipinfo

GOOGLE_CLIENT_ID = '675774771358-d9cs6b29kg2ce9tao1l6kq0o55s76fku.apps.googleusercontent.com'

db_user = os.environ['MYSQL_USER']
db_pass = os.environ['MYSQL_PASSWORD']
db_name = os.environ['MYSQL_DATABASE']
db_host = os.environ['MYSQL_HOST']
access_token = os.environ['ip_token']
handler = ipinfo.getHandler(access_token)

app = Flask(__name__)
app.secret_key = 'thissecretisrequired'


@app.route('/database_test')
def database_test():
  # Connect to the database and retrieve the users
  db = mysql.connect(host=db_host, database=db_name, user=db_user, passwd=db_pass)
  cursor = db.cursor()
  cursor.execute("select first_name, last_name, email from Users;")
  records = cursor.fetchall()
  db.close()
  return records


@app.route('/get_main_posts/<offset>', methods=['GET'])
def get_main_posts(offset):
    try:
        ip = request.remote_addr
        print(ip)
        city = handler.getDetails(ip).city
        print(city)
    except:
        city = "San Diego"
        print("ip error")
        print("ip = " + str(ip))

    print(city)
    records = database(f'select id, title, created_at, city from Posts where city="{city}" limit {offset}, 12;')
    thePosts = []

    for post in records:
        url = database(f"select url_link from Images where postID={post[0]} limit 1;")

        if url == []:
            url = ""
        else:
            url = url[0]

        thePosts.append({"id": post[0],
                         "title": post[1],
                         "image_url": url,
                         "elapsed": get_hours(post[2]),
                         "city": post[3]})

    return {"posts": thePosts}


def get_hours(then):
    if then is None:
        return "?"
    now = datetime.datetime.now()
    hours = (now - then).total_seconds() // 3600

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
    posts_query = f"select * from Posts where id = {id};"
    post = database_posts(posts_query)[0]
    user_id = post[1]
    user = database(f"select * from Users where id = {user_id};")[0]
    print(post)
    print(user)
    # db = mysql.connect(host=db_host, database=db_name, user=db_user, passwd=db_pass)
    # cursor = db.cursor()
    # cursor.execute(f"select * from Posts where id = {id};")
    # temp1 = cursor.fetchall()
    # print(temp1)
    # user_id = temp1[0][1]
    # cursor.execute(f"select * from Users where id = {user_id};")
    # temp2 = cursor.fetchall()
    # print(temp2)
    # cursor.execute(f"select * from Images where postID = {temp1[0][0]};")
    # temp3 = cursor.fetchall()
    # db.close()
    # arr1 = convert_json(temp1, ['id', 'userID', 'title', 'description', 'price', 'tag', 'city', 'createdAt'])
    # arr2 = convert_json(temp2, ['id', 'email', 'first_name', 'last_name', 'picture'])
    # arr3 = convert_json(temp3, ['id', 'postID', 'url_link'])

    # users = database(f"select * from Users where {users_query};")
    # print(users)
    # if not users:
    #     return jsonify([])
    # posts_query = f"select * from Posts where userID = {users[0][0]};"
    # return jsonify(database_posts(posts_query))
    # print(arr1)
    # print(arr2)
    # # , {"picture":temp2[0][4], 'Service':}
    return render_template('post.html', data={'post':post, 'user':user})

@app.route('/login',methods = ['POST'])
def login():
    print('---This is a test---') 
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
        return 'invalid token'

@app.route('/logout')
def logout():
    email = session['idinfo']['email']
    session.clear()
    return email

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
    email = session['idinfo']['email']
    userID = database(f'select id from Users where email="{email}";')[0][0]

    theDict = request.form.to_dict()

    if request.form.get('city', type=str) == "":
        try:
            ip = request.remote_addr
            print(ip)
            city = handler.getDetails(ip).city
        except:
            city = "San Diego"

        theDict["city"] = city

    # put everything in the databases
    print(theDict)
    title = theDict["title"]
    description = theDict["desc"]
    price = theDict["price"]
    tag = theDict["tag"]
    database(f'insert into Posts (userID, title, description, price, tag, city) VALUES ({userID}, "{title}", "{description}", {price}, "{tag}", "{city}");')
    postID = database(f'SELECT id FROM Posts ORDER BY ID DESC LIMIT 1;')[0][0]

    for the_url in image_links:
        database(f'insert into Images (postID, url_link) values ({postID}, "{the_url}");')

    return redirect('/listing?id=' + str(postID))


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
        city = handler.getDetails(ip).city
    except:
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
                                     "city": post[5]})

    db.close()

    records = {"posts": filtered_records}

    return records

# Renders the custom user profile if logged in, redirects to home otherwise
@app.route('/profile')
def profile():
    if 'idinfo' not in session:
        return 'MUST BE LOGGED IN'

    email = session['idinfo']['email']
    print(email)
    user = database(f'select * from Users where email="{email}";')
    print(user)

    return render_template('profile.html', data=user[0])


# Returns the exact query result from the SQL database
def database(query):       
    db = mysql.connect(host=db_host, database=db_name, user=db_user, passwd=db_pass)
    cursor = db.cursor()

    try:
        cursor.execute(query)
        record = cursor.fetchall()
        db.commit()
        db.close()

        return record
    except Exception as e:
        print(e)
    db.close()

    return None

# Runs query SPECIFICALLY for Posts table, and then finds each image related to each post returned in the 
# query, and links them together, and returns one large list of all posts linked with lists of their images
def database_posts(query):
    posts = database(query)
    print(posts)
    data = []
    for post in posts:
        images = database(f'select url_link from Images where postID={post[0]};')
        print(images)
        post_with_image = list(post)
        post_with_image.append([t[0] for t in images])
        data.append(post_with_image)
    print(data)
    return data

# Endpoint to query Post table, accepts either specific post id, post tag, or user id, email, first and/or last name
# Example get request: serviceup.com/get_posts?tag=paint&email=test@gmail.com
# This returns a list of all posts (with images) made by user with email test@gmail with tag of paint
@app.route('/get_posts')
def get_posts():
    if not request.args:
        return 'empty query', 400
    viable_posts_query = ['id', 'tag' ]
    viable_users_query = ['userID', 'email', 'firstName', 'lastName']
    query = {'posts': {}, 'users':{} }
    for key in request.args:
        print(key, request.args[key])
        if key in viable_posts_query:
            query['posts'][key] = request.args[key]
        elif key in viable_users_query:
            query['users'][key] = request.args[key]
        else:
            return f'INVALID QUERY, usage: {viable_posts_query} {viable_users_query}'
    
    posts_query = ' and'.join([f'{key}="{val}"' for key, val in query['posts'].items()])
    users_query = ' and'.join([f'{key}="{val}"' for key, val in query['users'].items()])
    print(posts_query, users_query)

    if query['posts'] and query['users']:
        users = database(f"select * from Users where {users_query};")
        print(users)
        if users: 
            posts_query += ' and userID = {users[0][0]}'
        return jsonify(database_posts(posts_query))
    elif query['posts']:
        return jsonify(database_posts(posts_query))
    elif query['users']:
        users = database(f"select * from Users where {users_query};")
        print(users)
        if not users:
            return jsonify([])
        posts_query = f"select * from Posts where userID = {users[0][0]};"
        return jsonify(database_posts(posts_query))

@app.route('/post')
def post():
    return render_template('post.html')

@app.route('/new_post')
def new_post():
    return render_template('new_postNEW.html')

@app.route('/messaging')
def messaging():
    if 'idinfo' not in session:
        return 'MUST BE LOGGED IN'

    return render_template('messaging.html')

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
        city = handler.getDetails(ip).city
    except:
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


@app.route('/get_chats', methods=['GET'])
def get_chats():
    userEmail = session['idinfo']['email']
    userID = database(f'select id from Users where email="{userEmail}";')[0][0]
    senderChats = database(f'select receiverID from Chats where senderID="{userID}";')
    receiverChats = database(f'select senderID from Chats where receiverID="{userID}";')
    userIDs = [chat[0] for chat in senderChats] + [chat[0] for chat in receiverChats]
    chats = []

    for id in userIDs:
        theUser = database(f'select firstName, lastName from Users where id="{id}";')[0]

        if theUser is not None:
            chats.append((" ".join(theUser), id))

    return {"chats": chats}


@app.route('/get_messages/<recipientID>/<offset>', methods=['GET'])
def get_messages(recipientID, offset):
    userEmail = session['idinfo']['email']
    userID = database(f'select id from Users where email="{userEmail}";')[0][0]

    senderChatID = database(f'select id from Chats where senderID="{userID}" and receiverID="{recipientID}";')
    receiverChatID = database(f'select id from Chats where receiverID="{userID}" and senderID="{recipientID}";')
    chatID = 0

    if senderChatID:
        chatID = senderChatID[0][0]
        sender = True
    elif receiverChatID:
        chatID = receiverChatID[0][0]
        sender = False

    if chatID == 0:
        return {"messages": []}

    messages = database(f'select message, senderID, receiverID from Messages where chatID={chatID} order by created_at asc limit {offset}, 18446744073709551615;')
    messages = [(message[0], 0) if message[1] == userID else (message[0], 1) for message in messages]

    return {"messages": messages}


@app.route('/add_chat/<receiverId>', methods=['POST', 'GET'])
def add_chat(receiverId):
    if 'idinfo' not in session:
        return {"message": 'MUST BE LOGGED IN'}

    userEmail = session['idinfo']['email']
    userID = database(f'select id from Users where email="{userEmail}";')[0][0]

    if userID == int(receiverId):
        return {"message": 'You cannot message yourself'}

    chats = database(f'SELECT EXISTS(SELECT * FROM Chats WHERE receiverID="{userID}" OR senderID="{userID}" LIMIT 1);')[0][0]

    #chat doesnt already exists between users
    if chats == 0:
        database(f'insert into Chats (receiverID, senderID) values ("{receiverId}", "{userID}");')
        print(database("select * from Chats;"))

    print(receiverId, userID)
    print(database("select * from Chats;"))

    return {"message": 'success'}


@app.route('/add_message', methods=['POST'])
def add_message():
    if 'idinfo' not in session:
        return {"message": 'MUST BE LOGGED IN'}

    userEmail = session['idinfo']['email']
    userID = database(f'select id from Users where email="{userEmail}";')[0][0]
    data = request.get_json()

    senderChatID = database(f'select id from Chats where senderID="{userID}" and receiverID="{data["recipient"]}";')
    receiverChatID = database(f'select id from Chats where receiverID="{userID}" and senderID="{data["recipient"]}";')
    chatID = 0

    if senderChatID:
        chatID = senderChatID[0][0]
        sender = True
    elif receiverChatID:
        chatID = receiverChatID[0][0]
        sender = False

    if chatID == 0:
        return {"messages": []}

    database(f'insert into Messages (chatID, message, receiverID, senderID) values ({chatID}, "{data["message"]}", {data["recipient"]}, {userID});')

    return {}


@app.route('/remove_post/<postID>', methods=['POST', 'GET'])
def remove_post(postID):
    if 'idinfo' not in session:
        return {"message": 'MUST BE LOGGED IN'}

    userEmail = session['idinfo']['email']
    userID = database(f'select id from Users where email="{userEmail}";')[0][0]

    postUserID = database(f'select userID from Posts where id={postID};')[0][0]

    if userID == postUserID:
        database(f'delete from Posts where id={postID};')

        return {"message": "success"}

    return {"message": "This is not your post. You cannot mark it as complete"}


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