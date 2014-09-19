# !/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask, url_for, request, render_template, redirect, \
    send_from_directory, session, flash, make_response, g, abort, escape
from werkzeug.utils import secure_filename
import os

basedir = os.path.abspath(os.path.dirname(__file__))
UPLOAD_FOLDER = os.path.normpath(basedir + '/upload')
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
USERNAME = 'admin'
PASSWORD = 'default'
SECRET_KEY = os.urandom(24)

app = Flask(__name__)
app.config.from_object(__name__)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@app.before_request
def before_request():
    g.user = None
    if 'user' in session:
        g.user = escape(session['user'])


@app.route('/')
def index():
    if not g.user:
        return render_template('index.html')
        # response = make_response(render_template('index.html', user=abc:w
        # ))
    else:
        resp = make_response(render_template('index.html'))
        resp.set_cookie('username', g.user)
        return resp


@app.route('/user/')
@app.route('/user/<name>')
def user(name=None):
    return render_template('user.html', name=name)
    # use flask.request flask.session flask.g get_flashed_messages()


@app.route('/post/<int:post_id>')
def show_post(post_id):
    # show the post with the given id, the id is an integer
    return 'Post %d' % post_id


@app.route('/projects/')
def projects():
    return 'The project page'


@app.route('/about')
def about():
    return 'The about page'


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME'] or app.config['PASSWORD'] != request.form['password']:
            error = 'Wrong Username and password combination.'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            session['user'] = request.form['username']
            session["remember"] = "set"
            return redirect(url_for('index'))
    return render_template('login.html', error=error)


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('user', None)
    flash('You were logged out')
    return redirect(url_for('index'))


# File Upload
@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return send_from_directory(app.config['UPLOAD_FOLDER'],
                                       filename)
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form action="" method=post enctype=multipart/form-data>
      <p><input type=file name=file>
         <input type=submit value=Upload>
    </form>
    '''


    #    Static Files
    url_for('static', filename='style.css')


@app.route('/redirect/')
def test_redirect():
    return redirect(url_for('test_error'))


@app.route('/test_error/')
def test_error():
    abort(404)


with app.test_request_context():
    print url_for('user', name="John Doe")
    print url_for('index', next='/')


@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404


@app.route('/setcookie')
def set_cookie():
    count = request.cookies.get('num')
    resp = make_response(render_template('index.html'))
    if 'num' in request.cookies:
        count = int(request.cookies['num']) + 1
    else:
        count = 0
    resp.set_cookie('num', value=str(count), max_age=60, expires=None, domain='*.example.com')  # 60s
    return resp


@app.route('/tools')
def tools():
    return render_template('tools.html')


app.debug = True
if __name__ == '__main__':
    app.run(host="localhost", port=8888, debug=True)
    # ace