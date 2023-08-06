
# -*- coding: utf-8 -*-

# The setuptools script to build, install and test a PyGeodesy distribution.

# Tested with 64-bit Python 2.7.13-18, 3.6.1-2, 3.7.0-6 and 3.8.0-5
# (using setuptools 28.8.0), but only on macOS 10.12.3-6 Sierra,
# 10.13.0-6 High Sierra, 10.15.5-7 Catalina and 11.0.1 (10.16) Big Sur

# python setup.py sdist --formats=gztar,bztar,zip  # ztar,tar
# python setup.py bdist_wheel --universal  # XXX
# python setup.py test
# python setup.py install

# <https://packaging.Python.org/key_projects/#setuptools>
# <https://packaging.Python.org/distributing>
# <https://docs.Python.org/2/distutils/sourcedist.html>
# <https://docs.Python.org/3.6/distutils/sourcedist.html>
# <https://setuptools.ReadTheDocs.io/en/latest/setuptools.html#developer-s-guide>
# <https://setuptools.ReadTheDocs.io/en/latest/setuptools.html#test-build-package-and-run-a-unittest-suite>

from setuptools import setup

__all__ = ()
__version__ = '21.02.27'


def _c2(*names):
    return ' :: '.join(names)


def _long_description():
    with open('README.rst', 'rb') as f:
        t = f.read()
        if isinstance(t, bytes):
            t = t.decode('utf-8')
        return t


def _version():
    with open('pygeodesy/__init__.py') as f:
        for t in f.readlines():
            if t.startswith('__version__'):
                v = t.split('=')[-1].strip().strip('\'"')
                return '.'.join(map(str, map(int, v.split('.'))))


_KeyWords = ('Albers', 'altitude', 'Andoyer', 'antipode', 'area',
             'Authalic', 'auxiliary', 'azimuth', 'azimuthal',
             'bearing', 'Barsky',
             'cached', 'cartesian', 'Cassini', 'Cassini-Soldner', 'circle-intersections',
             'clip', 'Cohen', 'Cohen-Sutherland', 'conformal', 'conic',
             'cosines-law', 'coverage', 'curvature', 'cylindrical',
             'datum', 'deprecation', 'deficit', 'development', 'discrete', 'distance', 'Douglas',
             'earth', 'eccentricity', 'ECEF', 'elevation', 'ellipsoid', 'elliptic',
             'EPSG', 'equal-area', 'equidistant', 'equirectangular', 'ETM', 'ETRF',
             'Euclidean', 'ExactTM', 'excess',
             'flattening', 'fmath', 'Forsythe', 'fractional', 'Frechet', 'Fréchet',
             'GARS', 'geocentric', 'geodesy', 'geodetic', 'GeodTest', 'geographiclib',
             'geohash', 'geoid', 'geoidHeight', 'GeoidHeights', 'georef', 'Girard', 'gnomonic',
             'gons', 'grades', 'gradians',
             'Hausdorff', 'Haversine', 'height', 'Hodgman', 'horizon', 'Hubeny',
             'IDW', 'intermediate', 'interpolate',
             'intersect', 'intersection', 'intersections',
             'Inverse-Distance-Weighting', 'Isometric', 'ITRF',
             'Karney', 'Krueger', 'Krüger',
             'Lambert', 'latitude', 'law-of-cosines', 'Lesh',
             'L_Huilier', 'LHuilier', 'Liang', 'Liang-Barsky', 'linearize',
             'LocalCartesian', 'longitude', 'lune',
             'mean', 'memoize', 'Mercator', 'MGRS',
             'nearest', 'Norrdine', 'numpy', 'n-vector', 'Nvector',
             'oblate', 'orthographic', 'OSGR', 'overlap',
             'parallel', 'parallel-of-latitude', 'Parametric', 'path-intersection',
             'perimeter', 'Peucker', 'polar', 'prolate', 'Pseudo-Mercator',
             'PyGeodesy', 'PyInstaller', 'PyPy',
             'radii', 'radius', 'Ramer', 'Ramer-Douglas-Peucker', 'Rectifying',
             'Reduced', 'Rey-Jer', 'Reumann', 'Reumann-Witkam', 'rhumb',
             'scipy', 'semi-perimeter', 'simplify', 'Snyder', 'Soldner',
             'sphere', 'sphere-intersections', 'stereographic', 'spherical_deficit', 'spherical_excess',
             'Sudano', 'surface-area', 'Sutherland', 'Sutherland-Hodgman',
             'Terrestrial-Reference-Frame', 'Thomas', 'TMcoords', 'TMExact',
             'Transverse', 'TransverseMercatorExact', 'TRF', 'trigonometry', 'trilateration',
             'unit', 'unroll', 'UPS', 'UTM', 'UTM/UPS',
             'Veness', 'Vermeille', 'Vincenty', 'Visvalingam', 'Visvalingam-Whyatt',
             'volume', ' volumetric',
             'Web-Mercator', 'WGRS', 'WGS', 'Whyatt', 'Witkam', 'You')

setup(name='PyGeodesy',
      packages=['pygeodesy', 'pygeodesy.deprecated'],
      description='Pure Python geodesy tools',
      version=_version(),

      author='Jean M. Brouwers',
      author_email='mrJean1@Gmail.com',
      maintainer='Jean M. Brouwers',
      maintainer_email='mrJean1@Gmail.com',

      license='MIT',
      keywords=' '.join(_KeyWords),
      url='https://GitHub.com/mrJean1/PyGeodesy',

      long_description=_long_description(),

      package_data={'pygeodesy': ['LICENSE']},

#     data_files=[('docs',         ['docs/*.*']),
#                 ('images',       ['test/testRoute.jpg']),
#                 ('test',         ['test/test*.py']),
#                 ('testcoverage', ['testcoverage/*.*',
#                                   'testcoverage.pdf',
#                                   'testcoverage.rc']),
#                 ('testresults',  ['testresults/*.txt'])],
#     data_files fails somehow, see file MANIFEST.in

      test_suite='test.TestSuite',

      zip_safe=False,

      # <https://PyPI.org/pypi?%3Aaction=list_classifiers>
      classifiers=[_c2('Development Status', '5 - Production/Stable'),
                   _c2('Environment', 'Console'),
                   _c2('Intended Audience', 'Developers'),
                   _c2('License', 'OSI Approved', 'MIT License'),
                   _c2('Operating System', 'OS Independent'),
                   _c2('Programming Language', 'Python'),
#                  _c2('Programming Language', 'Python', '2.6'),
                   _c2('Programming Language', 'Python', '2.7'),
#                  _c2('Programming Language', 'Python', '3.5'),
                   _c2('Programming Language', 'Python', '3.6'),
                   _c2('Programming Language', 'Python', '3.7'),
                   _c2('Programming Language', 'Python', '3.8'),
                   _c2('Programming Language', 'Python', '3.9'),
                   _c2('Topic', 'Software Development'),
                   _c2('Topic', 'Scientific/Engineering', 'GIS'),
      ],

#     download_url='https://GitHub.com/mrJean1/PyGeodesy',
#     entry_points={},
#     include_package_data=False,
#     install_requires=[],
#     namespace_packages=[],
#     py_modules=[],
)
