    >>> from dicttree.ordereddict import Node
    >>> node = Node()

Adoption behavior::

    >>> node['child'] = child = Node()
    >>> child.name
    'child'
    >>> child.parent is node
    True
    >>> del node['child']
    >>> child.name
    'child'
    >>> child.parent is None
    True

    >>> node['foo'] = 1
    Traceback (most recent call last):
      ...
    ValueError: Children need to provide INode

    >>> nope = Node()
    >>> nope.__parent__ = "foo"
    >>> node['bar'] = nope
    Traceback (most recent call last):
      ...
    ValueError: Cannot adopt child with parent


Children via attribute access::

    >>> node['child'] = child = Node()
    >>> node.child is node['child']
    True
    >>> node.child2 = Node()
    >>> node.child2 is node['child2']
    True

    >>> node._b = 3
    >>> node.get('_b') is None
    True
    >>> node._b
    3

    >>> node.keys()
    ['child', 'child2']
    
Node attributes::

    >>> node.attrs.a = 1
    >>> node.attrs.a
    1
    >>> node.attrs['a']
    1

Attribute names that exist in the MRO are not available as child names
for child attribute access::

    >>> node.attrs = 1
    Traceback (most recent call last):
      ...
    AttributeError: can't set attribute

    >>> node.keys = lambda : 1
    >>> node.keys()
    1

    >>> node.attrs.keys()
    ['a']

Using "/" to travers the dicttree::

    >>> node = Node()
    >>> node.a = Node()
    >>> node.a.b = Node()
    >>> c = node.a.b.c = Node()
    >>> node/"a"/"b"/"c" is c
    True
    >>> node/"a/b/c" is c
    True

Passing attributes via init::

    >>> node = Node(attrs=dict(a=1, b=2))
    >>> node.attrs.a
    1
    >>> node.attrs.b
    2

    >>> node = Node(attrs=(('c', 3), ('d', 4)))
    >>> node.attrs.c
    3
    >>> node.attrs.d
    4




mgroup / itervaluesobj::
    >>> from dicttree import aspects as dta

    >>> nodelist = [
    ...     Node(attrs=dict(a=1, b=10, c=100)),
    ...     Node(attrs=dict(a=1, b=10, c=200)),
    ...     Node(attrs=dict(a=1, b=10, c=300)),
    ...     Node(attrs=dict(a=1, b=20, c=100)),
    ...     Node(attrs=dict(a=1, b=20, c=200)),
    ...     Node(attrs=dict(a=1, b=20, c=300)),
    ...     Node(attrs=dict(a=2, b=10, c=100)),
    ...     Node(attrs=dict(a=2, b=10, c=200)),
    ...     Node(attrs=dict(a=2, b=10, c=300)),
    ...     Node(attrs=dict(a=2, b=20, c=100)),
    ...     Node(attrs=dict(a=2, b=20, c=200)),
    ...     Node(attrs=dict(a=2, b=20, c=300)),
    ...     ]

    >>> from dicttree.aspects import Itervalues
    >>> root = Itervalues(name="root", itervalues=lambda : iter(nodelist))

Iterator is not getting exhausted::

    >>> [x for x in root.itervalues()] == nodelist
    True
    >>> [x for x in root.itervalues()] == nodelist
    True

    >>> groupkeys = (
    ...     lambda x: x.attrs.a,
    ...     lambda x: x.attrs.b,
    ...     )
    >>> group = dta.mgroup(root, groupkeys=groupkeys)
    >>> group.name
    'root'
    >>> group.parent is None
    True
    >>> members = [x for x in group.itervalues()]
    >>> [x.name for x in members]
    [1, 2]
    >>> members[0].parent is group
    True
    >>> submembers = list(members[0].itervalues())
    >>> [x.name for x in submembers]
    [10, 20]
    >>> submembers[0].parent is members[0]
    True
    >>> subsubmembers = list(submembers[0].itervalues())
    >>> [x.attrs.c for x in subsubmembers]
    [100, 200, 300]
    >>> subsubmembers[0].parent is submembers[0]
    True
    >>> subsubmembers[0].__metachao_prototype__ is not submembers[0]
    True
