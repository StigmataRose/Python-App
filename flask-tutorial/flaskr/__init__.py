import os
from markupsafe import escape
from flask import Flask, url_for, request, redirect
from flask import render_template

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route('/hello/')
    @app.route('/hello/<name>')
    def hello(name=None):
        return render_template('hello.html', name=name)

    @app.route('/')
    def index():
        return 'index'

    # Define the log_the_user_in function
    def log_the_user_in(username):
    # Perform actions to log in the user
    # For demonstration purposes, I'll simply redirect to a dashboard page
        return redirect(url_for('dashboard', username=username))

    # Define the valid_login function
    def valid_login(username, password):
        # Implement your login validation logic here
        # For demonstration purposes, I'll assume a simple check
        return username == "admin" and password == "password"

    @app.route('/login', methods=['POST', 'GET'])
    def login():
        error = None
        if request.method == 'POST':
            if valid_login(request.form['username'],
                        request.form['password']):
                return log_the_user_in(request.form['username'])
            else:
                error = 'Invalid username/password'
        # the code below is executed if the request method
        # was GET or the credentials were invalid
        return render_template('login.html', error=error)

    @app.route('/user/<username>')
    def profile(username):
        return f'{username}\'s profile'

    with app.test_request_context():
        print(url_for('index'))
        print(url_for('login'))
        print(url_for('login', next='/'))
        print(url_for('profile', username='John Doe'))


    # Define the dashboard route
    @app.route('/dashboard/<username>')
    def dashboard(username):
        return render_template('dashboard.html', username=username)
    
    return app

    