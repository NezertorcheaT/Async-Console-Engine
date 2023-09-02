def all_subclasses(clss=object):
    return list(set(clss.__subclasses__()).union(
        [s for c in clss.__subclasses__() for s in all_subclasses(c)]))
