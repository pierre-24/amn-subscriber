import pathlib
import shutil
import click
import flask
from flask import Flask
from flask.cli import with_appcontext
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap5
import flask_login

from amn_subscriber.filters import filters

db = SQLAlchemy(session_options={'expire_on_commit': False})
bootstrap = Bootstrap5()
login_manager = flask_login.LoginManager()


class Config:
    # Flask
    SERVER_NAME = '127.0.0.1:5000'
    PREFERRED_URL_SCHEME = 'http'

    # Flask secret key: generate a new one with
    # `python -c "import random; print(repr(''.join([chr(random.randrange(32, 126)) for _ in range(24)])))"`
    SECRET_KEY = ';+b&#Yl] U$y7dzmW&IRh$GO'

    # username/password to access admin (change that in production)
    USERNAME = 'admin'
    PASSWORD = 'admin'

    DATA_DIRECTORY = pathlib.Path('data/')

    # database
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    WEBPAGE_INFO = {
        'author_name': 'Pierre',
        'site_name': 'Association Anne-Marie Nihoul (Ramillies 2024)',

        'site_version': '0.0.1',
    }


class User(flask_login.UserMixin):
    def __init__(self, id_):
        super().__init__()
        self.id = id_


@login_manager.user_loader
def load_user(login):
    if login != flask.current_app.config['USERNAME']:
        return

    return User(login)


@click.command('init')
@with_appcontext
def init_command():
    """Initializes stuffs:
    + data directory
    + database
    """

    # directories
    data_dir = flask.current_app.config['DATA_DIRECTORY']

    if data_dir.exists():
        shutil.rmtree(data_dir)

    data_dir.mkdir()
    print('!! Data directory in {}'.format(data_dir))

    # DB:
    db.create_all()
    print('!! database created')


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config())
    app.config.from_pyfile('settings.py', silent=True)

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///{}'.format(
        app.config['DATA_DIRECTORY'].resolve() / 'database.db')

    # init stuffs
    db.init_app(app)
    bootstrap.init_app(app)

    login_manager.init_app(app)
    login_manager.login_view = 'admin.login'  # automatic redirection

    # add CLI
    app.cli.add_command(init_command)

    # add blueprint
    from amn_subscriber.blueprints import bp_main, bp_admin
    app.register_blueprint(bp_main)
    app.register_blueprint(bp_admin)

    # add filters
    app.jinja_env.filters.update(**filters)

    return app
