# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['octadocs', 'octadocs.octiron', 'octadocs.octiron.plugins']

package_data = \
{'': ['*']}

install_requires = \
['backports.cached-property>=1.0.0,<2.0.0',
 'boltons>=20.2.1,<21.0.0',
 'deepmerge>=0.1.1,<0.2.0',
 'documented>=0.1.1,<0.2.0',
 'graphviz>=0.15,<0.16',
 'mkdocs-macros-plugin>=0.5.0,<0.6.0',
 'mkdocs>=1.1.2,<2.0.0',
 'owlrl>=5.2.1,<6.0.0',
 'pydotplus>=2.0.2,<3.0.0',
 'pyld>=2.0.3,<3.0.0',
 'python-frontmatter>=0.5.0,<0.6.0',
 'rdflib-jsonld>=0.5.0,<0.6.0',
 'rdflib>=5.0.0,<6.0.0',
 'requests>=2.25.1,<3.0.0',
 'typing-extensions>=3.7.4,<4.0.0']

entry_points = \
{'mkdocs.plugins': ['octadocs = octadocs.plugin:OctaDocsPlugin']}

setup_kwargs = {
    'name': 'octadocs',
    'version': '0.0.25',
    'description': 'MkDocs wiki made smart',
    'long_description': '# mkdocs meta\n\n[![Build Status](https://travis-ci.com/anatoly-scherbakov/octadocs.svg?branch=master)](https://travis-ci.com/anatoly-scherbakov/octadocs)\n[![Coverage](https://coveralls.io/repos/github/anatoly-scherbakov/octadocs/badge.svg?branch=master)](https://coveralls.io/github/anatoly-scherbakov/octadocs?branch=master)\n[![Python Version](https://img.shields.io/pypi/pyversions/octadocs.svg)](https://pypi.org/project/octadocs/)\n[![wemake-python-styleguide](https://img.shields.io/badge/style-wemake-000000.svg)](https://github.com/wemake-services/wemake-python-styleguide)\n\n## Features\n\n- Fully typed with annotations and checked with mypy, [PEP561 compatible](https://www.python.org/dev/peps/pep-0561/)\n- Add yours!\n\n\n## Installation\n\n```bash\npip install octadocs\n```\n\n## License\n\n[MIT](https://github.com/anatoly-scherbakov/octadocs/blob/master/LICENSE)\n\n\n## Credits\n\nThis project was generated with [`wemake-python-package`](https://github.com/wemake-services/wemake-python-package). Current template version is: [868260c2d659e455bafc2ed4fe242413ef39e4dc](https://github.com/wemake-services/wemake-python-package/tree/868260c2d659e455bafc2ed4fe242413ef39e4dc). See what is [updated](https://github.com/wemake-services/wemake-python-package/compare/868260c2d659e455bafc2ed4fe242413ef39e4dc...master) since then.\n',
    'author': None,
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/octadocs/octadocs',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<3.10',
}


setup(**setup_kwargs)
