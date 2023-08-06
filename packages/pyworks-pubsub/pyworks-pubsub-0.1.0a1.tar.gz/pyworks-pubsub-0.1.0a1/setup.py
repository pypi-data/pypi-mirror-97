# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyworks_pubsub']

package_data = \
{'': ['*']}

install_requires = \
['python-dotenv>=0.15.0,<0.16.0']

setup_kwargs = {
    'name': 'pyworks-pubsub',
    'version': '0.1.0a1',
    'description': 'Provide a variety of pubsub backends in a single library.',
    'long_description': '# pyworks-pubsub\nPyworks Pubsub provide simple method to work with PubSub messaging like Kafka, RabbitMQ.\n',
    'author': 'PyWorks Asia Team',
    'author_email': 'opensource@pyworks.asia',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/pyworksasia/pyworks-pubsub',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
