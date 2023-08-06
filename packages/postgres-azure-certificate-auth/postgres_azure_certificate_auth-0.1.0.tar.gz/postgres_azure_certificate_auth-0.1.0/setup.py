# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['postgres_azure_certificate_auth']
install_requires = \
['azure-appconfiguration>=1.1.1,<2.0.0',
 'azure-identity>=1.5.0,<2.0.0',
 'azure-keyvault-secrets>=4.2.0,<5.0.0',
 'compose>=1.1.1,<2.0.0',
 'psycopg2>=2.8.6,<3.0.0']

setup_kwargs = {
    'name': 'postgres-azure-certificate-auth',
    'version': '0.1.0',
    'description': 'Functions for connecting to a Postgres database using certificate authentication stored in Azure Key Vault',
    'long_description': None,
    'author': 'peder2911',
    'author_email': 'pedlan@prio.org',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
