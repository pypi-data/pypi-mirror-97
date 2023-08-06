
# -*- coding: utf-8 -*-

# Test namedTuples module.

__all__ = ('Tests',)
__version__ = '20.12.02'

from base import TestsBase
from pygeodesy import FIx, issubclassof
from pygeodesy.albers import _Ks
from pygeodesy.frechet import Frechet6Tuple
from pygeodesy.hausdorff import Hausdorff6Tuple
from pygeodesy.named import _Pass
from pygeodesy.namedTuples import _NamedTuple
from pygeodesy.units import _NamedUnit

_Units_ = '_Units_'


class Tests(TestsBase):

    def testNamedTuple(self, T, *args):
        m = T.__module__
        n = T.__name__ + '.' + _Units_
        t = T(*args)

        U = getattr(T, _Units_, ())
        if len(U) != len(t):  # check _Units_ len
            e = '%s = %r' % (n, tuple(u.__name__ for u in U))
            self.test(m, e, len(t))

        for i, u in enumerate(U):  # check _Units_ types
            if not (callable(u) and (u in (FIx, _Ks, _Pass) or
                                     issubclassof(u, _NamedUnit))):
                e = '%s[%s] %r' % (n, i, u)
                self.test(m, e, callable.__name__)

        u = t.toUnits()  # check _Units_ sample
        ru = repr(u)
        rt = repr(t)
        x = ru if rt == ru.replace("'0", '0').replace("5'", '5') \
                          .replace('True', '0.5').replace('0,', '0.5,') \
                          .replace('0)', '0.5)') else rt
        self.test(m, ru, x)

        u = ('%s=%s' % (n, u.__name__) for (n, u) in zip(T._Names_, U))
        u = '%s(%s)' % (T.__name__, ', '.join(u))
        self.test(m, u, u)  # the items as name=units

        self.testValidated(T, True)
        self.testValidated(t.__class__, True)

    def testNamedTuples(self):
        for T in self.pygeodesy_classes(Base=_NamedTuple):
            if T is not _NamedTuple:
                t = (0.5,) * len(T._Names_)  # some sample value
                if T in (Frechet6Tuple, Hausdorff6Tuple):
                    t = t[1:] + ('test',)
                self.testNamedTuple(T, *t)

        self.testValidated(_NamedTuple, False)

    def testValidated(self, T, x):
        n = T.__module__ + ': ' +  T.__name__ + '._validated'
        self.test(n , T._validated, x)


if __name__ == '__main__':

    t = Tests(__file__, __version__)
    t.testNamedTuples()
    t.results()
    t.exit()
