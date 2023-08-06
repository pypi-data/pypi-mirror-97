# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pytest_xfaillist']

package_data = \
{'': ['*']}

install_requires = \
['pytest>=6.2.2,<7.0.0']

entry_points = \
{'pytest11': ['pytest-xfaillist = pytest_xfaillist.hooks']}

setup_kwargs = {
    'name': 'pytest-xfaillist',
    'version': '0.1.0',
    'description': 'Maintain a xfaillist in an additional file to avoid merge-conflicts.',
    'long_description': 'pytest-xfaillist\n===============\n\nMaintain a xfaillist in an additional file to avoid merge-conflicts.\n\nDevelop\n=======\n\nWe have to workaround the missing support of "install -e ." in poetry. To\ndevelop please call:\n\n```bash\n./c/develop\n```\n',
    'author': 'Adfinis AG',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/projectcaluma/pytest-xfaillist',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
