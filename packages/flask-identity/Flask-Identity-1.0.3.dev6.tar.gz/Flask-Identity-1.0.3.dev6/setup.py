# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['flask_identity']

package_data = \
{'': ['*'],
 'flask_identity': ['translations/*',
                    'translations/en_US/LC_MESSAGES/*',
                    'translations/zh_Hans_CN/LC_MESSAGES/*']}

install_requires = \
['bcrypt>=3.2.0,<4.0.0',
 'cryptography>=3.4.6,<4.0.0',
 'flask-babel>=2.0.0,<3.0.0',
 'flask-wtf>=0.14.3,<0.15.0',
 'flask>=1.1.2,<2.0.0',
 'passlib>=1.7.4,<2.0.0']

setup_kwargs = {
    'name': 'flask-identity',
    'version': '1.0.3.dev6',
    'description': 'A lightweight extension & library to security Flask applications quickly and simply.',
    'long_description': "Flask-Identity\n===================\n\n.. image:: https://travis-ci.org/solardiax/flask-identity.svg?branch=master\n    :target: https://travis-ci.org/solardiax/flask-identity\n\n.. image:: https://coveralls.io/repos/github/solardiax/flask-identity/badge.svg?branch=master\n    :target: https://coveralls.io/github/solardiax/flask-identity?branch=master\n\n.. image:: https://img.shields.io/github/tag/solardiax/flask-identity.svg\n    :target: https://github.com/solardiax/flask-identity/releases\n\n.. image:: https://img.shields.io/pypi/dm/flask-identity.svg\n    :target: https://pypi.python.org/pypi/flask-identity\n    :alt: Downloads\n\n.. image:: https://img.shields.io/github/license/solardiax/flask-identity.svg\n    :target: https://github.com/solardiax/flask-identity/blob/master/LICENSE\n    :alt: License\n\n.. image:: https://readthedocs.org/projects/flask-identity/badge/?version=latest\n    :target: https://flask-identity.readthedocs.io/en/latest/?badge=latest\n    :alt: Documentation Status\n\nA lightweight extension & library to security Flask applications quickly and simply.\n\nAbout Flask-Identity\n--------------------\n\nFlask-Identity allows you to quickly add common security mechanisms to your\nFlask application. They include:\n\n1. Session based authentication\n2. User and role management\n3. Password hashing\n4. Basic HTTP authentication\n5. Token based authentication\n6. Login tracking\n7. JSON/Ajax Support\n\nWhy create Flask-Identity?\n--------------------------\n\nCurrently there are so many security middleware for Flask, most them depends on many extensions/libraries.\nIt's easy to start but hard to configure because some options are defined by the dependencies.\n\nFlask-Identity is a lightweight security extension with all-in-one configurations and less third dependencies,\nsome codes are direct merged from other successful open-source libraries:\n\n* `Flask-Login <https://flask-login.readthedocs.org/en/latest/>`_\n* `Flask-Security <https://flask-security.readthedocs.org/en/latest/>`_\n\nContributing\n++++++++++++\nIssues and pull requests are welcome. Other maintainers are also welcome. Unlike\nthe original Flask-Security - issue pull requests against the *master* branch.\nPlease consult these `contributing`_ guidelines.\n\n.. _contributing: https://github.com/solardiax/flask-identity/blob/master/CONTRIBUTING.rst\n\nInstalling\n----------\nInstall and update using `pip <https://pip.pypa.io/en/stable/quickstart/>`_:\n\n::\n\n    pip install -U Flask-Identity\n\n\nResources\n---------\n\n- `Documentation <https://flask-identity.readthedocs.io/>`_\n- `Releases <https://pypi.org/project/Flask-Identity/>`_\n- `Issue Tracker <https://github.com/solardiax/flask-identity/issues>`_\n- `Code <https://github.com/solardiax/flask-identity/>`_\n",
    'author': 'SolardiaX',
    'author_email': 'solardiax@hotmail.com',
    'maintainer': 'SolardiaX',
    'maintainer_email': 'solardiax@hotmail.com',
    'url': 'https://github.com/SolardiaX/flask-identity',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
