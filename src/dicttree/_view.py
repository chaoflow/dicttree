from zope.interface import implements

from dicttree import aspects as dta
from dicttree.interfaces import INode
from dicttree.utils import iterleaves


SCOPE_ITERATORS = {
    "leaves": iterleaves
    }


@dta.adoptable
@dta.children_as_attrs
class View(object):
    """A view looks like a node but does not store any data itself
    """
    implements(INode)

    @property
    def attrs(self):
        # XXX: overlay our attrs over our context's
        return self._context.attrs

    def __init__(self, node, groupkey=None, scope=None, sortkey=None):
        if hasattr(node, '__next__'):
            self._context = Node()
            for x in node:
                self._context[x.name] = x
        else:
            self._context = node
        self._groupkey = groupkey
        self._scope = scope
        self._sortkey = sortkey

    def __iter__(self):
        if self._groupkey or self._scope or self._sortkey:
            return (x.name for x in self.itervalues())
        return iter(self._context)

    def itervalues(self):
        iterator = self._context.itervalues()
        if self._scope:
            iterator = SCOPE_ITERATORS[self._scope](iterator)
        # iterator = igroupandsort(iterator)
        # if self._groupkey:
        #     return (View(x)

        #     iterator = groupby(sorted(iterator, self._groupkey),
        #                        self._groupkey)
        #     return (View(x, sortkey=self._sortkey) for x in iterator)
        if self._sortkey:
            iterator = sorted(iterator, key=self._sortkey)
        return iterator

    def keys(self):
        return [x for x in self]

    def values(self):
        return [x for x in self.itervalues()]

    def __getitem__(self, key):
        return self._context[key]
