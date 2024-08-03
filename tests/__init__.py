from unittest import TestCase

from amn_subscriber import create_app


class FlaskAppMixture(TestCase):
    def setUp(self) -> None:

        # create app
        self.app = create_app()
        self.app.config.update(
            TESTING=True
        )

        # push context
        self.app_context = self.app.app_context()
        self.app_context.push()

        # create client
        self.client = self.app.test_client(use_cookies=True)
