"""Unit tests for the helper functions in search.py.

Place this file next to search.py and run: python -m unittest -v test_search.py
"""
import unittest
from dataclasses import dataclass

import search as search_module


@dataclass
class DummyNode:
    state: str
    g: int
    h: int = 0

    @property
    def f(self):
        return self.g + self.h


class TestSearchHelpers(unittest.TestCase):
    def setUp(self):
        self.open_set = search_module.create_open_set()
        self.closed_set = search_module.create_closed_set()

    def test_create_sets_empty(self):
        self.assertEqual(self.open_set, [])
        self.assertEqual(self.closed_set, {})
        self.assertFalse(search_module.open_not_empty(self.open_set))

    def test_add_to_open(self):
        node = DummyNode('A', 2, 3)
        search_module.add_to_open(node, self.open_set)
        self.assertTrue(search_module.open_not_empty(self.open_set))
        self.assertIs(search_module.get_best(self.open_set), node)
        self.assertFalse(search_module.open_not_empty(self.open_set))

    def test_get_best_returns_lowest_f(self):
        nodes = [DummyNode('A', 3, 5), DummyNode('B', 2, 1), DummyNode('C', 4, 2)]
        for node in nodes:
            search_module.add_to_open(node, self.open_set)
        self.assertEqual([search_module.get_best(self.open_set).state for _ in nodes], ['B', 'C', 'A'])

    def test_equal_f_nodes_are_both_kept(self):
        first = DummyNode('A', 1, 3)
        second = DummyNode('B', 2, 2)
        search_module.add_to_open(first, self.open_set)
        search_module.add_to_open(second, self.open_set)
        result = [search_module.get_best(self.open_set), search_module.get_best(self.open_set)]
        self.assertCountEqual([n.state for n in result], ['A', 'B'])

    def test_duplicate_in_open_missing(self):
        self.assertFalse(search_module.duplicate_in_open(DummyNode('A', 2), self.open_set))

    def test_duplicate_in_open_keeps_cheaper_existing(self):
        old = DummyNode('A', 2)
        search_module.add_to_open(old, self.open_set)
        self.assertTrue(search_module.duplicate_in_open(DummyNode('A', 5), self.open_set))
        self.assertTrue(search_module.duplicate_in_open(DummyNode('A', 2), self.open_set))
        self.assertIs(search_module.get_best(self.open_set), old)

    def test_duplicate_in_open_replaces_expensive_existing(self):
        old = DummyNode('A', 8)
        new = DummyNode('A', 3)
        other = DummyNode('B', 4)
        search_module.add_to_open(old, self.open_set)
        search_module.add_to_open(other, self.open_set)
        self.assertFalse(search_module.duplicate_in_open(new, self.open_set))
        search_module.add_to_open(new, self.open_set)
        self.assertIs(search_module.get_best(self.open_set), new)
        self.assertIs(search_module.get_best(self.open_set), other)

    def test_add_to_closed(self):
        node = DummyNode('A', 2)
        search_module.add_to_closed(node, self.closed_set)
        self.assertIs(self.closed_set['A'], node)

    def test_duplicate_in_closed_missing(self):
        self.assertFalse(search_module.duplicate_in_closed(DummyNode('A', 2), self.closed_set))

    def test_duplicate_in_closed_keeps_cheaper_existing(self):
        old = DummyNode('A', 2)
        search_module.add_to_closed(old, self.closed_set)
        self.assertTrue(search_module.duplicate_in_closed(DummyNode('A', 5), self.closed_set))
        self.assertTrue(search_module.duplicate_in_closed(DummyNode('A', 2), self.closed_set))
        self.assertIs(self.closed_set['A'], old)

    def test_duplicate_in_closed_reopens_for_better_path(self):
        search_module.add_to_closed(DummyNode('A', 8), self.closed_set)
        self.assertFalse(search_module.duplicate_in_closed(DummyNode('A', 3), self.closed_set))
        self.assertNotIn('A', self.closed_set)


if __name__ == '__main__':
    unittest.main()
