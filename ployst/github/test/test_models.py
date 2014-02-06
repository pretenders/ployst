import unittest

from nose.tools import assert_items_equal, assert_equal

from ..models import Hierarchy


class TestHierarchy(unittest.TestCase):

    def setUp(self):
        self.h = Hierarchy()
        self.h[0].append(('a', '111'))
        self.h[2].append(('c', '333'))

    def test_acts_as_default_list(self):
        print self.h
        assert_items_equal(self.h, [[('a', '111')], [('c', '333')]])

        self.h[2].append(('c2', '444'))
        self.h[1].append(('b', '222'))
        assert_items_equal(
            self.h,
            [[('a', '111')], [('b', '222')], [('c', '333'), ('c2', '444')]])

    def test_get_parent(self):
        assert_equal(self.h.get_parent(1).branch, 'a')
        assert_equal(self.h.get_parent(2).branch, 'a')
        assert_equal(self.h.get_parent(3).branch, 'c')

    def test_assigns_parent_dynamically(self):
        assert_equal(self.h.get_node('c').parent.branch, 'a')

        self.h[1].append(('b', '111'))

        assert_equal(self.h.get_node('c').parent.branch, 'b')
        assert_equal(self.h.get_node('b').parent.branch, 'a')

    def test_children_assigned_dynamically(self):
        assert_equal(self.h.get_node('a').children[0].branch, 'c')

        self.h[1].append(('b', '111'))

        assert_equal(self.h.get_node('b').children[0].branch, 'c')
        assert_equal(self.h.get_node('a').children[0].branch, 'b')
