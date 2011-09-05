    >>> from dicttree import Node
    >>> from dicttree.utils import iterleaves
    >>> root = Node()
    >>> root.a = Node()
    >>> root.b = Node()
    >>> root.b.bb = Node()
    >>> root.b.bb.bbb = Node()
    >>> root.c = Node()
    >>> root.c.cc = Node()
    >>> [x.name for x in iterleaves(root.itervalues())]
    ['a', 'bbb', 'cc']
