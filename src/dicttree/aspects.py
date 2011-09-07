from metachao import aspect
from metachao.aspect import Aspect
from zope.interface import implements

from dicttree.interfaces import INode


# XXX: move somewhere: aspect.utils / dicttree.utils?
from itertools import imap
def name_in_mro(obj, key):
    return any(imap(lambda x: key in x.__dict__,
                    [obj] + obj.__class__.mro()))


class adopting(Aspect):
    @aspect.plumb
    def __delitem__(_next, self, key):
        # free the child for adoption
        value = self[key]
        value.__name__ = None
        value.__parent__ = None
        _next(self, key)

    @aspect.plumb
    def __setitem__(_next, self, key, value):
        if value.__name__ is not None:
            raise ValueError("Cannot adopt child with name")
        if value.__parent__ is not None:
            raise ValueError("Cannot adopt child with parent")
        # adopt
        value.__name__ = key
        value.__parent__ = self
        try:
            _next(self, key, value)
        except:
            value.__name__ = None
            value.__parent__ = None
            raise


# XXX: Is zope.location worth it, i.e. small enough to be used here?
# XXX: __name__/__parent__ vs _name/_parent
class adoptable(Aspect):
    __name__ = None
    __parent__ = None

    @property
    def name(self):
        return self.__name__

    @property
    def parent(self):
        return self.__parent__

    # XXX: *args are currently not supported, not even passing them on
    @aspect.plumb
    def __init__(_next, self, name=None, **kw):
        _next(self, **kw)
        if name is not None:
            self.__name__ = name


# XXX: generalize to readonly_property or something
class attrs(Aspect):
    _attrs_factory = aspect.aspectkw(factory=dict)

    @property
    def attrs(self):
        try:
            return object.__getattribute__(self, "_attrs")
        except AttributeError:
            object.__setattr__(self, "_attrs", self._attrs_factory())
            return object.__getattribute__(self, "_attrs")

    # XXX: there should be something to detect collision of init kw
    # XXX: *args are currently not supported, not even passing them on
    @aspect.plumb
    def __init__(_next, self, attrs=None, **kw):
        _next(self, **kw)
        if attrs:
            self.attrs.update(attrs)


# XXX: need @plumb - so far we are the only one tampering with
# __get/setattr__ with plumb we will run into a problem if nobody
# provides __getattr__ therefore there needs to be a @default
# __getattr__ that calls getattribute something is wrong - I think
# __getattr__ is only called if __getattribute__ failed...

class children_as_attrs(Aspect):
    # @aspect.plumb
    # def __getattr__(self, _next, name):
    def __getattr__(self, name):
        """Blend in children as attributes

        Children can be accessed via getattr, except if aliased by a
        real attribute.
        """
        try:
            # return _next(self, name)
            return object.__getattribute__(self, name)
        except AttributeError:
            try:
                return self[name]
            except KeyError:
                raise AttributeError(name)

    # @aspect.plumb
    # def __setattr__(self, _next, name, value):
    def __setattr__(self, name, value):
        """Blend in children as attributes

        For setattr, names starting with underscore and those existing
        in the mro are real attributes, everything else is considered
        to be a child.
        """
        if name.startswith('_') or name_in_mro(self, name):
            # _next(self, name, value)
            object.__setattr__(self, name, value)
        else:
            self[name] = value


class traverse_via_div(Aspect):
    def __div__(self, relpath):
        # FUTURE: some way to escape the /
        psegs = relpath.split('/')
        return reduce(lambda acc, x: acc[x], psegs, self)


@adopting            # XXX: Is every node adopting?
@adoptable
@children_as_attrs   # XXX: is this node or an addon?
@traverse_via_div
class nodify(Aspect):
    # XXX: split up this interface
    # INode here, but parts of it also above
    implements(INode)

    @aspect.plumb
    def __setitem__(_next, self, key, value):
        # XXX: does this test make sense?
        if not INode.providedBy(value):
            raise ValueError("Children need to provide INode")
        _next(self, key, value)
