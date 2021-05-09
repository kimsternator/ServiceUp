from flask import Flask, session, render_template, request
from google.oauth2 import id_token
from google.auth.transport import requests

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
    return ''

@app.route('/profile/<id>')
def profile():
    pass

@app.route('/listing/<id>')
def listing():
    pass

if __name__ == '__main__':
    app.run(debug=True)
