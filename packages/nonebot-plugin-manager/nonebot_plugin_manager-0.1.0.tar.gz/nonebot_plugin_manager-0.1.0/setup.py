# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nonebot_plugin_manager']

package_data = \
{'': ['*']}

install_requires = \
['nonebot-adapter-cqhttp>=2.0.0a11.post2,<3.0.0',
 'nonebot-plugin-trpglogger>=0.1.4,<0.2.0',
 'nonebot2>=2.0.0-alpha.11,<3.0.0']

setup_kwargs = {
    'name': 'nonebot-plugin-manager',
    'version': '0.1.0',
    'description': 'Plugin Manager base on import hook',
    'long_description': None,
    'author': 'Jigsaw',
    'author_email': 'j1g5aw@foxmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Jigsaw111/nonebot_plugin_manager',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
