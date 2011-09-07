try:
    from collections import OrderedDict
except ImportError:
    from ordereddict import OrderedDict

from dicttree import aspects as dta


@dta.children_as_attrs
class NodeAttr(OrderedDict):
    pass


@dta.attrs(factory=NodeAttr)
@dta.nodify
class Node(OrderedDict):
    pass
