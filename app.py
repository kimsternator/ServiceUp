from flask import Flask, session, render_template, request, redirect, send_from_directory
from google.oauth2 import id_token
from google.auth.transport import requests
import os

GOOGLE_CLIENT_ID = '675774771358-d9cs6b29kg2ce9tao1l6kq0o55s76fku.apps.googleusercontent.com'

# clientSecret: IQvNBGE53RwdJi3n32nABTmc

app = Flask(__name__)
app.secret_key = 'thissecretisrequired'


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

@app.route('/listing/<id>')
def listing():
    pass

@app.route('/favicon.ico') 
def favicon(): 
    return send_from_directory(os.path.join(app.root_path, 'static/images'), 'favicon.png', mimetype='image/vnd.microsoft.icon')

if __name__ == '__main__':
    app.run(debug=True)
