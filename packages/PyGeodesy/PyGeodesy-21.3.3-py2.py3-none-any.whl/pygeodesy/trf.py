
# -*- coding: utf-8 -*-

u'''Terrestrial Reference Frame (TRF) classes L{RefFrame}, registry L{RefFrames} and L{TRFError}.

Transcribed from I{Chris Veness'} (C) 2006-2019 JavaScript originals
U{latlon-ellipsoidal-referenceframe.js<https://GitHub.com/chrisveness/geodesy/blob/master/
latlon-ellipsoidal-referenceframe.js>} and U{latlon-ellipsoidal-referenceframe-txparams.js
<https://GitHub.com/chrisveness/geodesy/blob/master/latlon-ellipsoidal-referenceframe-txparams.js>}.

Following is a copy of I{Veness}' B{U{latlon-ellipsoidal-referenceframe.js
<https://GitHub.com/chrisveness/geodesy/blob/master/latlon-ellipsoidal-referenceframe.js>}} comments.

Modern geodetic reference frames: a latitude/longitude point defines a geographic location on,
above or below the earth’s surface, measured in degrees from the equator and the U{International
Reference Meridian<https://WikiPedia.org/wiki/IERS_Reference_Meridian>} (IRM) and metres above
the ellipsoid within a given I{Terrestrial Reference Frame} at a given I{epoch}.

This is scratching the surface of complexities involved in high precision geodesy, but may
be of interest and/or value to those with less demanding requirements.  More information U{here
<https://www.Movable-Type.co.UK/scripts/geodesy-library.html>} and U{here
<https://www.Movable-Type.co.UK/scripts/geodesy-library.html#latlon-ellipsoidal-referenceframe>}.

Note that I{ITRF solutions} do not directly use an ellipsoid, but are specified by Cartesian
coordinates.  The GRS80 ellipsoid is recommended for transformations to geographical coordinates.

Note WGS84(G730/G873/G1150) are coincident with ITRF at 10-centimetre level, see also U{here
<ftp://ITRF.ENSG.IGN.FR/pub/itrf/WGS84.TXT>}.  WGS84(G1674) and ITRF20014 / ITRF2008 I{"are likely
to agree at the centimeter level"}, see also U{QPS/Qinsy<https://Confluence.QPS.NL/qinsy/
en/how-to-deal-with-etrs89-datum-and-time-dependent-transformation-parameters-45353274.html>}.

@var RefFrames.ETRF2000: RefFrame(name='ETRF2000', epoch=2005, ellipsoid=Ellipsoid(name='GRS80')
@var RefFrames.GDA2020: RefFrame(name='GDA2020', epoch=2020, ellipsoid=Ellipsoid(name='GRS80')
@var RefFrames.GDA94: RefFrame(name='GDA94', epoch=1994, ellipsoid=Ellipsoid(name='GRS80')
@var RefFrames.ITRF2000: RefFrame(name='ITRF2000', epoch=1997, ellipsoid=Ellipsoid(name='GRS80')
@var RefFrames.ITRF2005: RefFrame(name='ITRF2005', epoch=2000, ellipsoid=Ellipsoid(name='GRS80')
@var RefFrames.ITRF2008: RefFrame(name='ITRF2008', epoch=2005, ellipsoid=Ellipsoid(name='GRS80')
@var RefFrames.ITRF2014: RefFrame(name='ITRF2014', epoch=2010, ellipsoid=Ellipsoid(name='GRS80')
@var RefFrames.ITRF91: RefFrame(name='ITRF91', epoch=1988, ellipsoid=Ellipsoid(name='GRS80')
@var RefFrames.ITRF93: RefFrame(name='ITRF93', epoch=1988, ellipsoid=Ellipsoid(name='GRS80')
@var RefFrames.NAD83: RefFrame(name='NAD83', epoch=1997, ellipsoid=Ellipsoid(name='GRS80')
@var RefFrames.WGS84g1150: RefFrame(name='WGS84g1150', epoch=2001, ellipsoid=Ellipsoid(name='WGS84')
@var RefFrames.WGS84g1674: RefFrame(name='WGS84g1674', epoch=2005, ellipsoid=Ellipsoid(name='WGS84')
@var RefFrames.WGS84g1762: RefFrame(name='WGS84g1762', epoch=2005, ellipsoid=Ellipsoid(name='WGS84')
'''

