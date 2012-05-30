from metachao import aspect
from metachao.aspect import Aspect


class adopting(Aspect):
    @aspect.plumb
    def __delitem__(_next, self, key):
        value = self[key]
        value.__parent__ = None
        _next(key)

    @aspect.plumb
    def __setitem__(_next, self, key, value):
        if value.__parent__ is not None:
            raise ValueError("Cannot adopt child with parent")
        oldname = value.__name__
        value.__name__ = key
        value.__parent__ = self
        try:
            _next(key, value)
        except:
            value.__name__ = oldname
            value.__parent__ = None
            raise


class hasname(Aspect):
    __name__ = aspect.aspectkw(name=None)

    @property
    def name(self):
        return self.__name__


class hasparent(Aspect):
    __parent__ = aspect.aspectkw(parent=None)

    @property
    def parent(self):
        return self.__parent__


# XXX: Is zope.location worth it, i.e. small enough to be used here?
# XXX: __name__/__parent__ vs _name/_parent
@hasname
@hasparent
class adoptable(Aspect):
    pass

#adoptable = hasname(hasparent)

#adoptable = compose(hasname, hasparent)
