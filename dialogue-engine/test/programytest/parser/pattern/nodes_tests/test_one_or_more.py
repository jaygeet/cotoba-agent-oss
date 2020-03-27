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
from programytest.parser.base import ParserTestsBaseClass

from programy.parser.exceptions import ParserException
from programy.parser.pattern.nodes.oneormore import PatternOneOrMoreWildCardNode
from programy.parser.pattern.nodes.word import PatternWordNode
from programy.dialog.sentence import Sentence


class PatternOneOrMoreWildCardNodeTests(ParserTestsBaseClass):

    def test_invalid_wildcard(self):
        with self.assertRaises(ParserException):
            node = PatternOneOrMoreWildCardNode("X")
            self.assertIsNone(node)

    def test_star(self):
        node = PatternOneOrMoreWildCardNode("*")
        self.assertIsNotNone(node)

        self.assertFalse(node.is_root())
        self.assertFalse(node.is_priority())
        self.assertFalse(node.is_zero_or_more())
        self.assertTrue(node.is_one_or_more())
        self.assertFalse(node.is_set())
        self.assertFalse(node.is_bot())
        self.assertFalse(node.is_template())
        self.assertFalse(node.is_that())
        self.assertFalse(node.is_topic())
        self.assertTrue(node.is_wildcard())
        self.assertFalse(node.is_iset())
        self.assertFalse(node.is_nlu())

        self.assertIsNotNone(node.children)
        self.assertFalse(node.has_children())

        self.assertEqual(node.wildcard, "*")

        sentence = Sentence(self._client_context.brain.tokenizer, "*")

        self.assertTrue(node.equivalent(PatternOneOrMoreWildCardNode("*")))
        result = node.equals(self._client_context, sentence, 0)
        self.assertFalse(result.matched)
        self.assertEqual(node.to_string(), "ONEORMORE [*] [P(0)^(0)#(0)C(0)_(0)*(0)To(0)Th(0)Te(0)] wildcard=[*]")
        self.assertEqual('<oneormore wildcard="*">\n</oneormore>\n', node.to_xml(self._client_context))

        self.assertFalse(node.equivalent(PatternWordNode("test")))

    def test_underline(self):
        node = PatternOneOrMoreWildCardNode("_")
        self.assertIsNotNone(node)

        self.assertFalse(node.is_root())
        self.assertFalse(node.is_priority())
        self.assertFalse(node.is_zero_or_more())
        self.assertTrue(node.is_one_or_more())
        self.assertFalse(node.is_set())
        self.assertFalse(node.is_bot())
        self.assertFalse(node.is_template())
        self.assertFalse(node.is_that())
        self.assertFalse(node.is_topic())
        self.assertTrue(node.is_wildcard())

        self.assertIsNotNone(node.children)
        self.assertFalse(node.has_children())

        self.assertEqual(node.wildcard, "_")

        sentence = Sentence(self._client_context.brain.tokenizer, "*")

        self.assertTrue(node.equivalent(PatternOneOrMoreWildCardNode("_")))
        result = node.equals(self._client_context, sentence, 0)
        self.assertFalse(result.matched)
        self.assertEqual(node.to_string(), "ONEORMORE [*] [P(0)^(0)#(0)C(0)_(0)*(0)To(0)Th(0)Te(0)] wildcard=[_]")
        self.assertEqual('<oneormore wildcard="_">\n</oneormore>\n', node.to_xml(self._client_context))

        self.assertFalse(node.equivalent(PatternWordNode("test")))

    def test_to_xml(self):
        node1 = PatternOneOrMoreWildCardNode("*")
        self.assertEqual('<oneormore wildcard="*">\n</oneormore>\n', node1.to_xml(self._client_context))
        self.assertEqual('<oneormore userid="*" wildcard="*">\n</oneormore>\n', node1.to_xml(self._client_context, include_user=True))

        node2 = PatternOneOrMoreWildCardNode("*", userid="testid")
        self.assertEqual('<oneormore wildcard="*">\n</oneormore>\n', node2.to_xml(self._client_context))
        self.assertEqual('<oneormore userid="testid" wildcard="*">\n</oneormore>\n', node2.to_xml(self._client_context, include_user=True))

    def test_to_string(self):
        node1 = PatternOneOrMoreWildCardNode("*")
        self.assertEqual("ONEORMORE [*]", node1.to_string(verbose=False))
        self.assertEqual("ONEORMORE [*] [P(0)^(0)#(0)C(0)_(0)*(0)To(0)Th(0)Te(0)] wildcard=[*]", node1.to_string(verbose=True))

        node1 = PatternOneOrMoreWildCardNode("*", userid="testid")
        self.assertEqual("ONEORMORE [*]", node1.to_string(verbose=False))
        self.assertEqual("ONEORMORE [testid] [P(0)^(0)#(0)C(0)_(0)*(0)To(0)Th(0)Te(0)] wildcard=[*]", node1.to_string(verbose=True))

    def test_equivalent_userid(self):
        node1 = PatternOneOrMoreWildCardNode("*")
        node2 = PatternOneOrMoreWildCardNode("*")
        node3 = PatternOneOrMoreWildCardNode("*", userid="testuser")

        self.assertTrue(node1.equivalent(node2))
        self.assertFalse(node1.equivalent(node3))
