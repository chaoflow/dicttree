View of a tree::

    >>> from dicttree.ordereddict import Node
    >>> from dicttree.view import View
    >>> node = Node()
    >>> a = node.a = Node()
    >>> view = View(node)
    >>> view.a is a
    True

    >>> b = node.b = Node()
    >>> view.b is b
    True
    >>> view.keys()
    ['a', 'b']

sortkey::

    >>> node = Node()
    >>> node.a = Node(attrs=dict(a=2))
    >>> node.b = Node(attrs=dict(a=1))
    >>> view = View(node, sortkey=lambda x: x.attrs.a)
    >>> view.keys()
    ['b', 'a']

leaves::

    >>> node = Node()
    >>> node.a = Node()
    >>> node.a.aa = Node()
    >>> node.b = Node()
    >>> node.b.bb = Node()
    >>> node.b.bb.bbb = Node()
    >>> view = View(node, scope="leaves")
    >>> view.keys()
    ['aa', 'bbb']
