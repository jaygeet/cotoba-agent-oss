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

from programytest.parser.pattern.matching.base import PatternMatcherBaseClass


class PatternMatcherTests(PatternMatcherBaseClass):

    def test_star_tree_matching_single(self):

        self.add_pattern_to_graph(pattern="*", topic="X", that="Y", template="1")

        context = self.match_sentence("A B D", topic="X", that="Y")
        self.assertIsNotNone(context)
        self.assertIsNotNone(context.template_node())
        self.assertEqual("1", context.template_node().template.word)

        self.assertEqual("A B D", context.star(1))

    def test_star_tree_matching_front(self):

        self.add_pattern_to_graph(pattern="* C D", topic="X", that="Y", template="1")

        context = self.match_sentence("A B C D", topic="X", that="Y")
        self.assertIsNotNone(context)
        self.assertIsNotNone(context.template_node())
        self.assertEqual("1", context.template_node().template.word)

        self.assertEqual("A B", context.star(1))

    def test_star_tree_matching_middle(self):

        self.add_pattern_to_graph(pattern="A * D", topic="X", that="Y", template="1")

        context = self.match_sentence("A B C D", topic="X", that="Y")
        self.assertIsNotNone(context)
        self.assertIsNotNone(context.template_node())
        self.assertEqual("1", context.template_node().template.word)

        self.assertEqual("B C", context.star(1))

    def test_star_tree_matching_end(self):

        self.add_pattern_to_graph(pattern="A B *", topic="X", that="Y", template="1")

        context = self.match_sentence("A B C D", topic="X", that="Y")
        self.assertIsNotNone(context)
        self.assertIsNotNone(context.template_node())
        self.assertEqual("1", context.template_node().template.word)

        self.assertEqual("C D", context.star(1))

    def test_star_tree_matching_multiple(self):

        self.add_pattern_to_graph(pattern="A * * D", topic="X", that="Y", template="1")

        context = self.match_sentence("A B C D", topic="X", that="Y")
        self.assertIsNotNone(context)
        self.assertIsNotNone(context.template_node())
        self.assertEqual("1", context.template_node().template.word)

        self.assertEqual("B", context.star(1))
        self.assertEqual("C", context.star(2))

    def test_star_tree_matching_all(self):

        self.add_pattern_to_graph(pattern="A * D", topic="*", that="*", template="1")

        context = self.match_sentence("A B C D", topic="X Y", that="Z1 Z2")
        self.assertIsNotNone(context)
        self.assertIsNotNone(context.template_node())
        self.assertEqual("1", context.template_node().template.word)

        self.assertEqual("B C", context.star(1))
        self.assertEqual("X Y", context.topicstar(1))
        self.assertEqual("Z1 Z2", context.thatstar(1))

    def test_stars_front_and_back(self):

        self.add_pattern_to_graph(pattern="* F G", topic="*", that="*", template="2")
        self.add_pattern_to_graph(pattern="* A B *", topic="*", that="*", template="1")

        context = self.match_sentence("F A B G", topic="X", that="Y")
        self.assertIsNotNone(context)
        self.assertIsNotNone(context.template_node())
        self.assertEqual("1", context.template_node().template.word)

        self.assertEqual("F", context.star(1))
        self.assertEqual("G", context.star(2))
        self.assertEqual("X", context.topicstar(1))
        self.assertEqual("Y", context.thatstar(1))

    def test_star_deep_tree_matching(self):

        self.add_pattern_to_graph(pattern="A * B * C", topic="X", that="Z", template="1")
        self.add_pattern_to_graph(pattern="A * B * C", topic="X", that="Y", template="1")

        context = self.match_sentence("A X1 X2 X3 X4 B Y1 Y2 Y3 Y4 C", topic="X", that="Y")
        self.assertIsNotNone(context)
        self.assertIsNotNone(context.template_node())
        self.assertEqual("1", context.template_node().template.word)

        self.assertEqual("X1 X2 X3 X4", context.star(1))
        self.assertEqual("Y1 Y2 Y3 Y4", context.star(2))

    def test_star_with_set_matching(self):
        self._client_context.brain.dynamics.add_dynamic_set('number', "programy.dynamic.sets.numeric.IsNumeric", None)

        self.add_pattern_to_graph(pattern="XXLENGTH * XS <set>number</set>", topic="*", that="*", template="1")
        self.add_pattern_to_graph(pattern="XXLENGTH * * XS <set>number</set>", topic="*", that="*", template="2")

        context = self.match_sentence("XXLENGTH X Y XS 1", topic="*", that="*")
        self.assertIsNotNone(context)
        self.assertIsNotNone(context.template_node())
        self.assertEqual("2", context.template_node().template.word)

        context = self.match_sentence("XXLENGTH X XS 1", topic="*", that="XXLENGTH X Y XS 2")
        self.assertIsNotNone(context)
        self.assertIsNotNone(context.template_node())
        self.assertEqual("1", context.template_node().template.word)
