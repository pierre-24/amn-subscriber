import tempfile
import shutil
import pathlib

from unittest import TestCase

import flask

from amn_subscriber import create_app, Config, db


class FlaskAppMixture(TestCase):
    def setUp(self) -> None:

        self.data_files_directory = pathlib.Path(tempfile.mkdtemp())
        Config.DATA_DIRECTORY = self.data_files_directory

        # create app
        self.app = create_app()
        self.app.config.update(
            TESTING=True,
            WTF_CSRF_ENABLED=False
        )

        # push context
        self.app_context = self.app.app_context()
        self.app_context.push()

        # db
        db.create_all()
        self.db_session = db.session

        # create client
        self.client = self.app.test_client(use_cookies=True)

    def tearDown(self):
        shutil.rmtree(self.data_files_directory)
        self.app_context.pop()

    def login(self):
        """Login client."""

        self.client.post(flask.url_for('admin.login'), data={
            'login': flask.current_app.config['USERNAME'],
            'password': flask.current_app.config['PASSWORD']
        }, follow_redirects=False)

        response = self.client.get(flask.url_for('admin.index'), follow_redirects=False)
        self.assertEqual(response.status_code, 200)

    def logout(self):
        """Logout client"""
        self.client.get(flask.url_for('admin.logout'), follow_redirects=False)

        response = self.client.get(flask.url_for('admin.index'), follow_redirects=False)
        self.assertEqual(response.status_code, 302)
