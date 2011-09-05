    >>> from dicttree import Node
    >>> node = Node()

Adoption behavior::

    >>> node['child'] = child = Node()
    >>> child.name
    'child'
    >>> child.parent is node
    True
    >>> del node['child']
    >>> child.name is None
    True
    >>> child.parent is None
    True

    >>> node['foo'] = 1
    Traceback (most recent call last):
      ...
    ValueError: Children need to provide INode

    >>> nope = Node()
    >>> nope.__name__ = "foo"
    >>> node['bar'] = nope
    Traceback (most recent call last):
      ...
    ValueError: Cannot adopt child with name

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