from pygeodesy.basics import map1
from pygeodesy.datums import _ellipsoid, Transform
from pygeodesy.ellipsoids import Ellipsoids
from pygeodesy.errors import TRFError
from pygeodesy.interns import NN, _COMMASPACE_, _conversion_, _ellipsoid_, \
                             _epoch_, _float as _F, _floatuple as _T, \
                             _GRS80_, _NAD83_, _name_, _no_, _s_, _to_, \
                             _WGS84_, _0_0, _0_001, _0_01, _0_1, _0_26, \
                             _0_5, _1_0
from pygeodesy.lazily import _ALL_LAZY
from pygeodesy.named import classname, _lazyNamedEnumItem as _lazy, \
                           _NamedDict as _D, _NamedEnum, _NamedEnumItem
from pygeodesy.props import Property_RO
from pygeodesy.streprs import Fmt
from pygeodesy.units import Epoch

from math import ceil

__all__ = _ALL_LAZY.trf
__version__ = '21.01.30'

_0_02  = _F(  0.02)
_0_06  = _F(  0.06)
_0_09  = _F(  0.09)
_366_0 = _F(366)
_mDays = (0, 31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31, 0)

_ETRF2000_   = 'ETRF2000'
_GDA2020_    = 'GDA2020'
_GDA94_      = 'GDA94'
_ITRF_       = 'ITRF'
_ITRF88_     = 'ITRF88'
_ITRF89_     = 'ITRF89'
_ITRF90_     = 'ITRF90'
_ITRF91_     = 'ITRF91'
_ITRF92_     = 'ITRF92'
_ITRF93_     = 'ITRF93'
_ITRF94_     = 'ITRF94'
_ITRF96_     = 'ITRF96'
_ITRF97_     = 'ITRF97'
_ITRF2000_   = 'ITRF2000'
_ITRF2005_   = 'ITRF2005'
_ITRF2008_   = 'ITRF2008'
_ITRF2014_   = 'ITRF2014'
_WGS84g1150_ = 'WGS84g1150'
_WGS84g1674_ = 'WGS84g1674'
_WGS84g1762_ = 'WGS84g1762'


class RefFrame(_NamedEnumItem):
    '''Terrestrial Reference Frame (TRF) parameters.
    '''
    _ellipsoid =  None  # ellipsoid GRS80 or WGS84 (L{Ellipsoid} or L{Ellipsoid2})
    _epoch     = _0_0   # epoch, calendar year (L{Epoch} or C{float})

    def __init__(self, epoch, ellipsoid, name=NN):
        '''New L{RefFrame}.

           @arg epoch: Epoch, a fractional calendar year (C{scalar} or C{str}).
           @arg ellipsoid: The ellipsoid (L{Ellipsoid}, L{Ellipsoid2},
                           L{datum} or L{a_f2Tuple}).
           @kwarg name: Optional, unique name (C{str}).

           @raise NameError: A L{RefFrame} with that B{C{name}}
                             already exists.

           @raise TRFError: Invalid B{C{epoch}}.

           @raise TypeError: Invalid B{C{ellipsoid}}.
        '''
        self._ellipsoid = _ellipsoid(ellipsoid, name=name)
        self._epoch = Epoch(epoch)
        self._register(RefFrames, name)

    @Property_RO
    def ellipsoid(self):
        '''Get this reference frame's ellipsoid (L{Ellipsoid} or L{Ellipsoid2}).
        '''
        return self._ellipsoid

    @Property_RO
    def epoch(self):
        '''Get this reference frame's epoch (C{Epoch}).
        '''
        return self._epoch

    def toStr(self, **unused):  # PYCHOK expected
        '''Return this reference frame as a text string.

           @return: This L{RefFrame}'s attributes (C{str}).
        '''
        e = self.ellipsoid
        t = (Fmt.EQUAL(_name_, repr(self.name)),
             Fmt.EQUAL(_epoch_, self.epoch),
             Fmt.PAREN(Fmt.EQUAL(_ellipsoid_, classname(e)),
                       Fmt.EQUAL(_name_, repr(e.name))))
        return _COMMASPACE_.join(t)


class RefFrames(_NamedEnum):
    '''(INTERNAL) L{RefFrame} registry, I{must} be a sub-class
       to accommodate the L{_LazyNamedEnumItem} properties.
    '''
    def _Lazy(self, epoch, ellipsoid_name, name=NN):
        '''(INTERNAL) Instantiate the L{RefFrame}.
        '''
        return RefFrame(epoch, Ellipsoids.get(ellipsoid_name), name=name)

