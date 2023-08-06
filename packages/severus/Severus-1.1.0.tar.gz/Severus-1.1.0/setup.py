# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['severus', 'tests']

package_data = \
{'': ['*'], 'tests': ['lang1/*', 'lang2/*', 'lang2/it/*']}

install_requires = \
['pyyaml>=5.4.1,<6.0.0']

setup_kwargs = {
    'name': 'severus',
    'version': '1.1.0',
    'description': 'An internationalization engine designed with simplicity in mind',
    'long_description': '# Severus\n\nSeverus – */seˈweː.rus/* – is a Python internationalization engine designed with simplicity in mind.\n\n[![pip version](https://img.shields.io/pypi/v/severus.svg?style=flat)](https://pypi.python.org/pypi/Severus) \n![Tests Status](https://github.com/emmett-framework/severus/workflows/Tests/badge.svg)\n\n## In a nutshell\n\n*it.json*\n\n```json\n{\n    "Hello world!": "Ciao mondo!"\n}\n```\n\n*translate.py*\n\n```python\nfrom severus import Severus, language\n\nT = Severus()\n\nwith language("it"):\n    print(T("Hello world!"))\n```\n\n## Documentation\n\nThe documentation is available under the [docs folder](https://github.com/emmett-framework/severus/tree/master/docs).\n\n## License\n\nSeverus is released under the BSD License.\n',
    'author': 'Giovanni Barillari',
    'author_email': 'gi0baro@d4net.org',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/emmett-framework/severus',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
