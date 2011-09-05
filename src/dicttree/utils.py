def iterleaves(iterator):
    for x in iterator:
        if x.keys():
            for y in iterleaves(x.itervalues()):
                yield y
        else:
            yield x


def igroupandsort(iterator, groupkey=None, sortkey=None):
    if groupkey:
        iterator = groupby(sorted(iterator, self._groupkey),
                           self._groupkey)
        return (sorted(x, key=sortkey) for x in iterator)
    if sortkey:
        iterator = sorted(iterator, key=sortkey)
    return iterator



