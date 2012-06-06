from metachao import aspect
from metachao.aspect import Aspect
from zope.interface import implements

from dicttree.aspects._views import Itervalues
from dicttree.aspects._views import leaves
from dicttree.aspects._views import mgroup
from dicttree.aspects.adoption import *
from dicttree.interfaces import INode
from dicttree.tools import name_in_mro

try:
    from collections import OrderedDict
except ImportError:                      #pragma NO COVERAGE
    from ordereddict import OrderedDict  #pragma NO COVERAGE


class appendchild(Aspect):
    """
        >>> @appendchild
        ... @adopting
        ... class Parent(dict): pass
        >>> @adoptable
        ... class Child(dict): pass
        >>> parent = Parent()
        >>> childA = Child(name="a")
        >>> childB = Child(name="b")
        >>> parent.append(childA)
        >>> parent.append(childB)
        >>> parent.keys()
        ['a', 'b']
        >>> parent.append(childB)
        Traceback (most recent call last):
        ...
        KeyError: 'b'
    """
    def append(self, value):
        """Append a value that has a name, "" and None are valid names
        """
        key = value.__name__
        if key in self:
            raise KeyError("%s" % (key,))
        self[key] = value


# XXX: generalize to readonly_property or something
class attrs(Aspect):
    """
    Ideally:
    - attrs is created automatically for instances
    - attrs is fetched from the prototype for prototypees
    - attrs dict prototype is achieved through special factory

    attrs factory ends up in the class dictionary. If it is a class
    itself it will just be called, if it is a function, it will result
    in a bound method call being passed self as single argument.
    """
    _cfg_attrs_factory = aspect.aspectkw(factory=OrderedDict)

    @property
    def attrs(self):
        # If we have _attrs, return it
        try:
            return object.__getattribute__(self, "_attrs")
        except AttributeError:
            pass
        # Fallback to our eventual prototype
        try:
            return self.__metachao_prototype__.attrs
        except AttributeError:
            pass
        # Create _attrs for us
        attrs = self._cfg_attrs_factory()
        if getattr(attrs, '__name__', None) is None:
            attrs.__name__ = '__attrs__'
        attrs.__parent__ = self
        object.__setattr__(self, "_attrs", attrs)
        return attrs

    # XXX: there should be something to detect collision of init kw
    # XXX: *args are currently not supported, not even passing them on
    @aspect.plumb
    def __init__(_next, self, attrs=None, **kw):
        _next(**kw)
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
            # return _next(name)
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
            # _next(name, value)
            object.__setattr__(self, name, value)
        else:
            self[name] = value


class populate(Aspect):
    _childspec = aspect.cfg(())

    @aspect.plumb
    def __init__(_next, self, **kw):
        _next(**kw)
        for name, factory in self._childspec:
            self[name] = factory()


class traverse_via_div(Aspect):
    def __div__(self, relpath):
        # FUTURE: some way to escape the /
        psegs = relpath.split('/')
        return reduce(lambda acc, x: acc[x], psegs, self)


class provideINode(Aspect):
    @aspect.plumb
    def __setitem__(_next, self, key, value, **kw):
        # XXX: does this test make sense?
        if not INode.providedBy(value):
            raise ValueError("Children need to provide INode")
        _next(key, value, **kw)


@provideINode
@appendchild         # XXX: is this node or an addon?
@adopting            # XXX: Is every node adopting?
@adoptable
@children_as_attrs   # XXX: is this node or an addon?
@traverse_via_div
class nodify(Aspect):
    # XXX: split up this interface
    # INode here, but parts of it also above
    implements(INode)
