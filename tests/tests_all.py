import flask

from amn_subscriber.models import Request
from tests import FlaskAppMixture


class TestForm(FlaskAppMixture):
    def test_form_ok(self):
        self.assertEqual(Request.query.count(), 0)

        surname = 'betty'
        name = 'vandeput'
        email = 'betty@test.com'

        self.client.post(flask.url_for('main.index'), data={
            'surname': surname,
            'name': name,
            'email': email,
            'gdpr': '1',
        }, follow_redirects=False)

        self.assertEqual(Request.query.count(), 1)

        req = Request.query.first()
        self.assertEqual(req.surname, surname)
        self.assertEqual(req.name, name)
        self.assertEqual(req.email, email)

    def test_no_gdpr_ko(self):
        self.assertEqual(Request.query.count(), 0)

        surname = 'betty'
        name = 'vandeput'
        email = 'betty@test.com'

        self.client.post(flask.url_for('main.index'), data={
            'surname': surname,
            'name': name,
            'email': email,
        }, follow_redirects=False)

        self.assertEqual(Request.query.count(), 0)

    def test_invalid_email_ko(self):
        self.assertEqual(Request.query.count(), 0)

        surname = 'betty'
        name = 'vandeput'
        email = 'bettyxx'

        self.client.post(flask.url_for('main.index'), data={
            'surname': surname,
            'name': name,
            'email': email,
            'gdpr': '1'
        }, follow_redirects=False)

        self.assertEqual(Request.query.count(), 0)
