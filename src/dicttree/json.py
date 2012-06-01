"""json (de)serialization for dicttrees
"""
from __future__ import absolute_import

import json as jsonlib

from metachao import aspect


class json(aspect.Aspect):
    """highly experimental and probably not good
    """
    _encoding = aspect.cfg(None)
    _parse_float = aspect.cfg(None)
    _parse_int = aspect.cfg(None)
    _parse_constant = aspect.cfg(None)

    @aspect.cfg
    def _child_factory(self, pairs):
        node = self.__class__()
        for pair in pairs:
            node[pair[0]] = pair[1]
        return node

    def loads(self, s):
        root = jsonlib.loads(s,
                             encoding=self._encoding,
                             object_pairs_hook=self._child_factory,
                             parse_float=self._parse_float,
                             parse_int=self._parse_int,
                             parse_constant=self._parse_constant)
        for k,v in root.items():
            self[k] = v