RefFrames = RefFrames(RefFrame)  # PYCHOK singleton
'''Some pre-defined L{RefFrame}s, all I{lazily} instantiated.'''
# <https://GitHub.com/chrisveness/geodesy/blob/master/latlon-ellipsoidal-referenceframe.js>
RefFrames._assert(
    ETRF2000   = _lazy(_ETRF2000_,   _F(2005), _GRS80_),  # ETRF2000(R08)
    GDA2020    = _lazy(_GDA2020_,    _F(2020), _GRS80_),  # Australia
    GDA94      = _lazy(_GDA94_,      _F(1994), _GRS80_),  # Australia
    ITRF2000   = _lazy(_ITRF2000_,   _F(1997), _GRS80_),
    ITRF2005   = _lazy(_ITRF2005_,   _F(2000), _GRS80_),
    ITRF2008   = _lazy(_ITRF2008_,   _F(2005), _GRS80_),  # aks ITRF08
    ITRF2014   = _lazy(_ITRF2014_,   _F(2010), _GRS80_),
    ITRF91     = _lazy(_ITRF91_,     _F(1988), _GRS80_),
    ITRF93     = _lazy(_ITRF93_,     _F(1988), _GRS80_),
    NAD83      = _lazy(_NAD83_,      _F(1997), _GRS80_),  # CORS96
    WGS84g1150 = _lazy(_WGS84g1150_, _F(2001), _WGS84_),
    WGS84g1674 = _lazy(_WGS84g1674_, _F(2005), _WGS84_),
    WGS84g1762 = _lazy(_WGS84g1762_, _F(2005), _WGS84_))  # same epoch


def date2epoch(year, month, day):
    '''Return the reference frame C{epoch} for a calendar day.

       @arg year: Year of the date (C{scalar}).
       @arg month: Month in the B{C{year}} (C{scalar}, 1..12).
       @arg day: Day in the B{C{month}} (C{scalar}, 1..31).

       @return: Epoch, the fractional year (C{float}).

       @raise TRFError: Invalid B{C{year}}, B{C{month}} or B{C{day}}.

       @note: Any B{C{year}} is considered a leap year, i.e. having
              29 days in February.
    '''
    try:
        y, m, d = map1(int, year, month, day)
        if y > 0 and 1 <= m <= 12 and 1 <= d <= _mDays[m]:
            return Epoch(y + float(sum(_mDays[:m]) + d) / _366_0, low=0)

        t = NN  # _invalid_
    except (TRFError, TypeError, ValueError) as x:
        t = str(x)
    raise TRFError(year=year, month=month, day=day, txt=t)


def epoch2date(epoch):
    '''Return the date for a reference frame C{epoch}.

       @arg epoch: Fractional year (C{scalar}).

       @return: 3-Tuple C{(year, month, day)}.

       @raise TRFError: Invalid B{C{epoch}}.

       @note: Any B{C{year}} is considered a leap year, i.e. having
              29 days in February.
    '''
    e = Epoch(epoch, Error=TRFError, low=0)
    y = int(e)
    d = int(ceil(_366_0 * (e - y)))
    for m, n in enumerate(_mDays[1:]):
        if d > n:
            d -= n
        else:
            break
    return y, (m + 1), max(1, d)


