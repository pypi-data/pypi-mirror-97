# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['spherical',
 'spherical.grid',
 'spherical.modes',
 'spherical.recursions',
 'spherical.utilities']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.13,<2.0', 'quaternionic>=0.2.0,<0.3.0']

extras_require = \
{':implementation_name == "cpython"': ['numba>=0.50'],
 ':python_version < "3.8"': ['importlib-metadata>=1.0,<2.0'],
 ':sys_platform != "win32"': ['spinsfast>=104.2020.8,<105.0.0'],
 'mkdocs:implementation_name == "cpython"': ['mkdocs>=1.1.2'],
 'mktheapidocs:implementation_name == "cpython"': ['mktheapidocs>=0.2'],
 'pymdown-extensions:implementation_name == "cpython"': ['pymdown-extensions>=8,<9']}

setup_kwargs = {
    'name': 'spherical',
    'version': '1.0.5',
    'description': 'Evaluate and transform D matrices, 3-j symbols, and (scalar or spin-weighted) spherical harmonics',
    'long_description': "[![Test Status](https://github.com/moble/spherical/workflows/tests/badge.svg)](https://github.com/moble/spherical/actions)\n[![Test Coverage](https://codecov.io/gh/moble/spherical/branch/master/graph/badge.svg)](https://codecov.io/gh/moble/spherical)\n[![Documentation Status](https://readthedocs.org/projects/spherical/badge/?version=main)](https://spherical.readthedocs.io/en/main/?badge=main)\n[![PyPI Version](https://img.shields.io/pypi/v/spherical?color=)](https://pypi.org/project/spherical/)\n[![Conda Version](https://img.shields.io/conda/vn/conda-forge/spherical.svg?color=)](https://anaconda.org/conda-forge/spherical)\n\n\n# Spherical Functions\n\nPython/numba package for evaluating and transforming Wigner's 𝔇 matrices,\nWigner's 3-j symbols, and spin-weighted (and scalar) spherical harmonics.\nThese functions are evaluated directly in terms of quaternions, as well as in\nthe more standard forms of spherical coordinates and Euler\nangles.<sup>[1](#1-euler-angles-are-awful)</sup>\n\nThese quantities are computed using recursion relations, which makes it\npossible to compute to very high ℓ values.  Unlike direct evaluation of\nindividual elements, which will generally cause overflow or underflow beyond\nℓ≈30, these recursion relations should be accurate for ℓ values beyond 1000.\n\nThe conventions for this package are described in detail on\n[this page](http://moble.github.io/spherical/).\n\n## Installation\n\nBecause this package is pure python code, installation is very simple.  In\nparticular, with a reasonably modern installation, you can just run a command\nlike\n\n```bash\nconda install -c conda-forge spherical\n```\n\nor\n\n```bash\npython -m pip install spherical\n```\n\nEither of these will download and install the package.\n\n\n## Usage\n\n#### Functions of angles or rotations\n\nCurrently, due to the nature of recursions, this module does not allow\ncalculation of individual elements, but returns ranges of results.  For\nexample, when computing Wigner's 𝔇 matrix, all matrices up to a given ℓ will be\nreturned; when evaluating a spin-weighted spherical harmonic, all harmonics up\nto a given ℓ will be returned.  Fortunately, this is usually what is required\nin any case.\n\nTo calculate Wigner's d or 𝔇 matrix or spin-weighted spherical harmonics, first\nconstruct a `Wigner` object.\n\n```python\nimport quaternionic\nimport spherical\nell_max = 16  # Use the largest ℓ value you expect to need\nwigner = spherical.Wigner(ell_max)\n```\n\nThis module takes input as quaternions.  The `quaternionic` module has [various\nways of constructing\nquaternions](https://quaternionic.readthedocs.io/en/latest/#rotations),\nincluding direct construction or conversion from rotation matrices, axis-angle\nrepresentation, Euler angles,<sup>[1](#euler-angles-are-awful)</sup> or\nspherical coordinates, among others:\n\n```python\nR = quaternionic.array([1, 2, 3, 4]).normalized\nR = quaternionic.array.from_axis_angle(vec)\nR = quaternionic.array.from_euler_angles(alpha, beta, gamma)\nR = quaternionic.array.from_spherical_coordinates(theta, phi)\n```\n\nMode weights can be rotated as\n\n```python\nwigner.rotate(modes, R)\n```\n\nor evaluated as\n\n```python\nwigner.evaluate(modes, R)\n```\n\nWe can compute the 𝔇 matrix as\n\n```python\nD = wigner.D(R)\n```\n\nwhich can be indexed as\n\n```python\nD[wigner.Dindex(ell, mp, m)]\n```\n\nor we can compute the spin-weighted spherical harmonics as\n\n```python\nY = wigner.sYlm(s, R)\n```\n\nwhich can be indexed as\n\n```python\nY[wigner.Yindex(ell, m)]\n```\n\nNote that, if relevant, it is probably more efficient to use the `rotate` and\n`evaluate` methods than to use `D` or `Y`.\n\n\n\n#### Clebsch-Gordan and 3-j symbols\n\nIt is possible to compute individual values of the 3-j or Clebsch-Gordan\nsymbols:\n\n```python\nw3j = spherical.Wigner3j(j_1, j_2, j_3, m_1, m_2, m_3)\ncg = spherical.clebsch_gordan(j_1, m_1, j_2, m_2, j_3, m_3)\n```\n\nHowever, when more than one element is needed (as is typically the case), it is\nmuch more efficient to compute a range of values:\n\n```python\ncalc3j = spherical.Wigner3jCalculator(j2_max, j3_max)\nw3j = calc3j.calculate(j2, j3, m2, m3)\n```\n\n\n## Acknowledgments\n\nI very much appreciate Barry Wardell's help in sorting out the relationships\nbetween my conventions and those of other people and software packages\n(especially Mathematica's crazy conventions).\n\nThis code is, of course, hosted on github.  Because it is an open-source\nproject, the hosting is free, and all the wonderful features of github are\navailable, including free wiki space and web page hosting, pull requests, a\nnice interface to the git logs, etc.\n\nThe work of creating this code was supported in part by the Sherman Fairchild\nFoundation and by NSF Grants No. PHY-1306125 and AST-1333129.\n\n\n<br/>\n\n---\n\n###### <sup>1</sup> Euler angles are awful\n\nEuler angles are pretty much\n[the worst things ever](http://moble.github.io/spherical/#euler-angles)\nand it makes me feel bad even supporting them.  Quaternions are\nfaster, more accurate, basically free of singularities, more\nintuitive, and generally easier to understand.  You can work entirely\nwithout Euler angles (I certainly do).  You absolutely never need\nthem.  But if you're so old fashioned that you really can't give them\nup, they are fully supported.\n",
    'author': 'Michael Boyle',
    'author_email': 'michael.oliver.boyle@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/moble/spherical',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
