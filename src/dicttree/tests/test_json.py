from pkg_resources import resource_string

from unittest import TestCase

from dicttree.aspects import children_as_attrs
from dicttree.json import json
from dicttree.ordereddict import OrderedDict


@json
@children_as_attrs
class Node(OrderedDict):
    pass


class Json(TestCase):
    def runTest(self):
        node = Node()
        node.loads(resource_string(__name__, 'test_json.json'))
        self.assertListEqual(node.keys(), [u'a', u'b'])
        self.assertListEqual(node.a.keys(), [u'aa'])
        self.assertListEqual(node.a.aa.keys(), [u'aaa'])
        self.assertEqual(node.a.aa.aaa, 111)
        self.assertListEqual(node.b.keys(), [u'ba', u'bb'])
        self.assertListEqual(node.b.ba.keys(), [u'baa'])
        self.assertEqual(node.b.ba.baa, 211)
        self.assertListEqual(node.b.bb.keys(), [u'bba'])
        self.assertEqual(node.b.bb.bba, 221)
        