# TRF conversions specified as 7-parameter Helmert transforms and an epoch.  Most
# from U{Transformation Parameters<http://ITRF.IGN.FR/trans_para.php>}, more at U{QPS
# <https://Confluence.QPS.NL/qinsy/files/en/29856813/45482834/2/1453459502000/ITRF_Transformation_Parameters.xlsx>}.
_trfNs =                                  ('tx',    'ty',    'tz',   _s_,   'sx',    'sy',    'sz')
_trfXs = {  # (from_TRF, to_TRF):           mm       mm       mm     ppb     mas      mas      mas
    # see U{Transformation Parameters ITRF2014<http://ITRF.IGN.FR/doc_ITRF/Transfo-ITRF2014_ITRFs.txt>}
    (_ITRF2014_, _ITRF2008_): _D(epoch=_F(2010),  # <http://ITRF.ENSG.IGN.FR/ITRF_solutions/2014/tp_14-08.php>
                                 xform=_T(  1.6,     1.9,     2.4,  -0.02,  _0_0,    _0_0,    _0_0),
                                 rates=_T( _0_0,    _0_0,   -_0_1,   0.03,  _0_0,    _0_0,    _0_0)),
    (_ITRF2014_, _ITRF2005_): _D(epoch=_F(2010),
                                 xform=_T(  2.6,    _1_0,    -2.3,   0.92,  _0_0,    _0_0,    _0_0),
                                 rates=_T(  0.3,    _0_0,   -_0_1,   0.03,  _0_0,    _0_0,    _0_0)),
    (_ITRF2014_, _ITRF2000_): _D(epoch=_F(2010),
                                 xform=_T(  0.7,     1.2,   -26.1,   2.12,  _0_0,    _0_0,    _0_0),
                                 rates=_T( _0_1,    _0_1,    -1.9,   0.11,  _0_0,    _0_0,    _0_0)),
    (_ITRF2014_, _ITRF97_):   _D(epoch=_F(2010),
                                 xform=_T(  7.4,   -_0_5,   -62.8,   3.8,   _0_0,    _0_0,    _0_26),
                                 rates=_T( _0_1,   -_0_5,    -3.3,   0.12,  _0_0,    _0_0,    _0_02)),
    (_ITRF2014_, _ITRF96_):   _D(epoch=_F(2010),
                                 xform=_T(  7.4,   -_0_5,   -62.8,   3.8,   _0_0,    _0_0,    _0_26),
                                 rates=_T( _0_1,   -_0_5,    -3.3,   0.12,  _0_0,    _0_0,    _0_02)),
    (_ITRF2014_, _ITRF94_):   _D(epoch=_F(2010),
                                 xform=_T(  7.4,   -_0_5,   -62.8,   3.8,   _0_0,    _0_0,    _0_26),
                                 rates=_T( _0_1,   -_0_5,    -3.3,   0.12,  _0_0,    _0_0,    _0_02)),
    (_ITRF2014_, _ITRF93_):   _D(epoch=_F(2010),
                                 xform=_T(-50.4,     3.3,   -60.2,   4.29,  -2.81,   -3.38,    0.4),
                                 rates=_T( -2.8,   -_0_1,    -2.5,   0.12,  -0.11,   -0.19,    0.07)),
    (_ITRF2014_, _ITRF92_):   _D(epoch=_F(2010),
                                 xform=_T( 15.4,     1.5,   -70.8,   3.09,  _0_0,    _0_0,    _0_26),
                                 rates=_T( _0_1,   -_0_5,    -3.3,   0.12,  _0_0,    _0_0,    _0_02)),
    (_ITRF2014_, _ITRF91_):   _D(epoch=_F(2010),
                                 xform=_T( 27.4,    15.5,   -76.8,   4.49,  _0_0,    _0_0,    _0_26),
                                 rates=_T( _0_1,   -_0_5,    -3.3,   0.12,  _0_0,    _0_0,    _0_02)),
    (_ITRF2014_, _ITRF90_):   _D(epoch=_F(2010),
                                 xform=_T( 25.4,    11.5,   -92.8,   4.79,  _0_0,    _0_0,    _0_26),
                                 rates=_T( _0_1,   -_0_5,    -3.3,   0.12,  _0_0,    _0_0,    _0_02)),
    (_ITRF2014_, _ITRF89_):   _D(epoch=_F(2010),
                                 xform=_T( 30.4,    35.5,  -130.8,   8.19,  _0_0,    _0_0,    _0_26),
                                 rates=_T( _0_1,   -_0_5,    -3.3,   0.12,  _0_0,    _0_0,    _0_02)),
    (_ITRF2014_, _ITRF88_):   _D(epoch=_F(2010),
                                 xform=_T( 25.4,   -_0_5,  -154.8,  11.29,  _0_1,    _0_0,    _0_26),
                                 rates=_T( _0_1,   -_0_5,    -3.3,   0.12,  _0_0,    _0_0,    _0_02)),

    # see U{Transformation Parameters ITRF2008<http://ITRF.IGN.FR/doc_ITRF/Transfo-ITRF2008_ITRFs.txt>}
#   (_ITRF2008_, _ITRF2005_): _D(epoch=_F(2005),  # <http://ITRF.ENSG.IGN.FR/ITRF_solutions/2008/tp_08-05.php>
#                                xform=_T(-_0_5,    -0.9,    -4.7,   0.94,  _0_0,    _0_0,    _0_0),
#                                rates=_T(  0.3,    _0_0,    _0_0,  _0_0,   _0_0,    _0_0,    _0_0)),
    (_ITRF2008_, _ITRF2005_): _D(epoch=_F(2000),
                                 xform=_T( -2.0,    -0.9,    -4.7,   0.94,  _0_0,    _0_0,    _0_0),
                                 rates=_T(  0.3,    _0_0,    _0_0,  _0_0,   _0_0,    _0_0,    _0_0)),
    (_ITRF2008_, _ITRF2000_): _D(epoch=_F(2000),
                                 xform=_T( -1.9,    -1.7,   -10.5,   1.34,  _0_0,    _0_0,    _0_0),
                                 rates=_T( _0_1,    _0_1,    -1.8,   0.08,  _0_0,    _0_0,    _0_0)),
    (_ITRF2008_, _ITRF97_):   _D(epoch=_F(2000),
                                 xform=_T(  4.8,     2.6,   -33.2,   2.92,  _0_0,    _0_0,    _0_06),
                                 rates=_T( _0_1,   -_0_5,    -3.2,  _0_09,  _0_0,    _0_0,    _0_02)),
    (_ITRF2008_, _ITRF96_):   _D(epoch=_F(2000),
                                 xform=_T(  4.8,     2.6,   -33.2,   2.92,  _0_0,    _0_0,    _0_06),
                                 rates=_T( _0_1,   -_0_5,    -3.2,  _0_09,  _0_0,    _0_0,    _0_02)),
    (_ITRF2008_, _ITRF94_):   _D(epoch=_F(2000),
                                 xform=_T(  4.8,     2.6,   -33.2,   2.92,  _0_0,    _0_0,    _0_06),
                                 rates=_T( _0_1,   -_0_5,    -3.2,  _0_09,  _0_0,    _0_0,    _0_02)),
    (_ITRF2008_, _ITRF93_):   _D(epoch=_F(2000),
                                 xform=_T(-24.0,     2.4,   -38.6,   3.41,  -1.71,   -1.48,   -0.3),
                                 rates=_T( -2.8,   -_0_1,    -2.4,  _0_09,  -0.11,   -0.19,    0.07)),
    (_ITRF2008_, _ITRF92_):   _D(epoch=_F(2000),
                                 xform=_T( 12.8,     4.6,   -41.2,   2.21,  _0_0,    _0_0,    _0_06),
                                 rates=_T( _0_1,   -_0_5,    -3.2,  _0_09,  _0_0,    _0_0,    _0_02)),
    (_ITRF2008_, _ITRF91_):   _D(epoch=_F(2000),
                                 xform=_T( 24.8,    18.6,   -47.2,   3.61,  _0_0,    _0_0,    _0_06),
                                 rates=_T( _0_1,   -_0_5,    -3.2,  _0_09,  _0_0,    _0_0,    _0_02)),
    (_ITRF2008_, _ITRF90_):   _D(epoch=_F(2000),
                                 xform=_T( 22.8,    14.6,   -63.2,   3.91,  _0_0,    _0_0,    _0_06),
                                 rates=_T( _0_1,   -_0_5,    -3.2,  _0_09,  _0_0,    _0_0,    _0_02)),
    (_ITRF2008_, _ITRF89_):   _D(epoch=_F(2000),
                                 xform=_T( 27.8,    38.6,  -101.2,   7.31,  _0_0,    _0_0,    _0_06),
                                 rates=_T( _0_1,   -_0_5,    -3.2,  _0_09,  _0_0,    _0_0,    _0_02)),
    (_ITRF2008_, _ITRF88_):   _D(epoch=_F(2000),
                                 xform=_T( 22.8,     2.6,  -125.2,  10.41,  _0_1,    _0_0,    _0_06),
                                 rates=_T( _0_1,   -_0_5,    -3.2,  _0_09,  _0_0,    _0_0,    _0_02)),

    (_ITRF2005_, _ITRF2000_): _D(epoch=_F(2000),  # <http://ITRF.ENSG.IGN.FR/ITRF_solutions/2005/tp_05-00.php>
                                 xform=_T( _0_1,    -0.8,    -5.8,   0.4,   _0_0,    _0_0,    _0_0),
                                 rates=_T( -0.2,    _0_1,    -1.8,   0.08,  _0_0,    _0_0,    _0_0)),

    (_ITRF2000_, _ITRF97_):   _D(epoch=_F(1997),
                                 xform=_T( 0.67,     0.61,   -1.85,  1.55,  _0_0,    _0_0,    _0_0),
                                 rates=_T(_0_0,     -0.06,   -0.14, _0_01,  _0_0,    _0_0,    _0_02)),
    (_ITRF2000_, _ITRF96_):   _D(epoch=_F(1997),
                                 xform=_T( 0.67,     0.61,   -1.85,  1.55,  _0_0,    _0_0,    _0_0),
                                 rates=_T(_0_0,     -0.06,   -0.14, _0_01,  _0_0,    _0_0,    _0_02)),
    (_ITRF2000_, _ITRF94_):   _D(epoch=_F(1997),
                                 xform=_T( 0.67,     0.61,   -1.85,  1.55,  _0_0,    _0_0,    _0_0),
                                 rates=_T(_0_0,     -0.06,   -0.14, _0_01,  _0_0,    _0_0,    _0_02)),
    (_ITRF2000_, _ITRF93_):   _D(epoch=_F(1988),
                                 xform=_T( 12.7,     6.5,   -20.9,   1.95,  -0.39,    0.8,    -1.14),
                                 rates=_T( -2.9,    -0.2,    -0.6,  _0_01,  -0.11,   -0.19,    0.07)),
    (_ITRF2000_, _ITRF92_):   _D(epoch=_F(1988),
                                 xform=_T( 1.47,     1.35,   -1.39,  0.75,  _0_0,    _0_0,    -0.18),
                                 rates=_T(_0_0,     -0.06,   -0.14, _0_01,  _0_0,    _0_0,    _0_02)),
    (_ITRF2000_, _ITRF91_):   _D(epoch=_F(1988),
                                 xform=_T( 26.7,    27.5,   -19.9,   2.15,  _0_0,    _0_0,    -0.18),
                                 rates=_T( _0_0,    -0.6,    -1.4,  _0_01,  _0_0,    _0_0,    _0_02)),
    (_ITRF2000_, _ITRF90_):   _D(epoch=_F(1988),
                                 xform=_T( 2.47,     2.35,   -3.59,  2.45,  _0_0,    _0_0,    -0.18),
                                 rates=_T(_0_0,     -0.06,   -0.14, _0_01,  _0_0,    _0_0,    _0_02)),
    (_ITRF2000_, _ITRF89_):   _D(epoch=_F(1988),
                                 xform=_T( 2.97,     4.75,   -7.39,  5.85,  _0_0,    _0_0,    -0.18),
                                 rates=_T(_0_0,     -0.06,   -0.14, _0_01,  _0_0,    _0_0,    _0_02)),
    (_ITRF2000_, _ITRF88_):   _D(epoch=_F(1988),
                                 xform=_T( 2.47,     1.15,   -9.79,  8.95,  _0_1,    _0_0,    -0.18),
                                 rates=_T(_0_0,     -0.06,   -0.14, _0_01,  _0_0,    _0_0,    _0_02)),

    # see U{Boucher, C. & Altamimi, Z. "Memo: Specifications for reference frame fixing in the
    # analysis of a EUREF GPS campaign" (2011) <https://ETRS89.ENSG.IGN.FR/memo-V8.pdf>} and
    # Altamimi, Z. U{"Key results of ITRF2014 and implication to ETRS89 realization", EUREF2016
    # <https://www.EUREF.EU/symposia/2016SanSebastian/01-02-Altamimi.pdf>}.
    (_ITRF2014_, _ETRF2000_): _D(epoch=_F(2000),
                                 xform=_T( 53.7,    51.2,   -55.1,   1.02,   0.891,   5.39,   -8.712),
                                 rates=_T( _0_1,    _0_1,    -1.9,   0.11,   0.081,   0.49,   -0.792)),
    (_ITRF2008_, _ETRF2000_): _D(epoch=_F(2000),
                                 xform=_T( 52.1,    49.3,   -58.5,   1.34,   0.891,   5.39,   -8.712),
                                 rates=_T( _0_1,    _0_1,    -1.8,   0.08,   0.081,   0.49,   -0.792)),
    (_ITRF2005_, _ETRF2000_): _D(epoch=_F(2000),
                                 xform=_T( 54.1,    50.2,   -53.8,   0.4,    0.891,   5.39,   -8.712),
                                 rates=_T( -0.2,    _0_1,    -1.8,   0.08,   0.081,   0.49,   -0.792)),
    (_ITRF2000_, _ETRF2000_): _D(epoch=_F(2000),
                                 xform=_T( 54.0,    51.0,   -48.0,  _0_0,    0.891,   5.39,   -8.712),
                                 rates=_T( _0_0,    _0_0,    _0_0,  _0_0,    0.081,   0.49,   -0.792)),

    # see U{Solar, T. & Snay, R.A. "Transforming Positions and Velocities between the
    # International Terrestrial Reference Frame of 2000 and North American Datum of 1983"
    # (2004)<https://www.NGS.NOAA.gov/CORS/Articles/SolerSnayASCE.pdf>}
    (_ITRF2000_, _NAD83_):    _D(epoch=_F(1997),  # note NAD83(CORS96)
                                 xform=_T(995.6, -1901.3,  -521.5,   0.62,  25.915,   9.426,  11.599),
                                 rates=_T(  0.7,    -0.7,    _0_5,  -0.18,   0.067,  -0.757,  -0.051)),

    # GDA2020 "Geocentric Datum of Australia 2020 Technical Manual", v1.5, 2020-12-09, Table 3.3 and 3.4
    # <https://www.ICSM.gov.AU/sites/default/files/2020-12/GDA2020%20Technical%20Manual%20V1.5_4.pdf>
    # (the GDA2020 xforms are different but the rates are the same as GDA94, further below)
    (_ITRF2014_, _GDA2020_):  _D(epoch=_F(2020),
                                 xform=_T( _0_0,    _0_0,   _0_0,  _0_0,    _0_0,    _0_0,    _0_0),
                                 rates=_T( _0_0,    _0_0,   _0_0,  _0_0,     1.50379, 1.18346, 1.20716)),
    (_ITRF2008_, _GDA2020_):  _D(epoch=_F(2020),
                                 xform=_T( 13.79,    4.55,   15.22,  2.5,    0.2808,  0.2677, -0.4638),
                                 rates=_T(  1.42,    1.34,    0.9,   0.109,  1.5461,  1.182,   1.1551)),
    (_ITRF2005_, _GDA2020_):  _D(epoch=_F(2020),
                                 xform=_T( 40.32,  -33.85,  -16.72,  4.286, -1.2893, -0.8492, -0.3342),
                                 rates=_T(  2.25,   -0.62,   -0.56,  0.294, -1.4707, -1.1443, -1.1701)),
    (_ITRF2000_, _GDA2020_):  _D(epoch=_F(2020),
                                 xform=_T(-105.52,  51.58,  231.68,  3.55,   4.2175,  6.3941,  0.8617),
                                 rates=_T(  -4.66,   3.55,   11.24,  0.249,  1.7454,  1.4868,  1.224)),

    # see Table 2 in U{Dawson, J. & Woods, A. "ITRF to GDA94 coordinate transformations", Journal of
    # Applied Geodesy 4 (2010), 189-199<https://www.ResearchGate.net/publication/258401581_ITRF_to_GDA94_coordinate_transformations>}
    # (note, sign of rotations for GDA94 reversed as "Australia assumes rotation to be of coordinate
    # axes" rather than the more conventional "position around the coordinate axes")
    (_ITRF2008_, _GDA94_):    _D(epoch=_F(1994),
                                 xform=_T(-84.68,  -19.42,   32.01,  9.71,  -0.4254,  2.2578,  2.4015),
                                 rates=_T(  1.42,    1.34,    0.9,   0.109,  1.5461,  1.182,   1.1551)),
    (_ITRF2005_, _GDA94_):    _D(epoch=_F(1994),
                                 xform=_T(-79.73,   -6.86,   38.03,  6.636,  0.0351, -2.1211, -2.1411),
                                 rates=_T(  2.25,   -0.62,   -0.56,  0.294, -1.4707, -1.1443, -1.1701)),
    (_ITRF2000_, _GDA94_):    _D(epoch=_F(1994),
                                 xform=_T(-45.91,  -29.85,  -20.37,  7.07,  -1.6705,  0.4594,  1.9356),
                                 rates=_T( -4.66,    3.55,   11.24,  0.249,  1.7454,  1.4868,  1.224)),
}

