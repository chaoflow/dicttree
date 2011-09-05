from zope.interface import Interface
from zope.interface import Attribute
from zope.interface.common.mapping import IFullMapping


class INode(IFullMapping):
    """A dictionary located in a tree
    """
    attrs = Attribute(u"A dictionary containing node attributes")
    name = Attribute(
        u"Name by which the node is known to its parent (readonly)"
        )
    parent = Attribute(u"Parent of the node (readonly)")

    # XXX: the test here is currently not found
    def __div__(relpath):
        """Traverse a dicttree

        >>> from dicttree import Node
        >>> node = Node()
        >>> node.a = Node()
        >>> node.a.b = Node()
        >>> c = node.a.b.c = Node()
        >>> node/"a"/"b"/"c" is c
        True
        >>> node/"a/b/c" is c
        True
        """
