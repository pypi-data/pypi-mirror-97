# -*- coding: utf-8 -*-
"""
package/install module package oathldap
"""

import sys
import os
from setuptools import setup, find_packages

PYPI_NAME = 'oath-ldap-tool'

BASEDIR = os.path.dirname(os.path.realpath(__file__))

sys.path.insert(0, os.path.join(BASEDIR, 'oathldap_tool'))
import __about__

setup(
    name=PYPI_NAME,
    license=__about__.__license__,
    version=__about__.__version__,
    description='OATH-LDAP command-line tool',
    author=__about__.__author__,
    author_email=__about__.__mail__,
    maintainer=__about__.__author__,
    maintainer_email=__about__.__mail__,
    url='https://oath-ldap.stroeder.com',
    download_url='https://pypi.org/project/{0}/#files'.format(PYPI_NAME),
    keywords=['LDAP', 'OpenLDAP', 'OATH', 'OATH-LDAP', 'HOTP', 'TOTP', 'Yubikey'],
    packages=find_packages(exclude=['tests']),
    package_dir={'': '.'},
    package_data = {
        'oathldap_tool': ['py.typed'],
    },
    #test_suite='tests',
    python_requires='>=3.6',
    include_package_data=True,
    install_requires=[
        'setuptools',
        'ldap0 >= 1.0.0',
        'jwcrypto',
        'python-yubico >= 1.3.3',
    ],
    zip_safe=False,
    entry_points={
        'console_scripts': [
            'oath-ldap-tool = oathldap_tool.cli:main',
        ],
    }
)
