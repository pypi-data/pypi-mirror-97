# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tests', 'xeauth', 'xeauth.integrations']

package_data = \
{'': ['*']}

install_requires = \
['Authlib>=0.15.3,<0.16.0',
 'appdirs>=1.4.4,<2.0.0',
 'click',
 'httpx>=0.16.1,<0.17.0',
 'panel>=0.11,<0.12']

entry_points = \
{'console_scripts': ['xeauth = xeauth.cli:main'],
 'eve_panel.auth': ['XenonAuth = xeauth.integrations.eve_panel:XenonEveAuth']}

setup_kwargs = {
    'name': 'xeauth',
    'version': '0.1.3',
    'description': 'Top-level package for xeauth.',
    'long_description': '======\nxeauth\n======\n\n\n.. image:: https://img.shields.io/pypi/v/xeauth.svg\n        :target: https://pypi.python.org/pypi/xeauth\n\n.. image:: https://img.shields.io/travis/jmosbacher/xeauth.svg\n        :target: https://travis-ci.com/jmosbacher/xeauth\n\n.. image:: https://readthedocs.org/projects/xeauth/badge/?version=latest\n        :target: https://xeauth.readthedocs.io/en/latest/?badge=latest\n        :alt: Documentation Status\n\n\n\n\nAuthentication client for the Xenon edark matter experiment.\n\n\n* Free software: MIT\n* Documentation: https://xeauth.readthedocs.io.\n\n\nFeatures\n--------\n\n* TODO\n\nCredits\n-------\n\nThis package was created with Cookiecutter_ and the `briggySmalls/cookiecutter-pypackage`_ project template.\n\n.. _Cookiecutter: https://github.com/audreyr/cookiecutter\n.. _`briggySmalls/cookiecutter-pypackage`: https://github.com/briggySmalls/cookiecutter-pypackage\n',
    'author': 'Yossi Mosbacher',
    'author_email': 'joe.mosbacher@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/jmosbacher/xeauth',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7',
}


setup(**setup_kwargs)
