# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cgmodels', 'cgmodels.crunchy', 'cgmodels.demultiplex']

package_data = \
{'': ['*']}

install_requires = \
['pydantic>=1.7.3,<2.0.0', 'typing-extensions>=3.7.4,<4.0.0']

setup_kwargs = {
    'name': 'cgmodels',
    'version': '0.2.0',
    'description': 'Models used at clinical genomics',
    'long_description': '# cgmodels\n\n![Tests][tests-badge] [![codecov][codecov-badge]][codecov-url][![CodeFactor][codefactor-badge]][codefactor-url][![Code style: black][black-badge]][black-url]\n\nLibrary that work as an interface between services at Clinical Genomics. \nIn most cases where multiple services needs access to a common API, those models should be defined here.\n\n### Pypi\n\n```\npip install cgmodels\n```\n\n### Github\n\nInstall [poetry][poetry]\n\n```\ngit clone https://github.com/Clinical-Genomics/cgmodels\npoetry install \n```\n\n\n[black-badge]: https://img.shields.io/badge/code%20style-black-000000.svg\n[black-url]: https://github.com/psf/black \n[codefactor-badge]: https://www.codefactor.io/repository/github/clinical-genomics/cgmodels/badge\n[codefactor-url]: https://www.codefactor.io/repository/github/clinical-genomics/cgmodels\n[tests-badge]: https://github.com/Clinical-Genomics/cgmodels/workflows/Tests/badge.svg\n[codecov-badge]: https://codecov.io/gh/Clinical-Genomics/cgmodels/branch/main/graph/badge.svg?token=MA62EOQTX7\n[codecov-url]: https://codecov.io/gh/Clinical-Genomics/cgmodels\n[poetry]: https://python-poetry.org/docs/#installation',
    'author': 'moonso',
    'author_email': 'mans.magnusson@scilifelab.se',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Clinical-Genomics/cgmodels',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
