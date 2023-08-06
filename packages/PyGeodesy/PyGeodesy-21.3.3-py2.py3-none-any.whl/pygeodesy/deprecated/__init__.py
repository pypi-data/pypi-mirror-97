
# -*- coding: utf-8 -*-

u'''DEPRECATED classes, functions, etc. exported for backward compatibility,
including deprecated modules C{pygeodesy.bases}, C{pygeodesy.datum} and
C{pygeodesy,nvector}, previously inside the C{pygeodesy} package.

Use either C{from pygeodesy import bases} or C{from pygeodesy.deprecated import
bases}.  Likewise for C{datum} and C{nvector}.
'''
from pygeodesy.heights import HeightIDWequirectangular as _HeightIDWequirectangular, \
                              HeightIDWeuclidean as _HeightIDWeuclidean, \
                              HeightIDWhaversine as _HeightIDWhaversine
from pygeodesy.errors import TRFError as _TRFError
from pygeodesy.interns import EPS, NN, R_M, _COMMASPACE_, _scalar_, _SPACE_, _UNDER_
from pygeodesy.interns import _easting_, _end_, _hemipole_, _northing_, _sep_, \
                              _start_, _zone_  # PYCHOK used!
from pygeodesy.lazily import _ALL_LAZY, isLazy
from pygeodesy.props import deprecated_class, deprecated_function
from pygeodesy.named import _NamedTuple, _Pass
from pygeodesy.streprs import Fmt as _Fmt
from pygeodesy.units import Easting, Northing, Number_, Scalar_, Str
if isLazy:  # XXX force import of all deprecated modules
    import pygeodesy.deprecated.bases as bases, \
           pygeodesy.deprecated.datum as datum, \
           pygeodesy.deprecated.nvector as nvector  # PYCHOK unused
    # XXX instead, use module_property or enhance .lazily

__all__ = _ALL_LAZY.deprecated
__version__ = '21.02.12'

OK      = 'OK'  # OK for test like I{if ... is OK: ...}
_value_ = 'value'
_WGS84  = _UTM = object()


# DEPRECATED classes, for export only
@deprecated_class
class ClipCS3Tuple(_NamedTuple):  # PYCHOK no cover
    '''3-Tuple C{(start, end, index)} DEPRECATED, see function L{clipCS3}.
    '''
    _Names_ = (_start_, _end_, 'index')
    _Units_ = (_Pass,   _Pass,  Number_)


@deprecated_class
class HeightIDW(_HeightIDWeuclidean):  # PYCHOK no cover
    '''DEPRECATED, use class L{HeightIDWeuclidean}.
    '''
    pass


@deprecated_class
class HeightIDW2(_HeightIDWequirectangular):  # PYCHOK no cover
    '''DEPRECATED, use class L{HeightIDWequirectangular}.
    '''
    pass


@deprecated_class
class HeightIDW3(_HeightIDWhaversine):  # PYCHOK no cover
    '''DEPRECATED, use class L{HeightIDWhaversine}.
    '''
    pass


@deprecated_class
class RefFrameError(_TRFError):  # PYCHOK no cover
    '''DEPRECATED, use class L{TRFError}.
    '''
    pass


@deprecated_class
class UtmUps4Tuple(_NamedTuple):  # PYCHOK no cover
    '''OBSOLETE, expect a L{UtmUps5Tuple} from method C{Mgrs.toUtm(utm=None)}.

       4-Tuple C{(zone, hemipole, easting, northing)} as C{str},
       C{str}, C{meter} and C{meter}.
    '''
    _Names_ = (_zone_, _hemipole_, _easting_, _northing_)  # band
    _Units_ = ( Str,    Str,        Easting,   Northing)


@deprecated_function
def anStr(name, OKd='._-', sub=_UNDER_):  # PYCHOK no cover
    '''DEPRECATED, use function L{anstr}.
    '''
    from pygeodesy.streprs import anstr
    return anstr(name, OKd=OKd, sub=sub)


@deprecated_function
def areaof(points, adjust=True, radius=R_M, wrap=True):  # PYCHOK no cover
    '''DEPRECATED, use function L{areaOf}.
    '''
    from pygeodesy.points import areaOf
    return areaOf(points, adjust=adjust, radius=radius, wrap=wrap)


@deprecated_function
def bounds(points, wrap=True, LatLon=None):  # PYCHOK no cover
    '''DEPRECATED, use function L{boundsOf}.

       @return: 2-Tuple C{(latlonSW, latlonNE)} as B{C{LatLon}}
                or 4-Tuple C{(latS, lonW, latN, lonE)} if
                B{C{LatLon}} is C{None}.
    '''
    from pygeodesy.points import boundsOf
    return tuple(boundsOf(points, wrap=wrap, LatLon=LatLon))


