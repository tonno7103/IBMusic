import os

from dotenv import load_dotenv
from flask import render_template, redirect, url_for, session, request

from bot import start
from server import app, socket

load_dotenv()


@app.route('/')
def error_index():
    return render_template("error.html")


@app.route('/queue')
def queue():
    if session.get('guild_id') is None:
        return render_template("error.html")

    return render_template('index.html', user_code=session.get('code'), guild_id=session.get('guild_id'))


@app.route('/<path:path>')
def index(path):
    if path != 'favicon.ico':
        session['guild_id'] = path

    return redirect(url_for('login'))


@app.route('/static/empty.png')
def empty():
    return app.send_static_file('empty.png')


@app.route('/login', methods=['GET'])
def login():
    return redirect(os.getenv('OAUTH_URL'))


@app.route('/callback', methods=['GET'])
def oauth_callback():
    session['code'] = request.args.get('code')
    return redirect(url_for('queue'))


if __name__ == '__main__':
    start()
    socket.run(app, allow_unsafe_werkzeug=True, host='0.0.0.0', port='80')
