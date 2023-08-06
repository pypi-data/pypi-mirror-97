# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['exposure']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'exposure',
    'version': '0.1.0',
    'description': 'tool for compute with exposure settings and metrics for cameras',
    'long_description': '# Exposure\n\n![Build](https://github.com/mrijken/exposure/workflows/CI/badge.svg)\n\nWith Exposure you can compute the exposure for a photo camera based\non settings of the camera and metrics of the environment.\n\n## Installation\n\n`pip install exposure`\n\n## Usage\n\n    >>> from exposure import Av, Tv, Sv, Bv, Iv, Exposure\n    >>> from decimal import Decimal\n    >>> from fractions import Fraction\n\n### Aperture\n\n    >>> Av.from_stop(1)\n    Av f/1.4\n\n    >>> Av.from_focal_length_and_diameter(10, 5)\n    Av f/2.0\n\n    >>> Av.from_fstop(Decimal("1.4"))\n    Av f/1.4\n\n    >>> Av.from_fstop(Decimal("22")).stop\n    Fraction(9, 1)\n\n    >>> Av.from_fstop(Decimal("22")).fstop\n    Decimal(\'22\')\n\n### Speed\n\n    >>> Sv.from_iso(100)\n    Sv 100 ISO\n\n    >>> Sv.from_stop(Fraction(1, 1))\n    Sv 200 ISO\n\n    >>> Sv.from_iso(100).stop\n    Fraction(0, 1)\n\n    >>> Sv.from_iso(100).iso\n    100\n\n### Shutter\n\n    >>> Tv.from_stop(1)\n    Tv 2 sec\n\n    >>> Tv.from_time(Fraction(10, 13))\n    Tv 10/13 sec\n\n    >>> Tv.from_time(Fraction(2, 1)).stop\n    Fraction(1, 1)\n\n    >>> Tv.from_time(Fraction(2, 1)).time\n    Fraction(2, 1)\n\n### Brightness\n\n    >>> Bv.from_foot_lamberts(1)\n    Bv 3.4 cd/m2\n\n    >>> Bv.from_candelas(109)\n    Bv 109.2 cd/m2\n\n    >>> Bv.from_stop(3)\n    Bv 27.4 cd/m2\n\n    >>> Bv.from_stop(3).stop\n    Fraction(3, 1)\n\n    >>> Bv.from_stop(3).candelas\n    27.4\n\n    >>> Bv.from_stop(3).foot_lamberts\n    8\n\n### Incident Light\n\n    >>> Iv.from_foot_candles(25)\n    Iv 269.2 lux\n\n    >>> Iv.from_lux(1076)\n    Iv 1076.0 lux\n\n    >>> Iv.from_stop(3)\n    Iv 537.6 lux\n\n    >>> Iv.from_lux(1076).stop\n    Fraction(4, 1)\n\n    >>> Iv.from_lux(1076).lux\n    1076.0\n\n    >>> Iv.from_lux(1076).foot_candles\n    99.9\n\n\n### Exposure\n\n    >>> tv = Tv.from_stop(1)\n    >>> av = Av.from_stop(2)\n    >>> sv = Sv.from_stop(2)\n    >>> bv = Bv.from_stop(1)\n    >>> iv = Iv.from_stop(1)\n\n    The exposure is in balance when\n\n    >>> tv + av == sv + bv\n    True\n\n    or\n\n    >>> tv + av == sv + iv\n    True\n\n    This can also be used to compute a needed setting, like\n\n    >>> Tv.from_exposures(sv, bv, av)\n    Tv 2 sec\n    >>> Tv.from_exposures(sv, bv, av) == tv\n    True\n\n    >>> Av.from_exposures(sv, bv, tv)\n    Av f/2.0\n\n    >>> Sv.from_exposures(tv, bv, av)\n    Sv 400 ISO\n\n    >>> Sv.from_exposures(tv, iv, av)\n    Sv 400 ISO\n\nFuture work:\n\n* from_exif\n\n## Disclaimer\n\nThis package is based on http://dougkerr.net/Pumpkin/articles/APEX.pdf\n',
    'author': 'Marc Rijken',
    'author_email': 'marc@rijken.org',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
