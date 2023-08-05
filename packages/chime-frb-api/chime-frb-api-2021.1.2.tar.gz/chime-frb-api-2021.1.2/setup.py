# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['chime_frb_api',
 'chime_frb_api.backends',
 'chime_frb_api.core',
 'chime_frb_api.modules',
 'chime_frb_api.stations',
 'chime_frb_api.tests']

package_data = \
{'': ['*']}

install_requires = \
['attrs>=19.3.0,<20.0.0',
 'pyjwt>=1.7',
 'python-dateutil>=2.8,<3.0',
 'requests>=2.22,<3.0']

setup_kwargs = {
    'name': 'chime-frb-api',
    'version': '2021.1.2',
    'description': 'CHIME/FRB API',
    'long_description': "# CHIME/FRB API\n\n|   **`Build`**   | **`Coverage`**  |  **`Release`**  |   **`Style`**   |\n|-----------------|-----------------|-----------------|-----------------|\n|[![Build Status](https://travis-ci.com/CHIMEFRB/frb-api.svg?token=mRNzzrGmJQewCpZQsov9&branch=master)](https://travis-ci.com/CHIMEFRB/frb-api)| [![Coverage Status](https://coveralls.io/repos/github/CHIMEFRB/frb-api/badge.svg?branch=master&t=uYdqsa)](https://coveralls.io/github/CHIMEFRB/frb-api?branch=master) | [![PyPI version](https://img.shields.io/pypi/v/chime-frb-api.svg)](https://pypi.org/project/chime-frb-api/) | [![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://black.readthedocs.io/en/stable/)\n\n--------\n\n`chime-frb-api` is a python library to access CHIME/FRB backend. This library enables you interact with resources such as databases, event headers, calibration products, cluster jobs etc.\n\nCheck out the **[documentation](https://chimefrb.github.io/frb-api/)** for more details.\n\n## Installation\nThe latest stable version is available on [PyPI](https://pypi.org/project/chime-frb-api/). Either add `chime-frb-api` to your requirements.txt file or install with pip:\n```\npip install chime-frb-api\n```\n\n## Usage\n```python\nfrom chime_frb_api.backends import frb_master\nmaster = frb_master.FRBMaster()\nmaster.events.get_event(65540476)\n{'beam_numbers': [185, 1185, 2185, 3185],\n 'event_type': 'EXTRAGALACTIC',\n 'fpga_time': 271532193792,\n 'id': 65540476,\n  ...\n```\n\n## Documentation\nFor further reading, please refer to the [documentation](https://chimefrb.github.io/frb-api/).\n",
    'author': 'Shiny Brar',
    'author_email': 'charanjotbrar@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/CHIMEFRB/frb-api',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
