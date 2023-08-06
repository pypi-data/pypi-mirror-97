# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nonebot_plugin_manager']

package_data = \
{'': ['*']}

install_requires = \
['nonebot-adapter-cqhttp>=2.0.0a11.post2,<3.0.0',
 'nonebot2>=2.0.0-alpha.11,<3.0.0']

setup_kwargs = {
    'name': 'nonebot-plugin-manager',
    'version': '0.1.0.post1',
    'description': 'Plugin Manager base on import hook',
    'long_description': '# TRPGLogger\n\n*基于 [nonebot2](https://github.com/nonebot/nonebot2) 以及 [go-cqhttp](https://github.com/Mrs4s/go-cqhttp) 插件管理器*\n\n[![License](https://img.shields.io/github/license/Jigsaw111/nonebot_plugin_manager)](LICENSE)\n![Python Version](https://img.shields.io/badge/python-3.7+-blue.svg)\n![NoneBot Version](https://img.shields.io/badge/nonebot-2+-red.svg)\n![Pypi Version](https://img.shields.io/pypi/v/nonebot-plugin-manager.svg)\n\n### 安装\n\n* 使用nb-cli（推荐）  \n\n```bash\nnb plugin install nonebot_plugin_manager\n```\n\n* 使用poetry\n\n```bash\npoetry add nonebot_plugin_manager\n```\n\n### 开始使用\n\n`.plugin list` 查看插件列表\n`.plugin block 插件名` 屏蔽插件\n`.plugin unblock 插件名` 启用插件\n\n### TO DO\n\n[ ] 分群插件管理',
    'author': 'Jigsaw',
    'author_email': 'j1g5aw@foxmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Jigsaw111/nonebot_plugin_manager',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.3,<4.0.0',
}


setup(**setup_kwargs)