@deprecated_function
def clipCS3(points, lowerleft, upperright, closed=False, inull=False):  # PYCHOK no cover
    '''DEPRECATED, use function L{clipCS4}.

       @return: Yield a L{ClipCS3Tuple}C{(start, end, index)} for each
                edge of the I{clipped} path.
    '''
    from pygeodesy.clipy import clipCS4
    for p1, p2, _, j in clipCS4(points, lowerleft, upperright,
                                        closed=closed, inull=inull):
        yield ClipCS3Tuple(p1, p2, j)


@deprecated_function
def clipDMS(deg, limit):  # PYCHOK no cover
    '''DEPRECATED, use function L{clipDegrees}.
    '''
    from pygeodesy.dms import clipDegrees
    return clipDegrees(deg, limit)


@deprecated_function
def clipStr(bstr, limit=50, white=NN):  # PYCHOK no cover
    '''DEPRECATED, use function L{clips}.
    '''
    from pygeodesy.basics import clips
    return clips(bstr, limit=limit, white=white)


@deprecated_function
def decodeEPSG2(arg):  # PYCHOK no cover
    '''DEPRECATED, use function L{epsg.decode2}.

       @return: 2-Tuple C{(zone, hemipole)}
    '''
    from pygeodesy.epsg import decode2
    return tuple(decode2(arg))


@deprecated_function
def encodeEPSG(zone, hemipole=NN, band=NN):  # PYCHOK no cover
    '''DEPRECATED, use function L{epsg.encode}.

       @return: C{EPSG} code (C{int}).
    '''
    from pygeodesy.epsg import encode
    return int(encode(zone, hemipole=hemipole, band=band))


@deprecated_function
def enStr2(easting, northing, prec, *extras):  # PYCHOK no cover
    '''DEPRECATED, use function L{enstr2}.
    '''
    from pygeodesy.streprs import enstr2
    return enstr2(easting, northing, prec, *extras)


@deprecated_function
def equirectangular3(lat1, lon1, lat2, lon2, **options):  # PYCHOK no cover
    '''DEPRECATED, use function C{equirectangular_}.

       @return: 3-Tuple C{(distance2, delta_lat, delta_lon)}.
    '''
    from pygeodesy.formy import equirectangular_
    return tuple(equirectangular_(lat1, lon1, lat2, lon2, **options)[:3])


@deprecated_function
def false2f(value, name=_value_, false=True, Error=ValueError):  # PYCHOK no cover
    '''DEPRECATED, use function L{falsed2f}.
    '''
    return falsed2f(falsed=false, Error=Error, **{name: value})


@deprecated_function
def falsed2f(falsed=True, Error=ValueError, **name_value):  # PYCHOK no cover
    '''DEPRECATED, use class L{Easting} or L{Northing}.

       Convert a falsed east-/northing to non-negative C{float}.

       @kwarg falsed: Value includes false origin (C{bool}).
       @kwarg Error: Optional, overriding error (C{Exception}).
       @kwarg name_value: One B{C{name=value}} pair.

       @return: The value (C{float}).

       @raise Error: Invalid or negative B{C{name=value}}.
    '''
    t = NN
    if len(name_value) == 1:
        try:
            for f in name_value.values():
                f = float(f)
                if falsed and f < 0:
                    break
                return f
            t = 'falsed, negative'
        except (TypeError, ValueError) as x:
            t = str(x)
    from pygeodesy.errors import _InvalidError
    raise _InvalidError(Error=Error, txt=t, **name_value)


@deprecated_function
def fStr(floats, prec=6, fmt=_Fmt.f, ints=False, sep=_COMMASPACE_):  # PYCHOK no cover
    '''DEPRECATED, use function L{fstr}.
    '''
    from pygeodesy.streprs import fstr
    return fstr(floats, prec=prec, fmt=fmt, ints=ints, sep=sep)


@deprecated_function
def fStrzs(floatstr):  # PYCHOK no cover
    '''DEPRECATED, use function L{fstrzs}.
    '''
    from pygeodesy.streprs import fstrzs
    return fstrzs(floatstr)


@deprecated_function
def hypot3(x, y, z):  # PYCHOK no cover
    '''DEPRECATED, use function L{hypot_}.
    '''
    from pygeodesy.fmath import hypot_
    return hypot_(x, y, z)


@deprecated_function
def inStr(inst, *args, **kwds):  # PYCHOK no cover
    '''DEPRECATED, use function L{instr}.
    '''
    from pygeodesy.streprs import instr
    return instr(inst, *args, **kwds)


@deprecated_function
def isenclosedby(point, points, wrap=False):  # PYCHOK no cover
    '''DEPRECATED, use function L{isenclosedBy}.
    '''
    from pygeodesy.points import isenclosedBy
    return isenclosedBy(point, points, wrap=wrap)


@deprecated_function
def joined(*words, **sep):  # sep=NN
    '''DEPRECATED, use C{NN(...)}, C{NN.join_} or C{B{sep}.join}.
    '''
    return sep.get(_sep_, NN).join(map(str, words))


@deprecated_function
def joined_(*words, **sep):  # PYCHOK no cover
    '''DEPRECATED, use C{_SPACE_(...)}, C{_SPACE_.join_} or C{B{sep}.join}, sep=" ".
    '''
    return sep.get(_sep_, _SPACE_).join(map(str, words))


