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
import re

from programy.processors.post.denormalize import DenormalizePostProcessor
from programy.bot import Bot
from programy.config.bot.bot import BotConfiguration
from programy.context import ClientContext

from programytest.client import TestClient


class DenormalizeTests(unittest.TestCase):

    def setUp(self):
        self.client = TestClient()
        self.bot = Bot(config=BotConfiguration(), client=self.client)
        self.bot.brain.denormals.add_to_lookup("dot com", '.com')

    def test_denormalize(self):
        processor = DenormalizePostProcessor()

        context = ClientContext(self.client, "testid")
        context.bot = self.bot
        context.brain = self.bot.brain
        result = processor.process(context, "Hello")
        self.assertIsNotNone(result)
        self.assertEqual("Hello", result)

        result = processor.process(context, "hello dot com")
        self.assertIsNotNone(result)
        self.assertEqual("hello.com", result)
