from itertools import groupby, imap


def iterleaves(iterator):
    """return an iterator over the leaves of a tree
    """
    for x in iterator:
        if x.keys():
            for y in iterleaves(x.itervalues()):
                yield y
        else:
            yield x


isiter = lambda x: hasattr(x, 'next')


def printgiter(giter, level=0):
    for x in giter:
        print " " * level, x
        if type(x) is tuple and isiter(x[1]):
            printgiter(x[1], level+1)


def mgroupby(iterator, groupkeys=()):
    """multiple groupby, nested groupby

    As with groupby, iterator needs to be sorted already.

    List of tuples to be put in nested groups::

        >>> items = [
        ...     (1, 3, 5),
        ...     (1, 3, 6),
        ...     (1, 4, 5),
        ...     (1, 4, 6),
        ...     (2, 3, 5),
        ...     (2, 3, 6),
        ...     (2, 4, 5),
        ...     (2, 4, 6),
        ...     ]

    For debugging purposes (hopefully not again) these are not lambdas::

        >>> def gkey0(x):
        ...     return x[0]
        >>> def gkey1(x):
        ...     return x[1]
        >>> def gkey2(x):
        ...     return x[2]

        >>> a = mgroupby(items, groupkeys=[gkey0, gkey1, gkey2])
        >>> printgiter(a) # doctest: +NORMALIZE_WHITESPACE
        (1, <generator object <genexpr> at 0x...>)
         (3, <itertools.groupby object at 0x...>)
          (5, <itertools._grouper object at 0x...>)
           (1, 3, 5)
          (6, <itertools._grouper object at 0x...>)
           (1, 3, 6)
         (4, <itertools.groupby object at 0x...>)
          (5, <itertools._grouper object at 0x...>)
           (1, 4, 5)
          (6, <itertools._grouper object at 0x...>)
           (1, 4, 6)
        (2, <generator object <genexpr> at 0x...>)
         (3, <itertools.groupby object at 0x...>)
          (5, <itertools._grouper object at 0x...>)
           (2, 3, 5)
          (6, <itertools._grouper object at 0x...>)
           (2, 3, 6)
         (4, <itertools.groupby object at 0x...>)
          (5, <itertools._grouper object at 0x...>)
           (2, 4, 5)
          (6, <itertools._grouper object at 0x...>)
           (2, 4, 6)
    """
    gkey = groupkeys[0]
    groupkeys = groupkeys[1:]
    iterator = groupby(iterator, gkey)
    if not groupkeys:
        return iterator
    return ((x[0], mgroupby(x[1], groupkeys)) for x in iterator)


def name_in_mro(obj, key):
    return any(imap(lambda x: key in x.__dict__,
                    [obj] + obj.__class__.mro()))
