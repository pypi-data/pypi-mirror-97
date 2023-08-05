# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dorado',
 'dorado.sensitivity',
 'dorado.sensitivity.data',
 'dorado.sensitivity.tests']

package_data = \
{'': ['*']}

install_requires = \
['pyyaml', 'synphot']

setup_kwargs = {
    'name': 'dorado-sensitivity',
    'version': '0.2.0',
    'description': 'Dorado sensitivity and exposure time calculator',
    'long_description': '# Dorado sensitivity and exposure time calculator\n\nDorado is a proposed space mission for ultraviolet follow-up of gravitational\nwave events. This repository contains a simple sensitivity and exposure time\ncalculator for Dorado.\n\nThis package can estimate the signal to noise, exposure time, or limiting\nmagnitude for an astronomical source with a given spectrum using the [CCD\nsignal to noise equation]. It models the following noise contributions:\n\n*   Zodiacal light\n*   Airglow (geocoronal emission)\n*   Standard CCD noise (shot noise, read noise, dark current)\n\n## Installation\n\nTo install with [Pip]:\n\n    $ pip install dorado-sensitivity\n\n## Examples\n\nFor examples, see the [Jupyter notebook].\n\n## Dependencies\n\n*   [Astropy]\n*   [Synphot] for combining bandpasses and source spectra\n*   [PyYAML] for reading [ECSV] data files\n\n[CCD signal to noise equation]: https://hst-docs.stsci.edu/stisihb/chapter-6-exposure-time-calculations/6-4-computing-exposure-times\n[Pip]: https://pip.pypa.io\n[Astropy]: https://www.astropy.org\n[Synphot]: https://synphot.readthedocs.io/\n[PyYAML]: https://pyyaml.org/\n[ECSV]: https://github.com/astropy/astropy-APEs/blob/master/APE6.rst\n[Jupyter notebook]: https://github.com/nasa/dorado-sensitivity/blob/master/example.ipynb\n',
    'author': 'Brad Cenko',
    'author_email': 'brad.cenko@nasa.gov',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/nasa/dorado-sensitivity',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
