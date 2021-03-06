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

from programy.rdf.collection import RDFCollection


class RDFCollectionUnificationTests(unittest.TestCase):

    def test_unify_on_single_var(self):
        collection = RDFCollection()
        self.assertIsNotNone(collection)

        collection.add_entity("MONKEY", "LEGS", "2", "ANIMAL")
        collection.add_entity("MONKEY", "HASFUR", "true", "ANIMAL")
        collection.add_entity("ZEBRA", "LEGS", "4", "ANIMAL")
        collection.add_entity("BIRD", "LEGS", "2", "ANIMAL")
        collection.add_entity("ELEPHANT", "TRUNK", "true", "ANIMAL")

        set1 = collection.match_to_vars("?x", "LEGS", "2")
        set2 = collection.match_to_vars("?x", "HASFUR", "true")

        unified = collection.unify(["?x"], [set1, set2])
        self.assertIsNotNone(unified)
        self.assertEqual(1, len(unified))
        self.assertTrue([['?x', 'MONKEY']] in unified)

    def test_unify_on_single_var_with_not(self):
        collection = RDFCollection()
        self.assertIsNotNone(collection)

        collection.add_entity("MONKEY", "LEGS", "2", "ANIMALS")
        collection.add_entity("MONKEY", "HASFUR", "true", "ANIMALS")
        collection.add_entity("ZEBRA", "LEGS", "4", "ANIMALS")
        collection.add_entity("BIRD", "LEGS", "2", "ANIMALS")
        collection.add_entity("ELEPHANT", "TRUNK", "true", "ANIMALS")

        set1 = collection.match_to_vars("?x", "LEGS", "2")
        set2 = collection.not_match_to_vars("?x", "HASFUR", "true")

        unified = collection.unify(["?x"], [set1, set2])
        self.assertIsNotNone(unified)
        self.assertEqual(2, len(unified))
        self.assertTrue([['?x', 'BIRD']] in unified)
        self.assertTrue([['?x', 'MONKEY']] in unified)

    def test_unify_on_multi_vars(self):
        collection = RDFCollection()
        self.assertIsNotNone(collection)

        collection.add_entity("TEST1", "ISA", "TEST2", "TEST")
        collection.add_entity("TEST2", "ISA", "TEST3", "TEST")

        set1 = collection.match_to_vars("?x", "ISA", "?y")
        set2 = collection.match_to_vars("?y", "ISA", "?z")

        unified = collection.unify(("?x", "?y", "?z"), [set1, set2])
        self.assertIsNotNone(unified)
        self.assertEqual(1, len(unified))
        self.assertTrue(["?x", "TEST1"] in unified[0])
        self.assertTrue(["?y", "TEST2"] in unified[0])
        self.assertTrue(["?z", "TEST3"] in unified[0])

    def test_unify_multi_var_deep(self):
        collection = RDFCollection()
        self.assertIsNotNone(collection)

        collection.add_entity("TEST1", "ISA", "TEST2", "TEST")
        collection.add_entity("TEST2", "ISA", "TEST3", "TEST")
        collection.add_entity("TEST3", "ISA", "TEST4", "TEST")
        collection.add_entity("TEST4", "ISA", "TEST5", "TEST")

        set1 = collection.match_to_vars("?x", "ISA", "?y")
        set2 = collection.match_to_vars("?y", "ISA", "?z")
        set3 = collection.match_to_vars("?z", "ISA", "?w")

        unified = collection.unify(("?x", "?y", "?z", "?w"), [set1, set2, set3])
        self.assertIsNotNone(unified)
        self.assertEqual(2, len(unified))
        self.assertTrue([['?x', 'TEST1'], ['?y', 'TEST2'], ['?z', 'TEST3'], ['?w', 'TEST4'], ] in unified)
        self.assertTrue([['?x', 'TEST2'], ['?y', 'TEST3'], ['?z', 'TEST4'], ['?w', 'TEST5']] in unified)
