from itertools import groupby

from metachao import aspect
from metachao.aspect import Aspect

from dicttree.aspects.adoption import adoptable, hasparent


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


@adoptable
class Itervalues(object):
    def __init__(self, itervalues=None):
        if itervalues is not None:
            self._cfg_itervalues = itervalues

    def itervalues(self):
        # XXX: should we ensure nodes?
        # XXX: should we ensure parenthood and name?
        return self._cfg_itervalues()


class mgroup(Aspect):
    """nested tree by (multi-level) grouping a flat tree

    input tree needs to be sorted
    """
    _cfg_aspects = aspect.aspectkw(aspects=())
    # a list of functions to derive the group key for each tier
    _cfg_groupkeys = aspect.aspectkw(groupkeys=())

    # @aspect.plumb
    # def __init__(_next, self, groupkeys=None, **kw):
    #     _next(**kw)
    #     if groupkeys is not None:
    #         self._cfg_groupkeys = groupkeys

    @aspect.plumb
    def itervalues(_next, self):
        # XXX: check during aspect application
        if type(self._cfg_aspects) is not tuple:
            raise ValueError("Expected aspects tuple")
        gener = _next()
        if self._cfg_groupkeys:
            gkey = self._cfg_groupkeys[0]
            query = lambda key: lambda : filter(lambda x: gkey(x) == key, _next())
            gener = (mgroup(Itervalues(name=key,
                                       parent=self,
                                       itervalues=query(key)),
                            groupkeys=self._cfg_groupkeys[1:],
                            aspects=self._cfg_aspects[1:])
                     for key, _ in groupby(gener, gkey))
        else:
            gener = (hasparent(x, parent=self) for x in gener)
        if self._cfg_aspects:
            gener = (self._cfg_aspects[0](x) for x in gener)
        return gener
