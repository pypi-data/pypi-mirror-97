# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['thanakan',
 'thanakan.models',
 'thanakan.services',
 'thanakan.services.model',
 'thanakan.slip']

package_data = \
{'': ['*']}

install_requires = \
['Pillow>=8.1.0,<9.0.0',
 'crccheck>=1.0,<2.0',
 'fastapi-utils>=0.2.1,<0.3.0',
 'furl>=2.1.0,<3.0.0',
 'google-cloud-documentai>=0.3.0,<0.4.0',
 'httpx-auth>=0.8.0,<0.9.0',
 'httpx[http2]>=0.16.1,<0.17.0',
 'locate>=0.0.1,<0.0.2',
 'loguru>=0.5.3,<0.6.0',
 'parse-with-dot-access>=1.18.0,<2.0.0',
 'pydantic>=1.7.3,<2.0.0',
 'pyzbar-x>=0.2.1,<0.3.0']

setup_kwargs = {
    'name': 'thanakan',
    'version': '0.1.1',
    'description': 'Awesome `thanakan` is a Python cli/package created with https://github.com/TezRomacH/python-package-template',
    'long_description': '# thanakan\nPython Interface for Thai Bank API, KBANK, SCB, QR Code and slip verification\n',
    'author': 'codustry',
    'author_email': 'hello@codustry.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/codustry/thanakan',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
