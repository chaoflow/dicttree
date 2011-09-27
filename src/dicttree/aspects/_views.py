from itertools import groupby

from metachao import aspect
from metachao.aspect import Aspect


class leaves(Aspect):
    """Take a tree's leaves as direct children
    """
    @aspect.plumb
    def itervalues(_next, self):
        for x in _next():
            if len(x) > 0:
                for y in leaves(x).itervalues():
                    yield y
            else:
                yield x


class Itervalues(object):
    def __init__(self, name=None, itervalues=None):
        if name is not None:
            self.name = name
        if itervalues is not None:
            self._cfg_itervalues = itervalues

    def itervalues(self):
        return self._cfg_itervalues()


class mgroup(Aspect):
    """nested tree by (multi-level) grouping a flat tree

    input tree needs to be sorted
    """
    # a list of functions to derive the group key for each tier
    _cfg_groupkeys = aspect.aspectkw(groupkeys=())

    # @aspect.plumb
    # def __init__(_next, self, groupkeys=None, **kw):
    #     _next(**kw)
    #     if groupkeys is not None:
    #         self._cfg_groupkeys = groupkeys

    @aspect.plumb
    def itervalues(_next, self):
        if not self._cfg_groupkeys:
            return _next()
        gkey = self._cfg_groupkeys[0]
        query = lambda key: lambda : filter(lambda x: gkey(x) == key, _next())
        return (mgroup(Itervalues(name=key, itervalues=query(key)),
                       groupkeys=self._cfg_groupkeys[1:])
                for key, _ in groupby(_next(), gkey))
