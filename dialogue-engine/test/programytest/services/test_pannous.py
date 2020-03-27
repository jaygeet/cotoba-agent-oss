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
import json

from programy.services.pannous import PannousService, PannousAPI
from programy.services.service import BrainServiceConfiguration
from programytest.services.mock_requests import MockRequestsAPI

from programytest.client import TestClient


class PannousAPITests(unittest.TestCase):

    def test_ask_question_valid_json(self):

        request_api = MockRequestsAPI()
        pannous_api = PannousAPI(request_api=request_api)
        request_api._response = json.loads("""
        {
            "output": [
                { "actions": { "say": {"text": "Hello"} } }
            ]
        }
        """)
        response = pannous_api.ask_question("http://testurl", "Hello", "testid")
        self.assertEqual(response, "Hello")

    def test_ask_question_no_response(self):

        with self.assertRaises(Exception) as raised:
            request_api = MockRequestsAPI(response=None)
            pannous_api = PannousAPI(request_api=request_api)
            pannous_api.ask_question("http://testurl", "Hello", "testid")
        self.assertEqual(raised.exception.args[0], "No response from pannous service")

    def test_ask_question_missing_text(self):

        with self.assertRaises(Exception) as raised:
            request_api = MockRequestsAPI()
            pannous_api = PannousAPI(request_api=request_api)
            request_api._response = json.loads("""
            {
                "output": [
                    { "actions": { "say": {"response": "Hello"} } }
                ]
            }
            """)
            pannous_api.ask_question("http://testurl", "Hello", "testid")
        self.assertEqual(raised.exception.args[0], "'text' section missing from output[0]['actions']['say'] in pannous json_data")

    def test_ask_question_missing_say(self):

        with self.assertRaises(Exception) as raised:
            request_api = MockRequestsAPI()
            pannous_api = PannousAPI(request_api=request_api)
            request_api._response = json.loads("""
            {
                "output": [
                    { "actions": { "said": {"response": "Hello"} } }
                ]
            }
            """)
            pannous_api.ask_question("http://testurl", "Hello", "testid")
        self.assertEqual(raised.exception.args[0], "'say' section missing from output[0]['actions'] in pannous json_data")

    def test_ask_question_missing_actions(self):

        with self.assertRaises(Exception) as raised:
            request_api = MockRequestsAPI()
            pannous_api = PannousAPI(request_api=request_api)
            request_api._response = json.loads("""
            {
                "output": [
                    { "items": { "say": {"response": "Hello"} } }
                ]
            }
            """)
            pannous_api.ask_question("http://testurl", "Hello", "testid")
        self.assertEqual(raised.exception.args[0], "'actions' section in output[0] in pannous json_data")

    def test_ask_question_empty_output(self):

        with self.assertRaises(Exception) as raised:
            request_api = MockRequestsAPI()
            pannous_api = PannousAPI(request_api=request_api)
            request_api._response = json.loads("""
            {
                "output": []
            }
            """)
            pannous_api.ask_question("http://testurl", "Hello", "testid")
        self.assertEqual(raised.exception.args[0], "'output' section has no elements in pannous json_data")

        with self.assertRaises(Exception) as raised:
            request_api = MockRequestsAPI()
            pannous_api = PannousAPI(request_api=request_api)
            request_api._response = json.loads("""
            {
                "output": null
            }
            """)
            pannous_api.ask_question("http://testurl", "Hello", "testid")
        self.assertEqual(raised.exception.args[0], "'output' section has no elements in pannous json_data")

    def test_ask_question_missing_output(self):

        with self.assertRaises(Exception) as raised:
            request_api = MockRequestsAPI()
            pannous_api = PannousAPI(request_api=request_api)
            request_api._response = json.loads("""
            {
                "result": [
                    { "items": { "say": {"response": "Hello"} } }
                ]
            }
            """)
            pannous_api.ask_question("http://testurl", "Hello", "testid")
        self.assertEqual(raised.exception.args[0], "'output' section missing from pannous json_data")


class MockPannousAPI(object):

    def __init__(self, response=None, throw_exception=False):
        self._throw_exception = throw_exception
        self._response = response

    def ask_question(self, url, question, login):
        if self._throw_exception is True:
            raise Exception(self._response)
        else:
            return self._response


class PannousServiceTests(unittest.TestCase):

    def setUp(self):
        client = TestClient()
        client.add_license_keys_store()
        self._client_context = client.create_client_context("testid")

    def test_ask_question(self):

        config = BrainServiceConfiguration("pannous")
        config._url = "http://test.pandora.url"

        service = PannousService(config=config, api=MockPannousAPI(response="Test pannous response"))
        self.assertIsNotNone(service)

        response = service.ask_question(self._client_context, "what is a cat")
        self.assertEqual("Test pannous response", response)

    def test_ask_question_no_url(self):

        config = BrainServiceConfiguration("pannous")

        with self.assertRaises(Exception) as raised:
            service = PannousService(config=config, api=MockPannousAPI(response="Test pannous response"))
            self.assertIsNotNone(service)

            response = service.ask_question(self._client_context, "what is a cat")
            self.assertEqual("", response)

        self.assertEqual(raised.exception.args[0], "Undefined url parameter")

    def test_ask_question_no_license_key(self):

        self._client_context.client.license_keys._keys.clear()

        config = BrainServiceConfiguration("pannous")
        config._url = "http://test.pandora.url"

        service = PannousService(config=config, api=MockPannousAPI(response="Test pannous response"))
        self.assertIsNotNone(service)

        response = service.ask_question(self._client_context, "what is a cat")
        self.assertEqual("", response)

    def test_ask_question_with_exception(self):

        config = BrainServiceConfiguration("pannous")
        config._url = "http://test.pandora.url"

        service = PannousService(config=config, api=MockPannousAPI(response="Some wierd error", throw_exception=True))
        self.assertIsNotNone(service)

        response = service.ask_question(self._client_context, "what is a cat")
        self.assertEqual("", response)
