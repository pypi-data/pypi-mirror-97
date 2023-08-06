# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['renoir', 'renoir.parsing', 'tests']

package_data = \
{'': ['*'], 'tests': ['blocks/*', 'html/*', 'yaml/*']}

setup_kwargs = {
    'name': 'renoir',
    'version': '1.3.2',
    'description': 'A templating engine designed with simplicity in mind',
    'long_description': '# Renoir\n\nRenoir – */ˈrɛnwɑːr/* – is a Python templating engine designed with simplicity in mind.\n\n[![pip version](https://img.shields.io/pypi/v/renoir.svg?style=flat)](https://pypi.python.org/pypi/Renoir)\n![Tests Status](https://github.com/emmett-framework/renoir/workflows/Tests/badge.svg)\n\n## In a nutshell\n\n```html\n{{ extend "layout.html" }}\n{{ block title }}Members{{ end }}\n{{ block content }}\n<ul>\n  {{ for user in users: }}\n  <li><a href="{{ =user[\'url\'] }}">{{ =user[\'name\'] }}</a></li>\n  {{ pass }}\n</ul>\n{{ end }}\n```\n\n## Documentation\n\nThe documentation is available under the [docs folder](https://github.com/emmett-framework/renoir/tree/master/docs).\n\n## License\n\nRenoir is released under the BSD License.\n',
    'author': 'Giovanni Barillari',
    'author_email': 'gi0baro@d4net.org',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/emmett-framework/renoir',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