_Forward =  _0_001  # mm2m, ppb2ppM, mas2as
_Reverse = -_0_001  # same, inverse transforms


def _intermediate(n1, n2):
    '''(INTERNAL) Find a trf* "in between" C{n1} and C{n2}.
    '''
    f1 = set(m for n, m in _trfXs.keys() if n == n1)  # from trf1
    t2 = set(n for n, m in _trfXs.keys() if m == n2)  # to trf2
    n = f1.intersection(t2)
    return n.pop() if n else NN


def _reframeTransforms2(rf2, rf, epoch):
    '''(INTERNAL) Get 0, 1 or 2 Helmert L{Transform}s to convert
       reference frame B{C{rf}} observed at B{C{epoch}} into B{C{rf2}}.
    '''
    e = rf.epoch if epoch is None else Epoch(epoch)

    n2 = rf2.name  # .upper()
    n1 = rf.name   # .upper()
    if n1 == n2 or (n1.startswith(_ITRF_) and n2.startswith(_WGS84_)) \
                or (n2.startswith(_ITRF_) and n1.startswith(_WGS84_)):
        return e, ()  # PYCHOK returns

    if (n1, n2) in _trfXs:
        return e, (_2Transform((n1, n2), e, _Forward),)  # PYCHOK returns

    if (n2, n1) in _trfXs:
        return e, (_2Transform((n2, n1), e, _Reverse),)  # PYCHOK returns

    n = _intermediate(n1, n2)
    if n:
        return e, (_2Transform((n1, n), e, _Forward),  # PYCHOK returns
                   _2Transform((n, n2), e, _Forward))

    n = _intermediate(n2, n1)
    if n:
        return e, (_2Transform((n, n1), e, _Reverse),  # PYCHOK returns
                   _2Transform((n2, n), e, _Reverse))

    t = _SPACE_(RefFrame.__name__, repr(n1), _to_, repr(n2))
    raise TRFError(_no_(_conversion_), txt=t)


