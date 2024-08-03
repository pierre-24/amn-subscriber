import os

DATA_DIRECTORY = 'data/'


APP_CONFIG = {
    # Flask secret key: generate a new one with
    # `python -c "import random; print(repr(''.join([chr(random.randrange(32, 126)) for _ in range(24)])))"`
    'SECRET_KEY': ';+b&#Yl] U$y7dzmW&IRh$GO',

    # username/password to access admin (change that in production)
    'USERNAME': 'admin',
    'PASSWORD': 'admin',

    # database
    'SQLALCHEMY_TRACK_MODIFICATIONS': False,
    'SQLALCHEMY_DATABASE_URI': 'sqlite:///' + os.path.join(os.path.abspath(DATA_DIRECTORY), 'database.db'),
}

WEBPAGE_INFO = {
    'author_name': 'Pierre Beaujean',
    'site_name': 'Association Anne-Marie Nihoul (Ramillies 2024)',

    'site_version': '0.0.1',
}

# Load the production settings, overwrite the existing ones if needed
try:
    from settings_prod import *  # noqa
except ImportError:
    pass
