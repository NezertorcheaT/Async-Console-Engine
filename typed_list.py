from all_subclasses import all_subclasses

try:
    # Python 3
    from collections.abc import MutableSequence
except ImportError:
    # Python 2.7
    from collections import MutableSequence

import VectorUtils


class TypedList(MutableSequence):
    """A container for manipulating lists of hosts"""

    def __init__(self, type_of=int, data=None, from_dict: dict = None):
        """Initialize the class"""
        super(TypedList, self).__init__()
        if from_dict is None:
            self.type_of = type_of
            for i in range(len(list(data))):
                if not isinstance(list(data)[i], self.type_of):
                    raise ValueError(
                        f"Value ({list(data)[i]}; class: {list(data)[i].__class__.__name__}; position: {i}) must be of type \"{self.type_of.__name__}\"")

            if data is not None:
                self._list = list(data)
            else:
                self._list = list()
        else:
            tf = from_dict["type_of"]
            lst = from_dict["_list"]
            for i in object.__subclasses__():
                if tf == i.__name__:
                    self.type_of = i
                    break
            for i in range(len(lst)):
                if self.type_of == VectorUtils.vec3:
                    try:
                        lst[i] = VectorUtils.vec3(lst[i]['x'], lst[i]['y'],
                                                  lst[i]['z'])
                        continue
                    except TypeError:
                        raise ValueError(
                            f"Value \"{lst[i]}\" of type \"{VectorUtils.vec3.__name__}\" at position \"{i}\" must be of type \"{self.type_of.__name__}\"")
                if self.type_of == VectorUtils.vec2:
                    try:
                        lst[i] = VectorUtils.vec2(lst[i]['x'], lst[i]['y'])
                        continue
                    except TypeError:
                        raise ValueError(
                            f"Value \"{lst[i]}\" of type \"{VectorUtils.vec2.__name__}\" at position \"{i}\" must be of type \"{self.type_of.__name__}\"")
                if not isinstance(lst[i], self.type_of):
                    raise ValueError(
                        f"Value ({lst[i]}; class: {lst[i].__class__.__name__}; position: {i}) must be of type \"{self.type_of.__name__}\"")

            if lst is not None:
                self._list = lst
            else:
                self._list = list()

    def __repr__(self):
        return "<{0} {1}>".format(self.__class__.__name__, self._list)

    def __len__(self):
        """List length"""
        return len(self._list)

    def __getitem__(self, ii):
        """Get a list item"""
        if isinstance(ii, slice):
            return self.__class__(self._list[ii])
        else:
            return self._list[ii]

    def __delitem__(self, ii):
        """Delete an item"""
        del self._list[ii]

    def __setitem__(self, ii, val):
        # optional: self._acl_check(val)
        if isinstance(val, self.type_of):
            self._list[ii] = val
        else:
            raise ValueError(
                f"Value ({val}; class: {val.__class__.__name__}) must be of type \"{self.type_of.__name__}\"")

    def __str__(self):
        s = f'{self.__class__.__name__}({self.type_of.__name__}) = ['
        for i in range(len(self._list)):
            if i < len(self._list) - 1:
                s += f'{str(self._list[i])}, '
            else:
                s += f'{str(self._list[i])}]'
        return s

    def insert(self, ii, val):
        # optional: self._acl_check(val)
        if isinstance(val, self.type_of):
            self._list.insert(ii, val)
        else:
            raise ValueError(
                f"Value ({val}; class: {val.__class__.__name__}) must be of type \"{self.type_of.__name__}\"")

    def append(self, val):
        if isinstance(val, self.type_of):
            self.insert(len(self._list), val)
        else:
            raise ValueError(
                f"Value ({val}; class: {val.__class__.__name__}) must be of type \"{self.type_of.__name__}\"")

    def returnAsDict(self):
        return {"type_of": self.type_of.__name__, "_list": self._list}

    def returnAsList(self):
        return self._list