def _2Transform(n1_n2, epoch, _Forward_Reverse):
    '''(INTERNAL) Combine a 14-element Helmert C{trfXB{[n1_n2]}}
       into a 7-element L{Transform} observed at B{C{epoch}}.
    '''
    X = _trfXs[n1_n2]
    e = epoch - X.epoch  # fractional delta years
    d = dict((n, (x + r * e) * _Forward_Reverse) for
              n,  x,  r in zip(_trfNs, X.xform, X.rates))
    return Transform(**d)


if __name__ == '__main__':

    from pygeodesy.interns import _COMMA_, _SPACE_, _NL_, _NL_var_

    n, y = date2epoch.__name__, 2020
    for m in range(1, 13):
        for d in (1, _mDays[m] - 1, _mDays[m]):
            e = date2epoch(y, m, d)
            print(_SPACE_('#', Fmt.PAREN(n, _COMMASPACE_(y, m, d)), Fmt.f(e, prec=3)))

    # __doc__ of this file, force all into registery
    t = [NN] + RefFrames.toRepr(all=True).split(_NL_)
    print(_NL_var_.join(i.strip(_COMMA_) for i in t))

# **) MIT License
#
# Copyright (C) 2016-2021 -- mrJean1 at Gmail -- All Rights Reserved.
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
# OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR
# OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
# ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.

