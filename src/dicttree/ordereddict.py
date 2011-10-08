from __future__ import absolute_import
try:
    from collections import OrderedDict
except ImportError:                      #pragma NO COVERAGE
    from ordereddict import OrderedDict  #pragma NO COVERAGE

from dicttree import aspects as dta


@dta.children_as_attrs
class NodeAttrs(OrderedDict):
    pass


@dta.attrs(factory=NodeAttrs)
@dta.nodify
class Node(OrderedDict):
    pass
