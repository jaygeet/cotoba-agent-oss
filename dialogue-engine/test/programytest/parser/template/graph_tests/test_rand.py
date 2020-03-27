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

from programy.parser.exceptions import ParserException
from programy.parser.template.nodes.base import TemplateNode
from programy.parser.template.nodes.rand import TemplateRandomNode

from programytest.parser.template.graph_tests.graph_test_client import TemplateGraphTestClient


class TemplateGraphRandomTests(TemplateGraphTestClient):

    def test_random_template_no_li(self):
        template = ET.fromstring("""
            <template>
                <random>
                </random>
            </template>
            """)
        with self.assertRaises(ParserException):
            self._graph.parse_template_expression(template)

    def test_random_template_none_li(self):
        template = ET.fromstring("""
            <template>
                <random>
                    <lowercase>FAIL</lowercase>
                </random>
            </template>
            """)
        with self.assertRaises(ParserException):
            self._graph.parse_template_expression(template)

    def test_random_template(self):
        template = ET.fromstring("""
            <template>
                <random>
                    <li>1</li>
                    <li>2</li>
                    <li>3</li>
                </random>
            </template>
            """)
        ast = self._graph.parse_template_expression(template)
        self.assertIsNotNone(ast)

        self.assertIsInstance(ast, TemplateNode)
        self.assertIsNotNone(ast.children)
        self.assertIsNotNone(ast.children[0])
        self.assertIsInstance(ast.children[0], TemplateRandomNode)
        self.assertEqual(3, len(ast.children[0].children))

        self.assertIsInstance(ast.children[0].children[0], TemplateNode)
        self.assertIsInstance(ast.children[0].children[1], TemplateNode)
        self.assertIsInstance(ast.children[0].children[2], TemplateNode)

        selection = ast.children[0].resolve(self._client_context)
        self.assertIsNotNone(selection)
        self.assertIn(selection, ['1', '2', '3'])

    def test_random_nested_template(self):
        template = ET.fromstring("""
            <template>
                <random>
                    <li>
                        <random>
                            <li>Say something</li>
                            <li>Say the other</li>
                        </random>
                    </li>
                    <li>
                        <random>
                            <li>Hello world!</li>
                            <li>Goodbye cruel world</li>
                        </random>
                    </li>
                </random>
            </template>
            """)
        ast = self._graph.parse_template_expression(template)

        self.assertIsNotNone(ast)
        self.assertIsInstance(ast, TemplateNode)
        self.assertIsNotNone(ast.children)
        self.assertIsNotNone(ast.children[0])
        self.assertIsInstance(ast.children[0], TemplateRandomNode)
        self.assertEqual(2, len(ast.children[0].children))

        self.assertIsInstance(ast.children[0].children[0], TemplateNode)
        self.assertEqual(1, len(ast.children[0].children[0].children))
        self.assertIsInstance(ast.children[0].children[0].children[0], TemplateRandomNode)
        self.assertEqual(2, len(ast.children[0].children[0].children[0].children))

        self.assertIsInstance(ast.children[0].children[1], TemplateNode)
        self.assertEqual(1, len(ast.children[0].children[1].children))
        self.assertIsInstance(ast.children[0].children[1].children[0], TemplateRandomNode)
        self.assertEqual(2, len(ast.children[0].children[1].children[0].children))

        selection = ast.children[0].resolve(self._client_context)
        self.assertIsNotNone(selection)
        self.assertIn(selection, ['Say something', 'Say the other', 'Hello world!', 'Goodbye cruel world'])
