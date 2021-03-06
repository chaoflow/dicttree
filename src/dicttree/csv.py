from __future__ import absolute_import

import csv as csvlib

from metachao import aspect


class _NONE:
    pass


class Field(object):
    default = _NONE
    name = None
    readonly = False
    type = None

    def __init__(self, name, type=None, default=None, readonly=None):
        self.name = name
        if type is not None:
            self.type = type
        if default is not None:
            self.default = default
        if readonly is not None:
            self.readonly = readonly


class csv(aspect.Aspect):
    """A two-level tree from a csv file

    The table itself is the parent node, each row represents a child
    node of the table and the cells are parsed as child attributes
    using the columns specification.
    """
    # XXX: childtype might be moved out if needed by other aspects
    _childtype = aspect.cfg(None)
    _schema = aspect.cfg(None)
    _skip = aspect.cfg(0)

    def load(self, stream):
        """Load tree from csv stream
        """
        if self._schema is None:
            raise ValueError('schema not set')

        # XXX: make all dialect stuff configureable via aspect.cfg
        reader = csvlib.reader(stream, delimiter=';')
        for i,row in enumerate(reader):
            if i < self._skip:
                continue
            name = i - self._skip
            childtype = self._childtype or self.__metachao_class__
            child = childtype(name=name)
            for k,col in enumerate(self._schema):
                try:
                    value = row.pop(0)
                except IndexError:
                    if col.default is _NONE:
                        raise ValueError('Lacking value for row %s col %s' % (i, k))
                    else:
                        value = col.default
                else:
                    if col.type and not isinstance(value, col.type):
                        value = col.type(value)
                child.attrs[col.name] = value
            self.append(child)
