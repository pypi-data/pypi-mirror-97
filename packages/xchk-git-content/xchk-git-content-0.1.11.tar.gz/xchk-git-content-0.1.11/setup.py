# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['xchk_git_content']

package_data = \
{'': ['*'],
 'xchk_git_content': ['static/xchk_git_content/images/*',
                      'templates/xchk_git_content/*']}

setup_kwargs = {
    'name': 'xchk-git-content',
    'version': '0.1.11',
    'description': 'Course material related to Git for the xchk teaching framework',
    'long_description': None,
    'author': 'Vincent Nys',
    'author_email': 'vincentnys@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
