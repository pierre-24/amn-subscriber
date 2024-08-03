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

        valid_surname = 'betty'
        valid_name = 'vandeput'
        valid_email = 'betty@test.com'

        self.client.post(flask.url_for('main.index'), data={
            'surname': valid_surname,
            'name': valid_name,
            'email': valid_email,
            'gdpr': ''
        }, follow_redirects=False)

        self.assertEqual(Request.query.count(), 0)

    def test_invalid_inputs_ko(self):
        self.assertEqual(Request.query.count(), 0)

        valid_surname = 'betty'
        valid_name = 'vandeput'
        valid_email = 'betty@test.com'

        inputs = [
            (valid_surname, valid_name, valid_email, ''),  # no gdpr
            (valid_surname, valid_name, 'xxx', '1'),  # invalid address
            (valid_surname[0], valid_name, valid_email, '1'),  # to small
            (valid_surname, valid_name[0], valid_email, '1'),  # to small
            (valid_surname * 50, valid_name, valid_email, '1'),  # to large
            (valid_surname, valid_name * 50, valid_email, '1'),  # to large
        ]

        for surname, name, email, gdpr in inputs:

            self.client.post(flask.url_for('main.index'), data={
                'surname': surname,
                'name': name,
                'email': email,
                'gdpr': gdpr
            }, follow_redirects=False)

            self.assertEqual(Request.query.count(), 0)


class TestAdmin(FlaskAppMixture):

    def test_show_results_ok(self):
        self.login()

        valid_surname = 'betty'
        valid_name = 'vandeput'
        valid_email = 'betty@test.com'

        req = Request.create(valid_surname, valid_name, valid_email)
        self.db_session.add(req)
        self.db_session.commit()

        self.assertEqual(Request.query.count(), 1)

        response = self.client.get(flask.url_for('admin.index'), follow_redirects=False)
        self.assertEqual(response.status_code, 200)

        self.assertIn(valid_surname, response.text)
        self.assertIn(valid_name, response.text)
        self.assertNotIn(valid_email, response.text)  # hide full email...
        self.assertIn(req.get_scrambled_email(), response.text)  # ...show only scrambled

    def test_no_login_ko(self):
        response = self.client.get(flask.url_for('admin.index'), follow_redirects=False)
        self.assertEqual(response.status_code, 302)