# % python -m pygeodesy.trf
#
# date2epoch(2020, 1, 1) 2020.003
# date2epoch(2020, 1, 30) 2020.082
# date2epoch(2020, 1, 31) 2020.085
# date2epoch(2020, 2, 1) 2020.087
# date2epoch(2020, 2, 28) 2020.161
# date2epoch(2020, 2, 29) 2020.164
# date2epoch(2020, 3, 1) 2020.167
# date2epoch(2020, 3, 30) 2020.246
# date2epoch(2020, 3, 31) 2020.249
# date2epoch(2020, 4, 1) 2020.251
# date2epoch(2020, 4, 29) 2020.328
# date2epoch(2020, 4, 30) 2020.331
# date2epoch(2020, 5, 1) 2020.333
# date2epoch(2020, 5, 30) 2020.413
# date2epoch(2020, 5, 31) 2020.415
# date2epoch(2020, 6, 1) 2020.418
# date2epoch(2020, 6, 29) 2020.495
# date2epoch(2020, 6, 30) 2020.497
# date2epoch(2020, 7, 1) 2020.5
# date2epoch(2020, 7, 30) 2020.579
# date2epoch(2020, 7, 31) 2020.582
# date2epoch(2020, 8, 1) 2020.585
# date2epoch(2020, 8, 30) 2020.664
# date2epoch(2020, 8, 31) 2020.667
# date2epoch(2020, 9, 1) 2020.669
# date2epoch(2020, 9, 29) 2020.746
# date2epoch(2020, 9, 30) 2020.749
# date2epoch(2020, 10, 1) 2020.751
# date2epoch(2020, 10, 30) 2020.831
# date2epoch(2020, 10, 31) 2020.833
# date2epoch(2020, 11, 1) 2020.836
# date2epoch(2020, 11, 29) 2020.913
# date2epoch(2020, 11, 30) 2020.915
# date2epoch(2020, 12, 1) 2020.918
# date2epoch(2020, 12, 30) 2020.997
# date2epoch(2020, 12, 31) 2021.0
