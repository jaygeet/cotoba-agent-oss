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

from programy.dialog.sentence import Sentence
from programy.dialog.question import Question
from programy.dialog.conversation import Conversation
from programy.bot import Bot
from programy.config.bot.bot import BotConfiguration

from programytest.client import TestClient


class SentimentTests(unittest.TestCase):

    def setUp(self):
        self._client = TestClient()

        config = BotConfiguration()
        config.sentiment_analyser._classname = "programy.sentiment.textblob_sentiment.TextBlobSentimentAnalyser"

        self.client_context = self._client.create_client_context("testuser")

        self.client_context._bot = Bot(config=config, client=self._client)
        self.client_context._bot.initiate_sentiment_analyser()

    def test_sentence_sentiment(self):

        sentence = Sentence(self.client_context._bot.brain.tokenizer, "HELLO")
        sentence.calculate_sentinment_score(self.client_context)

        self.assertEqual(0.00, sentence.positivity)
        self.assertEqual(0.00, sentence.subjectivity)

        sentence = Sentence(self.client_context._bot.brain.tokenizer, "I hate you")
        sentence.calculate_sentinment_score(self.client_context)

        self.assertEqual(-0.8, sentence.positivity)
        self.assertEqual(0.9, sentence.subjectivity)

    def test_question_sentiment(self):

        question = Question.create_from_text(self.client_context, "Hello There. How Are you")

        for sentence in question.sentences:
            sentence.calculate_sentinment_score(self.client_context)

        positivity, subjectivity = question.calculate_sentinment_score()
        self.assertEqual(0.0, positivity)
        self.assertEqual(0.0, subjectivity)

        question = Question.create_from_text(self.client_context, "I hate you. Your car is rubbish")
        question.recalculate_sentinment_score(self.client_context)

        positivity, subjectivity = question.calculate_sentinment_score()
        self.assertEqual(-0.4, positivity)
        self.assertEqual(0.45, subjectivity)

    def test_conversation_sentiment(self):
        conversation = Conversation(self.client_context)

        question1 = Question.create_from_text(self.client_context, "I am so unhappy")
        conversation.record_dialog(question1)

        question2 = Question.create_from_text(self.client_context, "I do not like the colour red")
        conversation.record_dialog(question2)

        question3 = Question.create_from_text(self.client_context, "Custard makes me feel sick")
        conversation.record_dialog(question3)

        conversation.recalculate_sentiment_score(self.client_context)

        positivity, subjectivity = conversation.calculate_sentiment_score()
        self.assertEqual(-0.4380952380952381, positivity)
        self.assertEqual(0.5857142857142857, subjectivity)
