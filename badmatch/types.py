from sys import intern


class AtomMeta(type):

    def __new__(self, name, bases, attrs):
        attrs.setdefault("_container", {})
        return type.__new__(self, name, bases, attrs)

    def __call__(self, s):
        atom = self._container.get(s, None)
        if atom is None:
            s = intern(s)
            atom = super(AtomMeta, self).__call__(s)
            self._container[s] = atom
        return atom


class Atom(metaclass=AtomMeta):

    def __init__(self, s):
        self.__s = s

    def __repr__(self):
        return self.__s