@deprecated_function
def nearestOn3(point, points, closed=False, wrap=False, **options):  # PYCHOK no cover
    '''DEPRECATED, use function L{nearestOn5}.

       @return: 3-Tuple C{(lat, lon, distance)}
    '''
    from pygeodesy.points import nearestOn5  # no name conflict
    return tuple(nearestOn5(point, points, closed=closed, wrap=wrap, **options)[:3])


@deprecated_function
def nearestOn4(point, points, closed=False, wrap=False, **options):  # PYCHOK no cover
    '''DEPRECATED, use function L{nearestOn5}.

       @return: 4-Tuple C{(lat, lon, distance, angle)}
    '''
    from pygeodesy.points import nearestOn5  # no name conflict
    return tuple(nearestOn5(point, points, closed=closed, wrap=wrap, **options)[:4])


@deprecated_function
def parseUTM(strUTM, datum=_WGS84, Utm=_UTM, name=NN):  # PYCHOK no cover
    '''DEPRECATED, use function L{parseUTM5}.

       @return: The UTM coordinate (B{L{Utm}}) or 4-tuple C{(zone,
                hemisphere, easting, northing)} if B{C{Utm}} is C{None}.
    '''
    from pygeodesy.datums import Datums  # PYCHOK shadows?
    from pygeodesy.utm import parseUTM5, Utm as _Utm
    d = Datums.WGS84 if datum is _WGS84 else datum  # PYCHOK shadows?
    U = _Utm if Utm is _UTM else Utm
    r = parseUTM5(strUTM, datum=d, Utm=U, name=name)
    if isinstance(r, tuple):  # UtmUps5Tuple
        r = r.zone, r.hemipole, r.easting, r.northing  # no band
    return r


@deprecated_function
def perimeterof(points, closed=False, adjust=True, radius=R_M, wrap=True):  # PYCHOK no cover
    '''DEPRECATED, use function L{perimeterOf}.
    '''
    from pygeodesy.points import perimeterOf
    return perimeterOf(points, closed=closed, adjust=adjust, radius=radius, wrap=wrap)


@deprecated_function
def polygon(points, closed=True, base=None):  # PYCHOK no cover
    '''DEPRECATED, use function L{points2}.
    '''
    from pygeodesy.deprecated.bases import points2  # PYCHOK import
    return points2(points, closed=closed, base=base)


@deprecated_function
def scalar(value, low=EPS, high=1.0, name=_scalar_, Error=ValueError):  # PYCHOK no cover
    '''DEPRECATED, use class L{Number_} or L{Scalar_}.

       @return: New value (C{float} or C{int} for C{int} B{C{low}}).

       @raise Error: Invalid B{C{value}}.
    '''
    from pygeodesy.basics import isint
    C_ = Number_ if isint(low) else Scalar_
    return C_(value, name=name, Error=Error, low=low, high=high)


@deprecated_function
def simplify2(points, pipe, radius=R_M, shortest=False, indices=False, **options):  # PYCHOK no cover
    '''DEPRECATED, use function L{simplifyRW}.
    '''
    from pygeodesy.simplify import simplifyRW
    return simplifyRW(points, pipe, radius=radius, shortest=shortest, indices=indices, **options)


@deprecated_function
def toUtm(latlon, lon=None, datum=None, Utm=_UTM, cmoff=True, name=NN):  # PYCHOK no cover
    '''DEPRECATED, use function L{toUtm8}.

       @return: The UTM coordinate (B{C{Utm}}) or a 6-tuple C{(zone,
                easting, northing, band, convergence, scale)} if
                B{C{Utm}} is C{None} or B{C{cmoff}} is C{False}.
    '''
    from pygeodesy.utm import toUtm8, Utm as _Utm
    U = _Utm if Utm is _UTM else Utm
    r = toUtm8(latlon, lon=lon, datum=datum, Utm=U, name=name, falsed=cmoff)
    if isinstance(r, tuple):  # UtmUps8Tuple
        # no hemisphere/pole and datum
        r = r.zone, r.easting, r.northing, r.band, r.convergence, r.scale
    return r


@deprecated_function
def unStr(name, *args, **kwds):  # PYCHOK no cover
    '''DEPRECATED, use function L{unstr}.
    '''
    from pygeodesy.streprs import unstr
    return unstr(name, *args, **kwds)


@deprecated_function
def utmZoneBand2(lat, lon):  # PYCHOK no cover
    '''DEPRECATED, use function L{utmZoneBand5}.

       @return: 2-Tuple C{(zone, band)}.
    '''
    from pygeodesy.utm import utmZoneBand5
    r = utmZoneBand5(lat, lon)  # UtmUpsLatLon5Tuple
    return r.zone, r.band

# **) MIT License
#
# Copyright (C) 2018-2021 -- mrJean1 at Gmail -- All Rights Reserved.
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
