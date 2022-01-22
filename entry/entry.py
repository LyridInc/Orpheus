import os

from flask import Flask, render_template, request, redirect, session, url_for
from werkzeug.middleware.proxy_fix import ProxyFix
from dotenv import load_dotenv

load_dotenv()

from backend import request_functions
from backend import spotify_user_auth


# App setup
app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_host=1)
#CORS(app)
### Set app secret
app.secret_key = os.environ.get('APP_SECRET', '')
### Set content security policy and enable Talisman
#SELF = "'self'"
#talisman = Talisman(
#    app,
#    content_security_policy={
#        'default-src': [SELF, '*.gstatic.com', '*.fontawesome.com',
#                        '*.jsdelivr.net', '*.googleapis.com', '*.spotify.com'],
#    },
#    content_security_policy_nonce_in=['script-src'],
#    feature_policy={
#        'geolocation': '\'none\'',
#    }
#)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/auth')
def auth():
    return redirect(spotify_user_auth.AUTH_URL)


@app.route('/callback/')
def callback():
    auth_token = request.args['code']
    session['user_auth'] = auth_token
    session['auth_header'] = spotify_user_auth.authorize(auth_token)
    return redirect(url_for('playlist_creation'))


@app.route('/selections', methods=['POST'])
def save_selections():
    response = request.form
    session['selections'] = response
    return redirect(url_for('auth'))


@app.route('/playlist')
def playlist_creation():
    pump_level = session['selections']['pumped']
    bpm = session['selections']['bpm']
    complete_playlist_data = request_functions.get_complete_playlist(session['auth_header'], [pump_level, bpm])
    return render_template('final.html', playlist_data=complete_playlist_data, app_url=os.environ.get('APP_URL', ''))
