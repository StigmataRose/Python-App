import os
from markupsafe import escape
from flask import Flask


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

    @app.route("/<name>")
    def hello(name):
        return f"Hello, {escape(name)}!"

    # a simple page that says hello
    @app.route('/')
    def home():
        return 'Home'

    @app.route('/projects/')
    def projects():
        return 'The project page'

    @app.route('/about')
    def about():
        return 'The about page'

    @app.route('/user/<username>')
    def show_user_profile(username):
    # show the user profile for that user
        return f'User {escape(username)}'

    @app.route('/post/<int:post_id>')
    def show_post(post_id):
    # show the post with the given id, the id is an integer
        return f'Post {post_id}'

    @app.route('/path/<path:subpath>')
    def show_subpath(subpath):
    # show the subpath after /path/
        return f'Subpath {escape(subpath)}'

    return app

    