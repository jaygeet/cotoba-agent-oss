"""
Copyright (c) 2020 COTOBA DESIGN, Inc.

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
documentation files (the "Software"), to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software,
and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO
THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""
import unittest
import os

from programy.config.brain.security import BrainSecurityAuthenticationConfiguration
from programy.security.authenticate.authenticator import Authenticator
from programy.utils.substitutions.substitues import Substitutions

from programytest.client import TestClient


class MockAuthenticationService(Authenticator):

    AUTHENTICATION_SUCCESS = False

    def __init__(self, configuration: BrainSecurityAuthenticationConfiguration):
        Authenticator.__init__(self, configuration)

    def authenticate(self, context: str):
        return MockAuthenticationService.AUTHENTICATION_SUCCESS


class AuthenticateTestClient(TestClient):

    def __init__(self):
        TestClient.__init__(self)

    def load_storage(self):
        super(AuthenticateTestClient, self).load_storage()
        self.add_default_stores()
        self.add_categories_store([os.path.dirname(__file__)])

    def load_configuration(self, arguments, subs: Substitutions = None):
        super(AuthenticateTestClient, self).load_configuration(arguments)
        self.configuration.client_configuration.configurations[0].configurations[0].security._authentication = BrainSecurityAuthenticationConfiguration("authentication")
        self.configuration.client_configuration.configurations[0].configurations[0].security.authentication._classname = \
            "programytest.aiml_tests.authenticate_tests.test_authenticate_aiml.MockAuthenticationService"
        self.configuration.client_configuration.configurations[0].configurations[0].security.authentication._denied_srai = "AUTHENTICATED_FAILED"


class AuthenticateAIMLTests(unittest.TestCase):

    def setUp(self):
        client = AuthenticateTestClient()
        self._client_context = client.create_client_context("testid")

    def test_authentication_passed(self):
        MockAuthenticationService.AUTHENTICATION_SUCCESS = True

        response = self._client_context.bot.ask_question(self._client_context, "AUTHENTICATE PASSED")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'User allowed.')

    def test_authentication_failed_with_srai(self):
        MockAuthenticationService.AUTHENTICATION_SUCCESS = False
        self._client_context.brain.security.authentication.configuration._denied_srai = "AUTHENTICATED_FAILED"
        self._client_context.brain.security.authentication.configuration._denied_text = "AUTHENTICATED FAILED TEXT"

        response = self._client_context.bot.ask_question(self._client_context, "AUTHENTICATE FAIL SRAI")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'Authentication failed.')

    def test_authentication_failed_with_unknown_srai(self):
        MockAuthenticationService.AUTHENTICATION_SUCCESS = False
        self._client_context.brain.security.authentication.configuration._denied_srai = "AUTHENTICATED_FAILEDX"
        self._client_context.brain.security.authentication.configuration._denied_text = "AUTHENTICATED FAILED TEXT"

        response = self._client_context.bot.ask_question(self._client_context, "AUTHENTICATE FAIL SRAI")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'AUTHENTICATED FAILED TEXT.')

    def test_authentication_failed_with_text(self):
        MockAuthenticationService.AUTHENTICATION_SUCCESS = False
        self._client_context.brain.security.authentication.configuration._denied_srai = None
        self._client_context.brain.security.authentication.configuration._denied_text = "AUTHENTICATED FAILED TEXT"

        response = self._client_context.bot.ask_question(self._client_context, "AUTHENTICATE FAIL TEXT")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'AUTHENTICATED FAILED TEXT.')
