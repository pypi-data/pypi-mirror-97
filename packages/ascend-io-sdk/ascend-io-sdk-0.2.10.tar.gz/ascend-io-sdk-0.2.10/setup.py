# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ascend',
 'ascend.auth',
 'ascend.external',
 'ascend.external.protoc_gen_swagger.options',
 'ascend.log',
 'ascend.openapi',
 'ascend.openapi.openapi.openapi_client',
 'ascend.openapi.openapi.openapi_client.api',
 'ascend.protos.api',
 'ascend.protos.ascend',
 'ascend.protos.component',
 'ascend.protos.connection',
 'ascend.protos.content_encoding',
 'ascend.protos.core',
 'ascend.protos.expression',
 'ascend.protos.external',
 'ascend.protos.fault',
 'ascend.protos.format',
 'ascend.protos.function',
 'ascend.protos.io',
 'ascend.protos.metrics',
 'ascend.protos.operator',
 'ascend.protos.pattern',
 'ascend.protos.preview',
 'ascend.protos.resource',
 'ascend.protos.resources',
 'ascend.protos.schema',
 'ascend.protos.task',
 'ascend.protos.text',
 'ascend.protos.worker',
 'ascend.sdk',
 'ascend.sdk.drd']

package_data = \
{'': ['*'], 'ascend.sdk': ['templates/*']}

install_requires = \
['Jinja2==2.11.2',
 'certifi==2020.6.20',
 'chardet==3.0.4',
 'glog==0.3.1',
 'googleapis-common-protos>=1.52,<2.0',
 'idna==2.10',
 'networkx==2.5',
 'protobuf==3.13.0',
 'python-dateutil>=2.8.1,<3.0.0',
 'requests==2.23',
 'six==1.15.0',
 'urllib3==1.25.10']

entry_points = \
{'console_scripts': ['ascend = ascend.sdk.cli:run']}

setup_kwargs = {
    'name': 'ascend-io-sdk',
    'version': '0.2.10',
    'description': 'The Ascend SDK for Python',
    'long_description': None,
    'author': 'Ascend Engineering',
    'author_email': 'support@ascend.io',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
