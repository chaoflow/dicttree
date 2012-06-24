from pkg_resources import resource_stream

from unittest import TestCase

from dicttree.csv import csv, Field
from dicttree.ordereddict import Node


class CSVTest(TestCase):
    def runTest(self):
        node = Node()
        schema = [
            Field(name='a', type=int),
            Field(name='b', type=str),
            Field(name='c', type=int, default=9),
            ]
        with resource_stream(__name__, 'test_csv.csv') as s:
            csv(node, schema=schema, skip=1).load(s)
        self.assertListEqual(node.keys(), [0,1])
        self.assertListEqual(node[0].attrs.keys(), ['a', 'b', 'c'])
        self.assertListEqual(node[1].attrs.keys(), ['a', 'b', 'c'])
        self.assertListEqual(node[0].attrs.values(), [1, '10', 9])
        self.assertListEqual(node[1].attrs.values(), [2, '20', 9])
