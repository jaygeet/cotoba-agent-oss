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

from programy.utils.newsapi.newsapi import NewsAPI
from programytest.client import TestClient


class MockResponse(object):

    def __init__(self, status_code, headers, data):
        self.status_code = status_code
        self.headers = headers
        self.data = data

    def json(self):
        return self.data


class MockNewsApiApi(object):

    def __init__(self):
        self._repsonse = ""

    @property
    def response(self):
        return self._repsonse

    @response.setter
    def response(self, response):
        self._repsonse = response

    def get_news(self, url):
        return self._repsonse


class NewsAPITests(unittest.TestCase):

    def test_missing_license_keys(self):
        with self.assertRaises(Exception):
            NewsAPI(None)

    def test_missing_keys(self):
        client = TestClient()

        with self.assertRaises(Exception):
            NewsAPI(client.license_keys)

    def test_format_url(self):
        self.assertEqual("https://newsapi.org/v1/articles?source=testservice&sortBy=top&apiKey=key", NewsAPI._format_url("testservice", "key"))
        self.assertEqual("https://newsapi.org/v1/articles?source=testservice&sortBy=bottom&apiKey=key", NewsAPI._format_url("testservice", "key", sort_by="bottom"))

    def test_get_news_feed_articles(self):
        client = TestClient()
        client.add_license_keys_store()

        mock_api = MockNewsApiApi()

        newsapi = NewsAPI(client.license_keys, mock_api)
        self.assertIsNotNone(newsapi)

        mock_api.response = MockResponse(200, {"content-type": "application/json"}, json.loads("""
        {
            "articles": [
                {
                "title":        "test title",
                "description":  "test description",
                "publishedAt":  "test publishedAt",
                "author":       "test author",
                "url":          "test url",
                "urlToImage":   "test urlToImage"
                }
            ]
        }
        """))
        mock_url = NewsAPI._format_url("testservice", "key")

        articles = newsapi._get_news_feed_articles(mock_url, 10, True, False)
        self.assertIsNotNone(articles)
        self.assertEqual(1, len(articles))
        self.assertEqual("test title", articles[0].title)
        self.assertEqual("test description", articles[0].description)
        self.assertEqual("test publishedAt", articles[0].published_at)
        self.assertEqual("test author", articles[0].author)
        self.assertEqual("test url", articles[0].url)
        self.assertEqual("test urlToImage", articles[0].url_to_image)

    def test_get_news_feed_articles_none_200_response(self):
        client = TestClient()
        client.add_license_keys_store()

        mock_api = MockNewsApiApi()

        newsapi = NewsAPI(client.license_keys, mock_api)
        self.assertIsNotNone(newsapi)

        mock_api.response = MockResponse(401, {"content-type": "application/json"}, json.loads("""
        {
            "articles": [
                {
                "title":        "test title",
                "description":  "test description",
                "publishedAt":  "test publishedAt",
                "author":       "test author",
                "url":          "test url",
                "urlToImage":   "test urlToImage"
                }
            ]
        }
        """))
        mock_url = NewsAPI._format_url("testservice", "key")

        articles = newsapi._get_news_feed_articles(mock_url, 10, True, False)
        self.assertIsNotNone(articles)
        self.assertEqual(0, len(articles))

    def test_get_news_feed_articles_content_not_json(self):
        client = TestClient()
        client.add_license_keys_store()

        mock_api = MockNewsApiApi()

        newsapi = NewsAPI(client.license_keys, mock_api)
        self.assertIsNotNone(newsapi)

        mock_api.response = MockResponse(200, {"content-type": "application/xml"}, None)

        mock_url = NewsAPI._format_url("testservice", "key")

        articles = newsapi._get_news_feed_articles(mock_url, 10, True, False)
        self.assertIsNotNone(articles)
        self.assertEqual(0, len(articles))

    def test_get_news_feed_articles_no_articles(self):
        client = TestClient()
        client.add_license_keys_store()

        mock_api = MockNewsApiApi()

        newsapi = NewsAPI(client.license_keys, mock_api)
        self.assertIsNotNone(newsapi)

        mock_api.response = MockResponse(200, {"content-type": "application/json"}, json.loads("""
        {
        }
        """))
        mock_url = NewsAPI._format_url("testservice", "key")

        articles = newsapi._get_news_feed_articles(mock_url, 10, True, False)
        self.assertIsNotNone(articles)
        self.assertEqual(0, len(articles))

    def test_get_news_feed_articles_no_articles_included(self):
        client = TestClient()
        client.add_license_keys_store()

        mock_api = MockNewsApiApi()

        newsapi = NewsAPI(client.license_keys, mock_api)
        self.assertIsNotNone(newsapi)

        mock_api.response = MockResponse(200, {"content-type": "application/json"}, json.loads("""
        {
            "articles": [
            ]
        }
        """))
        mock_url = NewsAPI._format_url("testservice", "key")

        articles = newsapi._get_news_feed_articles(mock_url, 10, True, False)
        self.assertIsNotNone(articles)
        self.assertEqual(0, len(articles))
