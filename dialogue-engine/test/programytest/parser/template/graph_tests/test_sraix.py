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

import xml.etree.ElementTree as ET

from programy.parser.template.nodes.base import TemplateNode
from programy.parser.template.nodes.sraix import TemplateSRAIXNode
from programy.parser.exceptions import ParserException

from programytest.parser.template.graph_tests.graph_test_client import TemplateGraphTestClient


class TemplateGraphSraixTests(TemplateGraphTestClient):

    def test_sraix_template_GeneralRest_attribs(self):
        template = ET.fromstring("""
            <template>
                <sraix default="unknown">
                    <host>http://www.com/</host>
                </sraix>
            </template>
            """)
        ast = self._graph.parse_template_expression(template)
        self.assertIsInstance(ast, TemplateNode)
        self.assertIsNotNone(ast.children)
        self.assertIsNotNone(ast.children[0])
        self.assertIsInstance(ast.children[0], TemplateSRAIXNode)
        self.assertEqual("unknown", ast.children[0]._default)

    def test_sraix_template_PublishedBot_attribs(self):
        template = ET.fromstring("""
            <template>
                <sraix botId="testbot" host="www.co.jp" default="unknown">
                    Ask this question
                </sraix>
            </template>
            """)
        ast = self._graph.parse_template_expression(template)
        self.assertIsInstance(ast, TemplateNode)
        self.assertIsNotNone(ast.children)
        self.assertIsNotNone(ast.children[0])
        self.assertIsInstance(ast.children[0], TemplateSRAIXNode)
        self.assertEqual("testbot", ast.children[0]._botId)
        self.assertEqual("www.co.jp", ast.children[0]._botHost)
        self.assertEqual("unknown", ast.children[0]._default)

    def test_sraix_template_CustomService_attribs(self):
        template = ET.fromstring("""
            <template>
                <sraix service="ask" default="unknown">
                    Ask this question
                </sraix>
            </template>
            """)
        ast = self._graph.parse_template_expression(template)
        self.assertIsInstance(ast, TemplateNode)
        self.assertIsNotNone(ast.children)
        self.assertIsNotNone(ast.children[0])
        self.assertIsInstance(ast.children[0], TemplateSRAIXNode)
        self.assertEqual("ask", ast.children[0]._service)
        self.assertEqual("unknown", ast.children[0]._default)

    def test_sraix_template_no_service(self):
        template = ET.fromstring("""
            <template>
                <sraix>
                    Ask this question
                </sraix>
            </template>
            """)

        with self.assertRaises(ParserException):
            self._graph.parse_template_expression(template)

    def test_sraix_template_GeneralRest_children(self):
        template = ET.fromstring("""
            <template>
                <sraix>
                    <host>hostname</host>
                    <method>POST</method>
                    <query>"userid":"1234567890"</query>
                    <header>"Content-Type":"application/json"</header>
                    <body>Ask this question <get name="somevar" /></body>
                </sraix>
            </template>
            """)
        ast = self._graph.parse_template_expression(template)
        self.assertIsInstance(ast, TemplateNode)
        self.assertIsNotNone(ast.children)
        self.assertIsNotNone(ast.children[0])
        self.assertIsInstance(ast.children[0], TemplateSRAIXNode)
        self.assertEqual("hostname", ast.children[0]._host.children[0].word)
        self.assertEqual("POST", ast.children[0]._method.children[0].word)
        self.assertEqual('"userid":"1234567890"', ast.children[0]._query.children[0].word)
        self.assertEqual('"Content-Type":"application/json"', ast.children[0]._header.children[0].word)

    def test_sraix_template_PublishedBot_children(self):
        template = ET.fromstring("""
            <template>
                <sraix botId="publishedBot">
                    <locale>ja-JP</locale>
                    <time>2019-01-01:00:00:00+09:00</time>
                    <userId>1234567890</userId>
                    <topic>*</topic>
                    <deleteVariable>false</deleteVariable>
                    <metadata>1234567890</metadata>
                    <config>{"config":{"logLevel":"debug"}}</config>
                    Ask this question <get name="somevar" />
                </sraix>
            </template>
            """)
        ast = self._graph.parse_template_expression(template)
        self.assertIsInstance(ast, TemplateNode)
        self.assertIsNotNone(ast.children)
        self.assertIsNotNone(ast.children[0])
        self.assertIsInstance(ast.children[0], TemplateSRAIXNode)
        self.assertEqual("publishedBot", ast.children[0]._botId)
        self.assertEqual("ja-JP", ast.children[0]._locale.children[0].word)
        self.assertEqual("2019-01-01:00:00:00+09:00", ast.children[0]._time.children[0].word)
        self.assertEqual("1234567890", ast.children[0]._userId.children[0].word)
        self.assertEqual("*", ast.children[0]._topic.children[0].word)
        self.assertEqual("false", ast.children[0]._deleteVariable.children[0].word)
        self.assertEqual("1234567890", ast.children[0]._metadata.children[0].word)
        self.assertEqual('{"config":{"logLevel":"debug"}}', ast.children[0]._config.children[0].word)

    def test_sraix_template_CustomService_children(self):
        template = ET.fromstring("""
            <template>
                <sraix service="ask">
                    Ask this question <get name="somevar" />
                </sraix>
            </template>
            """)
        ast = self._graph.parse_template_expression(template)
        self.assertIsInstance(ast, TemplateNode)
        self.assertIsNotNone(ast.children)
        self.assertIsNotNone(ast.children[0])
        self.assertIsInstance(ast.children[0], TemplateSRAIXNode)
        self.assertEqual("ask", ast.children[0]._service)

    def test_sraix_template_GeneralRest_invalid_attribute(self):
        template = ET.fromstring("""
            <template>
                <sraix method="POST" query="userid=1234567890"
                    header="Content-Type=application/json"
                    body="Ask this question">
                    <host>hostname</host>
                </sraix>
            </template>
            """)
        ast = self._graph.parse_template_expression(template)
        self.assertIsInstance(ast, TemplateNode)
        self.assertIsNotNone(ast.children)
        self.assertIsNotNone(ast.children[0])
        self.assertIsInstance(ast.children[0], TemplateSRAIXNode)
        self.assertEqual("hostname", ast.children[0]._host.children[0].word)
        self.assertIsNone(ast.children[0]._method)
        self.assertIsNone(ast.children[0]._query)
        self.assertIsNone(ast.children[0]._header)

    def test_sraix_template_PublishedBot_invalid_attribute(self):
        template = ET.fromstring("""
            <template>
                <sraix botId="publishedBot" apiKey="00000000"
                    locale="ja-JP" time="2019-01-01:00:00:00+09:00"
                    userId="1234567890" topic="*" deleteVariable="false"
                    metadata="1234567890" config="logLevel=debug">
                    Hellow
                </sraix>
            </template>
            """)
        ast = self._graph.parse_template_expression(template)
        self.assertIsInstance(ast, TemplateNode)
        self.assertIsNotNone(ast.children)
        self.assertIsNotNone(ast.children[0])
        self.assertIsInstance(ast.children[0], TemplateSRAIXNode)
        self.assertEqual("publishedBot", ast.children[0]._botId)
        self.assertIsNone(ast.children[0]._locale)
        self.assertIsNone(ast.children[0]._time)
        self.assertIsNone(ast.children[0]._userId)
        self.assertIsNone(ast.children[0]._topic)
        self.assertIsNone(ast.children[0]._deleteVariable)
        self.assertIsNone(ast.children[0]._metadata)
        self.assertIsNone(ast.children[0]._config)

    def test_sraix_template_invalid_children(self):
        template = ET.fromstring("""
            <template>
                <sraix>
                    <host>hostname</host>
                    <botId>publishedBot</botId>
                    <apiKey>00000000</apiKey>
                    <service>test</service>
                    <default>unknown"</default>
                </sraix>
            </template>
            """)
        ast = self._graph.parse_template_expression(template)
        self.assertIsInstance(ast, TemplateNode)
        self.assertIsNotNone(ast.children)
        self.assertIsNotNone(ast.children[0])
        self.assertIsInstance(ast.children[0], TemplateSRAIXNode)
        self.assertEqual("hostname", ast.children[0]._host.children[0].word)
        self.assertIsNone(ast.children[0]._botId)
        self.assertIsNone(ast.children[0]._service)
        self.assertIsNone(ast.children[0]._default)

    def test_sraix_template_GeneralRest_and_PublishedBot(self):
        template = ET.fromstring("""
            <template>
                <sraix botId="publishedBot">
                    <host>hostname</host>
                    Hello
                </sraix>
            </template>
            """)
        with self.assertRaises(ParserException):
            self._graph.parse_template_expression(template)

    def test_sraix_template_GeneralRest_and_CustomService(self):
        template = ET.fromstring("""
            <template>
                <sraix service="test">
                    <host>hostname</host>
                    Hello
                </sraix>
            </template>
            """)
        with self.assertRaises(ParserException):
            self._graph.parse_template_expression(template)

    def test_sraix_template_PublishedBot_CustomService(self):
        template = ET.fromstring("""
            <template>
                <sraix botId="publishedBot" service="test">
                    Hello
                </sraix>
            </template>
            """)
        with self.assertRaises(ParserException):
            self._graph.parse_template_expression(template)
