# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ladm']

package_data = \
{'': ['*'],
 'ladm': ['main/*',
          'main/util/*',
          'tests/*',
          'tests/resources/correct-skill-ladm/*',
          'tests/resources/correct-skill-ladm/src/*',
          'tests/resources/correct-skill-ladm/src/contract/*',
          'tests/resources/incorrect-skill-ladm/*',
          'tests/resources/incorrect-skill-ladm/src/*',
          'tests/resources/incorrect-skill-ladm/src/contract/*']}

install_requires = \
['gaia-sdk>=3.1.0,<4.0.0', 'pyyaml>=5.3.1,<6.0.0']

entry_points = \
{'console_scripts': ['test = poetry_scripts:test']}

setup_kwargs = {
    'name': 'ladm',
    'version': '0.1.3',
    'description': 'Language Agnostic Dependency Management',
    'long_description': None,
    'author': 'Leftshift One',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7.7,<4.0.0',
}


setup(**setup_kwargs)
