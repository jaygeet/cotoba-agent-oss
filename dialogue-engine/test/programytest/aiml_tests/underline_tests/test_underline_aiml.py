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

from programytest.client import TestClient


class UnderlineTestClient(TestClient):

    def __init__(self):
        TestClient.__init__(self)

    def load_storage(self):
        super(UnderlineTestClient, self).load_storage()
        self.add_default_stores()
        self.add_categories_store([os.path.dirname(__file__)])


class UnderlineAIMLTests(unittest.TestCase):

    def setUp(self):
        client = UnderlineTestClient()
        self._client_context = client.create_client_context("testid")

    def test_underline_first(self):
        response = self._client_context.bot.ask_question(self._client_context,  "SAY HEY")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'STAR IS SAY.')

    def test_underline_first_multi_words(self):
        response = self._client_context.bot.ask_question(self._client_context,  "THE MAN SAYS HEY")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'STAR IS THE MAN SAYS.')

    def test_underline_last(self):
        response = self._client_context.bot.ask_question(self._client_context,  "HELLO KEIFFBOT")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'HI KEIFFBOT.')

    def test_underline_last_multi_words(self):
        response = self._client_context.bot.ask_question(self._client_context,  "HELLO KEIFFBOT MATE")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'HI KEIFFBOT MATE.')

    def test_multi_underline(self):
        response = self._client_context.bot.ask_question(self._client_context, "WELL HI THERE")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'YOU SAID WELL AND THERE.')

    def test_multi_underline_mulit_words(self):
        response = self._client_context.bot.ask_question(self._client_context, "WELL THEN HI THERE MATE")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'YOU SAID WELL THEN AND THERE MATE.')

    def test_underline_middle(self):
        response = self._client_context.bot.ask_question(self._client_context, "GOODBYE KEIFF SEEYA")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'LATER KEIFF.')

    def test_underline_middle_mulit_words(self):
        response = self._client_context.bot.ask_question(self._client_context, "GOODBYE KEIFF MATE SEEYA")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'LATER KEIFF MATE.')
